from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw=dict(width_ratios=[1, 1.05]))

# 왼쪽: NaCl 결정의 한 면
d = 0.282
for i in range(5):
    for j in range(5):
        x, y = i * d, j * d
        if (i + j) % 2 == 0:
            a1.add_patch(plt.Circle((x, y), 0.10, color=C["green"], zorder=3))
            a1.text(x, y, "Na⁺", ha="center", va="center", fontsize=7, color="white", zorder=4)
        else:
            a1.add_patch(plt.Circle((x, y), 0.172, facecolor=C["light"], edgecolor=C["green"], lw=1, zorder=2))
            a1.text(x, y, "Cl⁻", ha="center", va="center", fontsize=7.5, color=C["ink"], zorder=4)
a1.annotate("", xy=(0, -0.24), xytext=(d, -0.24), arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=1))
a1.text(d / 2, -0.29, "0.282 nm", ha="center", va="top", fontsize=8.5, color=C["gray"])
a1.text(2 * d, 4 * d + 0.24, "이온 결합: Na가 Cl에게 전자를 준다", ha="center", va="bottom", fontsize=9.5)
a1.text(2 * d, -0.44, "+ 와 − 가 번갈아 쌓인 결정 (방향이 없다)", ha="center", va="top", fontsize=8.5)
a1.set_xlim(-0.25, 4 * d + 0.25)
a1.set_ylim(-0.62, 4 * d + 0.42)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: H2의 전자 밀도 (두 원자 사이에 쌓인다)
x = np.linspace(-0.16, 0.16, 300)
y = np.linspace(-0.11, 0.11, 220)
X, Y = np.meshgrid(x, y)
h = 0.037
rho = np.exp(-np.hypot(X - h, Y) / 0.022) + np.exp(-np.hypot(X + h, Y) / 0.022)
rho += 0.55 * np.exp(-(X / 0.03) ** 2 - (Y / 0.022) ** 2)
a2.contourf(X, Y, rho, levels=np.linspace(0.05, rho.max(), 9), cmap="Blues", alpha=0.85)
for s in (-h, h):
    a2.plot(s, 0, "o", color=C["ink"], ms=4)
    a2.text(s, -0.018, "H", ha="center", va="top", fontsize=10, weight="bold")
a2.annotate("두 원자 사이에 모인\n공유 전자쌍", xy=(0, 0.012), xytext=(0.035, 0.085), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.text(0, 0.135, "공유 결합: 전자쌍을 함께 쓴다", ha="center", va="bottom", fontsize=9.5)
a2.text(0, -0.105, "두 원자핵이 사이의 전자에 함께 끌린다\n(방향이 있는 결합)", ha="center", va="top", fontsize=8.5)
a2.set_xlim(-0.16, 0.16)
a2.set_ylim(-0.16, 0.16)
a2.set_aspect("equal")
a2.axis("off")
fig.tight_layout()
save(fig, __file__)
