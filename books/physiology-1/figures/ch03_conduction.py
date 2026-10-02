from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(7.5, 3.0))
a1 = fig.add_axes([0.0, 0.08, 0.5, 0.84])
a2 = fig.add_axes([0.62, 0.17, 0.36, 0.72])

# (가) 유수초 축삭과 국소 전류
a1.set_xlim(-0.6, 10.2)
a1.set_ylim(-2.6, 2.6)
a1.axis("off")
a1.add_patch(plt.Rectangle((-0.6, -0.35), 10.8, 0.7, color=C["green"], alpha=0.18, lw=0))
nodes = [1.0, 4.0, 7.0]
for x0, x1 in ((-0.6, 0.85), (1.15, 3.85), (4.15, 6.85), (7.15, 10.2)):
    for y in (0.35, -0.95):
        a1.add_patch(FancyBboxPatch((x0, y), x1 - x0, 0.6, boxstyle="round,pad=0,rounding_size=0.25",
                                    color=C["gray"], alpha=0.35, lw=0))
for i, x in enumerate(nodes):
    col = C["red"] if i == 0 else C["ink"]
    a1.text(x, 1.2, "결절", ha="center", fontsize=8, color=col)
a1.text(-0.5, 1.6, "활동전위 발생 중", ha="left", fontsize=8, color=C["red"], weight="bold")
a1.text(2.5, -1.25, "수초 (절연, 수십 겹)", ha="center", va="top", fontsize=8, color=C["gray"])
# Na⁺ 유입
a1.annotate("", xy=(1.0, 0.05), xytext=(1.0, 1.05),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.6, mutation_scale=11))
a1.text(0.8, 0.55, "Na⁺", fontsize=8, color=C["green"], ha="right")
# 축 안 전류 → 다음 결절에서 밖으로
a1.annotate("", xy=(3.85, 0.0), xytext=(1.25, 0.0),
            arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.6, mutation_scale=11))
a1.text(2.5, 0.08, "축 안 전류", ha="center", va="bottom", fontsize=7.5, color=C["blue"])
a1.add_patch(FancyArrowPatch((4.0, 0.3), (1.2, 1.0), connectionstyle="arc3,rad=0.55",
                             arrowstyle="-|>", mutation_scale=10, color=C["blue"], lw=1.1, ls="--"))
a1.text(4.3, 1.6, "다음 결절을 문턱까지\n탈분극시키고 되돌아오는 전류", fontsize=7.5, color=C["blue"], va="bottom")
a1.annotate("", xy=(7.0, -1.75), xytext=(1.0, -1.75),
            arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.0))
a1.text(4.0, -1.85, "결절 간격 약 0.2–2 mm, 결절에서 결절로 건너뛴다", ha="center", va="top", fontsize=7.5)
a1.set_title("(가) 도약 전도", fontsize=10)

# (나) 전도 속도와 지름
d_u = np.logspace(-1, np.log10(700), 100)
k = 20 / np.sqrt(500)          # 오징어 거대 축삭 0.5 mm에서 약 20 m/s에 맞춘 √d 비례
a2.loglog(d_u, k * np.sqrt(d_u), color=C["gray"], lw=1.8, label="무수초: v ∝ √d")
d_m = np.logspace(0, np.log10(20), 50)
a2.loglog(d_m, 6 * d_m, color=C["blue"], lw=2.0, label="유수초: v ≈ 6 × d")
a2.plot([500], [20], "o", color=C["gray"], ms=5)
a2.text(120, 32, "오징어\n거대 축삭", ha="center", va="bottom", fontsize=7.5, color=C["gray"])
a2.plot([1], [k], "o", color=C["gray"], ms=4)
a2.text(1.2, k * 0.75, "C 섬유", fontsize=7.5, va="top", color=C["gray"])
a2.plot([3.3], [20], "o", color=C["blue"], ms=5)
a2.annotate("같은 20 m/s를\n3.3 μm로", xy=(3.3, 20), xytext=(1.0, 60), fontsize=7.5, color=C["blue"],
            arrowprops=dict(arrowstyle="->", color=C["blue"], lw=0.8))
a2.set_xlabel("축삭(섬유) 지름 d (μm)")
a2.set_ylabel("전도 속도 (m/s)")
a2.set_xticks([0.1, 1, 10, 100, 1000])
a2.set_xticklabels(["0.1", "1", "10", "100", "1000"])
a2.set_yticks([0.1, 1, 10, 100])
a2.set_yticklabels(["0.1", "1", "10", "100"])
a2.minorticks_off()
a2.set_ylim(0.15, 200)
a2.legend(fontsize=7.5, loc="lower right")
a2.set_title("(나) 지름과 전도 속도", fontsize=10)
save(fig, __file__)
