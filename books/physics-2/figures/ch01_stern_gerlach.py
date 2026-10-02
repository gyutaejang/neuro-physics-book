from figstyle import plt, np, save, C
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch

# 슈테른-게를라흐 실험. 은 원자 빔이 불균일한 자기장을 지나 스크린에 닿는다.
# 고전적으로 자석의 방향이 무작위라면 z 성분이 -μ..+μ에 고르게 퍼져 띠가 생긴다.
# 실제로는 두 점으로만 갈라진다. 원자 2만 개를 모의 실험했다.
rng = np.random.default_rng(3)
N = 20000
width = 0.08
cl = rng.uniform(-1, 1, N) + rng.normal(0, width, N)    # 고전: 무작위 방향의 z 성분
qu = rng.choice([-1, 1], N) + rng.normal(0, width, N)    # 양자: ±1 두 값

fig = plt.figure(figsize=(7.3, 3.2))
ax = fig.add_axes([0.0, 0.08, 0.5, 0.84])
ax.set_xlim(0, 10)
ax.set_ylim(-3, 3)
ax.axis("off")
ax.add_patch(FancyBboxPatch((0.2, -0.6), 1.3, 1.2, boxstyle="round,pad=0.05", color=C["gray"], alpha=0.5))
ax.text(0.85, -0.85, "은 원자\n가열로", ha="center", va="top", fontsize=8)
ax.plot([1.5, 4.0], [0, 0], color=C["blue"], lw=2)
# 자석: 위 N(뾰족), 아래 S(홈)
ax.add_patch(Polygon([[3.8, 2.4], [6.2, 2.4], [6.2, 0.9], [5.0, 0.45], [3.8, 0.9]], color=C["red"], alpha=0.85))
ax.add_patch(Polygon([[3.8, -2.4], [6.2, -2.4], [6.2, -0.8], [5.6, -0.8], [5.6, -1.2], [4.4, -1.2], [4.4, -0.8], [3.8, -0.8]],
                     color=C["blue"], alpha=0.85))
ax.text(5.0, 1.75, "N", color="white", ha="center", va="center", fontsize=12)
ax.text(5.0, -1.9, "S", color="white", ha="center", va="center", fontsize=12)
ax.plot([4.0, 6.0], [0, 0], color=C["blue"], lw=2, alpha=0.5)
for dy in (1, -1):
    ax.plot([6.0, 8.6], [0, dy * 1.5], color=C["purple"], lw=1.6)
ax.add_patch(Rectangle((8.6, -2.3), 0.25, 4.6, color=C["ink"], alpha=0.25))
ax.text(8.75, 2.55, "스크린", ha="center", fontsize=8)
ax.text(5.0, 2.65, "불균일한 자기장", ha="center", fontsize=8, color=C["purple"])
ax.set_title("(가) 실험 장치", fontsize=10.5)

bx = fig.add_axes([0.6, 0.17, 0.38, 0.72])
bins = np.linspace(-1.6, 1.6, 81)
bx.hist(cl, bins=bins, orientation="horizontal", color=C["gray"], alpha=0.55, label="고전적 예상")
bx.hist(qu, bins=bins, orientation="horizontal", histtype="step", color=C["purple"], lw=1.6, label="실제 (스핀 ½)")
bx.set_ylabel("스크린 위 위치 (위·아래)")
bx.set_xlabel("원자 수")
bx.set_yticks([-1, 0, 1])
bx.set_yticklabels(["−", "0", "+"])
bx.legend(fontsize=8, loc="center right", bbox_to_anchor=(1.02, 0.5))
bx.set_title("(나) 스크린에 닿은 원자 2만 개", fontsize=10.5)
save(fig, __file__)
