from figstyle import plt, np, save, C

alpha, lam, tau = 0.85, 0.9, 1.8


def dm(pld, f_ml, att, T1b=1.65):
    """연속 표지(pCASL)의 단일 구획 모형, ΔM/M0. f_ml: mL/100 g/분."""
    f = f_ml / 6000.0
    t = pld + tau                      # 표지 시작부터의 시간
    A = 2 * alpha * f * T1b / lam * np.exp(-att / T1b)
    out = np.where(t < att, 0.0,
                   np.where(t < att + tau, A * (1 - np.exp(-(t - att) / T1b)),
                            A * np.exp(-(t - tau - att) / T1b) * (1 - np.exp(-tau / T1b))))
    return out * 100                   # %


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
# 왼쪽: 표지가 바래는 속도 (혈액 T1)
tt = np.linspace(0, 5, 300)
for T1b, col, lab in ((1.35, C["gray"], "1.5 T (혈액 T1 약 1.35 s)"), (1.65, C["blue"], "3 T (혈액 T1 약 1.65 s)")):
    a1.plot(tt, np.exp(-tt / T1b) * 100, color=col, lw=1.8, label=lab)
a1.axvline(1.8, color=C["red"], lw=0.8, ls="--")
a1.text(1.88, 86, "PLD 1.8 s", fontsize=7.8, color=C["red"])
a1.scatter([1.8], [np.exp(-1.8 / 1.65) * 100], color=C["blue"], s=20, zorder=3)
a1.text(1.95, np.exp(-1.8 / 1.65) * 100 + 2, f"{np.exp(-1.8 / 1.65) * 100:.0f} %", fontsize=7.8, color=C["blue"])
a1.set_xlabel("표지 뒤 시간 (s)")
a1.set_ylabel("남은 표지 (%)")
a1.set_title("표지는 수 초 안에 바랜다", fontsize=10)
a1.set_xlim(0, 5)
a1.set_ylim(0, 105)
a1.legend(fontsize=7.3, loc="upper right")

pld = np.linspace(0, 4, 400)
for att, col in ((0.8, C["blue"]), (1.5, C["purple"]), (2.5, C["red"])):
    a2.plot(pld, dm(pld, 60, att), color=col, lw=1.7, label=f"동맥 통과 시간 {att} s")
a2.axvline(1.8, color=C["gray"], lw=0.8, ls="--")
a2.text(1.86, 0.02, "PLD 1.8 s", fontsize=7.5, color=C["gray"])
a2.set_xlabel("표지 뒤 지연 PLD (s)")
a2.set_ylabel(r"ASL 차이 신호 $\Delta M/M_0$ (%)")
a2.set_title("CBF 60일 때의 차이 신호 (pCASL 모형)", fontsize=10)
a2.set_xlim(0, 4)
a2.set_ylim(0, 1.4)
a2.legend(fontsize=7.3, loc="upper right")
fig.tight_layout()
save(fig, __file__)
