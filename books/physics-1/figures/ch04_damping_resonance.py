from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9))

t = np.linspace(0, 6, 1200)
for Q, col, lab in ((3, C["red"], "Q = 3"), (20, C["blue"], "Q = 20")):
    env = np.exp(-np.pi * t / Q)  # f0 = 1 Hz, 진폭은 e^(-ω0 t / 2Q)
    a1.plot(t, env * np.cos(2 * np.pi * t), color=col, lw=1.3, label=lab)
    a1.plot(t, env, color=col, lw=0.7, ls="--")
a1.axhline(0, color=C["gray"], lw=0.5)
a1.set_xlabel("시간 (주기 단위)")
a1.set_ylabel("변위")
a1.set_title("감쇠 진동", fontsize=10)
a1.legend(fontsize=8.5, loc="upper right")
a1.text(3.0, -0.95, "점선: 포락선(진폭)", fontsize=8, color=C["gray"])
a1.set_ylim(-1.1, 1.15)

r = np.linspace(0.01, 2.0, 800)
for Q, col in ((2, C["gray"]), (5, C["red"]), (20, C["blue"])):
    A = 1 / np.sqrt((1 - r ** 2) ** 2 + (r / Q) ** 2)
    a2.plot(r, A, color=col, lw=1.4, label=f"Q = {Q}")
a2.set_yscale("log")
a2.set_ylim(0.2, 40)
a2.set_yticks([0.3, 1, 3, 10, 30])
a2.set_yticklabels(["0.3", "1", "3", "10", "30"])
a2.minorticks_off()
a2.set_xlabel("구동 주파수 / 고유 주파수")
a2.set_ylabel("진폭 (로그 눈금)")
a2.set_title("강제 진동의 공명 곡선", fontsize=10)
a2.axvline(1, color=C["gray"], lw=0.6, ls=":")
a2.legend(fontsize=8.5, loc="upper right")
a2.text(1.04, 0.25, "공명", fontsize=8.5, color=C["gray"])
fig.tight_layout()
save(fig, __file__)
