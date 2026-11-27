#!/usr/bin/env python3
"""Sand dune / barchan terrain for battle maps (FDM STL, ~32mm scale).

Pieces sit flat on the table. Surfaces are gently rippled so minis can stand
on windward slopes; leeward faces are steeper (difficult / cover terrain).
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import trimesh

OUT = Path(__file__).resolve().parent / "stl"


def heightfield_mesh(
    Z: np.ndarray,
    cell: float = 2.0,
    base_z: float = 0.0,
    solid: bool = True,
) -> trimesh.Trimesh:
    """Build a printable solid from a 2D height map Z[y, x] in mm."""
    ny, nx = Z.shape
    xs = (np.arange(nx) - (nx - 1) / 2.0) * cell
    ys = (np.arange(ny) - (ny - 1) / 2.0) * cell
    xx, yy = np.meshgrid(xs, ys)

    # top surface vertices
    top = np.column_stack([xx.ravel(), yy.ravel(), Z.ravel()])

    faces = []
    def vid(i, j):
        return j * nx + i

    for j in range(ny - 1):
        for i in range(nx - 1):
            # skip degenerate flat zero cells at the very edge if both quads near zero
            z00, z10, z01, z11 = Z[j, i], Z[j, i + 1], Z[j + 1, i], Z[j + 1, i + 1]
            if max(z00, z10, z01, z11) <= base_z + 0.15:
                continue
            a, b, c, d = vid(i, j), vid(i + 1, j), vid(i, j + 1), vid(i + 1, j + 1)
            faces.append([a, b, d])
            faces.append([a, d, c])

    if not faces:
        raise ValueError("empty heightfield")

    if not solid:
        mesh = trimesh.Trimesh(vertices=top, faces=np.array(faces), process=True)
        mesh.apply_translation([0, 0, -mesh.bounds[0][2]])
        return mesh

    # bottom vertices (same XY, z=base)
    bottom = np.column_stack([xx.ravel(), yy.ravel(), np.full(nx * ny, base_z)])
    n_top = len(top)
    verts = np.vstack([top, bottom])

    # top faces already index into top verts
    all_faces = list(faces)

    # bottom faces (reversed winding)
    for f in faces:
        all_faces.append([f[0] + n_top, f[2] + n_top, f[1] + n_top])

    # side walls along grid edges where height > base
    # horizontal edges (along x)
    for j in range(ny):
        for i in range(nx - 1):
            if j not in (0, ny - 1):
                # only silhouette edges: if neighbor outside skipped region
                pass
    # Build boundary by checking each top triangle edge usage
    from collections import Counter

    edge_count: Counter = Counter()
    for a, b, c in faces:
        for u, v in ((a, b), (b, c), (c, a)):
            edge_count[tuple(sorted((u, v)))] += 1
    boundary = [e for e, n in edge_count.items() if n == 1]
    for u, v in boundary:
        # side quad u,v -> v+n, u+n
        all_faces.append([u, v, v + n_top])
        all_faces.append([u, v + n_top, u + n_top])

    mesh = trimesh.Trimesh(vertices=verts, faces=np.array(all_faces), process=False)
    mesh.remove_unreferenced_vertices()
    mesh.merge_vertices()
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    # sit on bed
    mesh.apply_translation([0, 0, -mesh.bounds[0][2]])
    return mesh


def ripples(X: np.ndarray, Y: np.ndarray, amp: float = 0.45, wavelength: float = 8.0, angle_deg: float = 15.0) -> np.ndarray:
    ang = math.radians(angle_deg)
    u = X * math.cos(ang) + Y * math.sin(ang)
    return amp * np.sin(2 * math.pi * u / wavelength)


def soft_mask(dist: np.ndarray, inner: float, outer: float) -> np.ndarray:
    """1 inside inner, 0 outside outer, smoothstep between."""
    t = np.clip((outer - dist) / max(outer - inner, 1e-6), 0, 1)
    return t * t * (3 - 2 * t)


def barchan_height(
    nx: int,
    ny: int,
    cell: float,
    length: float,
    width: float,
    height: float,
    horn_spread: float = 1.15,
    seed: int = 0,
) -> np.ndarray:
    """Classic crescent barchan: gentle windward (+Y), steep slip face (-Y horns).

    Wind assumed from +Y toward -Y; horns point downwind (-Y).
    """
    rng = np.random.default_rng(seed)
    xs = (np.arange(nx) - (nx - 1) / 2.0) * cell
    ys = (np.arange(ny) - (ny - 1) / 2.0) * cell
    X, Y = np.meshgrid(xs, ys)

    # normalize ellipse coords
    a = length / 2.0
    b = width / 2.0
    # crescent: push center of mass windward, carve leeward bowl
    Yn = Y / a
    Xn = X / (b * horn_spread)

    # base mound (asymmetric)
    windward = np.exp(-((Xn) ** 2) * 1.1 - ((Yn - 0.15) ** 2) * 0.9)
    # slip face drop on leeward side
    slip = 1.0 / (1.0 + np.exp(-(Y + a * 0.05) / (a * 0.08)))  # sigmoid
    # horns: raise sides on leeward
    horns = np.exp(-((np.abs(Xn) - 0.55) ** 2) / 0.12) * soft_mask(-Y, 0, a * 0.9)
    horns *= soft_mask(np.abs(X), b * 0.15, b * 0.95)

    body = windward * (0.55 + 0.45 * slip)
    body = np.maximum(body, horns * 0.85)

    # footprint mask — crescent outline
    # distance field approx
    r_ell = np.sqrt(Xn**2 + (Yn * 0.95) ** 2)
    # bite a crescent notch on leeward center
    notch = np.exp(-((X / (b * 0.35)) ** 2) - (((Y + a * 0.35) / (a * 0.45)) ** 2))
    mask = soft_mask(r_ell, 0.55, 1.05) * (1.0 - 0.85 * notch * (Y < 0))

    Z = height * body * mask
    Z += ripples(X, Y, amp=height * 0.04, wavelength=7.5, angle_deg=8) * mask
    # tiny noise
    Z += rng.normal(0, height * 0.012, size=Z.shape) * mask
    Z = np.clip(Z, 0, None)
    # ensure printable minimum slope start — flatten near zero
    Z[Z < 0.4] = 0
    return Z


def ridge_height(nx, ny, cell, length, width, height, seed=1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    xs = (np.arange(nx) - (nx - 1) / 2.0) * cell
    ys = (np.arange(ny) - (ny - 1) / 2.0) * cell
    X, Y = np.meshgrid(xs, ys)
    # elongated along X, crest slightly sinuous
    crest_y = 3.0 * np.sin(X / (length / 6))
    dist = np.abs(Y - crest_y)
    # asymmetric: gentle +Y, steep -Y
    gentle = np.exp(-((dist / (width * 0.55)) ** 2)) * (Y >= crest_y)
    steep = np.exp(-((dist / (width * 0.28)) ** 2)) * (Y < crest_y)
    body = np.where(Y >= crest_y, gentle, steep)
    mask_x = soft_mask(np.abs(X), length * 0.35, length * 0.5)
    mask_y = soft_mask(np.abs(Y), width * 0.35, width * 0.55)
    mask = mask_x * np.maximum(mask_y, body * 0.2)
    Z = height * body * mask_x
    Z += ripples(X, Y, amp=height * 0.05, wavelength=6.5, angle_deg=-5) * mask_x
    Z += rng.normal(0, height * 0.01, size=Z.shape) * mask_x
    Z = np.clip(Z, 0, None)
    Z[Z < 0.35] = 0
    return Z


def mound_height(nx, ny, cell, radius, height, seed=2) -> np.ndarray:
    rng = np.random.default_rng(seed)
    xs = (np.arange(nx) - (nx - 1) / 2.0) * cell
    ys = (np.arange(ny) - (ny - 1) / 2.0) * cell
    X, Y = np.meshgrid(xs, ys)
    # slightly oval, off-center peak
    R = np.sqrt(((X - radius * 0.08) / (radius * 1.05)) ** 2 + ((Y + radius * 0.05) / (radius * 0.9)) ** 2)
    body = np.clip(1 - R, 0, 1) ** 1.35
    mask = soft_mask(R, 0.75, 1.05)
    Z = height * body * mask
    Z += ripples(X, Y, amp=height * 0.06, wavelength=5.5, angle_deg=20) * mask
    Z += rng.normal(0, height * 0.015, size=Z.shape) * mask
    Z = np.clip(Z, 0, None)
    Z[Z < 0.3] = 0
    return Z


def ripple_tile(nx, ny, cell, height=2.8, seed=3) -> np.ndarray:
    """Low ripple ground tile for dune field fill (2x2 inch-ish)."""
    rng = np.random.default_rng(seed)
    xs = (np.arange(nx) - (nx - 1) / 2.0) * cell
    ys = (np.arange(ny) - (ny - 1) / 2.0) * cell
    X, Y = np.meshgrid(xs, ys)
    base = 1.2
    Z = base + ripples(X, Y, amp=height * 0.45, wavelength=9.0, angle_deg=12)
    Z += 0.25 * ripples(X, Y, amp=1.0, wavelength=4.0, angle_deg=-25)
    Z += rng.normal(0, 0.08, size=Z.shape)
    # soft edge fade so tiles blend visually
    edge = soft_mask(np.maximum(np.abs(X), np.abs(Y)) / (max(xs[-1], 1)), 0.72, 1.02)
    Z = Z * edge
    Z = np.clip(Z, 0, None)
    return Z


def seif_height(nx, ny, cell, length, width, height, seed=4) -> np.ndarray:
    """Longitudinal seif dune — snake ridge."""
    rng = np.random.default_rng(seed)
    xs = (np.arange(nx) - (nx - 1) / 2.0) * cell
    ys = (np.arange(ny) - (ny - 1) / 2.0) * cell
    X, Y = np.meshgrid(xs, ys)
    path = 6.0 * np.sin(X * 2 * math.pi / (length * 0.7)) + 2.5 * np.sin(X * 4 * math.pi / length)
    dist = np.abs(Y - path)
    body = np.exp(-((dist / (width * 0.4)) ** 2))
    mask_x = soft_mask(np.abs(X), length * 0.38, length * 0.5)
    Z = height * body * mask_x
    Z += ripples(X, Y, amp=height * 0.05, wavelength=7.0, angle_deg=70) * mask_x
    Z += rng.normal(0, height * 0.012, size=Z.shape) * mask_x
    Z = np.clip(Z, 0, None)
    Z[Z < 0.35] = 0
    return Z


def export(name: str, mesh: trimesh.Trimesh) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.stl"
    mesh.export(path)
    e = mesh.extents
    print(f"  {path.name:36s}  {e[0]:5.1f}×{e[1]:5.1f}×{e[2]:5.1f} mm  faces={len(mesh.faces)}")


def make_barchan(name: str, length: float, width: float, height: float, cell: float = 2.0, seed: int = 0) -> trimesh.Trimesh:
    nx = int(width / cell) + 3
    ny = int(length / cell) + 3
    # ensure odd-ish coverage
    nx = max(nx, 24)
    ny = max(ny, 24)
    Z = barchan_height(nx, ny, cell, length=length, width=width, height=height, seed=seed)
    return heightfield_mesh(Z, cell=cell)


def make_ridge(name, length, width, height, cell=2.0, seed=1):
    nx = int(length / cell) + 3
    ny = int(width / cell) + 3
    Z = ridge_height(nx, ny, cell, length, width, height, seed=seed)
    return heightfield_mesh(Z, cell=cell)


def make_mound(radius, height, cell=2.0, seed=2):
    n = int((radius * 2.2) / cell) + 3
    Z = mound_height(n, n, cell, radius, height, seed=seed)
    return heightfield_mesh(Z, cell=cell)


def make_tile(size=50.8, cell=2.0, seed=3):
    n = int(size / cell) + 1
    Z = ripple_tile(n, n, cell, height=2.8, seed=seed)
    return heightfield_mesh(Z, cell=cell)


def make_seif(length, width, height, cell=2.0, seed=4):
    nx = int(length / cell) + 3
    ny = int(width / cell) + 3
    Z = seif_height(nx, ny, cell, length, width, height, seed=seed)
    return heightfield_mesh(Z, cell=cell)


def layout_preview(meshes: list[tuple[trimesh.Trimesh, float, float]]) -> trimesh.Trimesh:
    parts = []
    for m, x, y in meshes:
        c = m.copy()
        c.apply_translation([x, y, 0])
        parts.append(c)
    return trimesh.util.concatenate(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Generating sand dune terrain...")

    pieces = {}
    pieces["01_barchan_small"] = make_barchan("01", length=55, width=70, height=12, cell=2.0, seed=11)
    pieces["02_barchan_medium"] = make_barchan("02", length=75, width=95, height=18, cell=2.2, seed=22)
    pieces["03_barchan_large"] = make_barchan("03", length=100, width=130, height=26, cell=2.5, seed=33)
    pieces["04_dune_ridge"] = make_ridge("04", length=120, width=50, height=16, cell=2.2, seed=44)
    pieces["05_sand_mound"] = make_mound(radius=32, height=14, cell=2.0, seed=55)
    pieces["06_seif_dune"] = make_seif(length=130, width=45, height=15, cell=2.2, seed=66)
    pieces["07_ripple_tile_2x2"] = make_tile(size=50.8, cell=2.0, seed=77)
    pieces["08_barchan_pair"] = None  # built below

    # pair: two small barchans offset
    a = make_barchan("a", length=50, width=65, height=11, cell=2.0, seed=81)
    b = make_barchan("b", length=48, width=60, height=10, cell=2.0, seed=82)
    b.apply_translation([38, -22, 0])
    a.apply_translation([-20, 18, 0])
    pieces["08_barchan_pair"] = trimesh.util.concatenate([a, b])
    # re-ground
    pieces["08_barchan_pair"].apply_translation([0, 0, -pieces["08_barchan_pair"].bounds[0][2]])

    for name, mesh in pieces.items():
        export(name, mesh)

    preview = layout_preview(
        [
            (pieces["01_barchan_small"], -90, 60),
            (pieces["02_barchan_medium"], 30, 70),
            (pieces["03_barchan_large"], 160, 40),
            (pieces["04_dune_ridge"], -40, -70),
            (pieces["05_sand_mound"], 80, -60),
            (pieces["06_seif_dune"], 200, -80),
            (pieces["07_ripple_tile_2x2"], -120, -40),
            (pieces["08_barchan_pair"], -100, -120),
        ]
    )
    export("99_dune_field_preview", preview)
    print("Done.")


if __name__ == "__main__":
    main()
