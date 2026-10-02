from figstyle import plt, np, save, C

k = 1.380649e-23
m = 18.015 * 1.66054e-27  # 물 분자 질량
v = np.linspace(0, 1800, 600)


def maxwell(v, T):
    a = m / (2 * k * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v ** 2 * np.exp(-a * v ** 2)


fig, ax = plt.subplots(figsize=(6.5, 3.0))
for T, lab, col in [(273, "0 °C (273 K)", C["blue"]), (310, "37 °C (310 K)", C["red"]),
                    (373, "100 °C (373 K)", C["gray"])]:
    ax.plot(v, maxwell(v, T) * 1e3, color=col, lw=1.8 if T == 310 else 1.2, label=lab)
vrms = np.sqrt(3 * k * 310 / m)
ax.axvline(vrms, color=C["red"], lw=0.8, ls=":")
ax.annotate(f"37 °C의 제곱평균속력\n약 {vrms:.0f} m/s", xy=(vrms, 1.62), xytext=(980, 1.38),
            fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.text(1150, 0.55, "드물지만 아주 빠른 분자도 있다\n(분포의 긴 꼬리)", fontsize=8.5, color=C["ink"])
ax.set_xlabel("물 분자의 속력 (m/s)")
ax.set_ylabel("상대 비율")
ax.set_yticks([])
ax.set_ylim(0, 2.3)
ax.set_xlim(0, 1800)
ax.legend(loc="upper right", fontsize=8.5, bbox_to_anchor=(1.0, 1.0))
save(fig, __file__)
