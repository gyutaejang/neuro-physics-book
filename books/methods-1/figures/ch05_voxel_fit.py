import math

from figstyle import plt, np, save, C

# 두 조건(A, B) 블록 설계 + 시간 미분 + 움직임 6 + 표류(DCT, 128 s) + 상수 = 17열.
dt, TR, N = 0.1, 2.0, 200
T = N * TR
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6
hd = np.gradient(h, dt)
rng = np.random.default_rng(6)

t = np.arange(0, T, dt)
onsA, onsB, o, k = [], [], 10.0, 0
while o < T - 30:
    (onsA if k % 2 == 0 else onsB).append(o)
    o += 16 + rng.uniform(10, 18)
    k += 1


def reg(ons, kern):
    s = np.zeros_like(t)
    for on in ons:
        s[(t >= on) & (t < on + 16)] = 1
    x = np.convolve(s, kern)[: len(t)] * dt
    return x[:: int(TR / dt)]


xa, xb = reg(onsA, h), reg(onsB, h)
sc = xa.max()
xa, xb = xa / sc, xb / sc
da, db = reg(onsA, hd), reg(onsB, hd)
da, db = da / np.abs(da).max(), db / np.abs(db).max()
mot = np.cumsum(rng.normal(0, 0.03, (N, 6)), axis=0)
mot -= mot.mean(0)
n = np.arange(N)
K = int(2 * N * TR / 128)
dct = np.array([np.cos(np.pi * kk * (2 * n + 1) / (2 * N)) for kk in range(1, K + 1)]).T
X = np.column_stack([xa, xb, da, db, mot, dct, np.ones(N)])
beta = np.r_[12, 4, 1.5, 0.5, rng.normal(0, 25, 6), 6, -3, 2, 0, 1, 0, 1000]
y = X @ beta + rng.normal(0, 5, N)
bh = np.linalg.lstsq(X, y, rcond=None)[0]
e = y - X @ bh
df = N - X.shape[1]
s2 = e @ e / df
cov = s2 * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(cov))
tcrit = 2.0  # 자유도 183에서 양측 95 %의 t 임계값은 약 1.97

tsec = n * TR
fig = plt.figure(figsize=(7.2, 4.6))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], width_ratios=[2.6, 0.05, 1], hspace=0.55, wspace=0.25)

a1 = fig.add_subplot(gs[0, :])
for on in onsA:
    a1.axvspan(on, on + 16, color=C["blue"], alpha=0.10, lw=0)
for on in onsB:
    a1.axvspan(on, on + 16, color=C["red"], alpha=0.10, lw=0)
a1.plot(tsec, y, color=C["gray"], lw=0.8, label="관측 $y$")
a1.plot(tsec, X @ bh, color=C["ink"], lw=1.4, label="전체 적합 $X\\hat\\beta$")
a1.set_xlim(0, T)
a1.set_ylabel("신호 (임의 단위)")
a1.set_title("(가) 원자료와 전체 모형: 표류와 움직임이 대부분을 차지한다", fontsize=9.5)
a1.legend(fontsize=7.8, loc="lower left", ncol=2)

a2 = fig.add_subplot(gs[1, 0])
nuis = X[:, 2:] @ bh[2:]
yc = y - nuis
for on in onsA:
    a2.axvspan(on, on + 16, color=C["blue"], alpha=0.10, lw=0)
for on in onsB:
    a2.axvspan(on, on + 16, color=C["red"], alpha=0.10, lw=0)
a2.plot(tsec, yc / bh[-1] * 100, color=C["gray"], lw=0.8, label="잡음 회귀자를 뺀 자료")
a2.plot(tsec, (X[:, :2] @ bh[:2]) / bh[-1] * 100, color=C["blue"], lw=1.5, label="A, B 성분")
a2.axhline(0, color=C["gray"], lw=0.5)
a2.set_xlim(0, T)
a2.set_ylim(-1.6, 2.6)
a2.set_xlabel("시간 (s)")
a2.set_ylabel("% 신호 변화")
a2.set_title("(나) 관심 성분만 보기 (파란 띠 A, 빨간 띠 B)", fontsize=9.5)
a2.legend(fontsize=7.5, loc="upper right", ncol=2)

a3 = fig.add_subplot(gs[1, 2])
pct = bh[:2] / bh[-1] * 100
pse = se[:2] / bh[-1] * 100
a3.bar([0, 1], pct, color=[C["blue"], C["red"]], width=0.6, alpha=0.85)
a3.errorbar([0, 1], pct, yerr=tcrit * pse, fmt="none", ecolor=C["ink"], capsize=4, lw=1)
a3.scatter([0, 1], [1.2, 0.4], marker="_", s=260, color=C["ink"], zorder=4, label="참값")
for i in range(2):
    a3.text(i + 0.36, pct[i], f"{pct[i]:.2f}", fontsize=7.5, va="center")
a3.set_xticks([0, 1])
a3.set_xticklabels(["$\\hat\\beta_A$", "$\\hat\\beta_B$"])
a3.set_xlim(-0.6, 1.8)
a3.set_ylim(0, 1.75)
a3.set_ylabel("% 신호 변화")
a3.set_title("(다) 추정값과 95 % 구간", fontsize=9.5)
a3.legend(fontsize=7.5, loc="upper right")
save(fig, __file__)
print("pct", pct, "se", pse, "t", bh[:2] / se[:2], "df", df, "s", np.sqrt(s2))
cvec = np.zeros(17); cvec[0], cvec[1] = 1, -1
print("A-B t", cvec @ bh / np.sqrt(cvec @ cov @ cvec), "diff pct", (pct[0] - pct[1]))
