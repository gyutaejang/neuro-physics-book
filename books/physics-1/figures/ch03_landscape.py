from figstyle import plt, np, save, C

x = np.linspace(0, 10, 500)
U = (1.6 * np.exp(-((x - 1.2) / 1.0) ** 2) * 0 + 0.9 - 0.8 * np.exp(-((x - 2.5) / 1.0) ** 2)
     + 0.7 * np.exp(-((x - 5.0) / 0.8) ** 2) - 0.45 * np.exp(-((x - 7.5) / 0.9) ** 2)
     + 0.6 * np.exp(-((x - 10.5) / 1.2) ** 2) + 0.6 * np.exp(-((x + 0.5) / 1.2) ** 2))

def u(x0):
    return float(np.interp(x0, x, U))

fig, ax = plt.subplots(figsize=(6.8, 3.2))
ax.fill_between(x, -0.45, U, color=C["light"])
ax.plot(x, U, color=C["ink"], lw=1.4)

# 평형점 찾기
iA = np.argmin(np.where((x > 1) & (x < 4), U, 9))
iB = np.argmax(np.where((x > 4) & (x < 6), U, -9))
iC = np.argmin(np.where((x > 6) & (x < 9), U, 9))
xA, xB, xC = x[iA], x[iB], x[iC]
for xp, col in ((xA, C["blue"]), (xB, C["red"]), (xC, C["blue"])):
    ax.scatter([xp], [u(xp) + 0.06], s=80, color=col, zorder=4)
ax.text(xA, u(xA) - 0.08, "안정 평형\n(가장 깊은 골짜기)", ha="center", va="top", fontsize=8.5)
ax.text(xB, u(xB) + 0.17, "불안정 평형 (꼭대기)", ha="center", va="bottom", fontsize=8.5, color=C["red"])
ax.text(xC, u(xC) - 0.08, "준안정 상태\n(얕은 골짜기)", ha="center", va="top", fontsize=8.5)

# 장벽 높이
ax.annotate("", xy=(xB, u(xB) - 0.03), xytext=(xB, u(xA)),
            arrowprops=dict(arrowstyle="<->", color=C["purple"], lw=1))
ax.plot([xA, xB], [u(xA), u(xA)], color=C["gray"], ls=":", lw=0.8)
ax.text(xB + 0.12, (u(xA) + u(xB)) / 2 - 0.1, "장벽\n높이 ΔE", ha="left", va="center", fontsize=8.5,
        color=C["purple"])

# 기울기 = 힘
for x0 in (1.5, 3.6, 6.3):
    du = (u(x0 + 0.05) - u(x0 - 0.05)) / 0.1
    ax.annotate("", xy=(x0 - 0.45 * np.sign(du), u(x0) + 0.25), xytext=(x0, u(x0) + 0.25),
                arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.4))
ax.text(1.5, u(1.5) + 0.32, "힘", ha="center", va="bottom", fontsize=8.5, color=C["red"])
ax.text(8.6, 1.35, "빨간 화살표: 힘은 언제나\n내리막 쪽을 향한다", fontsize=8.5, color=C["red"],
        ha="center")
ax.set_xlim(0, 10)
ax.set_ylim(-0.45, 1.75)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("상태 또는 위치 x")
ax.set_ylabel("위치에너지 U")
save(fig, __file__)
