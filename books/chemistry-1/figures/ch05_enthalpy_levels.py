from figstyle import plt, np, save, C

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))


def level(ax, x0, y, label, col):
    ax.plot([x0 - 0.35, x0 + 0.35], [y, y], color=col, lw=2.4)
    ax.text(x0, y + 0.04 * (1 if y >= 0 else 1), label, ha="center", va="bottom", fontsize=8.5)


# 왼쪽: 발열. 포도당의 연소
ax = axes[0]
level(ax, 0, 1.0, "포도당 + 6 O₂", C["green"])
level(ax, 1.4, 0.0, "6 CO₂ + 6 H₂O", C["gray"])
ax.plot([0.35, 1.05], [1.0, 0.0], color=C["gray"], lw=0.6, ls=":")
ax.annotate("", xy=(2.05, 0.0), xytext=(2.05, 1.0),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.6, mutation_scale=12))
ax.text(2.12, 0.5, "ΔH ≈ −2800\nkJ/mol\n열을 낸다", fontsize=8.5, color=C["red"], va="center")
ax.set_title("발열 반응 (ΔH < 0)", fontsize=10)

# 오른쪽: 흡열. 얼음의 융해
ax = axes[1]
level(ax, 0, 0.0, "얼음 H₂O(s)", C["blue"])
level(ax, 1.4, 1.0, "물 H₂O(l)", C["blue"])
ax.plot([0.35, 1.05], [0.0, 1.0], color=C["gray"], lw=0.6, ls=":")
ax.annotate("", xy=(2.05, 1.0), xytext=(2.05, 0.0),
            arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.6, mutation_scale=12))
ax.text(2.12, 0.5, "ΔH ≈ +6.0\nkJ/mol\n열을 흡수한다", fontsize=8.5, color=C["blue"], va="center")
ax.set_title("흡열 반응 (ΔH > 0)", fontsize=10)

for ax in axes:
    ax.set_xlim(-0.6, 3.1)
    ax.set_ylim(-0.3, 1.35)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel("엔탈피 H")
    ax.annotate("", xy=(-0.6, 1.35), xytext=(-0.6, -0.3),
                arrowprops=dict(arrowstyle="-|>", color="#444444", lw=0.8))
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
axes[1].text(1.4, -0.22, "(높이는 두 그림 사이에서 비례하지 않는다)", ha="center", fontsize=7.5, color=C["gray"])
fig.tight_layout()
save(fig, __file__)
