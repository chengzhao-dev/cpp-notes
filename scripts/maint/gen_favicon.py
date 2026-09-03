#!/usr/bin/env python3
"""生成站点图标 favicon.svg（纯标准库，无第三方依赖）。

图标形状参数集中在本文件顶部，`svg_text()` 据此序列化 SVG；同一套参数也能
光栅化（`render()`），供 `--preview` 出小尺寸放大图，人工核对 16/32px 是否糊。

用法：
    python scripts/maint/gen_favicon.py              # 写 theme/assets/favicon.svg
    python scripts/maint/gen_favicon.py --preview d  # 另存 16/32/256 预览 PNG 到目录 d

说明：_quarto.yml 的 book.favicon 只接受单个文件，现代浏览器（含 Safari 15+）
支持 SVG favicon，故不附带 ICO——避免发布无人引用的产物。
"""

import argparse
import math
import struct
import zlib
from pathlib import Path

ACCENT = (0xF5, 0x4E, 0x00)  # 与 tokens.css --link-color 亮色一致
WHITE = (0xFF, 0xFF, 0xFF)
VB = 64.0  # viewBox 边长
CORNER_R = 14.0  # 背景圆角半径

# 「C」：圆心、半径、笔画宽、开口半角（度）。开口朝右
C_CX, C_CY, C_R, C_W, C_OPEN = 22.0, 32.0, 11.0, 7.0, 55.0
# 两个「+」：中心 x（留 5 单位间隙，16px 下仍分得开）、臂长、笔画宽
PLUS_CY, PLUS_ARM, PLUS_W = 32.0, 4.5, 6.0
PLUS_CX = (40.0, 54.0)


def _in_bg(x, y):
    """背景圆角矩形命中判定。"""
    r = CORNER_R
    if r <= x <= VB - r or r <= y <= VB - r:
        return 0 <= x <= VB and 0 <= y <= VB
    cx = r if x < r else VB - r
    cy = r if y < r else VB - r
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def _dist_to_arc(x, y, cx, cy, r, half_deg):
    """到「C」中心线（角度区间内圆弧）的距离。"""
    dx, dy = x - cx, y - cy
    ang = math.degrees(math.atan2(dy, dx)) % 360.0
    lo, hi = 180.0 - half_deg, 180.0 + half_deg
    for cand in (ang, ang - 360.0, ang + 360.0):
        if lo <= cand <= hi:
            return abs(math.hypot(dx, dy) - r)
    def endpoint_dist(bound):
        rad = math.radians(bound)
        ex, ey = cx + r * math.cos(rad), cy + r * math.sin(rad)
        return math.hypot(x - ex, y - ey)

    return min(endpoint_dist(lo), endpoint_dist(hi))


def _dist_to_seg(x, y, ax, ay, bx, by):
    """到线段距离。"""
    px, py = x - ax, y - ay
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, (px * vx + py * vy) / L2))
    return math.hypot(px - t * vx, py - t * vy)


def _coverage(d, width):
    """描边覆盖率：距中心线 width/2 内为实，边缘 1 单位做抗锯齿。"""
    half = width / 2.0
    if d <= half - 0.5:
        return 1.0
    if d >= half + 0.5:
        return 0.0
    return half + 0.5 - d


def sample(x, y):
    """viewBox 坐标 -> (r, g, b, a)：背景 + 白色 C++ 合成。"""
    if not _in_bg(x, y):
        return 0, 0, 0, 0
    parts = [_coverage(_dist_to_arc(x, y, C_CX, C_CY, C_R, C_OPEN), C_W)]
    for cx in PLUS_CX:
        h = _dist_to_seg(x, y, cx - PLUS_ARM, PLUS_CY, cx + PLUS_ARM, PLUS_CY)
        v = _dist_to_seg(x, y, cx, PLUS_CY - PLUS_ARM, cx, PLUS_CY + PLUS_ARM)
        parts.append(_coverage(h, PLUS_W))
        parts.append(_coverage(v, PLUS_W))
    fa = 1.0 - math.prod(1.0 - min(1.0, max(0.0, p)) for p in parts)
    return (
        round(ACCENT[0] * (1 - fa) + WHITE[0] * fa),
        round(ACCENT[1] * (1 - fa) + WHITE[1] * fa),
        round(ACCENT[2] * (1 - fa) + WHITE[2] * fa),
        255,
    )


def render(size, ss=4):
    """光栅化 size×size（每边 ss 倍超采样），返回 RGBA 字节串。"""
    scale = VB / size
    px = bytearray(size * size * 4)
    for py_ in range(size):
        for pxx in range(size):
            acc = [0.0, 0.0, 0.0, 0.0]
            for sy in range(ss):
                for sx in range(ss):
                    vx = (pxx + (sx + 0.5) / ss) * scale
                    vy = (py_ + (sy + 0.5) / ss) * scale
                    r, g, b, a = sample(vx, vy)
                    acc[0] += r * a
                    acc[1] += g * a
                    acc[2] += b * a
                    acc[3] += a
            i = (py_ * size + pxx) * 4
            if acc[3] == 0:
                continue
            a = acc[3]
            px[i : i + 4] = bytes(
                (
                    round(acc[0] / a),
                    round(acc[1] / a),
                    round(acc[2] / a),
                    round(a / (ss * ss)),
                )
            )
    return bytes(px)


def png_bytes(size, data):
    """RGBA 字节串 -> PNG。"""

    def chunk(typ, payload):
        return (
            struct.pack(">I", len(payload))
            + typ
            + payload
            + struct.pack(">I", zlib.crc32(typ + payload) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    stride = size * 4
    raw = b"".join(b"\x00" + data[y * stride : (y + 1) * stride] for y in range(size))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def upscale(size, data, factor):
    """最近邻放大，便于肉眼检查小尺寸清晰度。"""
    w = size * factor
    big = bytearray(w * w * 4)
    for y in range(size):
        for x in range(size):
            src = (y * size + x) * 4
            for dy in range(factor):
                row = ((y * factor + dy) * w + x * factor) * 4
                for dx in range(factor):
                    big[row + dx * 4 : row + dx * 4 + 4] = data[src : src + 4]
    return w, bytes(big)


def svg_text():
    """按形状参数序列化 SVG（与 render() 同一套几何）。"""
    rad = math.radians(C_OPEN)
    ex, ey = C_R * math.cos(rad), C_R * math.sin(rad)
    start_x = C_CX - C_R + ex
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"'
        ' role="img" aria-label="C++">',
        f'  <rect width="64" height="64" rx="{CORNER_R:g}"'
        f' fill="#{ACCENT[0]:02X}{ACCENT[1]:02X}{ACCENT[2]:02X}"/>',
        f'  <path d="M{start_x:.2f} {C_CY + ey:.2f} A{C_R:g} {C_R:g} 0 1 1'
        f' {start_x:.2f} {C_CY - ey:.2f}"'
        f' fill="none" stroke="#FFF"'
        f' stroke-width="{C_W:g}" stroke-linecap="round"/>',
        f'  <g stroke="#FFF" stroke-width="{PLUS_W:g}" stroke-linecap="round">',
    ]
    for cx in PLUS_CX:
        lines.append(
            f'    <path d="M{cx - PLUS_ARM:g} {PLUS_CY:g}h{2 * PLUS_ARM:g}'
            f'M{cx:g} {PLUS_CY - PLUS_ARM:g}v{2 * PLUS_ARM:g}"/>'
        )
    lines += ["  </g>", "</svg>"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preview",
        metavar="DIR",
        help="额外输出 16/32/256 预览 PNG（16、32 做 10x 最近邻放大）到 DIR",
    )
    args = parser.parse_args()

    out = Path("theme/assets")
    out.mkdir(parents=True, exist_ok=True)
    target = out / "favicon.svg"
    target.write_text(svg_text(), encoding="utf-8", newline="\n")
    print(f"已生成 {target} ({target.stat().st_size} bytes)")

    if args.preview:
        prev = Path(args.preview)
        prev.mkdir(parents=True, exist_ok=True)
        for size in (16, 32):
            w, big = upscale(size, render(size), 10)
            (prev / f"favicon-{size}px@10x.png").write_bytes(png_bytes(w, big))
        (prev / "favicon-256.png").write_bytes(png_bytes(256, render(256)))
        print(f"预览已输出到 {prev}")


if __name__ == "__main__":
    main()