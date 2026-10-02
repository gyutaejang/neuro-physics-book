from figstyle import plt, save, C

fig, ax = plt.subplots(figsize=(7.0, 3.3))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")

ax.add_patch(plt.Rectangle((0.2, 0.6), 4.3, 3.6, color=C["blue"], alpha=0.07, lw=0))
ax.add_patch(plt.Rectangle((5.5, 0.6), 4.3, 3.6, color=C["red"], alpha=0.07, lw=0))
ax.add_patch(plt.Rectangle((4.5, 0.6), 1.0, 3.6, color=C["green"], alpha=0.22, lw=0))
ax.text(5.0, 4.32, "막", ha="center", va="bottom", fontsize=9, color=C["green"])
ax.text(2.35, 4.32, "혈장 pH 7.4", ha="center", va="bottom", fontsize=10)
ax.text(7.65, 4.32, "산성 구획 pH 5.0 (리소좀)", ha="center", va="bottom", fontsize=10)

# 중성형 B: 양쪽 같은 농도
ax.text(2.35, 3.3, "B  1", ha="center", va="center", fontsize=11, color=C["blue"], weight="bold")
ax.text(7.65, 3.3, "B  1", ha="center", va="center", fontsize=11, color=C["blue"], weight="bold")
ax.annotate("", xy=(6.7, 3.38), xytext=(3.3, 3.38),
            arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.3, mutation_scale=11))
ax.annotate("", xy=(3.3, 3.22), xytext=(6.7, 3.22),
            arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.3, mutation_scale=11))
ax.text(5.0, 3.62, "중성형만\n통과", ha="center", va="bottom", fontsize=7.5, color=C["blue"])

# 양이온형 BH+
ax.text(2.35, 2.05, "BH⁺  40", ha="center", va="center", fontsize=11, color=C["red"], weight="bold")
ax.text(7.65, 2.05, "BH⁺  10,000", ha="center", va="center", fontsize=11, color=C["red"], weight="bold")
ax.text(5.0, 2.05, "×", ha="center", va="center", fontsize=16, color=C["red"])
ax.text(5.0, 1.55, "이온형은\n못 지나감", ha="center", va="top", fontsize=7.5, color=C["red"])
ax.text(2.35, 1.5, r"$=10^{9-7.4}\approx 40$", ha="center", va="top", fontsize=8, color=C["gray"])
ax.text(7.65, 1.5, r"$=10^{9-5.0}=10^{4}$", ha="center", va="top", fontsize=8, color=C["gray"])

ax.text(2.35, 0.78, "합계 약 41", ha="center", va="bottom", fontsize=9.5)
ax.text(7.65, 0.78, "합계 약 10,000  (약 245배)", ha="center", va="bottom", fontsize=9.5, color=C["red"])
ax.text(5.0, 0.15, "약염기 B, pKa 9. 숫자는 각 구획의 상대 농도 (중성형 B = 1).", ha="center",
        va="center", fontsize=8.5, color=C["gray"])
save(fig, __file__)
