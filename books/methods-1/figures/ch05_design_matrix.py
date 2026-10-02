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

disp = (X - X.min(0)) / np.where(np.ptp(X, 0) > 0, np.ptp(X, 0), 1)
disp[:, -1] = 0.6

fig = plt.figure(figsize=(7.2, 3.6))
gs = fig.add_gridspec(1, 7, width_ratios=[1.0, 0.25, 4.6, 0.25, 0.42, 0.25, 1.0], wspace=0.08)
tsec = n * TR

ay = fig.add_subplot(gs[0])
ay.plot(y, tsec, color=C["blue"], lw=0.8)
ay.set_ylim(T, 0)
ay.set_xticks([])
ay.set_ylabel("시간 (s)")
ay.set_title("$y$\n복셀 시계열", fontsize=9)
ay.spines["bottom"].set_visible(False)

for i, sym in ((1, "="), (3, "×"), (5, "+")):
    a = fig.add_subplot(gs[i])
    a.axis("off")
    a.text(0.5, 0.5, sym, ha="center", va="center", fontsize=15, color=C["ink"])

ax = fig.add_subplot(gs[2])
ax.imshow(disp, aspect="auto", cmap="gray", interpolation="nearest", extent=(-0.5, 16.5, T, 0))
labels = ["A", "B", "A 미분", "B 미분"] + [f"움직임 {i}" for i in range(1, 7)] + \
         [f"표류 {i}" for i in range(1, K + 1)] + ["상수"]
ax.set_xticks(range(17))
ax.set_xticklabels(labels, rotation=90, fontsize=7.5)
ax.set_yticks([])
ax.set_title("$X$ 설계 행렬 (200 × 17)", fontsize=9)
for xline in (3.5, 9.5, 15.5):
    ax.axvline(xline, color=C["red"], lw=0.8)
for side in ("left", "bottom"):
    ax.spines[side].set_visible(False)

ab = fig.add_subplot(gs[4])
bshow = np.full((17, 1), np.nan)
bshow[:4, 0] = bh[:4] / np.abs(bh[:4]).max()
cm = plt.get_cmap("RdBu_r").copy()
cm.set_bad("#eeeeee")
ab.imshow(np.ma.masked_invalid(bshow), aspect="auto", cmap=cm, vmin=-1, vmax=1, extent=(0, 1, 16.5, -0.5))
ab.set_xticks([])
ab.set_yticks([0, 1])
ab.set_yticklabels([f"{bh[0]:.1f}", f"{bh[1]:.1f}"], fontsize=7)
ab.tick_params(length=0, pad=1)
ab.set_title("$\\hat\\beta$", fontsize=9)
for side in ("left", "bottom"):
    ab.spines[side].set_visible(False)

ae = fig.add_subplot(gs[6])
ae.plot(e, tsec, color=C["gray"], lw=0.8)
ae.set_ylim(T, 0)
ae.set_xlim(-25, 25)
ae.set_xticks([])
ae.set_yticks([])
ae.set_title("$e$\n잔차", fontsize=9)
for side in ("left", "bottom"):
    ae.spines[side].set_visible(False)
save(fig, __file__)
