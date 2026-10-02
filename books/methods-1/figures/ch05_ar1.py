import math

from figstyle import plt, np, save, C
from scipy import stats

# 귀무 자료(효과 없음)에 AR(1) 잡음을 넣고, 블록 회귀자의 t를 OLS와 선백화로 계산한다.
dt, TR, N = 0.1, 2.0, 200
T = N * TR
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6
t = np.arange(0, T, dt)
s = ((t % 40) < 20).astype(float)
x = (np.convolve(s, h)[: len(t)] * dt)[:: int(TR / dt)]
n = np.arange(N)
dct = np.array([np.cos(np.pi * k * (2 * n + 1) / (2 * N)) for k in range(1, 7)]).T
X = np.column_stack([x / x.max(), dct, np.ones(N)])
p = X.shape[1]
df = N - p
crit = stats.t.ppf(0.975, df)


def ar1(rho, rng, m):
    e = rng.standard_normal((m, N))
    y = np.zeros((m, N))
    y[:, 0] = e[:, 0] / np.sqrt(1 - rho ** 2)
    for i in range(1, N):
        y[:, i] = rho * y[:, i - 1] + e[:, i]
    return y


def tvals(Xm, Ym):
    # Xm: (m, N, p) 또는 (N, p), Ym: (m, N)
    if Xm.ndim == 2:
        Xm = np.broadcast_to(Xm, (Ym.shape[0],) + Xm.shape)
    XtX = np.einsum("mni,mnj->mij", Xm, Xm)
    XtY = np.einsum("mni,mn->mi", Xm, Ym)
    b = np.linalg.solve(XtX, XtY[..., None])[..., 0]
    r = Ym - np.einsum("mni,mi->mn", Xm, b)
    s2 = (r ** 2).sum(1) / df
    v = np.linalg.inv(XtX)[:, 0, 0]
    return b[:, 0] / np.sqrt(s2 * v), r


def whiten(rho, A):
    # A: (m, N) 또는 (m, N, p); rho: (m,)
    rr = rho.reshape((-1,) + (1,) * (A.ndim - 1))
    first = A[:, :1] * np.sqrt(1 - rr ** 2)
    return np.concatenate([first, A[:, 1:] - rr * A[:, :-1]], axis=1)


def acf(r, L=8):
    r = r - r.mean(1, keepdims=True)
    d = (r ** 2).sum(1)
    return np.array([((r[:, k:] * r[:, : N - k]).sum(1) / d).mean() for k in range(L + 1)])


rng = np.random.default_rng(2)
m = 3000
rhos = np.arange(0, 0.51, 0.1)
fpr_ols, fpr_est, fpr_true = [], [], []
for rho in rhos:
    Y = ar1(rho, rng, m)
    t0, r0 = tvals(X, Y)
    rh = (r0[:, 1:] * r0[:, :-1]).sum(1) / (r0 ** 2).sum(1)
    Xm = np.broadcast_to(X, (m, N, p))
    t1, r1 = tvals(whiten(rh, Xm), whiten(rh, Y))
    tr_ = np.full(m, rho)
    t2, _ = tvals(whiten(tr_, Xm), whiten(tr_, Y))
    fpr_ols.append(np.mean(abs(t0) > crit))
    fpr_est.append(np.mean(abs(t1) > crit))
    fpr_true.append(np.mean(abs(t2) > crit))
    if abs(rho - 0.3) < 1e-9:
        ac0, ac1 = acf(r0), acf(r1)
        sd0, sd1 = t0.std(), t1.std()
        rh_mean = rh.mean()

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"wspace": 0.35})
lags = np.arange(len(ac0))
a1.axhline(0, color=C["gray"], lw=0.5)
a1.plot(lags, 0.3 ** lags, color=C["gray"], ls=":", lw=1.2, label="참 잡음 $\\rho^k$ ($\\rho$ = 0.3)")
a1.plot(lags, ac0, "o-", color=C["red"], ms=3.5, lw=1.2, label="OLS 잔차")
a1.plot(lags, ac1, "s-", color=C["blue"], ms=3.5, lw=1.2, label="선백화 뒤 잔차")
a1.set_xlabel("시차 $k$ (TR 단위)")
a1.set_ylabel("자기상관")
a1.set_ylim(-0.15, 1.05)
a1.set_title("(가) 잔차의 자기상관", fontsize=9.5)
a1.legend(fontsize=7.8, loc="upper right")

a2.axhline(0.05, color=C["gray"], lw=0.8, ls="--")
a2.text(0.33, 0.032, "명목 5 %", fontsize=7.5, color=C["gray"])
a2.plot(rhos, fpr_ols, "o-", color=C["red"], ms=3.5, lw=1.4, label="OLS (자기상관 무시)")
a2.plot(rhos, fpr_est, "s-", color=C["blue"], ms=3.5, lw=1.4, label="추정한 $\\hat\\rho$로 선백화")
a2.plot(rhos, fpr_true, "^-", color=C["purple"], ms=3.5, lw=1.0, label="참 $\\rho$로 선백화")
a2.set_xlabel("잡음의 AR(1) 계수 $\\rho$")
a2.set_ylabel("거짓 양성률 ($p$ < 0.05)")
a2.set_ylim(0, 0.25)
a2.set_title("(나) 효과가 없을 때 '유의'로 나온 비율", fontsize=9.5)
a2.legend(fontsize=7.8, loc="upper left")
save(fig, __file__)
print("fpr ols", np.round(fpr_ols, 3), "est", np.round(fpr_est, 3), "true", np.round(fpr_true, 3))
print("acf0", ac0.round(2), "acf1", ac1.round(2), "sd", sd0, sd1, "rhat", rh_mean)
