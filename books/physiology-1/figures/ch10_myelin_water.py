from figstyle import plt, np, save, C
from matplotlib.patches import Circle

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[0.9, 1.1]))

# 왼쪽: 유수 축삭 단면과 g-ratio
d, g = 1.0, 0.7
D = d / g
a1.add_patch(plt.Rectangle((-1.25, -1.25), 2.5, 2.5, facecolor=C["blue"], alpha=0.08, lw=0))
n_wrap = 7
for k in range(n_wrap + 1):
    r = d / 2 + (D - d) / 2 * k / n_wrap
    a1.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=C["purple"], lw=1.6 if k in (0, n_wrap) else 0.9))
a1.add_patch(Circle((0, 0), d / 2 - 0.01, facecolor=C["green"], alpha=0.22, lw=0))
a1.annotate("", xy=(-d / 2, -0.0), xytext=(d / 2, -0.0),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=1.0, shrinkA=0, shrinkB=0))
a1.text(0, 0.07, "d", ha="center", va="bottom", fontsize=10, style="italic")
a1.annotate("", xy=(-D / 2, -0.85), xytext=(D / 2, -0.85),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=1.0, shrinkA=0, shrinkB=0))
a1.plot([-D / 2, -D / 2], [-0.85, -0.05], color=C["gray"], lw=0.6, ls=":")
a1.plot([D / 2, D / 2], [-0.85, -0.05], color=C["gray"], lw=0.6, ls=":")
a1.text(0, -0.92, "D", ha="center", va="top", fontsize=10, style="italic")
a1.text(0, 1.38, "g = d / D ≈ 0.7", ha="center", fontsize=10, color=C["ink"])
a1.annotate("축삭 안 물", xy=(0.1, 0.32), xytext=(1.45, 1.05), fontsize=8.5, color=C["green"],
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
a1.annotate("수초 겹 사이의 물\n(T2 약 10–20 ms)", xy=(0.6, 0.3), xytext=(1.45, 0.25), fontsize=8.5,
            color=C["purple"], arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
a1.annotate("축삭 밖 물", xy=(-1.0, -1.1), xytext=(1.45, -0.75), fontsize=8.5, color=C["blue"],
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
a1.set_xlim(-1.35, 2.9)
a1.set_ylim(-1.45, 1.6)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 백질 복셀의 T2 분포 (다중 에코 T2로 얻는 모양)
t2 = np.logspace(0.5, 3.5, 600)


def peak(center, width, area):
    x = np.log10(t2)
    y = np.exp(-0.5 * ((x - np.log10(center)) / width) ** 2)
    return area * y / np.trapezoid(y, x)


mw, ie = peak(15, 0.08, 0.12), peak(80, 0.07, 0.88)
a2.fill_between(t2, 0, mw, color=C["purple"], alpha=0.35, lw=0)
a2.plot(t2, mw + ie, color=C["ink"], lw=1.4)
a2.fill_between(t2, 0, ie, color=C["blue"], alpha=0.18, lw=0)
a2.text(15, mw.max() * 1.08, "미엘린 물\n약 12%", ha="center", va="bottom", fontsize=8.5, color=C["purple"])
a2.text(80, ie.max() * 1.02, "축삭 안팎의 물\n약 88%", ha="center", va="bottom", fontsize=8.5, color=C["blue"])
a2.axvspan(1000, 3000, color=C["gray"], alpha=0.12, lw=0)
a2.text(1700, ie.max() * 0.45, "뇌척수액\n(T2 1–2 s 이상)", ha="center", fontsize=8, color=C["gray"])
a2.axvline(40, color=C["gray"], lw=0.6, ls=":")
a2.text(42, ie.max() * 1.55, "TE 40 ms에서 미엘린 물은\n신호의 약 1.5%만 남는다", fontsize=7.5, color=C["gray"], ha="left")
a2.set_xscale("log")
a2.set_xlim(3, 3000)
a2.set_ylim(0, ie.max() * 1.9)
a2.set_xticks([10, 30, 100, 300, 1000])
a2.set_xticklabels(["10", "30", "100", "300", "1000"])
a2.minorticks_off()
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xlabel("T2 (ms, 로그 눈금, 3 T 백질)")
a2.set_ylabel("신호 비율")
fig.tight_layout()
save(fig, __file__)
