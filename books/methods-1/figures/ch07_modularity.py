"""모듈성: 순서를 섞은 행렬에서 모듈을 찾고, 무작위 그래프의 Q와 비교한다."""
import sys

from scipy import signal

from figstyle import plt, np, save, C

rng = np.random.default_rng(5)
n_mod, per = 4, 12
n = n_mod * per
lab = np.repeat(np.arange(n_mod), per)
load = rng.uniform(0.5, 1.0, n)
conn = np.array([i * per + j for i in range(n_mod) for j in (0, 1)])
b, a = signal.butter(2, [0.01, 0.1], btype="band", fs=0.5)

T = 300
m0 = rng.standard_normal((T, n_mod))
m = m0 + 0.4 * np.roll(m0, 1, axis=1)
x = 0.3 * rng.standard_normal((T, 1)) + load * m[:, lab] + rng.standard_normal((T, n))
x[:, conn] += 0.6 * m[:, (lab[conn] + 1) % n_mod]
x = signal.filtfilt(b, a, x, axis=0)
R = np.corrcoef(x.T)
np.fill_diagonal(R, 0)

iu = np.triu_indices(n, 1)
dens = 0.15
k_e = int(round(dens * len(iu[0])))
thr = np.sort(R[iu])[::-1][k_e - 1]
A = (R >= thr).astype(float)
np.fill_diagonal(A, 0)


def Q_of(A, c):
    k = A.sum(1)
    m2 = k.sum()
    B = A - np.outer(k, k) / m2
    return (B * (c[:, None] == c[None, :])).sum() / m2


def detect(A):
    """뉴먼의 고유벡터 이분할을 되풀이한 뒤, 노드를 하나씩 옮겨 Q를 다듬는다."""
    k = A.sum(1)
    m2 = k.sum()
    B = A - np.outer(k, k) / m2
    c = np.zeros(len(A), int)
    queue = [np.arange(len(A))]
    nxt = 1
    while queue:
        g = queue.pop()
        Bg = B[np.ix_(g, g)] - np.diag(B[np.ix_(g, g)].sum(1))
        w, v = np.linalg.eigh(Bg)
        if w[-1] < 1e-8:
            continue
        s = np.where(v[:, -1] >= 0, 1, -1)
        if s @ Bg @ s <= 1e-8 or abs(s.sum()) == len(s):
            continue
        g1, g2 = g[s > 0], g[s < 0]
        c[g2] = nxt
        nxt += 1
        queue += [g1, g2]
    improved = True
    while improved:
        improved = False
        for i in range(len(A)):
            best, bq = c[i], Q_of(A, c)
            for cc in np.unique(c):
                if cc == c[i]:
                    continue
                old = c[i]
                c[i] = cc
                q = Q_of(A, c)
                c[i] = old
                if q > bq + 1e-12:
                    best, bq = cc, q
            if best != c[i]:
                c[i] = best
                improved = True
    _, c = np.unique(c, return_inverse=True)
    return c


perm = rng.permutation(n)
Ap = A[np.ix_(perm, perm)]
c_det = detect(Ap)
Qb = Q_of(Ap, c_det)
# 참 모듈과의 일치: 같은 모듈 쌍 판정이 맞은 비율 (Rand 지수)
tl = lab[perm]
same_t = tl[:, None] == tl[None, :]
same_d = c_det[:, None] == c_det[None, :]
rand_idx = (same_t == same_d)[np.triu_indices(n, 1)].mean()
Q_true = Q_of(Ap, tl)

Qr = []
for _ in range(100):
    Ar = np.zeros((n, n))
    sel = rng.choice(len(iu[0]), k_e, replace=False)
    Ar[iu[0][sel], iu[1][sel]] = 1
    Ar = Ar + Ar.T
    Qr.append(Q_of(Ar, detect(Ar)))
Qr = np.array(Qr)
print(f"Q={Qb:.3f} Qtrue={Q_true:.3f} modules={c_det.max()+1} rand={rand_idx:.3f} "
      f"Qrand={Qr.mean():.3f}+-{Qr.std():.3f} max {Qr.max():.3f}", file=sys.stderr)

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.75), gridspec_kw=dict(width_ratios=[1, 1, 1.05], wspace=0.3))
ax = axes[0]
ax.imshow(Ap, cmap="Greys", interpolation="nearest")
ax.set_title("(가) 순서를 섞은 인접 행렬", fontsize=9.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("노드", fontsize=9)

ax = axes[1]
order = np.lexsort((tl, c_det))
ax.imshow(Ap[np.ix_(order, order)], cmap="Greys", interpolation="nearest")
cs = c_det[order]
start = 0
for cc in np.unique(cs):
    sz = (cs == cc).sum()
    ax.add_patch(plt.Rectangle((start - 0.5, start - 0.5), sz, sz, fill=False, ec=C["red"], lw=1.3))
    start += sz
ax.set_title("(나) 찾은 모듈로 다시 정렬", fontsize=9.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel(f"$Q$ = {Qb:.2f}, 모듈 {c_det.max()+1}개", fontsize=9)

ax = axes[2]
ax.hist(Qr, bins=np.arange(0.1, 0.62, 0.0125), color=C["gray"], alpha=0.8, label="무작위 그래프 100개")
ax.axvline(Qb, color=C["red"], lw=1.6)
ax.set_ylim(0, ax.get_ylim()[1] * 1.3)
ax.text(Qb - 0.025, ax.get_ylim()[1] * 0.8, "합성 뇌\n네트워크", color=C["red"], fontsize=8,
        ha="right", va="top")
ax.set_xlabel("모듈성 $Q$")
ax.set_ylabel("개수")
ax.set_xlim(0.1, 0.6)
ax.set_title("(다) 무작위 그래프도 $Q$ > 0", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper left")
save(fig, __file__)
