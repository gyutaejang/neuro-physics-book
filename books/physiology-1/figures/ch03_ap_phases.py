from figstyle import plt, np, save, C

# 호지킨-헉슬리 모형(오징어 축삭, 18.5 °C로 속도 보정)으로 활동전위 하나를 계산한다.
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
Vs = np.zeros_like(t)
for i, tt in enumerate(t):
    I = 40.0 if 0.5 <= tt < 0.8 else 0.0
    am, bm, ah, bh, an, bn = rates(V)
    m += dt * PHI * (am * (1 - m) - bm * m)
    h += dt * PHI * (ah * (1 - h) - bh * h)
    n += dt * PHI * (an * (1 - n) - bn * n)
    V += dt * (I - 120 * m ** 3 * h * (V - 50) - 36 * n ** 4 * (V + 77) - 0.3 * (V + 54.387))
    Vs[i] = V

ipk = Vs.argmax()
imin = ipk + Vs[ipk:].argmin()
dV = np.gradient(Vs, dt)
ithr = np.where((dV > 20) & (t > 0.8))[0][0]   # 상승 속도가 20 mV/ms를 넘는 곳 = 문턱

def mv(x):
    return f"{x:.0f}".replace("-", "−")


fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(t, Vs, color=C["blue"], lw=2)
ax.axhline(-65, color=C["gray"], lw=0.6, ls=":")
ax.axhline(0, color=C["gray"], lw=0.6, ls=":")
ax.axhline(Vs[ithr], color=C["red"], lw=0.8, ls="--")
ax.axvspan(0.5, 0.8, color=C["gray"], alpha=0.15, lw=0)
ax.text(0.65, 38, "자극", ha="center", fontsize=8.5, color=C["gray"])

ax.text(5.9, Vs[ithr] + 2, f"문턱 (약 {mv(Vs[ithr])} mV)", ha="right", va="bottom", fontsize=8.5, color=C["red"])
ax.text(5.9, -63, "휴지 전위 (모형 −65 mV)", ha="right", va="bottom", fontsize=8.5, color=C["gray"])
ax.annotate(f"최고점 약 +{Vs[ipk]:.0f} mV", xy=(t[ipk], Vs[ipk]), xytext=(t[ipk] + 0.9, 32),
            fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["gray"]))
iu = ipk - int(0.12 / dt)
ax.annotate("상승기 (탈분극)\nNa⁺ 유입", xy=(t[iu], Vs[iu]), xytext=(0.15, 5),
            fontsize=8.5, ha="left", arrowprops=dict(arrowstyle="->", color=C["gray"]))
idn = ipk + int(0.3 / dt)
ax.annotate("재분극\nK⁺ 유출", xy=(t[idn], Vs[idn]), xytext=(t[idn] + 0.75, 12),
            fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.annotate(f"후과분극 (약 {mv(Vs[imin])} mV)", xy=(t[imin], Vs[imin]), xytext=(t[imin] + 0.5, -40),
            fontsize=8.5, arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.set_xlim(0, 6)
ax.set_ylim(-85, 45)
ax.set_xlabel("시간 (ms)")
ax.set_ylabel("막전위 (mV)")
ax.set_yticks([-80, -65, -40, -20, 0, 20, 40])
ax.set_yticklabels(["−80", "−65", "−40", "−20", "0", "20", "40"])
fig.tight_layout()
save(fig, __file__)
