from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.4), gridspec_kw={"width_ratios": [1.5, 1]})


def channel(ax, x0, act_open, inact):
    """막 단면 위의 Na⁺ 통로 하나. x0는 통로 가운데."""
    ax.add_patch(Rectangle((x0 - 1.1, 0), 2.2, 1.6, color=C["green"], alpha=0.12, lw=0))
    for dx in (-0.55, 0.25):
        ax.add_patch(Rectangle((x0 + dx, -0.15), 0.3, 1.9, color=C["gray"], alpha=0.75, lw=0))
    # 활성화 문 (통로 가운데, 바깥쪽 근처)
    if act_open:
        ax.plot([x0 - 0.25, x0 - 0.25], [1.05, 1.45], color=C["blue"], lw=3)
    else:
        ax.plot([x0 - 0.25, x0 + 0.25], [1.25, 1.25], color=C["blue"], lw=3)
    # 불활성화 공 (안쪽, 사슬로 연결)
    if inact:
        ax.plot([x0 + 0.4, x0 + 0.2, x0], [-0.15, -0.35, -0.25], color=C["red"], lw=1.2)
        ax.add_patch(Circle((x0, -0.22), 0.17, color=C["red"]))
    else:
        ax.plot([x0 + 0.4, x0 + 0.7, x0 + 0.85], [-0.15, -0.45, -0.7], color=C["red"], lw=1.2)
        ax.add_patch(Circle((x0 + 0.9, -0.78), 0.17, color=C["red"]))


xs = [0.0, 3.6, 7.2]
names = ["닫힘 (휴지)", "열림", "불활성"]
states = [(False, False), (True, False), (True, True)]
for x, nm, (ao, ia) in zip(xs, names, states):
    channel(a1, x, ao, ia)
    a1.text(x, 2.25, nm, ha="center", fontsize=9.5, weight="bold")
a1.text(-1.25, 1.6, "밖", fontsize=8, color=C["gray"], ha="right", va="top")
a1.text(-1.25, 0.0, "안", fontsize=8, color=C["gray"], ha="right")
# Na⁺ 흐름 (열림 상태만)
a1.annotate("", xy=(3.6, -0.3), xytext=(3.6, 2.05),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.6, mutation_scale=12))
a1.text(3.75, 1.75, "Na⁺", fontsize=8.5, color=C["green"])
# 상태 전이 화살표
for xa, top, bot in ((1.8, "탈분극", "0.1–0.5 ms"), (5.4, "계속", "약 1 ms")):
    a1.annotate("", xy=(xa + 0.55, 0.8), xytext=(xa - 0.55, 0.8),
                arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.2))
    a1.text(xa, 0.98, top, ha="center", va="bottom", fontsize=7.5)
    a1.text(xa, 0.62, bot, ha="center", va="top", fontsize=7.5)
a1.add_patch(FancyArrowPatch((7.2, -1.0), (0.0, -1.0), connectionstyle="arc3,rad=-0.12",
                             arrowstyle="-|>", mutation_scale=12, color=C["ink"], lw=1.2))
a1.text(3.6, -1.95, "재분극 뒤 수 ms: 공이 빠지고 활성화 문이 닫힌다",
        ha="center", va="top", fontsize=7.5)
a1.set_xlim(-1.7, 8.5)
a1.set_ylim(-2.5, 2.6)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("(가) Na⁺ 통로의 세 상태", fontsize=10)


# (나) 정상 상태 개폐 곡선 (호지킨-헉슬리 모형)
def rates(V):
    am = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10)); bm = 4 * np.exp(-(V + 65) / 18)
    ah = 0.07 * np.exp(-(V + 65) / 20); bh = 1 / (1 + np.exp(-(V + 35) / 10))
    an = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10)); bn = 0.125 * np.exp(-(V + 65) / 80)
    return am, bm, ah, bh, an, bn


V = np.linspace(-100, 40, 400) + 1e-6
am, bm, ah, bh, an, bn = rates(V)
minf, hinf, ninf = am / (am + bm), ah / (ah + bh), an / (an + bn)
a2.plot(V, minf ** 3, color=C["red"], lw=1.8, label="Na⁺ 활성화 m∞³")
a2.plot(V, hinf, color=C["red"], lw=1.8, ls="--", label="Na⁺ 비불활성 h∞")
a2.plot(V, ninf ** 4, color=C["green"], lw=1.8, label="K⁺ 활성화 n∞⁴")
a2.fill_between(V, 0, np.minimum(minf ** 3, hinf), color=C["red"], alpha=0.25, lw=0)
a2.legend(fontsize=7.5, loc="lower right", bbox_to_anchor=(1.0, 0.07))
a2.annotate("창 전류 영역", xy=(-52, 0.03), xytext=(-99, 0.2), fontsize=7.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.axvline(-65, color=C["gray"], lw=0.6, ls=":")
a2.set_xlabel("막전위 (mV)")
a2.set_ylabel("열린 비율 (정상 상태)")
a2.set_xticks([-100, -65, -30, 0, 30])
a2.set_xticklabels(["−100", "−65", "−30", "0", "30"])
a2.set_ylim(0, 1.02)
a2.set_title("(나) 오래 기다렸을 때의 개폐", fontsize=10)
fig.tight_layout()
save(fig, __file__)
