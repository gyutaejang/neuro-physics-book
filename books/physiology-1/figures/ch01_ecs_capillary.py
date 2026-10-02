from collections import deque

from figstyle import plt, np, save, C
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

rng = np.random.default_rng(2)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4))

# ---- (가) 세포 사이 공간: 세포를 빽빽이 채우고 경계만 남긴다 (2차원 도식) ----
N = 260
gx, gy = np.meshgrid(np.arange(N), np.arange(N))
seeds = []
for i in range(7):
    for j in range(7):
        seeds.append((j * 40 + 20 + (i % 2) * 20 + rng.normal(0, 7), i * 40 + 20 + rng.normal(0, 7)))
seeds = np.array(seeds)
d = np.stack([np.hypot(gx - sx, gy - sy) for sx, sy in seeds])
d.sort(axis=0)
gap = d[1] - d[0]
ecs = gap < 4.4            # 두 세포의 경계 근처 = 세포 사이 공간
frac = ecs.mean()
a1.imshow(np.where(ecs, 0, 1), cmap=ListedColormap(["white", "#dcebd8"]), origin="lower",
          extent=(0, N, 0, N))
a1.contour(gx, gy, ecs.astype(float), levels=[0.5], colors=[C["green"]], linewidths=0.6)

# 왼쪽 가장자리에서 오른쪽 가장자리까지 세포 사이 공간만 따라가는 최단 경로 (BFS)
start_row = 130
starts = [(r, 0) for r in range(N) if ecs[r, 0]]
sr = min(starts, key=lambda p: abs(p[0] - start_row))
prev = {sr: None}
q = deque([sr])
goal = None
while q:
    r, c = q.popleft()
    if c == N - 1:
        goal = (r, c)
        break
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < N and ecs[nr, nc] and (nr, nc) not in prev:
            prev[(nr, nc)] = (r, c)
            q.append((nr, nc))
path = []
p = goal
while p is not None:
    path.append(p)
    p = prev[p]
path = np.array(path[::-1])
a1.plot(path[:, 1], path[:, 0], color=C["red"], lw=1.6)
a1.annotate("", xy=(N - 2, path[-1, 0]), xytext=(N - 12, path[-1, 0]),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4, mutation_scale=10))
a1.text(N / 2, -14, f"세포 사이 공간(흰색) ≈ 부피의 {frac * 100:.0f}%\n분자는 세포를 돌아서 간다 (굴곡도 λ ≈ 1.6)",
        ha="center", va="top", fontsize=8)
a1.set_xlim(0, N)
a1.set_ylim(0, N)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("(가) 세포 사이 공간 (도식)", fontsize=9.5)

# ---- (나) 모세혈관 사이 거리: 피질 단면에서 가장 가까운 모세혈관까지의 거리 ----
L = 300.0   # μm
caps = []
for i in range(6):
    for j in range(6):
        caps.append((j * 50 + 25 + rng.normal(0, 9), i * 50 + 25 + rng.normal(0, 9)))
caps = np.array(caps)
M = 300
ux, uy = np.meshgrid(np.linspace(0, L, M), np.linspace(0, L, M))
dist = np.min(np.stack([np.hypot(ux - cx, uy - cy) for cx, cy in caps]), axis=0)
cmap = LinearSegmentedColormap.from_list("d", ["white", C["blue"]])
im = a2.imshow(dist, origin="lower", extent=(0, L, 0, L), cmap=cmap, vmin=0, vmax=50)
cs = a2.contour(ux, uy, dist, levels=[25], colors=[C["ink"]], linewidths=0.6, linestyles="--")
a2.scatter(caps[:, 0], caps[:, 1], s=18, color=C["red"], zorder=3)
a2.plot([20, 70], [12, 12], color=C["ink"], lw=2)
a2.text(45, 16, "50 μm", ha="center", va="bottom", fontsize=7.5,
        bbox=dict(fc="white", ec="none", pad=0.5))
cb = fig.colorbar(im, ax=a2, fraction=0.046, pad=0.03)
cb.set_label("가장 가까운 모세혈관까지 (μm)", fontsize=8)
cb.ax.tick_params(labelsize=7.5)
a2.text(L / 2, -14, f"빨간 점: 모세혈관 단면 (간격 약 50 μm)\n최대 거리 약 {dist.max():.0f} μm, 평균 약 {dist.mean():.0f} μm",
        ha="center", va="top", fontsize=8)
a2.set_xlim(0, L)
a2.set_ylim(0, L)
a2.axis("off")
a2.set_title("(나) 모세혈관에서 세포까지의 거리", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
