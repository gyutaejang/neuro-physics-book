from figstyle import plt, np, save, C
from matplotlib.patches import FancyArrowPatch, Circle

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[1, 1, 1.3]))


def darrow(ax, p0, p1, col, lw=1.3, ms=9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw))


# (가) 개방장: 나란히 선 피라미드 뉴런
a = axes[0]
for x in np.linspace(-1.2, 1.2, 7):
    a.add_patch(plt.Polygon([[x - 0.1, -0.6], [x + 0.1, -0.6], [x, -0.4]], color=C["green"]))
    a.plot([x, x], [-0.4, 0.8], color=C["green"], lw=1.0)
    darrow(a, (x + 0.17, 0.7), (x + 0.17, -0.5), C["blue"], lw=1.0, ms=7)
darrow(a, (0, -0.9), (0, -1.9), C["blue"], lw=2.6, ms=14)
a.text(0.18, -1.4, "합이 크다", fontsize=8, va="center", color=C["blue"])
a.set_xlim(-1.6, 1.6)
a.set_ylim(-2.1, 1.2)
a.set_aspect("equal")
a.axis("off")
a.set_title("(가) 개방장: 피질 피라미드층", fontsize=9.5)

# (나) 폐쇄장: 수상돌기가 사방으로 뻗은 세포
a = axes[1]
a.add_patch(Circle((0, 0), 0.18, color=C["green"]))
for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
    c, s = np.cos(ang), np.sin(ang)
    a.plot([0.18 * c, 1.0 * c], [0.18 * s, 1.0 * s], color=C["green"], lw=1.0)
    darrow(a, (1.0 * c + 0.12 * -s, 1.0 * s + 0.12 * c), (0.3 * c + 0.12 * -s, 0.3 * s + 0.12 * c),
           C["blue"], lw=0.9, ms=6)
a.text(0, -1.45, "사방의 쌍극자가 서로 지워\n멀리서는 거의 0", fontsize=8, ha="center", va="top")
a.set_xlim(-1.6, 1.6)
a.set_ylim(-2.1, 1.2)
a.set_aspect("equal")
a.axis("off")
a.set_title("(나) 폐쇄장: 별 모양 수상돌기", fontsize=9.5)

# (다) 동기화의 효과: N 대 √N
a = axes[2]
N = np.logspace(0, 8, 100)
a.loglog(N, N, color=C["blue"], lw=1.6, label=r"위상이 맞으면 ∝ $N$")
a.loglog(N, np.sqrt(N), color=C["gray"], lw=1.6, ls="--", label=r"위상이 제각각이면 ∝ $\sqrt{N}$")
# 무작위 위상 합을 실제로 계산해 몇 점 찍는다
rng = np.random.default_rng(0)
for n in (10, 100, 1000, 10000, 100000):
    ph = rng.uniform(0, 2 * np.pi, (40, n))
    r = np.abs(np.exp(1j * ph).sum(axis=1))
    a.scatter([n], [np.sqrt(np.mean(r ** 2))], color=C["gray"], s=14, zorder=4)
a.annotate("", xy=(1e6, 1e6), xytext=(1e6, 1e3),
           arrowprops=dict(arrowstyle="<->", color=C["red"], lw=0.9, shrinkA=0, shrinkB=0))
a.text(1.6e6, 3e4, "N = 10⁶에서\n1000배", fontsize=7.5, color=C["red"], va="center")
a.set_xlabel("함께 활동하는 뉴런 수 N")
a.set_ylabel("합친 쌍극자 크기 (뉴런 1개 = 1)")
a.set_xticks([1, 1e2, 1e4, 1e6, 1e8])
a.set_xticklabels(["1", "10²", "10⁴", "10⁶", "10⁸"])
a.set_yticks([1, 1e2, 1e4, 1e6, 1e8])
a.set_yticklabels(["1", "10²", "10⁴", "10⁶", "10⁸"])
a.minorticks_off()
a.legend(fontsize=7, loc="upper left")
a.set_title("(다) 동기화가 신호를 키운다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
