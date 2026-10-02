"""HRF 지연의 지역 차이가 시간 순서를 뒤집는다: 교차 상관과 그레인저 인과."""
import math
import sys

from scipy import signal, stats

from figstyle import plt, np, save, C

rng = np.random.default_rng(2)
dt = 0.1
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)


def hrf(peak):
    a1 = peak + 1  # 감마 함수 t^(a-1)e^(-t)의 정점은 a-1
    h = g(th, a1) - g(th, a1 + 10) / 6
    return h / h.max()


hA, hB = hrf(6.0), hrf(5.0)  # A의 HRF가 1 s 느리다

T_s = 1200.0
N = int(T_s / dt)
bn, an = signal.butter(2, 0.5, fs=1 / dt)  # 신경 활동: 0.5 Hz 아래로 매끄럽게
xa = signal.filtfilt(bn, an, rng.standard_normal(N + 50))
lag = int(round(0.1 / dt))                     # B는 A를 100 ms 늦게 따른다
xb = 0.8 * xa[50 - lag:N + 50 - lag] + 0.6 * signal.filtfilt(bn, an, rng.standard_normal(N))
xa = xa[50:]
ya = np.convolve(xa, hA)[:N]
yb = np.convolve(xb, hB)[:N]


def xcorr(u, v, maxlag):
    u = (u - u.mean()) / u.std()
    v = (v - v.mean()) / v.std()
    L = np.arange(-maxlag, maxlag + 1)
    out = [np.mean(u[max(0, -l):len(u) - max(0, l)] * v[max(0, l):len(v) - max(0, -l)]) for l in L]
    return L, np.array(out)


L, cn = xcorr(xa, xb, 40)
L, cb = xcorr(ya, yb, 40)
ln, lb = L[np.argmax(cn)] * dt, L[np.argmax(cb)] * dt
print(f"neural lag {ln:+.1f} s, BOLD lag {lb:+.1f} s (양수 = B가 늦음)", file=sys.stderr)

# TR 0.72 s로 표본화하고 측정 잡음을 더한 뒤 그레인저 인과(AR 2차) 검정
TR = 0.72
idx = np.round(np.arange(0, N, TR / dt)).astype(int)
idx = idx[idx < N]
sa = ya[idx] + 0.3 * ya.std() * rng.standard_normal(len(idx))
sb = yb[idx] + 0.3 * yb.std() * rng.standard_normal(len(idx))


def granger(x, y, p=2):
    """y의 과거에 x의 과거를 더하면 y 예측이 나아지는가 (F 검정)."""
    n = len(y)
    Y = y[p:]
    own = np.column_stack([y[p - k:n - k] for k in range(1, p + 1)])
    oth = np.column_stack([x[p - k:n - k] for k in range(1, p + 1)])
    one = np.ones((len(Y), 1))
    X0 = np.hstack([one, own])
    X1 = np.hstack([one, own, oth])
    r0 = Y - X0 @ np.linalg.lstsq(X0, Y, rcond=None)[0]
    r1 = Y - X1 @ np.linalg.lstsq(X1, Y, rcond=None)[0]
    df2 = len(Y) - X1.shape[1]
    F = ((r0 @ r0 - r1 @ r1) / p) / (r1 @ r1 / df2)
    return F, stats.f.sf(F, p, df2)


Fab, pab = granger(sa, sb)
Fba, pba = granger(sb, sa)
print(f"Granger A->B F={Fab:.1f} p={pab:.2g}; B->A F={Fba:.1f} p={pba:.2g}; n={len(sa)}", file=sys.stderr)

fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw=dict(wspace=0.32))
ax = axes[0]
ax.plot(th, hA, color=C["blue"], lw=1.7, label="영역 A의 HRF (정점 6 s)")
ax.plot(th, hB, color=C["red"], lw=1.7, label="영역 B의 HRF (정점 5 s)")
ax.axhline(0, color=C["gray"], lw=0.5)
ax.set_xlim(0, 25)
ax.set_ylim(-0.3, 1.25)
ax.set_xlabel("자극 뒤 시간 (s)")
ax.set_ylabel("정규화한 반응")
ax.set_title("(가) 영역마다 다른 HRF", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper right")

ax = axes[1]
ax.plot(L * dt, cn, color=C["green"], lw=1.6, label="신경 활동 A, B")
ax.plot(L * dt, cb, color=C["purple"], lw=1.6, label="BOLD A, B")
for lv, cc, col in [(ln, cn.max(), C["green"]), (lb, cb.max(), C["purple"])]:
    ax.plot([lv, lv], [0.3, cc], color=col, lw=0.8, ls=":")
ax.text(ln + 0.15, 0.33, f"{ln:+.1f} s", color=C["green"], fontsize=8)
ax.text(lb - 0.15, 0.33, f"{lb:+.1f} s", color=C["purple"], fontsize=8, ha="right")
ax.text(-3.9, 1.1, f"그레인저 F (TR 0.72 s)\nA→B {Fab:.0f}, B→A {Fba:.0f}", fontsize=7.5, va="top",
        color=C["ink"])
ax.axvline(0, color=C["gray"], lw=0.5)
ax.set_xlim(-4, 4)
ax.set_ylim(0.3, 1.12)
ax.set_xlabel("지연 (s, 양수 = B가 늦다)")
ax.set_ylabel("교차 상관")
ax.set_title("(나) BOLD에서는 순서가 뒤집힌다", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper right")
save(fig, __file__)
