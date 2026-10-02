import math

from figstyle import plt, np, save, C

# 가상의 한 슬라이스(48 × 48 복셀)에서 복셀마다 GLM을 맞추고 대비 두 개의 t 지도를 그린다.
dt, TR, N = 0.1, 2.0, 200
T = N * TR
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6
rng = np.random.default_rng(6)
t = np.arange(0, T, dt)
onsA, onsB, o, k = [], [], 10.0, 0
while o < T - 30:
    (onsA if k % 2 == 0 else onsB).append(o)
    o += 16 + rng.uniform(10, 18)
    k += 1


def reg(ons):
    s = np.zeros_like(t)
    for on in ons:
        s[(t >= on) & (t < on + 16)] = 1
    return (np.convolve(s, h)[: len(t)] * dt)[:: int(TR / dt)]


xa, xb = reg(onsA), reg(onsB)
sc = xa.max()
xa, xb = xa / sc, xb / sc
n = np.arange(N)
dct = np.array([np.cos(np.pi * kk * (2 * n + 1) / (2 * N)) for kk in range(1, 7)]).T
X = np.column_stack([xa, xb, dct, np.ones(N)])

S = 48
yy, xx = np.mgrid[0:S, 0:S]
blob = lambda cx, cy, r: np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r ** 2))
r1, r2, r3 = blob(14, 30, 3.2), blob(34, 30, 3.2), blob(24, 13, 4.0)
# 영역 1: A를 선호, 영역 2: B를 선호, 영역 3: 둘 다 같은 크기
bA = 1.2 * r1 + 0.3 * r2 + 0.8 * r3
bB = 0.4 * r1 + 1.0 * r2 + 0.8 * r3
B = np.zeros((X.shape[1], S * S))
B[0], B[1], B[-1] = bA.ravel() * 10, bB.ravel() * 10, 1000
Y = X @ B + rng.normal(0, 6, (N, S * S))
bh = np.linalg.lstsq(X, Y, rcond=None)[0]
E = Y - X @ bh
df = N - X.shape[1]
s2 = (E ** 2).sum(0) / df
XtXi = np.linalg.inv(X.T @ X)


def tmap(c):
    c = np.r_[c, np.zeros(X.shape[1] - len(c))]
    return ((c @ bh) / np.sqrt(s2 * (c @ XtXi @ c))).reshape(S, S)


t_sum = tmap([0.5, 0.5])
t_dif = tmap([1, -1])

fig = plt.figure(figsize=(7.3, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[0.8, 1, 1], wspace=0.15)
a0 = fig.add_subplot(gs[0])
a0.axis("off")
a0.set_xlim(0, 1)
a0.set_ylim(0, 1)
a0.set_title("(가) 대비 벡터 $c$", fontsize=9.5)
rows = [("A > 기저", [1, 0]), ("두 조건 평균", [0.5, 0.5]), ("A > B", [1, -1])]
for i, (name, cv) in enumerate(rows):
    yv = 0.78 - i * 0.3
    a0.text(0.0, yv, name, fontsize=8.5, va="center")
    for j, v in enumerate(cv):
        col = C["blue"] if v > 0 else (C["red"] if v < 0 else "white")
        a0.add_patch(plt.Rectangle((0.55 + j * 0.2, yv - 0.08), 0.18, 0.16, fc=col,
                                   alpha=0.25 + 0.6 * abs(v), ec=C["gray"], lw=0.6))
        a0.text(0.64 + j * 0.2, yv, f"{v:g}", ha="center", va="center", fontsize=8)
for j, lab in enumerate(["A", "B"]):
    a0.text(0.64 + j * 0.2, 0.96, lab, ha="center", va="center", fontsize=8.5, color=C["gray"])
a0.text(0.0, 0.05, "잡음 회귀자 자리는 모두 0", fontsize=7.5, color=C["gray"])

lim = 12
for gi, (tm, title) in enumerate([(t_sum, "(나) 두 조건 평균의 $t$"), (t_dif, "(다) A − B의 $t$")]):
    a = fig.add_subplot(gs[gi + 1])
    im = a.imshow(tm, cmap="RdBu", vmin=-lim, vmax=lim, origin="lower")
    a.contour(np.abs(tm), levels=[3.34], colors=C["ink"], linewidths=0.6)
    a.set_xticks([])
    a.set_yticks([])
    a.set_title(title, fontsize=9.5)
    for (cx, cy, lab) in ((14, 30, "1"), (34, 30, "2"), (24, 13, "3")):
        a.text(cx - 7.5, cy + 4.5, lab, ha="center", fontsize=8.5, color=C["ink"])
cb = fig.colorbar(im, ax=fig.axes[1:], shrink=0.8, pad=0.03)
cb.set_label("$t$", fontsize=9, rotation=0, labelpad=8)
save(fig, __file__)
for nm, tm in (("sum", t_sum), ("dif", t_dif)):
    print(nm, [round(float(tm[cy, cx]), 1) for cx, cy in ((14, 30), (34, 30), (24, 13))])
