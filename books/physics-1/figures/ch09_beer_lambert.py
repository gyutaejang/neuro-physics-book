from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw={"width_ratios": [1, 1.3]})

# (가) 비어-람베르트: 거리에 따라 지수적으로 줄어든다
l = np.linspace(0, 5, 300)
for mu, col, lab in ((0.5, C["blue"], "흡수 계수 작음"), (1.5, C["red"], "흡수 계수 3배")):
    a1.plot(l, np.exp(-mu * l), color=col, lw=1.8, label=lab)
a1.axhline(np.exp(-1), color=C["gray"], lw=0.6, ls=":")
a1.text(4.9, np.exp(-1) + 0.02, "1/e ≈ 0.37", ha="right", va="bottom", fontsize=8, color=C["gray"])
a1.set_xlabel("빛이 지나간 거리 l (임의 단위)")
a1.set_ylabel("남은 빛의 비율 I / I₀")
a1.set_ylim(0, 1.05)
a1.legend(fontsize=8, loc="upper right")
a1.set_title("(가) 같은 거리마다 같은 비율로 준다", fontsize=9)

# (나) fNIRS: 머리 층 단면(평평하게 편 도식)과 바나나 모양 경로. 단위 cm.
layers = [("두피", 0.0, 0.5, "#f3e3d6"), ("머리뼈", 0.5, 1.2, "#e4e0d6"), ("뇌척수액", 1.2, 1.4, C["light"]),
          ("회백질", 1.4, 1.75, "#c9e0c4"), ("백질", 1.75, 2.6, "#e6f0e3")]
for name, top, bot, col in layers:
    a2.axhspan(-top, -bot, xmin=0, xmax=1, color=col, lw=0)
    a2.text(-1.15, -(top + bot) / 2, name, fontsize=7.5, va="center", ha="left", color=C["ink"])
xs, xd, xsh = -0.2, 2.8, 0.6
for x, lab, col in ((xs, "광원", C["red"]), (xd, "검출기", C["blue"]), (xsh, "짧은 거리\n검출기", C["gray"])):
    a2.plot(x, 0.07, marker="v", color=col, ms=8, clip_on=False)
    a2.text(x, 0.2, lab, ha="center", va="bottom", fontsize=7.5, color=col)
x = np.linspace(xs, xd, 200)
s = (x - xs) / (xd - xs)
for depth, alpha in ((1.75, 0.18), (1.4, 0.32), (1.0, 0.5)):
    a2.plot(x, -depth * np.sin(np.pi * s) ** 0.9, color=C["red"], lw=2.6, alpha=alpha)
x2 = np.linspace(xs, xsh, 60)
a2.plot(x2, -0.35 * np.sin(np.pi * (x2 - xs) / (xsh - xs)), color=C["gray"], lw=2, alpha=0.7)
a2.annotate("", xy=(xd, 0.75), xytext=(xs, 0.75), arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
a2.text((xs + xd) / 2, 0.8, "약 3 cm", ha="center", va="bottom", fontsize=8)
a2.set_xlim(-1.2, 3.4)
a2.set_ylim(-2.6, 1.15)
a2.set_aspect("equal")
a2.axis("off")
a2.set_title("(나) fNIRS의 빛 경로 (도식)", fontsize=9)
fig.tight_layout()
save(fig, __file__)
