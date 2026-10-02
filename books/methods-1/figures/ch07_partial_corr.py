"""상관과 부분 상관: 간접 경로가 만드는 가짜 연결."""
import sys

from scipy import signal

from figstyle import plt, np, save, C

rng = np.random.default_rng(4)
T = 1200  # 볼륨 수 (TR 0.72 s 기준 약 14분)
names = ["A", "B", "C", "D", "E", "F"]
n = rng.standard_normal((T, 6))
x = np.zeros((T, 6))
x[:, 0] = n[:, 0]
x[:, 1] = 0.7 * x[:, 0] + n[:, 1]          # A -> B
x[:, 2] = 0.7 * x[:, 1] + n[:, 2]          # B -> C (A-C는 간접)
x[:, 3] = n[:, 3]
x[:, 4] = 0.7 * x[:, 3] + n[:, 4]          # D -> E
x[:, 5] = 0.7 * x[:, 3] + n[:, 5]          # D -> F (E-F는 공통 입력)
b, a = signal.butter(2, [0.01, 0.1], btype="band", fs=1 / 0.72)
x = signal.filtfilt(b, a, x, axis=0)       # 모든 노드에 같은 대역 통과

R = np.corrcoef(x.T)
P = np.linalg.inv(R)
d = np.sqrt(np.diag(P))
PC = -P / np.outer(d, d)
np.fill_diagonal(PC, 1)
print(f"r(A,C)={R[0,2]:.2f} pr(A,C)={PC[0,2]:.2f} r(E,F)={R[4,5]:.2f} pr(E,F)={PC[4,5]:.2f} "
      f"r(A,B)={R[0,1]:.2f} pr(A,B)={PC[0,1]:.2f}", file=sys.stderr)

fig = plt.figure(figsize=(7.3, 2.9))
gs = fig.add_gridspec(1, 3, width_ratios=[0.9, 1, 1.18], wspace=0.35)

# (가) 참 구조
a0 = fig.add_subplot(gs[0])
pos = {"A": (0, 2), "B": (0, 1), "C": (0, 0), "D": (1.6, 2), "E": (1.1, 0.6), "F": (2.1, 0.6)}
for u, v in [("A", "B"), ("B", "C"), ("D", "E"), ("D", "F")]:
    a0.annotate("", xy=pos[v], xytext=pos[u],
                arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.4,
                                shrinkA=11, shrinkB=11, mutation_scale=10))
for u, v in [("A", "C"), ("E", "F")]:
    p, q = np.array(pos[u]), np.array(pos[v])
    rad = 0.55 if u == "A" else 0.0
    a0.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-", color=C["red"], lw=1, ls="--",
                                shrinkA=11, shrinkB=11, connectionstyle=f"arc3,rad={rad}"))
for k, (px, py) in pos.items():
    a0.scatter([px], [py], s=330, color="white", edgecolor=C["ink"], zorder=3, lw=1)
    a0.text(px, py, k, ha="center", va="center", fontsize=10, zorder=4)
a0.text(-0.98, 1.0, "간접", color=C["red"], fontsize=8, ha="center", rotation=90, va="center")
a0.text(1.6, 0.25, "공통 입력", color=C["red"], fontsize=8, ha="center")
a0.set_xlim(-1.15, 2.5)
a0.set_ylim(-0.3, 2.35)
a0.axis("off")
a0.set_title("(가) 참 구조", fontsize=9.5)


def mat(ax, M, title):
    M = M.copy()
    np.fill_diagonal(M, np.nan)
    im = ax.imshow(M, cmap="RdBu_r", vmin=-0.7, vmax=0.7)
    ax.set_xticks(range(6))
    ax.set_yticks(range(6))
    ax.set_xticklabels(names, fontsize=8.5)
    ax.set_yticklabels(names, fontsize=8.5)
    for i in range(6):
        for j in range(6):
            if i != j:
                v = M[i, j]
                ax.text(j, i, f"{v:.2f}".replace("-0.00", "0.00").replace("0.", "."),
                        ha="center", va="center", fontsize=6.8,
                        color="white" if abs(v) > 0.45 else C["ink"])
    for (i, j) in [(0, 2), (4, 5)]:
        for (p, q) in [(i, j), (j, i)]:
            ax.add_patch(plt.Rectangle((q - 0.5, p - 0.5), 1, 1, fill=False, ec=C["red"], lw=1.4))
    ax.set_title(title, fontsize=9.5)
    for s in ax.spines.values():
        s.set_visible(False)
    return im


a1 = fig.add_subplot(gs[1])
mat(a1, R, "(나) 상관 $r$")
a2 = fig.add_subplot(gs[2])
im = mat(a2, PC, "(다) 부분 상관")
cb = fig.colorbar(im, ax=a2, fraction=0.046, pad=0.04)
cb.ax.tick_params(labelsize=7.5)
save(fig, __file__)
