import math

from figstyle import plt, np, save, C

# 신호 모형: 사건 시간표 → 신경 상자 함수 → HRF 합성곱 → TR마다 표본화.
dt, TR = 0.1, 2.0
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6

T = 80.0
t = np.arange(0, T, dt)
ons = [4, 18, 24, 46, 58]
durs = [2, 2, 2, 8, 2]
s = np.zeros_like(t)
for o, d in zip(ons, durs):
    s[(t >= o) & (t < o + d)] = 1
x = np.convolve(s, h)[: len(t)] * dt
x = x / x.max()
tr = np.arange(0, T, TR)
xs = x[(tr / dt).astype(int)]

fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], width_ratios=[1.55, 1], hspace=0.65, wspace=0.3)

a1 = fig.add_subplot(gs[0, :])
a1.fill_between(t, 0, s, step="pre", color=C["light"], lw=0)
a1.step(t, s, where="pre", color=C["gray"], lw=0.8, label="자극 시간표 (상자 함수)")
a1.plot(t, x, color=C["blue"], lw=1.8, label="HRF와 합성곱한 예측 BOLD")
a1.plot(tr, xs, "o", color=C["blue"], ms=3.2, mfc="white", mew=1, label=f"TR = {TR:.0f} s마다 표본화")
a1.set_xlim(0, T)
a1.set_ylim(-0.25, 1.45)
a1.set_xlabel("시간 (s)")
a1.set_ylabel("크기 (최대 = 1)")
a1.set_title("(가) 시간표에서 회귀자로", fontsize=9.5)
a1.legend(fontsize=7.8, loc="upper right", ncol=3)
a1.annotate("가까운 사건 두 개는\n겹쳐 더해진다", xy=(29.5, 0.42), xytext=(32, 0.85), fontsize=7.8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")

# (나) 정점이 1 s 늦은 실제 반응을 표준 HRF만으로, 시간 미분을 더해 맞춘다
a2 = fig.add_subplot(gs[1, 0])
tt = np.arange(0, 30, dt)
hc = g(tt, 6) - g(tt, 16) / 6
hd = np.gradient(hc, dt)
lag = 2.0
true = np.interp(tt - lag, tt, hc, left=0)
X1 = hc[:, None]
X2 = np.column_stack([hc, hd])
b1 = np.linalg.lstsq(X1, true, rcond=None)[0]
b2 = np.linalg.lstsq(X2, true, rcond=None)[0]
a2.plot(tt, true / hc.max(), color=C["ink"], lw=2.2, label="실제 반응 (정점 2 s 늦음)")
a2.plot(tt, X1 @ b1 / hc.max(), color=C["red"], lw=1.3, ls="--",
        label=f"표준 HRF만: 정점 {(X1 @ b1).max() / hc.max():.2f}")
a2.plot(tt, X2 @ b2 / hc.max(), color=C["blue"], lw=1.3,
        label=f"표준 HRF + 시간 미분: 정점 {(X2 @ b2).max() / hc.max():.2f}")
a2.axhline(0, color=C["gray"], lw=0.5)
a2.set_xlim(0, 30)
a2.set_ylim(-0.3, 1.5)
a2.set_xlabel("사건 뒤 시간 (s)")
a2.set_ylabel("반응 (참 정점 = 1)")
a2.set_title("(나) 지연을 흡수하는 시간 미분", fontsize=9.5)
a2.legend(fontsize=7.3, loc="upper right")

# (다) 기저 함수 두 개
a3 = fig.add_subplot(gs[1, 1])
a3.plot(tt, hc / hc.max(), color=C["blue"], lw=1.8, label="표준 HRF")
a3.plot(tt, hd / np.abs(hd).max(), color=C["purple"], lw=1.4, ls="--", label="시간 미분")
a3.axhline(0, color=C["gray"], lw=0.5)
a3.set_xlim(0, 30)
a3.set_ylim(-1.15, 1.5)
a3.set_xlabel("사건 뒤 시간 (s)")
a3.set_title("(다) 기저 함수", fontsize=9.5)
a3.legend(fontsize=7.5, loc="upper right")
save(fig, __file__)
