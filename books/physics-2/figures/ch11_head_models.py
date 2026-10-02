from figstyle import plt, np, save, C
from matplotlib.patches import Circle, FancyArrowPatch
import matplotlib.tri as mtri

# 머리 모형 세 가지: (가) 동심 구 3겹, (나) 경계 요소(BEM): 실제 모양의 경계면,
# (다) 유한 요소(FEM): 부피를 작은 삼각형(3차원에서는 사면체)으로 나눔.
fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.75))

# (가) 동심 구
ax = axes[0]
layers = [(9.2, "#f3e3d3", "두피  0.43 S/m"), (8.6, "#d9d9d9", "두개골  0.01 S/m"),
          (8.0, C["light"], "뇌  0.33 S/m")]
for r, col, _ in layers:
    ax.add_patch(Circle((0, 0), r, fc=col, ec=C["ink"], lw=0.7))
ax.annotate("", xy=(0, 5.0), xytext=(0, 2.6),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=2.0))
# 체적 전류: 쌍극자 머리(+)에서 나와 바깥으로 돌아 꼬리(−)로 돌아오는 고리
t = np.linspace(0.12, 0.88, 80) * np.pi
for s in (1, -1):
    for a, bb in ((2.2, 1.9), (4.0, 3.2)):
        xx = s * a * np.sin(t)
        yy = 3.8 + bb * np.cos(t)
        ax.plot(xx, yy, color=C["blue"], lw=0.8)
        k = len(t) // 2
        ax.annotate("", xy=(xx[k + 2], yy[k + 2]), xytext=(xx[k], yy[k]),
                    arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=0.8))
ax.text(4.3, -0.2, "체적 전류", fontsize=8, color=C["blue"], ha="center")
ax.text(0, 1.5, "쌍극자", fontsize=8, color=C["red"], ha="center", va="top")
ax.text(0, -3.2, "뇌·뇌척수액\n0.33 S/m", ha="center", fontsize=8)
ax.annotate("두개골 0.01 S/m", xy=(-6.0, -6.0), xytext=(-9.6, -11.2), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.annotate("두피 0.43 S/m", xy=(6.5, -6.5), xytext=(3.2, -11.2), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.set_xlim(-10.2, 10.2)
ax.set_ylim(-11.8, 10)
ax.set_title("(가) 동심 구 3겹", fontsize=10)

# 실제 머리 모양 비슷한 윤곽: 반지름이 각도에 따라 조금씩 변하는 닫힌 곡선
def outline(r0, n=400, phase=0.0):
    t = np.linspace(0, 2 * np.pi, n)
    r = r0 * (1 + 0.07 * np.cos(2 * t) + 0.04 * np.sin(3 * t + phase) + 0.02 * np.cos(5 * t))
    return r * np.cos(t) * 0.92, r * np.sin(t)

# (나) BEM: 경계면만 점(절점)과 선분으로 나눈다
ax = axes[1]
for r0, col, nn in ((9.2, "#c9a27e", 46), (8.6, C["gray"], 42), (8.0, C["blue"], 38)):
    x, y = outline(r0)
    ax.plot(x, y, color=col, lw=0.6, alpha=0.5)
    xv, yv = outline(r0, nn + 1)
    ax.plot(xv, yv, "-", color=col, lw=0.9)
    ax.plot(xv[:-1], yv[:-1], "o", ms=2.2, color=col)
ax.text(0, 0.3, "경계면 안쪽은\n전도율 하나", ha="center", fontsize=8)
ax.text(0, -11.2, "면 3개를 삼각형으로 나눈다", ha="center", fontsize=8)
ax.set_xlim(-10.2, 10.2)
ax.set_ylim(-11.8, 10)
ax.set_title("(나) 경계 요소법(BEM)", fontsize=10)

# (다) FEM: 부피 전체를 삼각형으로 나누고 요소마다 전도율을 준다
ax = axes[2]
g = np.linspace(-10, 10, 37)
GX, GY = np.meshgrid(g, g)
rng = np.random.default_rng(2)
px = GX.ravel() + rng.uniform(-0.12, 0.12, GX.size)
py = GY.ravel() + rng.uniform(-0.12, 0.12, GX.size)
tri = mtri.Triangulation(px, py)
cx, cy = px[tri.triangles].mean(1), py[tri.triangles].mean(1)
th = np.arctan2(cy, cx / 0.92)
rr = np.hypot(cx / 0.92, cy)
shape = 1 + 0.07 * np.cos(2 * th) + 0.04 * np.sin(3 * th) + 0.02 * np.cos(5 * th)
rn = rr / shape
cols = np.full(len(cx), -1)
cols[rn < 9.2] = 0
cols[rn < 8.6] = 1
cols[rn < 8.0] = 2
cols[rn < 7.2] = 3          # 회백질 바깥 띠 안쪽은 백질
cols[(rn < 3.0)] = 4        # 가운데 뇌실(모식)
mask = cols < 0
tri.set_mask(mask)
palette = ["#f3e3d3", "#bdbdbd", "#9fd3e6", "#c9d8ec", "#9fd3e6"]
facec = np.array([palette[c] if c >= 0 else "#ffffff" for c in cols])
ax.tripcolor(tri, facecolors=np.arange(len(cx)), cmap=None, alpha=0)  # 자리 잡기
from matplotlib.collections import PolyCollection
polys = [np.c_[px[t], py[t]] for t, m in zip(tri.triangles, mask) if not m]
ax.add_collection(PolyCollection(polys, facecolors=facec[~mask], edgecolors="white", linewidths=0.35))
ax.text(0, -11.2, "요소마다 전도율 (비등방도 가능)", ha="center", fontsize=8)
ax.text(0, 0, "뇌실", ha="center", va="center", fontsize=7.5)
ax.set_xlim(-10.2, 10.2)
ax.set_ylim(-11.8, 10)
ax.set_title("(다) 유한 요소법(FEM)", fontsize=10)

for ax in axes:
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout(w_pad=0.6)
save(fig, __file__)
