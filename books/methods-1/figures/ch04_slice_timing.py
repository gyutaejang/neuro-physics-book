import math

from figstyle import plt, np, save, C

# (가) 슬라이스 획득 시각: TR 2 s, 36장, 순차/교차, 다중 대역 4(TR 0.8 s, 9장씩 4묶음).
TR, N = 2.0, 36
idx = np.arange(1, N + 1)
seq_t = (idx - 1) * TR / N
order = list(range(1, N + 1, 2)) + list(range(2, N + 1, 2))      # 홀수 먼저
inter_t = np.empty(N)
for k, s in enumerate(order):
    inter_t[s - 1] = k * TR / N
TRm, MB = 0.8, 4
nexc = N // MB                                                    # 들뜸 9번
mb_t = ((idx - 1) % nexc) * TRm / nexc

# (나) 시간 어긋남이 모형 적합을 얼마나 깎는가.
g = lambda t, a: np.where(t > 0, t ** (a - 1) * np.exp(-t) / math.gamma(a), 0.0)
dt = 0.01
th = np.arange(0, 32, dt)
hrf = g(th, 6) - g(th, 16) / 6
rng = np.random.default_rng(4)
T = 600.0
tt = np.arange(0, T, dt)
ev = np.zeros_like(tt)
ons = np.cumsum(rng.uniform(4, 10, 200))
ons = ons[ons < T - 30]
ev[(ons / dt).astype(int)] = 1
blk = ((tt // 20) % 2 == 1).astype(float)


def reg(stim):
    return np.convolve(stim, hrf)[: len(tt)] * dt


def r2_loss(x, shifts, deriv=False):
    out = []
    for s in shifts:
        k = int(round(s / dt))
        y = np.roll(x, k)
        sl = slice(int(40 / dt), len(tt))
        X = [x[sl] - x[sl].mean()]
        if deriv:
            d = np.gradient(x)[sl]
            X.append(d - d.mean())
        X = np.array(X).T
        yy = y[sl] - y[sl].mean()
        b = np.linalg.lstsq(X, yy, rcond=None)[0]
        out.append(1 - np.sum((yy - X @ b) ** 2) / np.sum(yy ** 2))
    return np.array(out)


shifts = np.linspace(0, 2, 41)          # 0.05 s 간격
xe, xb = reg(ev), reg(blk)
re_, rb, red = r2_loss(xe, shifts), r2_loss(xb, shifts), r2_loss(xe, shifts, True)
for s in (0.5, 0.7, 1.0, 1.5, 2.0):
    i = int(round(s / 0.05))
    print(f"shift {s}: event R2 {re_[i]:.3f}  block {rb[i]:.3f}  event+deriv {red[i]:.3f}")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(wspace=0.32))
a1.plot(idx, seq_t, color=C["gray"], lw=1.2, label="순차 (TR 2 s)")
a1.scatter(idx, inter_t, s=11, color=C["blue"], zorder=3, label="교차 (TR 2 s)")
a1.scatter(idx, mb_t, s=11, color=C["purple"], marker="s", zorder=3, label="다중 대역 4 (TR 0.8 s)")
a1.set_xlabel("슬라이스 번호 (아래 → 위)")
a1.set_ylabel("볼륨 시작 뒤 획득 시각 (s)")
a1.set_xlim(0, 37)
a1.set_ylim(-0.05, 2.25)
a1.legend(fontsize=7.5, loc="upper left", handletextpad=0.3)
a1.set_title("(가) 같은 볼륨, 다른 시각", fontsize=10)

a2.plot(shifts, re_, color=C["blue"], lw=1.8, label="사건 관련 설계")
a2.plot(shifts, rb, color=C["gray"], lw=1.4, label="블록 설계 (20 s)")
a2.plot(shifts, red, color=C["red"], lw=1.4, ls="--", label="사건 관련 + 시간 미분")
a2.set_xlabel("모형과 실제 획득 시각의 어긋남 (s)")
a2.set_ylabel("설명된 분산 비율 $R^2$")
a2.set_ylim(0.2, 1.03)
a2.set_xlim(0, 2)
a2.legend(fontsize=7.5, loc="lower left")
a2.set_title("(나) 어긋남이 깎는 적합", fontsize=10)
save(fig, __file__)
