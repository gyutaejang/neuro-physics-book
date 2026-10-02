"""문턱과 밀도: 그래프 지표가 밀도에 끌려간다."""
import sys

from scipy import signal
from scipy.sparse.csgraph import shortest_path

from figstyle import plt, np, save, C

rng = np.random.default_rng(11)
n_mod, per = 4, 12
n = n_mod * per
lab = np.repeat(np.arange(n_mod), per)
b, a = signal.butter(2, [0.01, 0.1], btype="band", fs=0.5)


load = rng.uniform(0.5, 1.0, n)                     # 노드마다 다른 모듈 소속 세기
conn = np.array([i * per + j for i in range(n_mod) for j in (0, 1)])  # 모듈마다 연결 노드 2개


def subject_corr(noise_sd, T=300):
    """모듈 4개짜리 합성 네트워크의 상관 행렬 (TR 2 s, 10분)."""
    g = rng.standard_normal((T, 1))
    m0 = rng.standard_normal((T, n_mod))
    m = m0 + 0.4 * np.roll(m0, 1, axis=1)          # 이웃 모듈끼리 약하게 상관
    e = rng.standard_normal((T, n))
    x = 0.3 * g + load * m[:, lab] + noise_sd * e
    x[:, conn] += 0.6 * m[:, (lab[conn] + 1) % n_mod]  # 연결 노드는 옆 모듈에도 속한다
    x = signal.filtfilt(b, a, x, axis=0)
    R = np.corrcoef(x.T)
    np.fill_diagonal(R, 0)
    return R


def binarize_density(R, d):
    iu = np.triu_indices(n, 1)
    k = int(round(d * len(iu[0])))
    thr = np.sort(R[iu])[::-1][k - 1]
    A = (R >= thr).astype(float)
    np.fill_diagonal(A, 0)
    return A


def clustering(A):
    k = A.sum(1)
    t = np.diag(A @ A @ A) / 2
    c = np.where(k > 1, 2 * t / np.maximum(k * (k - 1), 1), 0)
    return c.mean()


def path_length(A):
    """전역 효율: 1/거리의 평균. 끊어진 쌍은 0으로 센다."""
    D = shortest_path(A, unweighted=True, directed=False)
    iu = np.triu_indices(n, 1)
    return (1 / D[iu]).mean()


def random_graph(m):
    iu = np.triu_indices(n, 1)
    A = np.zeros((n, n))
    sel = rng.choice(len(iu[0]), m, replace=False)
    A[iu[0][sel], iu[1][sel]] = 1
    return A + A.T


dens = np.arange(0.05, 0.51, 0.025)
R0 = subject_corr(1.0)
Cb, Lb, Cr, Lr = [], [], [], []
for d in dens:
    A = binarize_density(R0, d)
    Cb.append(clustering(A))
    Lb.append(path_length(A))
    m = int(A.sum() / 2)
    rr = [random_graph(m) for _ in range(20)]
    Cr.append(np.mean([clustering(x) for x in rr]))
    Lr.append(np.mean([path_length(x) for x in rr]))
Cb, Lb, Cr, Lr = map(np.array, (Cb, Lb, Cr, Lr))
for d0 in (0.1, 0.3):
    i = np.argmin(abs(dens - d0))
    print(f"d={d0}: C={Cb[i]:.2f} Crand={Cr[i]:.2f} E={Lb[i]:.2f} Erand={Lr[i]:.2f}", file=sys.stderr)

# 두 집단: 연결 구조는 같고 잡음만 다르다
grp = {"집단 1": 1.0, "집단 2": 1.4}
res = {}
for gname, sd in grp.items():
    rows = []
    for s in range(20):
        R = subject_corr(sd)
        iu = np.triu_indices(n, 1)
        A_abs = (R > 0.3).astype(float)
        dd = A_abs[iu].mean()
        A_den = binarize_density(R, 0.15)
        rows.append((dd, clustering(A_abs), path_length(A_abs), clustering(A_den), path_length(A_den),
                     R[iu].mean()))
    res[gname] = np.array(rows)
    mu = res[gname].mean(0)
    print(gname, "density@r>.3 %.3f C %.3f E %.3f | C@15%% %.3f E %.3f | mean r %.3f" % tuple(mu),
          file=sys.stderr)

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.4), gridspec_kw=dict(wspace=0.45))
ax = axes[0]
ax.plot(dens * 100, Cb, color=C["blue"], lw=1.8, label="합성 뇌 네트워크")
ax.plot(dens * 100, Cr, color=C["gray"], lw=1.4, ls="--", label="같은 밀도의 무작위")
ax.set_xlabel("밀도 (%)")
ax.set_ylabel("군집 계수 $C$")
ax.set_title("(가) 군집 계수", fontsize=9.5)
ax.set_ylim(0, 1.15)
ax.legend(fontsize=7.5, loc="upper left")

ax = axes[1]
ax.plot(dens * 100, Lb, color=C["blue"], lw=1.8)
ax.plot(dens * 100, Lr, color=C["gray"], lw=1.4, ls="--")
ax.set_xlabel("밀도 (%)")
ax.set_ylabel("전역 효율 $E$")
ax.set_title("(나) 전역 효율", fontsize=9.5)
ax.set_ylim(0, 1)

ax = axes[2]
m1, m2 = res["집단 1"].mean(0), res["집단 2"].mean(0)
s1, s2 = res["집단 1"].std(0) / np.sqrt(20), res["집단 2"].std(0) / np.sqrt(20)
xs = np.array([0, 1])
w = 0.36
ax.bar(xs - w / 2, [m1[1], m1[3]], w, yerr=[s1[1], s1[3]], color=C["blue"], label="집단 1 (잡음 작음)",
       error_kw=dict(lw=0.8, capsize=2))
ax.bar(xs + w / 2, [m2[1], m2[3]], w, yerr=[s2[1], s2[3]], color=C["red"], label="집단 2 (잡음 큼)",
       error_kw=dict(lw=0.8, capsize=2))
ax.set_xticks(xs)
ax.set_xticklabels(["$r$ > 0.3 문턱", "밀도 15 %"], fontsize=8.5)
ax.set_ylabel("군집 계수 $C$")
ax.set_ylim(0, 1.25)
ax.set_title("(다) 문턱 방식과 집단 차이", fontsize=9.5)
ax.text(0.05, m1[1] + 0.04, f"밀도\n{m1[0]*100:.0f} % 대 {m2[0]*100:.0f} %", ha="center", va="bottom",
        fontsize=7.5, color=C["ink"])
ax.legend(fontsize=7.2, loc="upper center", ncol=1, bbox_to_anchor=(0.5, 1.02))
save(fig, __file__)
