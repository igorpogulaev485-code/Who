#!/usr/bin/env python3
"""Festival pavilion tents for 32mm terrain — hollow interiors + removable roofs.

Inspired by festival/tournament pavilion style. Each tent exports:
  - *_walls.stl  : hollow shell, open bottom, large doorway(s), roof ledge
  - *_roof.stl   : removable lid so minis can be placed inside
  - *_preview.stl: walls+roof assembled (visual only)

Clearance target for 32mm minis (bases up to 28–32 mm):
  door >= 32×42 mm, interior height under roof ledge >= 46 mm.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import trimesh
from trimesh.creation import box, cone, cylinder

OUT = Path(__file__).resolve().parent / "stl"
ENGINE = "manifold"

# --- playability constants (mm), sized for 32mm miniatures ---
WALL_T = 2.2
DOOR_W = 32.0
DOOR_H = 42.0
CLEAR_H = 46.0  # interior clear height to roof ledge
LEDGE = 1.8  # roof seating ledge inward
ROOF_OVERHANG = 1.8
ROOF_THICK = 2.0


def U(parts: list[trimesh.Trimesh]) -> trimesh.Trimesh:
    parts = [p for p in parts if p is not None and len(getattr(p, "faces", []))]
    if not parts:
        raise ValueError("empty union")
    m = parts[0]
    for p in parts[1:]:
        m = m.union(p, engine=ENGINE)
    return m


def D(a: trimesh.Trimesh, b: trimesh.Trimesh) -> trimesh.Trimesh:
    return a.difference(b, engine=ENGINE)


def T(m: trimesh.Trimesh, x=0.0, y=0.0, z=0.0) -> trimesh.Trimesh:
    out = m.copy()
    out.apply_translation([x, y, z])
    return out


def Rz(m: trimesh.Trimesh, deg: float) -> trimesh.Trimesh:
    out = m.copy()
    out.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg), [0, 0, 1]))
    return out


def Ry(m: trimesh.Trimesh, deg: float) -> trimesh.Trimesh:
    out = m.copy()
    out.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg), [0, 1, 0]))
    return out


def Rx(m: trimesh.Trimesh, deg: float) -> trimesh.Trimesh:
    out = m.copy()
    out.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg), [1, 0, 0]))
    return out


def finalize(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    m = mesh.copy()
    m.merge_vertices()
    m.update_faces(m.unique_faces())
    m.remove_unreferenced_vertices()
    m.apply_translation([0, 0, -m.bounds[0][2]])
    return m


def export(name: str, mesh: trimesh.Trimesh) -> Path:
    path = OUT / f"{name}.stl"
    finalize(mesh).export(path)
    m = trimesh.load(path)
    e = m.extents
    print(f"  {path.name:42s}  {e[0]:5.1f}×{e[1]:5.1f}×{e[2]:5.1f} mm  faces={len(m.faces)}")
    return path


def stake(x: float, y: float, h: float = 8.0, r: float = 1.3) -> trimesh.Trimesh:
    s = cylinder(radius=r, height=h, sections=12)
    s.apply_translation([x, y, h / 2])
    return s


def flag_finial(z: float = 0.0) -> trimesh.Trimesh:
    pole = cylinder(radius=0.7, height=8, sections=10)
    pole.apply_translation([0, 0, 4])
    flag = box(extents=[0.7, 7.5, 4.5])
    flag.apply_translation([0.6, 3.2, 5.5])
    # slight wave via second block
    tip = box(extents=[0.7, 3.0, 3.2])
    tip.apply_translation([0.6, 7.5, 5.0])
    return T(U([pole, flag, tip]), 0, 0, z)


def ball_finial(z: float = 0.0, r: float = 2.0) -> trimesh.Trimesh:
    # approximate sphere with stacked cylinders / icosphere if available
    try:
        ball = trimesh.creation.icosphere(subdivisions=2, radius=r)
    except Exception:
        ball = cylinder(radius=r, height=r * 1.6, sections=16)
    ball.apply_translation([0, 0, r])
    neck = cylinder(radius=0.8, height=2.5, sections=10)
    neck.apply_translation([0, 0, 1.25])
    return T(U([neck, ball]), 0, 0, z)


def rolled_flap(width: float, y: float, z: float) -> trimesh.Trimesh:
    """Rolled-up door curtain above the doorway (stays outside the opening)."""
    roll = cylinder(radius=2.2, height=width * 0.95, sections=16)
    roll = Ry(roll, 90)
    roll.apply_translation([0, y, z])
    # short decorative ties on the outside face only
    ties = []
    for x in (-width * 0.28, width * 0.28):
        t = cylinder(radius=0.5, height=3.0, sections=8)
        t.apply_translation([x, y - 0.2 if y < 0 else y + 0.2, z - 0.8])
        ties.append(t)
    return U([roll, *ties])


def fabric_ribs_rect(
    L: float,
    W: float,
    H: float,
    n: int = 8,
    door_xs: list[float] | None = None,
    door_face_y: float = -1.0,
) -> list[trimesh.Trimesh]:
    """Vertical fold ribs; skip zones over front doorways."""
    ribs = []
    door_xs = door_xs or []
    door_keepout = DOOR_W / 2 + 3.0

    def blocked(x: float, y: float) -> bool:
        if door_face_y < 0 and y < 0 and abs(y + W / 2) < 1.5:
            for dx in door_xs:
                if abs(x - dx) < door_keepout:
                    return True
        return False

    # long sides
    for i in range(n):
        t = (i + 0.5) / n
        x = -L / 2 + t * L
        for y in (-W / 2, W / 2):
            if blocked(x, y):
                continue
            r = cylinder(radius=0.7, height=H * 0.92, sections=8)
            r.apply_translation([x, y, H * 0.46])
            ribs.append(r)
    # short sides
    for i in range(max(3, n // 2)):
        t = (i + 0.5) / max(3, n // 2)
        y = -W / 2 + t * W
        for x in (-L / 2, L / 2):
            r = cylinder(radius=0.7, height=H * 0.92, sections=8)
            r.apply_translation([x, y, H * 0.46])
            ribs.append(r)
    return ribs


def fabric_ribs_circle(R: float, H: float, n: int = 16, door_angles: list[float] | None = None) -> list[trimesh.Trimesh]:
    """Skip ribs near door angle(s) in degrees (0= +X, 90=+Y, default door at -Y = 270)."""
    ribs = []
    door_angles = door_angles if door_angles is not None else [270.0]
    keepout = 40.0  # degrees — wide enough for 32mm door on small round tent

    def near_door(ang: float) -> bool:
        for d in door_angles:
            delta = abs((ang - d + 180) % 360 - 180)
            if delta < keepout:
                return True
        return False

    for i in range(n):
        ang = i * (360 / n)
        if near_door(ang):
            continue
        x = (R - 0.2) * math.cos(math.radians(ang))
        y = (R - 0.2) * math.sin(math.radians(ang))
        r = cylinder(radius=0.75, height=H * 0.92, sections=8)
        r.apply_translation([x, y, H * 0.46])
        ribs.append(r)
    return ribs


def scallop_band_rect(L: float, W: float, z: float) -> trimesh.Trimesh:
    parts = [box(extents=[L + 1, W + 1, 2.2])]
    parts[0].apply_translation([0, 0, z])
    # hanging scallops
    for side, sign in (("y", 1), ("y", -1), ("x", 1), ("x", -1)):
        count = 7 if side == "y" else 5
        span = L if side == "y" else W
        for i in range(count):
            t = (i + 0.5) / count
            pos = -span / 2 + t * span
            sc = cone(radius=1.8, height=3.2, sections=10)
            sc = Rx(sc, 180)
            if side == "y":
                sc.apply_translation([pos, sign * (W / 2 + 0.2), z - 0.5])
            else:
                sc.apply_translation([sign * (L / 2 + 0.2), pos, z - 0.5])
            parts.append(sc)
    return U(parts)


def doorway_cutter(width: float, height: float, depth: float, y: float) -> trimesh.Trimesh:
    # rectangular opening with slight arch top
    body = box(extents=[width, depth, height])
    body.apply_translation([0, y, height / 2])
    arch = cylinder(radius=width / 2, height=depth, sections=24)
    arch = Rx(arch, 90)
    arch.apply_translation([0, y, height])
    return U([body, arch])


def rect_walls(L: float, W: float, H: float, doors: list[tuple[float, float, float]]) -> trimesh.Trimesh:
    """Hollow rectangular pavilion walls with door cutouts.

    doors: list of (x_offset, yaw_deg, y_face_sign) — door centered on a long/short face.
    For simplicity doors are cut on +Y or -Y face (yaw rotates whole cut).
    """
    outer = box(extents=[L, W, H])
    outer.apply_translation([0, 0, H / 2])
    inner = box(extents=[L - 2 * WALL_T, W - 2 * WALL_T, H + 2])
    inner.apply_translation([0, 0, H / 2 + 0.5])
    shell = D(outer, inner)

    # roof ledge: leave a shelf by adding inner lip near top via smaller cut stop
    # Re-build with partial inner cut for better ledge:
    outer = box(extents=[L, W, H])
    outer.apply_translation([0, 0, H / 2])
    inner_low = box(extents=[L - 2 * WALL_T, W - 2 * WALL_T, H - LEDGE + 1])
    inner_low.apply_translation([0, 0, (H - LEDGE) / 2])
    shell = D(outer, inner_low)
    # open the very top center for roof insert clearance? keep ledge: cut only below ledge
    # top is open naturally since outer top face exists — need open top:
    top_open = box(extents=[L - 2 * WALL_T - 2 * LEDGE, W - 2 * WALL_T - 2 * LEDGE, WALL_T + 2])
    top_open.apply_translation([0, 0, H - WALL_T / 2])
    shell = D(shell, top_open)

    for x_off, yaw, face_y in doors:
        cut = doorway_cutter(DOOR_W, DOOR_H, WALL_T * 4 + 4, face_y * (W / 2))
        cut = T(Rz(cut, yaw), x_off, 0, 0)
        # if yaw 90, door on X face — rebuild cutter position
        if abs(yaw) % 180 == 90:
            cut = doorway_cutter(DOOR_W, DOOR_H, WALL_T * 4 + 4, 0)
            # place on +X or -X
            sign = 1 if yaw == 90 else -1
            cut.apply_translation([sign * (L / 2), x_off, 0])
            # rotate cutter so depth goes into wall
            cut = Rz(doorway_cutter(DOOR_W, DOOR_H, WALL_T * 4 + 4, 0), 90)
            cut.apply_translation([sign * (L / 2), x_off, 0])
        shell = D(shell, cut)

    front_door_xs = [x for x, yaw, face_y in doors if yaw == 0 and face_y < 0]
    details = fabric_ribs_rect(L, W, H, n=max(6, int(L / 10)), door_xs=front_door_xs)
    # perimeter stakes (skip mid-front stake if it sits in a doorway)
    for x, y in [(-L / 2, -W / 2), (-L / 2, W / 2), (L / 2, -W / 2), (L / 2, W / 2)]:
        details.append(stake(x, y))
    details.append(stake(0, W / 2))
    if not any(abs(dx) < DOOR_W / 2 + 2 for dx in front_door_xs):
        details.append(stake(0, -W / 2))
    # scallop band
    details.append(scallop_band_rect(L, W, H - 1.2))
    # rolled flaps above each -Y door (outside the wall, not in the opening)
    for x_off, yaw, face_y in doors:
        if yaw == 0:
            flap = rolled_flap(DOOR_W + 2, face_y * (W / 2 + 2.0), DOOR_H + 2.5)
            details.append(T(flap, x_off, 0, 0))

    return U([shell, *details])


def rect_roof(L: float, W: float, peak_h: float, style: str = "pyramid", finials: str = "flag") -> trimesh.Trimesh:
    """Removable roof that seats on wall ledge."""
    # seating plate
    plate_L = L - 2 * WALL_T + 0.4
    plate_W = W - 2 * WALL_T + 0.4
    plate = box(extents=[plate_L, plate_W, ROOF_THICK])
    plate.apply_translation([0, 0, ROOF_THICK / 2])
    # outer eaves
    eaves = box(extents=[L + ROOF_OVERHANG * 2, W + ROOF_OVERHANG * 2, 1.4])
    eaves.apply_translation([0, 0, ROOF_THICK + 0.5])

    hl, hw = L / 2 + ROOF_OVERHANG, W / 2 + ROOF_OVERHANG
    z0 = ROOF_THICK + 1.0
    parts = [plate, eaves]

    if style == "pyramid":
        verts = [
            [-hl, -hw, z0],
            [hl, -hw, z0],
            [hl, hw, z0],
            [-hl, hw, z0],
            [0, 0, z0 + peak_h],
        ]
        faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 3, 2], [0, 2, 1]]
        parts.append(trimesh.Trimesh(vertices=verts, faces=faces, process=True))
        if finials == "flag":
            parts.append(flag_finial(z0 + peak_h))
        else:
            parts.append(ball_finial(z0 + peak_h))
    elif style == "ridge":
        # prism roof
        verts = [
            [-hl, -hw, z0],
            [hl, -hw, z0],
            [hl, hw, z0],
            [-hl, hw, z0],
            [-hl, 0, z0 + peak_h],
            [hl, 0, z0 + peak_h],
        ]
        faces = [
            [0, 1, 5],
            [0, 5, 4],
            [3, 4, 5],
            [3, 5, 2],
            [0, 4, 3],
            [1, 2, 5],
            [0, 3, 2],
            [0, 2, 1],
        ]
        parts.append(trimesh.Trimesh(vertices=verts, faces=faces, process=True))
        if finials == "flag":
            parts.append(T(flag_finial(z0 + peak_h), -hl * 0.55, 0, 0))
            parts.append(T(flag_finial(z0 + peak_h), hl * 0.55, 0, 0))
        else:
            parts.append(T(ball_finial(z0 + peak_h), -hl * 0.55, 0, 0))
            parts.append(T(ball_finial(z0 + peak_h), hl * 0.55, 0, 0))
    elif style == "triple":
        # three peaks along length
        for px in (-hl * 0.55, 0.0, hl * 0.55):
            verts = [
                [px - hl * 0.35, -hw, z0],
                [px + hl * 0.35, -hw, z0],
                [px + hl * 0.35, hw, z0],
                [px - hl * 0.35, hw, z0],
                [px, 0, z0 + peak_h],
            ]
            faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 3, 2], [0, 2, 1]]
            parts.append(trimesh.Trimesh(vertices=verts, faces=faces, process=True))
            parts.append(T(ball_finial(z0 + peak_h), px, 0, 0))
        # fill valleys with low ridge
        fill = box(extents=[L + ROOF_OVERHANG * 2, W * 0.55, peak_h * 0.35])
        fill.apply_translation([0, 0, z0 + peak_h * 0.2])
        parts.append(fill)
    elif style == "double":
        for px in (-hl * 0.38, hl * 0.38):
            verts = [
                [px - hl * 0.42, -hw, z0],
                [px + hl * 0.42, -hw, z0],
                [px + hl * 0.42, hw, z0],
                [px - hl * 0.42, hw, z0],
                [px, 0, z0 + peak_h],
            ]
            faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 3, 2], [0, 2, 1]]
            parts.append(trimesh.Trimesh(vertices=verts, faces=faces, process=True))
            parts.append(T(flag_finial(z0 + peak_h), px, 0, 0))
        fill = box(extents=[L + ROOF_OVERHANG * 2, W * 0.5, peak_h * 0.3])
        fill.apply_translation([0, 0, z0 + peak_h * 0.18])
        parts.append(fill)

    # tiny alignment nubs underside (into wall opening)
    nub = cylinder(radius=1.5, height=2.2, sections=10)
    for x, y in [(-plate_L * 0.25, -plate_W * 0.25), (plate_L * 0.25, plate_W * 0.25)]:
        parts.append(T(nub, x, y, -0.2))

    return U(parts)


def circle_walls(R: float, H: float, n_seg: int = 28, door_count: int = 1, awning: bool = False) -> trimesh.Trimesh:
    outer = cylinder(radius=R, height=H, sections=n_seg)
    outer.apply_translation([0, 0, H / 2])
    inner = cylinder(radius=R - WALL_T, height=H - LEDGE + 1, sections=n_seg)
    inner.apply_translation([0, 0, (H - LEDGE) / 2])
    shell = D(outer, inner)
    # open top
    top_open = cylinder(radius=R - WALL_T - LEDGE, height=WALL_T + 3, sections=n_seg)
    top_open.apply_translation([0, 0, H - WALL_T / 2])
    shell = D(shell, top_open)

    # door(s) on -Y
    for i in range(door_count):
        x_off = 0.0 if door_count == 1 else (-R * 0.35 if i == 0 else R * 0.35)
        cut = doorway_cutter(DOOR_W, DOOR_H, WALL_T * 4 + 6, -(R - WALL_T / 2))
        shell = D(shell, T(cut, x_off, 0, 0))

    # door at -Y ≈ 270°
    details = fabric_ribs_circle(R, H, n=16, door_angles=[270.0])
    for i in range(8):
        ang = i * 45
        # skip stakes that would sit in the front doorway arc
        if abs((ang - 270 + 180) % 360 - 180) < 35:
            continue
        details.append(stake((R - 0.5) * math.cos(math.radians(ang)), (R - 0.5) * math.sin(math.radians(ang))))
    # band
    band = cylinder(radius=R + 0.6, height=2.2, sections=n_seg)
    band.apply_translation([0, 0, H - 1.2])
    inner_band = cylinder(radius=R - WALL_T - 0.2, height=3, sections=n_seg)
    inner_band.apply_translation([0, 0, H - 1.2])
    details.append(D(band, inner_band))
    details.append(rolled_flap(DOOR_W + 2, -(R + 1.8), DOOR_H + 2.5))

    if awning:
        # front canopy — poles outside the doorway clear width
        aw = box(extents=[R * 1.15, R * 0.55, 1.6])
        aw.apply_translation([0, -(R + R * 0.22), H - 2])
        details.append(aw)
        for x in (-R * 0.48, R * 0.48):
            pole = cylinder(radius=1.4, height=H - 1, sections=12)
            pole.apply_translation([x, -(R + R * 0.45), (H - 1) / 2])
            details.append(pole)
            details.append(stake(x, -(R + R * 0.45), h=6))

    return U([shell, *details])


def circle_roof(R: float, peak_h: float, style: str = "cone", finials: str = "flag") -> trimesh.Trimesh:
    plate_r = R - WALL_T + 0.2
    plate = cylinder(radius=plate_r, height=ROOF_THICK, sections=28)
    plate.apply_translation([0, 0, ROOF_THICK / 2])
    eaves = cylinder(radius=R + ROOF_OVERHANG, height=1.4, sections=28)
    eaves.apply_translation([0, 0, ROOF_THICK + 0.5])
    parts = [plate, eaves]
    z0 = ROOF_THICK + 1.0

    if style == "cone":
        roof = cone(radius=R + ROOF_OVERHANG, height=peak_h, sections=28)
        roof.apply_translation([0, 0, z0])
        parts.append(roof)
        parts.append(flag_finial(z0 + peak_h) if finials == "flag" else ball_finial(z0 + peak_h))
    else:
        # multi-bump shallow dome: base cone + satellite peaks
        base = cone(radius=R + ROOF_OVERHANG, height=peak_h * 0.65, sections=28)
        base.apply_translation([0, 0, z0])
        parts.append(base)
        for i in range(6):
            ang = i * 60
            x = (R * 0.45) * math.cos(math.radians(ang))
            y = (R * 0.45) * math.sin(math.radians(ang))
            bump = cone(radius=R * 0.28, height=peak_h * 0.55, sections=16)
            bump.apply_translation([x, y, z0 + peak_h * 0.25])
            parts.append(bump)
            parts.append(T(ball_finial(z0 + peak_h * 0.75, r=1.6), x, y, 0))
        parts.append(ball_finial(z0 + peak_h * 0.65, r=2.0))

    nub = cylinder(radius=1.5, height=2.2, sections=10)
    for ang in (45, 225):
        parts.append(T(nub, (plate_r * 0.4) * math.cos(math.radians(ang)), (plate_r * 0.4) * math.sin(math.radians(ang)), -0.2))
    return U(parts)


def make_set(prefix: str, walls: trimesh.Trimesh, roof: trimesh.Trimesh) -> None:
    export(f"{prefix}_walls", walls)
    # raise roof so preview seats on walls; separate roof file sits on Z=0 for printing
    export(f"{prefix}_roof", roof)
    # assembled preview
    wh = walls.bounds[1][2]
    preview = U([walls, T(roof, 0, 0, wh - LEDGE * 0.3)])
    export(f"{prefix}_preview", preview)


def tent_01_small_round() -> None:
    """Top-left: small conical round pavilion (fits one 32mm mini)."""
    R, H = 28.0, CLEAR_H
    walls = circle_walls(R, H, door_count=1)
    roof = circle_roof(R, peak_h=22, style="cone", finials="flag")
    make_set("01_small_round", walls, roof)


def tent_02_long_double() -> None:
    """Top-middle: elongated double-peak with two doors."""
    L, W, H = 86.0, 46.0, CLEAR_H
    doors = [(-20.0, 0, -1), (20.0, 0, -1)]
    walls = rect_walls(L, W, H, doors=doors)
    roof = rect_roof(L, W, peak_h=20, style="double", finials="flag")
    make_set("02_long_double", walls, roof)


def tent_03_grand_awning() -> None:
    """Top-right: large round with front awning."""
    R, H = 40.0, CLEAR_H + 2
    walls = circle_walls(R, H, door_count=1, awning=True)
    roof = circle_roof(R, peak_h=18, style="multi", finials="ball")
    make_set("03_grand_awning", walls, roof)


def tent_04_small_square() -> None:
    """Bottom-left: compact square single-peak."""
    L = W = 42.0
    H = CLEAR_H
    walls = rect_walls(L, W, H, doors=[(0.0, 0, -1)])
    roof = rect_roof(L, W, peak_h=20, style="pyramid", finials="flag")
    make_set("04_small_square", walls, roof)


def tent_05_ridge() -> None:
    """Bottom-middle: rectangular ridge with ball finials."""
    L, W, H = 58.0, 42.0, CLEAR_H
    walls = rect_walls(L, W, H, doors=[(0.0, 0, -1)])
    roof = rect_roof(L, W, peak_h=18, style="ridge", finials="ball")
    make_set("05_ridge", walls, roof)


def tent_06_triple() -> None:
    """Bottom-right: complex multi-peak rectangular."""
    L, W, H = 68.0, 46.0, CLEAR_H + 1
    walls = rect_walls(L, W, H, doors=[(0.0, 0, -1)])
    roof = rect_roof(L, W, peak_h=20, style="triple", finials="ball")
    make_set("06_triple", walls, roof)


def camp_layout() -> None:
    """3× layout of all tents for visual QA (not for printing)."""
    specs = []
    # load previews if exist after generation — rebuild lightly
    positions = [
        ("01", -100, 60),
        ("02", 15, 65),
        ("03", 120, 55),
        ("04", -95, -55),
        ("05", 10, -60),
        ("06", 110, -55),
    ]
    # regenerate compact previews from functions by reading exported files
    parts = []
    for key, x, y in positions:
        path = OUT / f"{key}_*_preview.stl"
        matches = list(OUT.glob(f"{key}_*_preview.stl"))
        if not matches:
            continue
        m = trimesh.load(matches[0])
        parts.append(T(m, x, y, 0))
    if parts:
        export("99_festival_camp_preview", U(parts))


def verify_door_clearance(walls: trimesh.Trimesh) -> dict:
    """Rough check: bounding box and that mesh is not solid brick."""
    e = walls.extents
    return {"extents": e.tolist(), "volume": float(walls.volume), "faces": len(walls.faces)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Generating festival tents (hollow + removable roofs)...")
    tent_01_small_round()
    tent_02_long_double()
    tent_03_grand_awning()
    tent_04_small_square()
    tent_05_ridge()
    tent_06_triple()
    camp_layout()
    print("Done.")
    print(
        f"\nPlayability targets: door ≥ {DOOR_W:.0f}×{DOOR_H:.0f} mm, "
        f"wall clear height ≥ {CLEAR_H:.0f} mm, wall thickness {WALL_T:.1f} mm."
    )
    print("Print walls and roofs separately; seat roof on the inner ledge after placing minis.")


if __name__ == "__main__":
    main()
