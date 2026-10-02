from figstyle import plt, np, save, C
from matplotlib.patches import Circle

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[0.9, 1.1]))

# 왼쪽: 백질 복셀 단면의 세 구획과 무작위 걸음
rng = np.random.default_rng(11)
axons = [(0.75, 0.85, 0.45), (2.45, 0.8, 0.4), (1.55, 2.0, 0.55), (2.95, 2.25, 0.38), (0.65, 3.2, 0.4),
         (2.1, 3.5, 0.42)]
for x, y, r in axons:
    a1.add_patch(Circle((x, y), r + 0.12, facecolor="none", edgecolor=C["purple"], lw=2.2, alpha=0.6))
    a1.add_patch(Circle((x, y), r, facecolor=C["green"], alpha=0.2, edgecolor=C["green"], lw=0.8))
a1.add_patch(plt.Rectangle((3.55, 0.2), 1.05, 3.9, facecolor=C["blue"], alpha=0.12, lw=0))


def walk(x0, y0, n, step, inside=None, box=None):
    pts = [(x0, y0)]
    for _ in range(n):
        while True:
            th = rng.uniform(0, 2 * np.pi)
            x, y = pts[-1][0] + step * np.cos(th), pts[-1][1] + step * np.sin(th)
            if inside is not None:
                cx, cy, r = inside
                ok = (x - cx) ** 2 + (y - cy) ** 2 < (r - 0.04) ** 2
            else:
                ok = all((x - cx) ** 2 + (y - cy) ** 2 > (r + 0.13) ** 2 for cx, cy, r in axons)
                ok = ok and 0.15 < x < 3.5 and 0.15 < y < 4.1
            if box is not None:
                ok = box[0] < x < box[1] and box[2] < y < box[3]
            if ok:
                pts.append((x, y))
                break
    return np.array(pts)


p = walk(1.55, 2.0, 260, 0.06, inside=axons[2])
a1.plot(p[:, 0], p[:, 1], color=C["red"], lw=0.8)
p = walk(2.2, 1.45, 1500, 0.05)
a1.plot(p[:, 0], p[:, 1], color=C["red"], lw=0.8)
p = walk(4.05, 2.1, 700, 0.06, box=(3.6, 4.55, 0.25, 4.05))
a1.plot(p[:, 0], p[:, 1], color=C["red"], lw=0.8)
a1.annotate("제한 (축삭 안)", xy=(1.55, 2.0), xytext=(1.0, 4.05), fontsize=8.5, color=C["ink"], ha="center",
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
a1.text(1.9, 0.0, "장애 (축삭 사이)", ha="center", va="top", fontsize=8.5, color=C["ink"])
a1.text(4.08, 0.0, "자유\n(뇌척수액)", ha="center", va="top", fontsize=8.5, color=C["blue"])
a1.text(2.4, -0.62, "보라 테두리 = 수초, 섬유는 지면에 수직", ha="center", va="top", fontsize=8, color=C["purple"])
a1.set_xlim(0, 4.7)
a1.set_ylim(-1.1, 4.4)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 섬유에 수직인 방향의 신호 감쇠
b = np.linspace(0, 5000, 300)
f_in = 0.5
free = np.exp(-b * 3.0e-3)
hind = np.exp(-b * 0.8e-3)
restr = np.ones_like(b)
mix = f_in * restr + (1 - f_in) * hind
adc = -np.log(mix[np.searchsorted(b, 1000)]) / 1000
fit = np.exp(-b * adc)
a2.semilogy(b, free, color=C["blue"], lw=1.6)
a2.semilogy(b, hind, color=C["green"], lw=1.6, ls="--")
a2.semilogy(b, restr, color=C["purple"], lw=1.6, ls=":")
a2.semilogy(b, mix, color=C["red"], lw=2.2)
a2.semilogy(b, fit, color=C["gray"], lw=1.0, ls="-.")
a2.text(1320, 0.03, "자유 물\n(D = 3.0)", fontsize=8, color=C["blue"])
a2.text(2250, 0.033, "장애 확산만 (D = 0.8)", fontsize=8, color=C["green"])
a2.text(4950, 1.07, "축삭 안 제한 확산만", fontsize=8, color=C["purple"], ha="right")
a2.text(4950, 0.6, "복셀 신호 (축삭 안 50%)", fontsize=8, color=C["red"], ha="right")
a2.set_ylim(0.01, 1.4)
a2.set_xlim(0, 5000)
fig.canvas.draw()
q0, q1 = a2.transData.transform((2500, np.exp(-2500 * adc))), a2.transData.transform((4500, np.exp(-4500 * adc)))
rot = np.degrees(np.arctan2(q1[1] - q0[1], q1[0] - q0[0]))
a2.text(2500, np.exp(-2500 * adc) * 0.82, f"b ≤ 1000으로 맞춘 단일 지수 (ADC {adc * 1e3:.2f})", fontsize=7.5,
        color=C["gray"], rotation=rot, rotation_mode="anchor", ha="left", va="top")
a2.axvline(1000, color=C["gray"], lw=0.6, ls=":")
a2.text(1050, 1.12, "임상 DWI b = 1000", fontsize=7.5, color=C["gray"])
a2.set_ylim(0.01, 1.4)
a2.set_xlim(0, 5000)
a2.set_yticks([0.01, 0.1, 1])
a2.set_yticklabels(["0.01", "0.1", "1"])
a2.minorticks_off()
a2.set_xlabel("b 값 (s/mm²)")
a2.set_ylabel("신호 S/S₀ (로그 눈금)")
fig.tight_layout()
save(fig, __file__)
