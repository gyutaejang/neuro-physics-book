from figstyle import plt, np, save, C

# 두피 전극 9개 위의 '참' 전위(측정할 수 없는 절대값)
names = ["Fpz", "AFz", "Fz", "FCz", "Cz", "CPz", "Pz", "POz", "Oz"]
xi = np.arange(9)
true = 3 + 6 * np.exp(-0.5 * ((xi - 4.2) / 1.4) ** 2) - 2.5 * np.exp(-0.5 * ((xi - 0.5) / 1.0) ** 2)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[1.25, 1]))
a1.plot(xi, true, "o-", color=C["gray"], ms=4, label="절대 전위 (알 수 없다)")
a1.plot(xi, true - true[-1], "o-", color=C["blue"], ms=4, label="Oz 기준")
a1.plot(xi, true - true.mean(), "o-", color=C["red"], ms=4, label="평균 기준")
a1.axhline(0, color=C["gray"], lw=0.6, ls=":")
a1.set_xticks(xi)
a1.set_xticklabels(names, fontsize=7.5)
a1.set_ylabel("전위 (μV)")
a1.set_title("기준을 바꾸면 곡선 전체가 위아래로 옮겨진다", fontsize=9.5)
a1.legend(fontsize=7.5, loc="upper right")
a1.set_ylim(-6, 13)
a1.text(4, -5.2, "전극 사이의 차이(곡선의 모양)는 세 곡선에서 같다", fontsize=8, ha="center", color=C["ink"])

# 오른쪽: 기준 전극이 스스로 활동하면 파형이 바뀐다
t = np.linspace(0, 0.6, 400)
act = 8 * np.exp(-0.5 * ((t - 0.30) / 0.05) ** 2)
ref = 4 * np.exp(-0.5 * ((t - 0.30) / 0.07) ** 2)
a2.plot(t * 1000, act, color=C["gray"], label="Cz의 절대 전위")
a2.plot(t * 1000, ref, color=C["gray"], ls="--", label="기준 전극의 절대 전위")
a2.plot(t * 1000, act - ref, color=C["blue"], lw=2, label="기록되는 값 (차이)")
a2.set_xlabel("시간 (ms)")
a2.set_ylabel("전위 (μV)")
a2.set_ylim(-1, 12.5)
a2.legend(fontsize=7.5, loc="upper left")
a2.set_title("기준 전극도 신호를 받으면 진폭이 줄어든다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
