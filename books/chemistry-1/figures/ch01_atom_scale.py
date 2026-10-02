from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.4), gridspec_kw=dict(width_ratios=[1.25, 1]))

# 왼쪽: 원자 도식. 전자 구름 + 확대한 원자핵
rng = np.random.default_rng(1)
r = np.abs(rng.normal(0, 0.55, 1400))
th = rng.uniform(0, 2 * np.pi, 1400)
a1.scatter(r * np.cos(th), r * np.sin(th), s=1.2, color=C["red"], alpha=0.25, lw=0)
a1.add_patch(plt.Circle((0, 0), 1.25, fill=False, ls="--", color=C["gray"], lw=0.8))
a1.scatter([0], [0], s=6, color=C["ink"], zorder=4)
a1.annotate("", xy=(-1.25, -1.45), xytext=(1.25, -1.45),
            arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.9))
a1.text(0, -1.55, "원자 지름 약 0.1–0.3 nm", ha="center", va="top", fontsize=8.5)
a1.text(0, 1.38, "전자 구름 (전자가 있을 확률)", ha="center", va="bottom", fontsize=8.5, color=C["red"])

# 확대 원
cx, cy, R = 2.7, 0.15, 0.95
a1.add_patch(plt.Circle((cx, cy), R, facecolor="white", edgecolor=C["gray"], lw=0.9))
a1.plot([0.03, cx - R * 0.94], [0.02, cy + R * 0.33], color=C["gray"], lw=0.6)
a1.plot([0.03, cx - R * 0.94], [-0.02, cy - R * 0.33], color=C["gray"], lw=0.6)
pts = [(-0.28, 0.15), (0.05, 0.3), (0.3, 0.08), (-0.1, -0.12), (0.2, -0.28), (-0.32, -0.22)]
for i, (x, y) in enumerate(pts):
    col = C["blue"] if i % 2 == 0 else C["gray"]
    a1.add_patch(plt.Circle((cx + x, cy + y), 0.2, facecolor=col, edgecolor="white", lw=0.8, alpha=0.9))
a1.text(cx, cy - R - 0.1, "원자핵 (확대)\n지름 수 fm\n($10^{-15}$ m 규모)", ha="center", va="top", fontsize=8.5)
a1.scatter([], [], s=40, color=C["blue"], label="양성자 (+)")
a1.scatter([], [], s=40, color=C["gray"], label="중성자 (0)")
a1.scatter([], [], s=10, color=C["red"], label="전자 (−)")
a1.legend(loc="lower right", bbox_to_anchor=(1.02, -0.06), fontsize=8, handletextpad=0.2, ncol=3, columnspacing=0.8)
a1.set_xlim(-1.6, 3.8)
a1.set_ylim(-2.75, 1.75)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 세로 로그 자
items = [
    (1.7e-15, "양성자 지름 약 1.7 fm"),
    (5.5e-15, "탄소 원자핵 약 5 fm"),
    (1.4e-14, "철 원자핵 약 10 fm"),
    (1.06e-10, "수소 원자 약 0.1 nm"),
    (3.0e-10, "Na⁺ 이온, 물 분자 0.2–0.3 nm"),
    (5e-9, "세포막 두께 약 5 nm"),
]
a2.set_yscale("log")
a2.set_ylim(5e-16, 3e-8)
a2.set_xlim(0, 1)
a2.axvline(0.12, color=C["gray"], lw=1.2)
for v, name in items:
    col = C["blue"] if v < 1e-12 else C["ink"]
    a2.scatter([0.12], [v], s=22, color=col, zorder=3)
    a2.text(0.18, v, name, va="center", fontsize=8.5, color=col)
a2.annotate("", xy=(0.95, 1.06e-10), xytext=(0.95, 3e-15),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1))
a2.text(0.9, 2e-12, "수만–10만 배\n(4–5자릿수)", ha="right", va="center", fontsize=8.5, color=C["red"])
a2.set_yticks([1e-15, 1e-14, 1e-13, 1e-12, 1e-11, 1e-10, 1e-9, 1e-8])
a2.set_yticklabels(["1 fm", "10 fm", "100 fm", "1 pm", "10 pm", "0.1 nm", "1 nm", "10 nm"], fontsize=8)
a2.minorticks_off()
a2.set_xticks([])
a2.spines["bottom"].set_visible(False)
a2.set_ylabel("크기 (로그 눈금)")
fig.tight_layout()
save(fig, __file__)
