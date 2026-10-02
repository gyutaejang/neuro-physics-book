from figstyle import plt, np, save, C

# 참조 영역 로건 도표와 시간에 따라 변하는 조직 비(SUVR - 1)
dt = 0.005
t = np.arange(0, 120 + dt, dt)
A1, A2, A3, l1, l2, l3 = 851.1, 21.88, 20.81, 4.134, 0.1191, 0.01043
Cp = np.maximum((A1 * t - A2 - A3) * np.exp(-l1 * t) + A2 * np.exp(-l2 * t) + A3 * np.exp(-l3 * t), 0)


def tcm(K1, k2, k3, k4):
    a, b = np.zeros_like(t), np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (K1 * Cp[i - 1] - (k2 + k3) * a[i - 1] + k4 * b[i - 1])
        b[i] = b[i - 1] + dt * (k3 * a[i - 1] - k4 * b[i - 1])
    return a + b


def case(K1, k2):
    return tcm(K1, k2, 0.24, 0.08), tcm(K1, k2, 0, 0)


CT, CR = case(0.1, 0.4)
CT2, CR2 = case(0.07, 0.28)   # 혈류가 줄어 K1, k2가 함께 30% 줄어든 경우 (BP_ND는 같다)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2))
# (가) 로건 도표: 5분 간격 프레임 중간 시각에서 표본
fr = np.arange(2.5, 90, 5.0)
idx = (fr / dt).astype(int)
iCT, iCR = np.cumsum(CT) * dt, np.cumsum(CR) * dt
X = (iCR[idx] + CR[idx] / 0.4) / CT[idx]
Y = iCT[idx] / CT[idx]
late = fr >= 30
p = np.polyfit(X[late], Y[late], 1)
a1.scatter(X[~late], Y[~late], s=16, facecolor="white", edgecolor=C["blue"], zorder=3, label="30분 이전 (곡선 구간)")
a1.scatter(X[late], Y[late], s=16, color=C["blue"], zorder=3, label="30분 이후 (직선 구간)")
xx = np.linspace(0, X.max() * 1.05, 50)
a1.plot(xx, np.polyval(p, xx), color=C["red"], lw=1.2)
a1.text(X.max() * 0.55, 12,
        f"기울기 = DVR = {p[0]:.2f}\n$BP_{{ND}}$ = DVR − 1 = {p[0] - 1:.2f}", fontsize=8.3, color=C["red"])
a1.set_xlabel("[∫참조 + 참조/$k_2'$] / 목표   (분)")
a1.set_ylabel("∫목표 / 목표   (분)")
a1.set_xlim(0, X.max() * 1.05)
a1.set_ylim(0, Y.max() * 1.1)
a1.legend(fontsize=7.6, loc="upper left")
a1.set_title("(가) 참조 영역 로건 도표", fontsize=9.5)

# (나) 비 - 1
m = t > 3
a2.plot(t[m], CT[m] / CR[m] - 1, color=C["blue"], lw=1.8, label="정상 혈류")
a2.plot(t[m], CT2[m] / CR2[m] - 1, color=C["red"], lw=1.5, ls="--", label="혈류 30% 감소")
a2.axhline(3, color=C["gray"], lw=1, ls=":")
a2.text(118, 2.82, "참 $BP_{ND}$ = 3", ha="right", va="top", fontsize=8, color=C["gray"])
for tt in (40,):
    i = int(tt / dt)
    v1, v2 = CT[i] / CR[i] - 1, CT2[i] / CR2[i] - 1
    a2.scatter([tt, tt], [v1, v2], color=[C["blue"], C["red"]], s=16, zorder=3)
    a2.text(tt + 2, v1 + 0.12, f"{v1:.2f}", fontsize=7.8, color=C["blue"], va="bottom")
    a2.text(tt + 2, v2 - 0.12, f"{v2:.2f}", fontsize=7.8, color=C["red"], va="top")
a2.set_xlim(0, 120)
a2.set_ylim(0, 4.5)
a2.set_xlabel("주사 뒤 시간 (분)")
a2.set_ylabel("목표/참조 비 − 1")
a2.legend(fontsize=7.6, loc="lower right")
a2.set_title("(나) 한 시점의 비는 시간과 혈류에 흔들린다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
