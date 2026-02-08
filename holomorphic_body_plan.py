#!/usr/bin/env python3
"""Toy holomorphic body-plan generator (ASCII)."""

from __future__ import annotations

import math


WIDTH = 80
HEIGHT = 40
X_MIN, X_MAX = -1.0, 1.0
Y_MIN, Y_MAX = -1.0, 1.0

HEAD_THRESHOLD = 0.6
TAIL_THRESHOLD = -0.6
SPINE_HALF_WIDTH = 0.08
SEGMENT_K = 10.0
LIMB_X0 = 0.35
LIMB_RADIUS = 0.08
LIMB_Y_RANGE = (0.18, 0.45)


def classify_point(x: float, y: float) -> str:
    z = complex(x, y)

    phi_1 = z.real  # f1(z) = z

    f_2 = 1j * z
    phi_2 = f_2.real  # -y

    f_3 = cmath_exp(1j * SEGMENT_K * z)
    phi_3 = f_3.real

    f_4 = (z - LIMB_X0) * (z + LIMB_X0)
    limb_near = abs(f_4) < LIMB_RADIUS
    limb_y_ok = LIMB_Y_RANGE[0] <= abs(y) <= LIMB_Y_RANGE[1]

    if limb_near and limb_y_ok and TAIL_THRESHOLD <= phi_1 <= HEAD_THRESHOLD:
        return "L"

    if phi_1 > HEAD_THRESHOLD:
        return "H"
    if phi_1 < TAIL_THRESHOLD:
        return "T"

    if abs(phi_2) < SPINE_HALF_WIDTH:
        return "|"

    return "A" if phi_3 >= 0 else "B"


def cmath_exp(z: complex) -> complex:
    """cmath.exp without importing cmath to keep dependencies minimal."""
    exp_real = math.exp(z.real)
    return complex(exp_real * math.cos(z.imag), exp_real * math.sin(z.imag))


def render() -> str:
    rows = []
    for j in range(HEIGHT):
        y = Y_MAX - (Y_MAX - Y_MIN) * (j / (HEIGHT - 1))
        row_chars = []
        for i in range(WIDTH):
            x = X_MIN + (X_MAX - X_MIN) * (i / (WIDTH - 1))
            row_chars.append(classify_point(x, y))
        rows.append("".join(row_chars))
    return "\n".join(rows)


if __name__ == "__main__":
    print(render())
