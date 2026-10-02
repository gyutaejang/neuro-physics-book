from matplotlib.patches import FancyBboxPatch

from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1]))

# 왼쪽: 소콜로프 3구획 모형
a1.set_xlim(0, 10)
a1.set_ylim(0, 6)
a1.axis("off")
a1.add_patch(FancyBboxPatch((3.0, 0.5), 6.9, 4.7, boxstyle="round,pad=0.02,rounding_size=0.3",
                            fc=C["green"], alpha=0.08, ec=C["green"], lw=1))
a1.text(9.7, 4.85, "뇌 조직", ha="right", va="center", fontsize=8.5, color=C["green"])


def box(x, y, t, col):
    a1.text(x, y, t, ha="center", va="center", fontsize=8.5, color=col,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=col, lw=1.2))


box(1.4, 2.9, "혈장\nFDG", C["red"])
box(5.0, 2.9, "조직\nFDG", C["red"])
box(8.25, 2.9, "FDG-6-\n인산", C["red"])
kw = dict(arrowstyle="-|>", lw=1.4, mutation_scale=11)
a1.annotate("", xy=(4.15, 3.25), xytext=(2.25, 3.25), arrowprops=dict(color=C["ink"], **kw))
a1.annotate("", xy=(2.25, 2.55), xytext=(4.15, 2.55), arrowprops=dict(color=C["ink"], **kw))
a1.text(3.2, 3.45, "$K_1$", ha="center", va="bottom", fontsize=10)
a1.text(3.2, 2.35, "$k_2$", ha="center", va="top", fontsize=10)
a1.annotate("", xy=(7.35, 2.9), xytext=(5.85, 2.9), arrowprops=dict(color=C["ink"], **kw))
a1.text(6.6, 3.1, "$k_3$", ha="center", va="bottom", fontsize=10)
a1.text(6.6, 2.6, "헥소키나아제", ha="center", va="top", fontsize=7.4, color=C["gray"])
a1.text(8.25, 1.6, "$k_4 \\approx 0$\n갇힌다", ha="center", va="top", fontsize=8, color=C["red"])
a1.text(1.4, 1.75, "운반체\n(GLUT1)", ha="center", va="top", fontsize=7.6, color=C["gray"])
a1.text(5.0, 0.9, "$K_i = K_1 k_3 / (k_2 + k_3)$", ha="center", va="center", fontsize=9.5)

# 오른쪽: 혈장 입력과 조직 곡선(전형적 매개변수로 계산한 예)
t = np.linspace(0, 60, 1201)
dt = t[1] - t[0]
cp = 40 * t * np.exp(-t / 0.6) + 8 * np.exp(-t / 3) + 6 * np.exp(-t / 60)


def tissue(K1, k2, k3):
    cf = np.zeros_like(t)
    cm = np.zeros_like(t)
    for i in range(1, len(t)):
        cf[i] = cf[i - 1] + dt * (K1 * cp[i - 1] - (k2 + k3) * cf[i - 1])
        cm[i] = cm[i - 1] + dt * k3 * cf[i - 1]
    return cf, cm


a2.plot(t, cp, color=C["gray"], lw=1.4, label="혈장")
for (K1, k2, k3), name, col in (((0.11, 0.12, 0.08), "회백질", C["blue"]),
                                ((0.06, 0.13, 0.05), "백질", C["purple"])):
    cf, cm = tissue(K1, k2, k3)
    a2.plot(t, cf + cm, color=col, lw=2, label=f"{name} ($K_i$ {K1 * k3 / (k2 + k3):.3f})")
    if name == "회백질":
        a2.fill_between(t, 0, cm, color=col, alpha=0.12, lw=0)
a2.text(47, 7.2, "회백질의 갇힌 몫", ha="center", va="bottom", fontsize=7.8, color=C["blue"])
a2.set_xlim(0, 60)
a2.set_ylim(0, 23)
a2.set_xlabel("주사 뒤 시간 (분)")
a2.set_ylabel("방사능 농도 (상대)")
a2.legend(fontsize=7.4, loc="upper right")
fig.tight_layout(w_pad=1.5)
save(fig, __file__)
