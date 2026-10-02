import math

from figstyle import plt, np, save, C

# 설계 효율 = 1 / (c (X^T X)^-1 c^T). 400 s, TR 2 s, 시행은 모두 1 s짜리 자극.
dt, TR, N = 0.1, 2.0, 200
T = N * TR
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6
t = np.arange(0, T, dt)
n = np.arange(N)
dct = np.array([np.cos(np.pi * k * (2 * n + 1) / (2 * N)) for k in range(1, 7)]).T


def reg(ons):
    s = np.zeros_like(t)
    for o in ons:
        s[(t >= o) & (t < o + 1)] = 1
    return (np.convolve(s, h)[: len(t)] * dt)[:: int(TR / dt)]


def eff(cols, c):
    X = np.column_stack(cols + [dct, np.ones(N)])
    c = np.r_[c, np.zeros(X.shape[1] - len(c))]
    return 1 / (c @ np.linalg.pinv(X.T @ X) @ c)


def designs(seed):
    r = np.random.default_rng(seed)
    d = {}
    d["블록\n20 s/20 s"] = np.array([o + k * 2 for o in np.arange(0, T, 40) for k in range(10)])
    d["느린 사건\nSOA 16 s"] = np.arange(2, T - 20, 16.0)
    d["빠른 고정\nSOA 4 s"] = np.arange(2, T - 20, 4.0)
    o = np.cumsum(2 + r.exponential(2.5, 400))
    d["지터\nSOA 평균 4.5 s"] = o[o < T - 20]
    grid = np.arange(2, T - 20, 2.0)
    d["널 사건\n2 s 격자의 절반"] = grid[r.random(len(grid)) < 0.5]
    return d


names = list(designs(0).keys())
E1 = {k: [] for k in names}
E2 = {k: [] for k in names}
for seed in range(100):
    r = np.random.default_rng(1000 + seed)
    for k, ons in designs(seed).items():
        E1[k].append(eff([reg(ons)], [1]))
        if k.startswith("블록"):
            A = np.array([o + j * 2 for o in np.arange(0, T, 80) for j in range(10)])
            B = A + 40
        else:
            typ = r.random(len(ons)) < 0.5
            A, B = ons[typ], ons[~typ]
        E2[k].append(eff([reg(A), reg(B)], [1, -1]))
e1 = np.array([np.mean(E1[k]) for k in names])
e2 = np.array([np.mean(E2[k]) for k in names])
rel1, rel2 = 100 * e1 / e1[0], 100 * e2 / e2[0]

fig = plt.figure(figsize=(7.3, 3.15))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1], wspace=0.32)
gl = gs[0].subgridspec(len(names), 1, hspace=0.25)
show = designs(0)
for i, k in enumerate(names):
    a = fig.add_subplot(gl[i])
    ons = show[k]
    x = reg(ons)
    a.vlines(ons[ons < 120], 0, 0.25, color=C["gray"], lw=0.7)
    a.plot(n * TR, x / reg(designs(0)[names[0]]).max() * 0.95 + 0.0, color=C["blue"], lw=1.4)
    a.set_xlim(0, 120)
    a.set_ylim(-0.1, 1.05)
    a.set_yticks([])
    a.spines["left"].set_visible(False)
    a.text(-6, 0.45, k, ha="right", va="center", fontsize=7.6)
    if i < len(names) - 1:
        a.set_xticklabels([])
    else:
        a.set_xlabel("시간 (s), 처음 120 s")
    if i == 0:
        a.set_title("(가) 자극 시점(회색)과 예측 BOLD(파랑)", fontsize=9.5, loc="left")

a2 = fig.add_subplot(gs[1])
yv = np.arange(len(names))[::-1]
a2.barh(yv + 0.18, rel1, height=0.34, color=C["blue"], label="A − 기저")
a2.barh(yv - 0.18, rel2, height=0.34, color=C["red"], label="A − B (무작위 순서)")
for y0, v1, v2 in zip(yv, rel1, rel2):
    a2.text(v1 + 1.5, y0 + 0.18, f"{v1:.0f}", va="center", fontsize=7.5)
    a2.text(v2 + 1.5, y0 - 0.18, f"{v2:.0f}", va="center", fontsize=7.5)
a2.set_yticks(yv)
a2.set_yticklabels([k.split("\n")[0] for k in names], fontsize=8)
a2.set_xlim(0, 118)
a2.set_xlabel("상대 효율 (블록 = 100)")
a2.set_title("(나) 대비별 설계 효율", fontsize=9.5)
a2.legend(fontsize=7.6, loc="lower right")
save(fig, __file__)
print("ntrials", [len(v) for v in designs(0).values()])
print("e1", e1.round(2), rel1.round(1))
print("e2", e2.round(2), rel2.round(1))
