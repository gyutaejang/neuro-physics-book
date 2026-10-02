from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0))

# (가) 계단 전류에 대한 충전과 방전
tau = 20.0
t = np.linspace(0, 200, 800)
on, off = 0, 100
v = np.where(t < off, 1 - np.exp(-(t - on) / tau),
             (1 - np.exp(-(off - on) / tau)) * np.exp(-(t - off) / tau))
a1.plot(t, v, color=C["blue"])
a1.axvspan(on, off, color=C["red"], alpha=0.07)
a1.text(50, 1.07, "전류 주입 중", ha="center", fontsize=8, color=C["red"])
for k, lab in [(1, "63%"), (2, "86%"), (3, "95%")]:
    y = 1 - np.exp(-k)
    a1.plot([k * tau], [y], "o", color=C["red"], ms=3.5)
    a1.text(k * tau + 3, y - 0.07, f"{k}τ: {lab}", fontsize=7.5, va="top")
a1.plot([0, tau], [0, 1], color=C["gray"], lw=0.7, ls="--")
a1.plot([off + tau], [np.exp(-1)], "o", color=C["red"], ms=3.5)
a1.text(off + tau + 4, np.exp(-1), "τ 뒤 37%", fontsize=7.5, va="bottom")
a1.axhline(1, color=C["gray"], lw=0.6, ls=":")
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("ΔV / 최종값")
a1.set_ylim(-0.05, 1.18)
a1.set_title("(가) 충전과 방전 (τ = 20 ms)", fontsize=10)

# (나) 시간 합산: 같은 입력, 다른 τ
dt = 0.05
t2 = np.arange(0, 60, dt)
I = np.zeros_like(t2)
for s in (5, 13, 21):
    I[(t2 >= s) & (t2 < s + 1)] = 1.0
for tau2, col, ls in [(4, C["gray"], "--"), (20, C["blue"], "-")]:
    V = np.zeros_like(t2)
    for i in range(1, len(t2)):
        V[i] = V[i - 1] + dt * (-V[i - 1] / tau2 + I[i - 1])   # C 고정, R만 다르다
    a2.plot(t2, V, color=col, ls=ls, label=f"τ = {tau2} ms")
for s in (5, 13, 21):
    a2.annotate("", xy=(s + 0.5, -0.05), xytext=(s + 0.5, -0.5),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1))
a2.text(13.5, -0.65, "짧은 입력 세 번", ha="center", va="top", fontsize=8, color=C["red"])
a2.set_xlabel("시간 (ms)")
a2.set_ylabel("ΔV (임의 단위)")
a2.set_ylim(-1.3, 2.9)
a2.legend(fontsize=8, loc="upper right")
a2.set_title("(나) τ가 길면 입력이 쌓인다", fontsize=10)
fig.tight_layout()
save(fig, __file__)
