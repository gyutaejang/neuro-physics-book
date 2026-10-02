from matplotlib.patches import FancyBboxPatch

from figstyle import plt, save, C

fig, ax = plt.subplots(figsize=(7.4, 2.7))
ax.set_xlim(0, 10)
ax.set_ylim(0.6, 3.9)
ax.axis("off")

W, H = 1.5, 1.05


def box(x, y, text, sec, col=C["blue"], fill=C["light"], ls="-"):
    p = FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.02,rounding_size=0.08",
                       facecolor=fill, edgecolor=col, lw=1.1, ls=ls)
    ax.add_patch(p)
    ax.text(x, y + 0.1, text, ha="center", va="center", fontsize=7.9, color=C["ink"])
    ax.text(x, y - 0.36, sec, ha="center", va="center", fontsize=6.8, color=C["gray"])


def arrow(x0, y0, x1, y1, col=C["gray"], ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, ls=ls, mutation_scale=9))


xs = [0.95, 2.95, 4.95, 6.95, 8.95]
top = [("원자료·\n이벤트 확인", "9.1"), ("(MEG) tSSS·\n움직임 보정", "9.6"), ("필터: 고역·\n저역·전원 잡음", "9.2"),
       ("나쁜 채널\n탐지·표시", "9.3"), ("ICA: 성분\n판별·제거", "9.5")]
bot = [("나쁜 채널\n보간", "9.3"), ("재기준\n(평균 등)", "9.3"), ("에포크·\n기저선 보정", "9.7"),
       ("시행 거부·\n개수 확인", "9.7"), ("평균·통계\n(10장)", "")]
yt, yb = 3.25, 1.35
for (txt, sec), x in zip(top, xs):
    box(x, yt, txt, sec, ls="--" if "MEG" in txt else "-")
for (txt, sec), x in zip(bot[::-1], xs):
    box(x, yb, txt, sec, col=C["green"] if "평균·통계" in txt else C["blue"])
for i in range(4):
    arrow(xs[i] + W / 2, yt, xs[i + 1] - W / 2, yt)
    arrow(xs[4 - i] - W / 2, yb, xs[3 - i] + W / 2, yb)
arrow(xs[4], yt - H / 2, xs[4], yb + H / 2)

# ICA 학습용 사본 가지
ax.text(8.05, 2.3, "ICA 학습은 1 Hz 고역 통과한\n사본에서, 분리 행렬은 원래 자료에 적용",
        ha="right", va="center", fontsize=7.2, color=C["red"])
save(fig, __file__)
