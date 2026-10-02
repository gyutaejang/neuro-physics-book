from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[0.85, 1.15]))

# 왼쪽: 세포 사이로 돌아가는 길 (육각 배열의 세포, 틈은 좁다)
from matplotlib.patches import Circle
rng = np.random.default_rng(3)
dx, dy = 1.2, 1.2 * np.sin(np.pi / 3)
for j in range(5):
    for i in range(6):
        x0 = i * dx + (dx / 2 if j % 2 else 0)
        if x0 > 6.2:
            continue
        a1.add_patch(Circle((x0, j * dy), 0.5 + rng.uniform(-0.03, 0.0), facecolor=C["green"], alpha=0.25,
                            edgecolor=C["green"], lw=0.8))
yrow = 2 * dy
a1.annotate("", xy=(6.0, yrow), xytext=(0.0, yrow),
            arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=1.3, ls="--"))
xs = np.arange(0.0, 6.01, dx / 2)
ys = [yrow + (dy / 3 if k % 2 else 2 * dy / 3) for k in range(len(xs))]
a1.plot(xs, ys, color=C["red"], lw=1.6)
start, end = None, None
a1.text(3.0, 4.95, "세포 사이 공간: 부피의 약 20% (α ≈ 0.2)", ha="center", fontsize=8.5)
a1.text(3.0, -0.7, "실제 길(빨강)은 직선(회색)보다 구불구불하다\n굴곡도 λ ≈ 1.6 → 유효 확산 D* = D/λ²", ha="center",
        va="top", fontsize=8.2)
a1.set_xlim(-0.6, 6.7)
a1.set_ylim(-1.7, 5.35)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 점에서 순간 방출한 표지 이온의 농도, 100 μm 떨어진 곳
D = 1.24e-9   # TMA⁺, 37 °C (m²/s)
r = 100e-6
t = np.linspace(0.05, 12, 600)


def conc(alpha, lam):
    Ds = D / lam ** 2
    return (1 / alpha) / (4 * np.pi * Ds * t) ** 1.5 * np.exp(-r ** 2 / (4 * Ds * t))


ref = conc(1, 1).max()
cases = [(1, 1, "자유 매질 (α = 1, λ = 1)", C["gray"], "--"),
         (0.2, 1.6, "정상 뇌 (α = 0.2, λ = 1.6)", C["blue"], "-"),
         (0.07, 2.0, "허혈 뒤 (α ≈ 0.07, λ ≈ 2.0)", C["red"], "-")]
for al, la, lab, col, ls in cases:
    c = conc(al, la) / ref
    a2.plot(t, c, color=col, lw=1.8, ls=ls, label=lab)
    k = c.argmax()
    a2.scatter([t[k]], [c[k]], color=col, s=16, zorder=4)
    a2.annotate(f"{t[k]:.1f} s, {c[k]:.0f}배" if c[k] > 1.5 else f"{t[k]:.1f} s", xy=(t[k], c[k]),
                xytext=(6, 4), textcoords="offset points", fontsize=8, color=col)
a2.set_yscale("log")
a2.set_ylim(0.01, 60)
a2.set_yticks([0.01, 0.1, 1, 10])
a2.set_yticklabels(["0.01", "0.1", "1", "10"])
a2.minorticks_off()
a2.set_xlim(0, 12)
a2.set_xlabel("방출 뒤 시간 (s)")
a2.set_ylabel("상대 농도 (자유 매질 최고점 = 1)")
a2.legend(fontsize=7.5, loc="lower right")
fig.tight_layout()
save(fig, __file__)
