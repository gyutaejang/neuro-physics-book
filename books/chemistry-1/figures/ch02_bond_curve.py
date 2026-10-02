from figstyle import plt, np, save, C

# 수소 분자(H2)의 위치에너지 곡선 (모스 퍼텐셜 근사)
De, a, re = 4.5, 19.4, 0.074   # eV, 1/nm, nm
r = np.linspace(0.045, 0.40, 500)
U = De * (1 - np.exp(-a * (r - re))) ** 2 - De

fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.plot(r, U, color=C["blue"], lw=2)
ax.axhline(0, color=C["gray"], lw=0.8, ls=":")
ax.set_xlim(0.04, 0.40)
ax.set_ylim(-5.2, 3.0)
ax.set_xlabel("두 수소 원자핵 사이 거리 r (nm)")
ax.set_ylabel("위치에너지 (eV)")

# 결합 길이
ax.plot([re, re], [-5.2, -De], color=C["gray"], lw=0.8, ls="--")
ax.text(re + 0.006, -5.0, "결합 길이 0.074 nm", fontsize=8.5, color=C["gray"], va="bottom")
# 결합 에너지 화살표
ax.annotate("", xy=(0.16, 0), xytext=(0.16, -De),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.3))
ax.plot([re, 0.17], [-De, -De], color=C["gray"], lw=0.6, ls=":")
ax.text(0.168, -2.6, "결합 에너지\n약 4.5 eV (436 kJ/mol)\n≈ 170 kT", fontsize=8.5, color=C["red"], va="center")
# kT 크기 비교: 우물 바닥에 kT 높이의 띠
ax.add_patch(plt.Rectangle((0.058, -De), 0.032, 0.027, color=C["green"], lw=0, zorder=3))
ax.annotate("kT = 0.027 eV (37 °C)\n이 띠의 높이", xy=(0.085, -De + 0.02), xytext=(0.205, -4.35),
            fontsize=8.5, color=C["green"], va="center",
            arrowprops=dict(arrowstyle="->", color=C["green"], lw=0.8))
# 설명 글
ax.text(0.052, 2.4, "너무 가까우면\n원자핵끼리 밀어낸다", fontsize=8.5, color=C["ink"], va="top")
ax.text(0.27, 0.35, "멀리 떨어지면 서로 무관 (0)", fontsize=8.5, color=C["gray"], va="bottom")
save(fig, __file__)
