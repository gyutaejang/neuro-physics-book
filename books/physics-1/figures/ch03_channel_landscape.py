from figstyle import plt, np, save, C

x = np.linspace(-1.75, 2.2, 400)


def U(x, s):
    return 9.5 * (x ** 2 - 1) ** 2 + s * x


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
for ax, s, title in ((axes[0], 2.5, "휴지 전위 (−70 mV)"), (axes[1], -2.5, "탈분극 (예: −20 mV)")):
    u = U(x, s)
    ax.plot(x, u, color=C["ink"], lw=1.4)
    ax.fill_between(x, -6, u, where=u < 17, color=C["light"])
    uc, uo, ub = U(-1, s), U(1, s), U(0, s)
    low_c = uc < uo
    ax.scatter([-1 if low_c else 1], [min(uc, uo) + 0.7], s=70, color=C["green"], zorder=4)
    ax.text(-1, uc - 1.0, "닫힘", ha="center", va="top", fontsize=9.5, weight="bold")
    ax.text(1, uo - 1.0, "열림", ha="center", va="top", fontsize=9.5, weight="bold")
    # 두 상태의 에너지 차
    ax.plot([-1.6, 2.05], [uc, uc], color=C["gray"], ls=":", lw=0.8)
    ax.plot([0.6, 2.05], [uo, uo], color=C["gray"], ls=":", lw=0.8)
    ax.annotate("", xy=(1.95, uo), xytext=(1.95, uc),
                arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.2))
    ax.text(1.95, max(uc, uo) + 0.5, f"{uo - uc:+.0f} kT".replace("-", "−"), ha="center", va="bottom", fontsize=8.5,
            color=C["red"])
    # 장벽
    ax.annotate("", xy=(0, ub), xytext=(0, uc), arrowprops=dict(arrowstyle="<->", color=C["purple"], lw=1))
    ax.text(0.07, (uc + ub) / 2, f"장벽\n약 {ub - uc:.0f} kT", fontsize=8.5, color=C["purple"], va="center")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_xlim(-1.75, 2.2)
    ax.set_ylim(-6, 17)
    ax.set_xlabel("통로 단백질의 모양")
axes[0].set_ylabel("자유 에너지 (kT 단위)")
axes[0].text(0, 16.3, "닫힘이 5 kT 낮다 → 대부분 닫혀 있다", fontsize=8.5, color=C["green"], va="top", ha="center")
axes[1].text(0, 16.3, "지형이 기울어 열림이 더 낮아진다", fontsize=8.5, color=C["green"],
             va="top", ha="center")
fig.tight_layout()
save(fig, __file__)
