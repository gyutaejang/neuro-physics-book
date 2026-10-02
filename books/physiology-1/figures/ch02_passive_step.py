from figstyle import plt, np, save, C

fig = plt.figure(figsize=(7.4, 3.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1], height_ratios=[0.35, 1], hspace=0.08, wspace=0.35)
ai = fig.add_subplot(gs[0, 0])
av = fig.add_subplot(gs[1, 0], sharex=ai)
ar = fig.add_subplot(gs[:, 1])

t = np.linspace(-20, 180, 1000)
on, off = 0, 120
I = np.where((t >= on) & (t < off), -50, 0)
tau, R = 15.0, 100.0  # ms, MΩ
dV = -50e-12 * R * 1e6 * 1e3  # mV
v = np.zeros_like(t)
m = (t >= on) & (t < off)
v[m] = dV * (1 - np.exp(-(t[m] - on) / tau))
v_off = dV * (1 - np.exp(-(off - on) / tau))
m2 = t >= off
v[m2] = v_off * np.exp(-(t[m2] - off) / tau)
V = -70 + v

ai.plot(t, I, color=C["red"], lw=1.4)
ai.set_ylim(-65, 15)
ai.set_yticks([0, -50])
ai.set_yticklabels(["0", "−50"])
ai.set_ylabel("pA", rotation=0, labelpad=12, va="center")
ai.tick_params(labelbottom=False)
ai.spines["bottom"].set_visible(False)
ai.tick_params(axis="x", length=0)
ai.text(60, -40, "주입 전류 −50 pA", fontsize=8, color=C["red"], ha="center")

av.plot(t, V, color=C["blue"], lw=1.6)
av.axhline(-70, color=C["gray"], lw=0.6, ls=":")
av.axhline(-75, color=C["gray"], lw=0.6, ls=":")
v63 = -70 + 0.632 * dV
av.plot([tau], [v63], "o", color=C["blue"], ms=4.5)
av.plot([tau, tau], [v63, -76.5], color=C["gray"], lw=0.7, ls="--")
av.annotate("63%에 이르는 시간\n= τ ≈ 15 ms", xy=(tau, v63), xytext=(32, -73.0), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")
av.annotate("", xy=(100, -75), xytext=(100, -70),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.9, mutation_scale=8))
av.text(103, -72.5, "ΔV = −5 mV", fontsize=8, va="center")
av.set_ylim(-76.5, -68.8)
av.set_yticks([-75, -70])
av.set_yticklabels(["−75", "−70"])
av.set_xlabel("시간 (ms)")
av.set_ylabel("막전위 (mV)")
av.set_xlim(-20, 180)
ai.set_title("(가) 전류 계단에 대한 막전위 반응", fontsize=10, loc="left")

Is = np.linspace(-50, 0, 10)
for Rin, col, lab in ((50, C["blue"], "큰 피라미드 뉴런 50 MΩ"), (150, C["green"], "작은 피라미드 뉴런 150 MΩ"),
                      (800, C["purple"], "작은 과립세포 800 MΩ")):
    ar.plot(Is, Is * Rin * 1e-3, color=col, lw=1.8, label=lab)
ar.axhline(0, color=C["gray"], lw=0.6)
ar.set_xlabel("주입 전류 (pA)")
ar.set_ylabel("정상 상태 ΔV (mV)")
ar.set_xticks([-50, -25, 0])
ar.set_xticklabels(["−50", "−25", "0"])
ar.set_ylim(-42, 3)
ar.set_yticks([-40, -30, -20, -10, 0])
ar.set_yticklabels(["−40", "−30", "−20", "−10", "0"])
ar.legend(fontsize=7.5, loc="lower right")
ar.set_title("(나) 기울기 = 입력 저항", fontsize=10, loc="left")
save(fig, __file__)
