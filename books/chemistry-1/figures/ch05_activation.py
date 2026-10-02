from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(width_ratios=[1.1, 1]))

# 왼쪽: 반응 좌표에 따른 자유에너지. 촉매는 장벽만 낮춘다.
x = np.linspace(0, 1, 400)
base = 0 + (-30) * (3 * x ** 2 - 2 * x ** 3)  # 반응물 0 → 생성물 −30
hump = lambda h: h * np.exp(-((x - 0.5) / 0.13) ** 2)
a1.plot(x, base + hump(80), color=C["ink"], lw=1.6, label="촉매 없음")
a1.plot(x, base + hump(35), color=C["blue"], lw=1.6, ls="--", label="효소 있음")
a1.annotate("", xy=(0.5, 80 - 15), xytext=(0.5, 0), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1))
a1.text(0.53, 30, "Eₐ", color=C["red"], fontsize=9.5)
a1.annotate("", xy=(0.36, 35 - 15 + 2), xytext=(0.36, 0), arrowprops=dict(arrowstyle="<->", color=C["blue"], lw=1))
a1.text(0.2, 22, "낮아진 Eₐ", color=C["blue"], fontsize=8.5)
a1.plot([0.85, 1.0], [-30, -30], color=C["gray"], lw=0.7, ls=":")
a1.plot([0, 1.0], [0, 0], color=C["gray"], lw=0.7, ls=":")
a1.annotate("", xy=(0.97, -30), xytext=(0.97, 0), arrowprops=dict(arrowstyle="<->", color=C["green"], lw=1))
a1.text(0.75, -16, "ΔG\n(그대로)", color=C["green"], fontsize=8.5)
a1.text(0.0, 3, "반응물", fontsize=8.5)
a1.text(0.86, -38, "생성물", fontsize=8.5)
a1.set_xticks([])
a1.set_yticks([])
a1.set_xlabel("반응 좌표 (반응이 진행된 정도)")
a1.set_ylabel("자유에너지")
a1.set_ylim(-45, 82)
a1.legend(fontsize=8, loc="upper right")
a1.set_title("활성화 에너지와 촉매", fontsize=10)

# 오른쪽: 아레니우스. 37 °C 대비 상대 속도
R = 8.314
Tc = np.linspace(28, 40, 200)
for Ea, col in ((30e3, C["gray"]), (50e3, C["blue"]), (80e3, C["red"])):
    r = np.exp(-Ea / R * (1 / (Tc + 273.15) - 1 / 310.15))
    a2.plot(Tc, r, color=col, lw=1.6, label=f"Eₐ = {Ea / 1e3:.0f} kJ/mol")
a2.axvline(37, color=C["gray"], lw=0.6, ls=":")
a2.axvspan(32, 36, color=C["purple"], alpha=0.08, lw=0)
a2.text(32.15, 1.22, "저체온 치료\n32–36 °C", fontsize=7.8, color=C["purple"])
a2.axhline(1, color=C["gray"], lw=0.6, ls=":")
a2.set_xlabel("온도 (°C)")
a2.set_ylabel("37 °C에 대한 상대 속도")
a2.set_ylim(0.3, 1.4)
a2.legend(fontsize=7.5, loc="lower right")
a2.set_title("온도에 따른 반응 속도", fontsize=10)
fig.tight_layout()
save(fig, __file__)
