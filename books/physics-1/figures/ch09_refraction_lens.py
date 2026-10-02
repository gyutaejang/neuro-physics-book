from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1.5]})

# (가) 굴절
a1.axhspan(-1.2, 0, color=C["light"], lw=0)
a1.axhline(0, color=C["gray"], lw=0.8)
a1.plot([0, 0], [-1.1, 1.1], color=C["gray"], lw=0.6, ls=":")
t1 = np.radians(45)
t2 = np.arcsin(np.sin(t1) / 1.33)
L = 1.05
a1.annotate("", xy=(0, 0), xytext=(-L * np.sin(t1), L * np.cos(t1)),
            arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.6))
a1.annotate("", xy=(L * np.sin(t2), -L * np.cos(t2)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.6))
a1.annotate("", xy=(0.6 * np.sin(t1), 0.6 * np.cos(t1)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8, ls="--"))
a1.text(-0.18, 0.55, r"$\theta_1$ = 45°", fontsize=8.5, ha="right")
a1.text(0.07, -0.55, r"$\theta_2$ ≈ 32°", fontsize=8.5)
a1.text(-1.05, 0.08, "공기 n=1.00", fontsize=8.5, va="bottom")
a1.text(-1.05, -0.08, "물 n=1.33", fontsize=8.5, va="top")
a1.text(0.45, 0.52, "반사", fontsize=8, color=C["gray"])
a1.set_xlim(-1.1, 1.0)
a1.set_ylim(-1.15, 1.15)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("(가) 굴절: 느린 매질에서 법선 쪽으로 꺾인다", fontsize=9)

# (나) 볼록 렌즈
f = 1.0
a2.axhline(0, color=C["gray"], lw=0.8)
lens = plt.matplotlib.patches.Ellipse((0, 0), 0.18, 1.9, color=C["blue"], alpha=0.25, lw=0)
a2.add_patch(lens)
for xf in (-f, f):
    a2.plot([xf], [0], "o", color=C["ink"], ms=3)
a2.text(f, -0.12, "초점 F", ha="center", va="top", fontsize=8)
a2.text(-f, -0.12, "F", ha="center", va="top", fontsize=8)
do = 2.0
di = 1 / (1 / f - 1 / do)
ho = 0.6
hi = -ho * di / do
a2.annotate("", xy=(-do, ho), xytext=(-do, 0), arrowprops=dict(arrowstyle="->", color=C["green"], lw=2))
a2.annotate("", xy=(di, hi), xytext=(di, 0), arrowprops=dict(arrowstyle="->", color=C["green"], lw=2))
a2.text(-do, ho + 0.08, "물체", ha="center", fontsize=8.5)
a2.text(di, hi - 0.1, "상 (거꾸로)", ha="center", va="top", fontsize=8.5)
# 광선 1: 평행 → 초점
a2.plot([-do, 0, di], [ho, ho, hi], color=C["red"], lw=1)
# 광선 2: 중심 통과
a2.plot([-do, di], [ho, hi], color=C["red"], lw=1)
# 광선 3: 앞 초점 통과 → 평행
yl = ho * (0 - (-f)) / (-do - (-f))
a2.plot([-do, 0, di], [ho, yl, yl], color=C["red"], lw=1)
a2.annotate("", xy=(-do, -0.85), xytext=(0, -0.85), arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
a2.text(-do / 2, -0.9, "a", ha="center", va="top", fontsize=9)
a2.annotate("", xy=(di, -0.85), xytext=(0, -0.85), arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
a2.text(di / 2, -0.9, "b", ha="center", va="top", fontsize=9)
a2.set_xlim(-2.3, 2.4)
a2.set_ylim(-1.15, 1.0)
a2.set_aspect("equal")
a2.axis("off")
a2.set_title("(나) 볼록 렌즈: 1/a + 1/b = 1/f", fontsize=9)
fig.tight_layout()
save(fig, __file__)
