from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
dt = 0.05  # ms
t = np.arange(0, 200, dt)
k_open, k_close = 0.2, 0.5  # /ms → 평균 닫힘 5 ms, 평균 열림 2 ms, Po ≈ 0.29
state = np.zeros(t.size)
s = 0
for n in range(t.size):
    if s == 0 and rng.random() < k_open * dt:
        s = 1
    elif s == 1 and rng.random() < k_close * dt:
        s = 0
    state[n] = s
i_open = 2.1  # pA, -20 mV에서 (구동력 70 mV, 30 pS)
noise = rng.normal(0, 0.22, t.size)
kern = np.ones(4) / 4
cur = np.convolve(state * i_open + noise, kern, mode="same")

fig = plt.figure(figsize=(7.4, 2.9))
gs = fig.add_gridspec(1, 3, width_ratios=[2.3, 0.4, 1.5], wspace=0.08)
a1 = fig.add_subplot(gs[0])
ah = fig.add_subplot(gs[1], sharey=a1)
gs2 = gs[2].subgridspec(1, 1)
a2 = fig.add_subplot(gs2[0])

a1.plot(t, cur, color=C["blue"], lw=0.5)
a1.axhline(0, color=C["gray"], lw=0.6, ls=":")
a1.axhline(i_open, color=C["gray"], lw=0.6, ls=":")
a1.set_xlim(0, 200)
a1.set_ylim(-1.0, 3.4)
a1.set_xlabel("시간 (ms)")
a1.set_yticks([-1, 0, 1, 2, 3])
a1.set_yticklabels(["−1", "0", "1", "2", "3"])
a1.set_ylabel("전류 (pA)")
a1.set_title("(가) 통로 하나의 전류 (막전위 −20 mV)", fontsize=10, loc="left")

ah.hist(cur, bins=60, orientation="horizontal", color=C["blue"], alpha=0.6)
ah.axis("off")
ah.text(ah.get_xlim()[1] * 0.35, 0.45, "닫힘", fontsize=8, color=C["gray"], va="bottom")
ah.text(ah.get_xlim()[1] * 0.35, i_open + 0.4, "열림", fontsize=8, color=C["gray"], va="bottom")

V = np.linspace(-120, 20, 50)
gam = 30e-3  # nS → pA/mV
a2.plot(V, gam * (V + 90), color=C["green"], lw=1.6)
a2.plot([-20], [gam * 70], "o", color=C["blue"], ms=5)
a2.axhline(0, color=C["gray"], lw=0.6)
a2.axvline(-90, color=C["gray"], lw=0.6, ls=":")
a2.text(-88, 2.9, "$E_K$ = −90 mV", fontsize=8, color=C["gray"])
a2.text(-58, -0.95, "기울기 = 단일 통로\n전도도 γ = 30 pS", fontsize=8, color=C["green"])
a2.set_xlabel("막전위 (mV)")
a2.set_ylabel("열린 통로 전류 (pA)")
a2.set_xticks([-120, -90, -60, -30, 0])
a2.set_xticklabels(["−120", "−90", "−60", "−30", "0"])
a2.set_yticks([-1, 0, 1, 2, 3])
a2.set_yticklabels(["−1", "0", "1", "2", "3"])
a2.set_title("(나) 전류–전압 관계", fontsize=10, loc="left")
fig.subplots_adjust(left=0.08, right=0.98)
a2.set_position([0.745, a1.get_position().y0, 0.235, a1.get_position().height])
save(fig, __file__)
