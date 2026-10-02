from figstyle import plt, np, save, C

# 호지킨-헉슬리 모형(오징어 축삭, 18.5 °C로 속도 보정). 막전위, 전도도, 개폐 변수를 함께 그린다.
PHI = 3 ** ((18.5 - 6.3) / 10)


def rates(V):
    am = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10)); bm = 4 * np.exp(-(V + 65) / 18)
    ah = 0.07 * np.exp(-(V + 65) / 20); bh = 1 / (1 + np.exp(-(V + 35) / 10))
    an = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10)); bn = 0.125 * np.exp(-(V + 65) / 80)
    return am, bm, ah, bh, an, bn


dt = 0.002
t = np.arange(0, 6, dt)
V = -65.0
am, bm, ah, bh, an, bn = rates(V)
m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
out = np.zeros((len(t), 6))
for i, tt in enumerate(t):
    I = 40.0 if 0.5 <= tt < 0.8 else 0.0
    am, bm, ah, bh, an, bn = rates(V)
    m += dt * PHI * (am * (1 - m) - bm * m)
    h += dt * PHI * (ah * (1 - h) - bh * h)
    n += dt * PHI * (an * (1 - n) - bn * n)
    gna, gk = 120 * m ** 3 * h, 36 * n ** 4
    V += dt * (I - gna * (V - 50) - gk * (V + 77) - 0.3 * (V + 54.387))
    out[i] = V, gna, gk, m, h, n

fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(6.5, 5.6), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.1, 1, 1], hspace=0.42))
a1.plot(t, out[:, 0], color=C["blue"], lw=1.8)
a1.axhline(50, color=C["red"], lw=0.7, ls="--")
a1.axhline(-77, color=C["green"], lw=0.7, ls="--")
a1.text(5.95, 46, "$E_{Na}$ = +50 mV", ha="right", va="top", fontsize=8, color=C["red"])
a1.text(5.95, -80, "$E_{K}$ = −77 mV", ha="right", va="top", fontsize=8, color=C["green"])
a1.set_ylabel("막전위 (mV)")
a1.set_ylim(-97, 60)
a1.set_yticks([-60, 0, 50])
a1.set_yticklabels(["−60", "0", "50"])
a1.set_title("(가) 막전위", fontsize=10, loc="left")

a2.plot(t, out[:, 1], color=C["red"], lw=1.8, label="$g_{Na}$")
a2.plot(t, out[:, 2], color=C["green"], lw=1.8, label="$g_{K}$")
ipk = out[:, 1].argmax()
a2.annotate("Na⁺ 통로: 빨리 열리고\n불활성으로 스스로 닫힌다", xy=(t[ipk], out[ipk, 1]),
            xytext=(t[ipk] + 0.55, 19), fontsize=8, arrowprops=dict(arrowstyle="->", color=C["gray"]))
ik = out[:, 2].argmax()
a2.annotate("K⁺ 통로: 늦게 열리고\n재분극 뒤에도 잠시 열려 있다", xy=(t[ik] + 0.6, out[ik + 300, 2]),
            xytext=(t[ik] + 1.4, 12), fontsize=8, arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.set_ylabel("전도도\n(mS/cm²)")
a2.legend(fontsize=8.5, loc="upper left")
a2.set_title("(나) 이온 전도도", fontsize=10, loc="left")

a3.plot(t, out[:, 3], color=C["red"], lw=1.6)
a3.plot(t, out[:, 4], color=C["red"], lw=1.6, ls="--")
a3.plot(t, out[:, 5], color=C["green"], lw=1.6)
a3.text(1.12, 0.93, "m: Na⁺ 활성화", ha="right", fontsize=8, color=C["red"])
a3.text(4.2, 0.68, "h: Na⁺ 불활성화 문 (1 = 열려 있음)", ha="center", fontsize=8, color=C["red"])
a3.text(4.4, 0.2, "n: K⁺ 활성화", ha="center", fontsize=8, color=C["green"])
a3.set_ylabel("개폐 변수")
a3.set_ylim(0, 1.08)
a3.set_xlabel("시간 (ms)")
a3.set_xlim(0, 6)
a3.set_title("(다) 개폐 변수 (0 = 모두 닫힘, 1 = 모두 열림)", fontsize=10, loc="left")
for a in (a1, a2, a3):
    a.axvspan(0.5, 0.8, color=C["gray"], alpha=0.12, lw=0)
save(fig, __file__)
