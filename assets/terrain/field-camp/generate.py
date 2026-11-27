#!/usr/bin/env python3
"""Generate printable STL terrain for a D&D field camp (28mm / 1\"=5ft)."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import trimesh
from trimesh.creation import box, cylinder, cone

OUT = Path(__file__).resolve().parent / "stl"
SCALE = 1.0  # mm already; keep hook for future rescale
TILE = 50.8  # 2 inch modular tile
WALL = 0.8  # min printable wall hint (mm), not enforced as hollow


def T(mesh: trimesh.Trimesh, x=0.0, y=0.0, z=0.0) -> trimesh.Trimesh:
    m = mesh.copy()
    m.apply_translation([x, y, z])
    return m


def R(mesh: trimesh.Trimesh, axis: str, deg: float) -> trimesh.Trimesh:
    m = mesh.copy()
    matrix = trimesh.transformations.rotation_matrix(math.radians(deg), {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[axis])
    m.apply_transform(matrix)
    return m


def union(parts: list[trimesh.Trimesh]) -> trimesh.Trimesh:
    clean = [p for p in parts if p is not None and len(p.faces)]
    if not clean:
        raise ValueError("empty union")
    if len(clean) == 1:
        return clean[0]
    return trimesh.util.concatenate(clean)


def ground_noise(size: float = TILE, thick: float = 2.5, seed: int = 1, bumps: int = 18) -> trimesh.Trimesh:
    """Solid ground tile with low bumps (FDM-friendly, no undercuts)."""
    rng = np.random.default_rng(seed)
    base = box(extents=[size, size, thick])
    base.apply_translation([0, 0, thick / 2])
    parts = [base]
    for _ in range(bumps):
        r = float(rng.uniform(2.5, 6.0))
        h = float(rng.uniform(0.35, 0.9))
        x = float(rng.uniform(-size / 2 + r, size / 2 - r))
        y = float(rng.uniform(-size / 2 + r, size / 2 - r))
        # flat discs = dirt clumps / stones, not tall bushes
        bump = cylinder(radius=r, height=h, sections=18)
        bump.apply_translation([x, y, thick + h / 2 - 0.15])
        parts.append(bump)
    # subtle edge lip so tiles nest visually on the table
    lip = box(extents=[size, size, 0.6])
    lip.apply_translation([0, 0, thick + 0.25])
    inset = box(extents=[size - 2.4, size - 2.4, 0.8])
    inset.apply_translation([0, 0, thick + 0.4])
    # keep lip as raised rim via concatenate (visual ridge)
    rim_n = 4
    for i in range(rim_n):
        ang = i * 90
        strip = box(extents=[size, 1.2, 0.7])
        strip.apply_translation([0, size / 2 - 0.6, thick + 0.25])
        parts.append(R(strip, "z", ang))
    return union(parts)


def path_tile(size: float = TILE, thick: float = 2.5) -> trimesh.Trimesh:
    base = ground_noise(size=size, thick=thick, seed=7, bumps=8)
    path = box(extents=[size * 0.42, size + 0.2, 1.0])
    path.apply_translation([0, 0, thick + 0.35])
    stones = []
    rng = np.random.default_rng(11)
    for _ in range(14):
        sx = float(rng.uniform(2.0, 4.0))
        sy = float(rng.uniform(2.0, 3.5))
        sz = float(rng.uniform(0.8, 1.4))
        x = float(rng.uniform(-size * 0.16, size * 0.16))
        y = float(rng.uniform(-size / 2 + 3, size / 2 - 3))
        stone = box(extents=[sx, sy, sz])
        stone.apply_translation([x, y, thick + 0.7])
        stones.append(stone)
    return union([base, path, *stones])


def _tri_prism(length: float, width: float, height: float) -> trimesh.Trimesh:
    """Solid A-frame / triangular prism along X."""
    hw, l2 = width / 2, length / 2
    vertices = [
        [-l2, -hw, 0],
        [l2, -hw, 0],
        [l2, hw, 0],
        [-l2, hw, 0],
        [-l2, 0, height],
        [l2, 0, height],
    ]
    faces = [
        [0, 1, 5],
        [0, 5, 4],  # left roof
        [3, 4, 5],
        [3, 5, 2],  # right roof
        [0, 4, 3],  # back
        [1, 2, 5],  # front
        [0, 3, 2],
        [0, 2, 1],  # floor
    ]
    return trimesh.Trimesh(vertices=vertices, faces=faces, process=True)


def _pyramid_roof(length: float, width: float, wall_h: float, peak_h: float) -> trimesh.Trimesh:
    """Rectangular wall box + pyramid roof."""
    hl, hw = length / 2, width / 2
    wall = box(extents=[length, width, wall_h])
    wall.apply_translation([0, 0, wall_h / 2])
    apex_z = wall_h + peak_h
    vertices = [
        [-hl, -hw, wall_h],
        [hl, -hw, wall_h],
        [hl, hw, wall_h],
        [-hl, hw, wall_h],
        [0, 0, apex_z],
    ]
    faces = [
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 3, 2],
        [0, 2, 1],
    ]
    roof = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    return union([wall, roof])


def wedge_tent() -> trimesh.Trimesh:
    """A-frame soldier tent ~24×40 mm footprint."""
    length, width, height = 40.0, 24.0, 20.0
    body = _tri_prism(length, width, height)
    # short floor plank for print bed adhesion
    floor = box(extents=[length - 1, width - 1, 1.2])
    floor.apply_translation([0, 0, 0.5])
    ridge = cylinder(radius=0.85, height=length + 1, sections=12)
    ridge = R(ridge, "y", 90)
    ridge.apply_translation([0, 0, height + 0.3])
    stakes = []
    for x, y in [(-length / 2 + 2, -width / 2), (-length / 2 + 2, width / 2), (length / 2 - 2, -width / 2), (length / 2 - 2, width / 2)]:
        s = cylinder(radius=0.75, height=5.5, sections=10)
        s.apply_translation([x, y, 2.75])
        stakes.append(s)
    # front entrance block (closed flap look)
    flap = box(extents=[1.4, width * 0.42, height * 0.45])
    flap.apply_translation([-length / 2 + 0.7, 0, height * 0.28])
    return union([body, floor, ridge, flap, *stakes])


def command_tent() -> trimesh.Trimesh:
    """Larger rectangular pavilion tent."""
    L, W, wall_h, peak = 48.0, 36.0, 12.0, 16.0
    body = _pyramid_roof(L, W, wall_h, peak)
    floor = box(extents=[L + 2, W + 2, 1.4])
    floor.apply_translation([0, 0, 0.7])
    # open front: cut look via recessed porch slab
    porch = box(extents=[L * 0.55, 6, 1.2])
    porch.apply_translation([0, -W / 2 - 2, 0.8])
    pole = cylinder(radius=1.1, height=wall_h + peak + 3, sections=14)
    pole.apply_translation([0, 0, (wall_h + peak + 3) / 2])
    finial = cone(radius=2.0, height=4.0, sections=14)
    finial.apply_translation([0, 0, wall_h + peak + 2.5])
    ropes = []
    for x in (-L / 2 + 5, L / 2 - 5):
        r = cylinder(radius=0.55, height=16, sections=8)
        r = R(r, "x", 40)
        r.apply_translation([x, -W / 2 - 3, 9])
        ropes.append(r)
        peg = cylinder(radius=0.85, height=3.5, sections=8)
        peg.apply_translation([x, -W / 2 - 9, 1.75])
        ropes.append(peg)
    # side guy pegs
    for x, y in [(-L / 2 - 3, 0), (L / 2 + 3, 0)]:
        peg = cylinder(radius=0.85, height=3.5, sections=8)
        peg.apply_translation([x, y, 1.75])
        ropes.append(peg)
    return union([floor, body, porch, pole, finial, *ropes])


def campfire() -> trimesh.Trimesh:
    ring = []
    for i in range(10):
        ang = i * (360 / 10)
        stone = box(extents=[4.5, 3.2, 2.8])
        stone = R(stone, "z", ang + 12)
        stone.apply_translation([8.5 * math.cos(math.radians(ang)), 8.5 * math.sin(math.radians(ang)), 1.4])
        ring.append(stone)
    ash = cylinder(radius=7.5, height=1.2, sections=24)
    ash.apply_translation([0, 0, 0.6])
    logs = []
    for i, a in enumerate([20, 80, 140]):
        log = cylinder(radius=1.8 - i * 0.15, height=14 - i, sections=12)
        log = R(log, "x", 90)
        log = R(log, "z", a)
        log.apply_translation([0, 0, 3.2 + i * 1.2])
        logs.append(log)
    flame = cone(radius=3.2, height=10, sections=16)
    flame.apply_translation([0, 0, 5.5])
    base = cylinder(radius=12, height=1.5, sections=28)
    base.apply_translation([0, 0, 0.75])
    return union([base, ash, *ring, *logs, flame])


def crate(w=12.0, d=10.0, h=10.0) -> trimesh.Trimesh:
    body = box(extents=[w, d, h])
    body.apply_translation([0, 0, h / 2])
    bands = []
    for z in (h * 0.25, h * 0.75):
        b = box(extents=[w + 0.6, d + 0.6, 1.2])
        b.apply_translation([0, 0, z])
        bands.append(b)
    lid_ridge = box(extents=[w * 0.9, 1.2, 1.0])
    lid_ridge.apply_translation([0, 0, h + 0.4])
    return union([body, *bands, lid_ridge])


def crate_stack() -> trimesh.Trimesh:
    a = crate(14, 11, 11)
    b = T(crate(12, 10, 9), 1.5, -1.0, 11)
    c = T(R(crate(10, 9, 8), "z", 18), -2.0, 1.5, 20)
    return union([a, b, c])


def barrel() -> trimesh.Trimesh:
    body = cylinder(radius=6.5, height=14, sections=28)
    body.apply_translation([0, 0, 7])
    rings = []
    for z in (2.5, 7, 11.5):
        r = cylinder(radius=7.1, height=1.1, sections=28)
        r.apply_translation([0, 0, z])
        rings.append(r)
    top = cylinder(radius=6.2, height=1.2, sections=28)
    top.apply_translation([0, 0, 14.2])
    return union([body, *rings, top])


def barricade() -> trimesh.Trimesh:
    """Low wooden barricade ~50 mm wide."""
    posts = []
    for x in (-22, -7, 7, 22):
        p = box(extents=[3.2, 3.2, 18])
        p.apply_translation([x, 0, 9])
        posts.append(p)
    planks = []
    for z, yoff in [(5, 0.8), (10, -0.6), (15, 0.4)]:
        plank = box(extents=[48, 2.4, 3.2])
        plank.apply_translation([0, yoff, z])
        planks.append(plank)
    braces = []
    for x, ang in [(-12, 28), (12, -28)]:
        b = box(extents=[3, 2.2, 16])
        b = R(b, "y", ang)
        b.apply_translation([x, 1.5, 9])
        braces.append(b)
    base = box(extents=[50, 10, 2])
    base.apply_translation([0, 0, 1])
    return union([base, *posts, *planks, *braces])


def palisade_wall(length: float = TILE) -> trimesh.Trimesh:
    logs = []
    n = int(length // 4.2)
    for i in range(n):
        x = -length / 2 + 2.1 + i * 4.2
        h = 28 + (i % 3) * 1.5
        log = cylinder(radius=2.0, height=h, sections=12)
        log.apply_translation([x, 0, h / 2])
        tip = cone(radius=2.0, height=4.0, sections=12)
        tip.apply_translation([x, 0, h])
        logs.extend([log, tip])
    rail = box(extents=[length - 2, 2.2, 2.2])
    rail.apply_translation([0, 1.6, 12])
    base = box(extents=[length, 8, 2])
    base.apply_translation([0, 0, 1])
    return union([base, rail, *logs])


def palisade_corner() -> trimesh.Trimesh:
    a = palisade_wall(TILE)
    b = R(palisade_wall(TILE), "z", 90)
    # overlap posts ok for terrain
    return union([a, b])


def weapon_rack() -> trimesh.Trimesh:
    posts = []
    for x in (-10, 10):
        p = box(extents=[2.5, 2.5, 22])
        p.apply_translation([x, 0, 11])
        posts.append(p)
    rails = []
    for z in (8, 16):
        r = box(extents=[22, 2.0, 2.0])
        r.apply_translation([0, 0, z])
        rails.append(r)
    spears = []
    for x in (-7, -2.5, 2.5, 7):
        shaft = cylinder(radius=0.7, height=26, sections=8)
        shaft.apply_translation([x, 1.2, 14])
        tip = cone(radius=1.3, height=4, sections=8)
        tip.apply_translation([x, 1.2, 28])
        spears.extend([shaft, tip])
    base = box(extents=[24, 8, 2])
    base.apply_translation([0, 0, 1])
    return union([base, *posts, *rails, *spears])


def banner_pole() -> trimesh.Trimesh:
    pole = cylinder(radius=1.4, height=46, sections=14)
    pole.apply_translation([0, 0, 23])
    base = cylinder(radius=6, height=2.5, sections=18)
    base.apply_translation([0, 0, 1.25])
    cross = cylinder(radius=0.9, height=16, sections=10)
    cross = R(cross, "x", 90)
    cross.apply_translation([0, 0, 42])
    flag = box(extents=[0.9, 14, 10])
    flag.apply_translation([0.8, 7, 36])
    # simple swallow-tail notch via second block omitted (keep solid)
    return union([base, pole, cross, flag])


def watch_post() -> trimesh.Trimesh:
    """Small raised lookout ~30 mm platform."""
    legs = []
    for x, y in [(-10, -10), (-10, 10), (10, -10), (10, 10)]:
        leg = box(extents=[3.2, 3.2, 26])
        leg.apply_translation([x, y, 13])
        legs.append(leg)
    deck = box(extents=[26, 26, 2.2])
    deck.apply_translation([0, 0, 27])
    rail = []
    for yaw in (0, 90, 180, 270):
        r = box(extents=[26, 1.6, 4])
        r.apply_translation([0, 12.2, 30])
        rail.append(R(r, "z", yaw))
    ladder = []
    for z in range(3, 26, 4):
        step = box(extents=[8, 1.6, 1.4])
        step.apply_translation([0, -13.5, z])
        ladder.append(step)
    sides = box(extents=[1.6, 1.6, 26])
    ladder.append(T(sides, -4, -13.5, 13))
    ladder.append(T(sides, 4, -13.5, 13))
    base = box(extents=[30, 30, 2])
    base.apply_translation([0, 0, 1])
    return union([base, *legs, deck, *rail, *ladder])


def bedroll() -> trimesh.Trimesh:
    mat = cylinder(radius=4.5, height=22, sections=18)
    mat = R(mat, "x", 90)
    mat.apply_translation([0, 0, 4.5])
    strap = box(extents=[10, 2, 1.2])
    strap.apply_translation([0, 0, 8.2])
    pack = box(extents=[8, 6, 5])
    pack.apply_translation([0, 10, 2.5])
    return union([mat, strap, pack])


def camp_layout_preview() -> trimesh.Trimesh:
    """Assembled preview for visualization only (large; not meant as one print)."""
    parts = []
    # 3x3 tile grid
    for ix in range(3):
        for iy in range(3):
            x = (ix - 1) * TILE
            y = (iy - 1) * TILE
            tile = path_tile() if (ix, iy) == (1, 1) else ground_noise(seed=ix * 10 + iy + 1, bumps=12)
            parts.append(T(tile, x, y, 0))
    z = 2.5
    parts.append(T(wedge_tent(), -TILE, TILE * 0.15, z))
    parts.append(T(R(wedge_tent(), "z", 90), TILE * 0.2, TILE, z))
    parts.append(T(command_tent(), 0, -TILE * 0.15, z))
    parts.append(T(campfire(), 0, 0, z))
    parts.append(T(crate_stack(), TILE * 0.75, -TILE * 0.7, z))
    parts.append(T(barrel(), TILE * 0.45, -TILE * 0.55, z))
    parts.append(T(barricade(), 0, TILE * 1.35, z))
    parts.append(T(palisade_wall(), -TILE, -TILE, z))
    parts.append(T(R(palisade_wall(), "z", 90), -TILE * 1.35, 0, z))
    parts.append(T(weapon_rack(), TILE, TILE * 0.35, z))
    parts.append(T(banner_pole(), -TILE * 0.35, TILE * 0.55, z))
    parts.append(T(watch_post(), TILE, -TILE, z))
    parts.append(T(bedroll(), -TILE * 0.55, TILE * 0.55, z))
    return union(parts)


MODELS = {
    "01_tile_ground_2x2": ground_noise,
    "02_tile_path_2x2": path_tile,
    "03_tent_wedge": wedge_tent,
    "04_tent_command": command_tent,
    "05_campfire": campfire,
    "06_crate_single": crate,
    "07_crate_stack": crate_stack,
    "08_barrel": barrel,
    "09_barricade": barricade,
    "10_palisade_wall": palisade_wall,
    "11_palisade_corner": palisade_corner,
    "12_weapon_rack": weapon_rack,
    "13_banner_pole": banner_pole,
    "14_watch_post": watch_post,
    "15_bedroll": bedroll,
    "99_camp_layout_preview": camp_layout_preview,
}


def finalize(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    m = mesh.copy()
    if SCALE != 1.0:
        m.apply_scale(SCALE)
    m.merge_vertices()
    m.update_faces(m.unique_faces())
    m.remove_unreferenced_vertices()
    # sit on build plate
    m.apply_translation([0, 0, -m.bounds[0][2]])
    return m


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in MODELS.items():
        mesh = finalize(fn())
        path = OUT / f"{name}.stl"
        mesh.export(path)
        extents = mesh.extents
        print(f"wrote {path.name:28s}  tris={len(mesh.faces):5d}  size={extents[0]:.1f}x{extents[1]:.1f}x{extents[2]:.1f} mm")


if __name__ == "__main__":
    main()
