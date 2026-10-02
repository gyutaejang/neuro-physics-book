from figstyle import plt, np, save, C
from matplotlib.patches import Circle, Polygon, FancyArrowPatch

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[1, 1, 1.25]))


def ecell(ax, x, y, label):
    ax.add_patch(Polygon([[x - 0.32, y - 0.25], [x + 0.32, y - 0.25], [x, y + 0.35]],
                         facecolor=C["green"], edgecolor=C["green"], alpha=0.9))
    ax.text(x + 0.42, y, label, fontsize=8, va="center")


def icell(ax, x, y, label):
    ax.add_patch(Circle((x, y), 0.25, facecolor=C["red"], edgecolor=C["red"], alpha=0.9))
    ax.text(x + 0.38, y, label, fontsize=8, va="center")


def exc(ax, p0, p1):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=11, color=C["blue"], lw=1.4))


def inh(ax, p0, p1):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-[", mutation_scale=6, color=C["red"], lw=1.4))


for ax in axes[:2]:
    ax.set_xlim(-1.3, 1.9)
    ax.set_ylim(-1.7, 1.9)
    ax.set_aspect("equal")
    ax.axis("off")

# (가) 앞먹임 억제
a = axes[0]
a.text(-1.1, 1.55, "입력", fontsize=8.5, color=C["blue"], va="center")
exc(a, (-0.75, 1.55), (-0.05, 0.5))
exc(a, (-0.75, 1.55), (-0.85, -0.7))
ecell(a, 0.0, 0.15, "E")
icell(a, -0.85, -0.95, "I")
inh(a, (-0.6, -0.9), (-0.08, -0.15))
a.text(0.3, -1.45, "입력이 E와 I를\n동시에 흥분시킨다", fontsize=8, ha="center", va="top")
a.set_title("(가) 앞먹임 억제", fontsize=10)

# (나) 되먹임 억제
a = axes[1]
a.text(-1.1, 1.55, "입력", fontsize=8.5, color=C["blue"], va="center")
exc(a, (-0.75, 1.55), (-0.05, 0.5))
ecell(a, 0.0, 0.15, "E")
icell(a, 0.0, -1.05, "I")
exc(a, (0.2, -0.12), (0.2, -0.78))
inh(a, (-0.2, -0.8), (-0.2, -0.15))
exc(a, (0.0, 0.5), (1.2, 1.4))
a.text(1.25, 1.55, "출력", fontsize=8.5, color=C["blue"], va="center")
a.text(0.3, -1.45, "E의 출력이 I를 거쳐\nE 자신을 누른다", fontsize=8, ha="center", va="top")
a.set_title("(나) 되먹임 억제", fontsize=10)

# (다) 앞먹임 억제가 통합 시간 창을 좁힌다
a = axes[2]
t = np.linspace(0, 40, 800)


def alpha(t, t0, tau):
    x = np.clip(t - t0, 0, None)
    return x / tau * np.exp(1 - x / tau)


ep = 4.0 * alpha(t, 0, 4.0)
ip = -3.0 * alpha(t, 2.0, 6.0)
a.plot(t, ep, color=C["blue"], lw=1.2, ls="--", label="EPSP만")
a.plot(t, ep + ip, color=C["ink"], lw=1.6, label="EPSP + 2 ms 늦은 IPSP")
a.axhline(0, color=C["gray"], lw=0.6)
w1 = t[ep > 2.0]
w2 = t[(ep + ip) > 2.0]
a.plot([w1[0], w1[-1]], [-2.0, -2.0], color=C["blue"], lw=3, solid_capstyle="butt")
a.plot([w2[0], w2[-1]], [-2.6, -2.6], color=C["ink"], lw=3, solid_capstyle="butt")
a.text(w1[-1] + 1, -2.0, f"{w1[-1] - w1[0]:.0f} ms", fontsize=7.5, va="center", color=C["blue"])
a.text(w2[-1] + 1, -2.6, f"{w2[-1] - w2[0]:.0f} ms", fontsize=7.5, va="center")
a.text(40, -2.3, "2 mV 이상\n머무는 시간", ha="right", fontsize=7.5, color=C["gray"], va="center")
a.set_xlabel("시간 (ms)")
a.set_ylabel("막전위 변화 (mV)")
a.set_ylim(-3.1, 5.2)
a.legend(fontsize=7.5, loc="upper right")
a.set_title("(다) 짧아진 통합 시간 창", fontsize=10)
fig.tight_layout()
save(fig, __file__)
