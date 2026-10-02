from figstyle import plt, np, save, C

fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.25], height_ratios=[1, 1.6], wspace=0.38, hspace=0.25)
a1 = fig.add_subplot(gs[:, 0])
b1 = fig.add_subplot(gs[0, 1])
b2 = fig.add_subplot(gs[1, 1], sharex=b1)

# 왼쪽: 산소 분압과 뇌혈류 (포화도가 떨어질 때 늘어난다, 개념도)
P = np.linspace(20, 150, 400)
sat = P ** 2.7 / (P ** 2.7 + 26.8 ** 2.7) * 100
rel = 100 + 1.5 * np.clip(97 - sat, 0, None)
a1.plot(P, rel, color=C["red"], lw=1.9)
a1.axvspan(80, 100, color=C["light"], zorder=0)
a1.text(90, 104, "정상\nP$_{aO_2}$", ha="center", fontsize=7.5, color=C["blue"])
a1.axvline(55, color=C["gray"], lw=0.6, ls=":")
a1.text(57, 175, "약 50–60 mmHg 아래에서\n가파르게 는다", fontsize=7.5, color=C["gray"], va="top")
a1.set_xlabel("동맥 산소 분압 P$_{aO_2}$ (mmHg)")
a1.set_ylabel("뇌혈류 (정상 = 100 %)")
a1.set_title("산소: 저산소에서만 반응", fontsize=10)
a1.set_ylim(80, 180)
a1.set_xlim(20, 150)

# 오른쪽: CVR 블록 실험 시뮬레이션
t = np.arange(0, 480, 1.0)
blocks = ((60, 120), (240, 300), (390, 450))
box = np.zeros_like(t)
for s, e in blocks:
    box[(t >= s) & (t < e)] = 8.0


def smooth(x, tau):
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = y[i - 1] + (x[i] - y[i - 1]) / tau
    return y


et = 40 + smooth(box, 8)
b1.plot(t, et, color=C["gray"], lw=1.4)
b1.set_ylabel("P$_{ETCO_2}$\n(mmHg)", fontsize=8.5)
b1.set_ylim(38, 50)
b1.set_yticks([40, 48])
b1.tick_params(labelbottom=False)
b1.set_title("CO$_2$ 흡입 블록과 BOLD 반응 (모형)", fontsize=10)

d = et - 40
for cvr, tau, col, lab in ((0.20, 12, C["blue"], "정상 회백질 0.20 %/mmHg"),
                           (0.05, 35, C["purple"], "예비능 감소 0.05 %/mmHg, 느림"),
                           (-0.04, 25, C["red"], "훔치기 −0.04 %/mmHg")):
    b2.plot(t, cvr * smooth(d, tau), color=col, lw=1.5, label=lab)
b2.axhline(0, color=C["gray"], lw=0.6)
for s, e in blocks:
    for ax in (b1, b2):
        ax.axvspan(s, e, color=C["light"], zorder=0)
b2.set_xlabel("시간 (s)")
b2.set_ylabel("BOLD 변화 (%)", fontsize=8.5)
b2.set_ylim(-0.6, 3.3)
b2.legend(fontsize=6.8, loc="upper left", ncol=1, borderaxespad=0.1)
save(fig, __file__)
