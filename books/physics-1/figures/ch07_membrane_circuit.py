from figstyle import plt, np, save, C


def wire(ax, *pts, color=None):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color or C["ink"], lw=1.4, solid_capstyle="round")


def resistor_v(ax, x, y0, y1, n=5, w=0.12, variable=False, color=None):
    """세로 지그재그 저항. variable=True면 대각선 화살표(변하는 전도도)."""
    col = color or C["ink"]
    a, b = y0 + 0.2 * (y1 - y0), y0 + 0.8 * (y1 - y0)
    ys = [y0, a] + [a + k / (2 * n) * (b - a) for k in range(1, 2 * n)] + [b, y1]
    xs = [x, x] + [x + w * (1 if k % 2 else -1) for k in range(1, 2 * n)] + [x, x]
    ax.plot(xs, ys, color=col, lw=1.4)
    if variable:
        ax.annotate("", xy=(x + 0.25, b + 0.05), xytext=(x - 0.25, a - 0.05),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1))


def battery_v(ax, x, y0, y1, plus_up=True, color=None):
    ym = (y0 + y1) / 2
    col = color or C["ink"]
    wire(ax, (x, y0), (x, ym - 0.07))
    wire(ax, (x, ym + 0.07), (x, y1))
    top_w, bot_w, top_lw, bot_lw = (0.22, 0.12, 1.4, 3) if plus_up else (0.12, 0.22, 3, 1.4)
    ax.plot([x - top_w, x + top_w], [ym + 0.07] * 2, color=col, lw=top_lw)
    ax.plot([x - bot_w, x + bot_w], [ym - 0.07] * 2, color=col, lw=bot_lw)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.6), gridspec_kw={"width_ratios": [1.45, 1]})

top, bot = 3.0, 0.0
xs = [0.4, 1.5, 2.6, 3.7]
wire(a1, (0, top), (4.1, top))
wire(a1, (0, bot), (4.1, bot))
a1.text(2.05, top + 0.25, "세포 밖", ha="center", fontsize=9)
a1.text(2.05, bot - 0.3, "세포 안", ha="center", va="top", fontsize=9)
for x in xs:
    a1.plot([x, x], [top, top], "o", color=C["ink"], ms=3)
    a1.plot([x, x], [bot, bot], "o", color=C["ink"], ms=3)

# 축전기
x = xs[0]
wire(a1, (x, top), (x, 1.58))
wire(a1, (x, 1.42), (x, bot))
a1.plot([x - 0.25, x + 0.25], [1.58] * 2, color=C["blue"], lw=2)
a1.plot([x - 0.25, x + 0.25], [1.42] * 2, color=C["blue"], lw=2)
a1.text(x + 0.3, 1.5, "$C_m$", fontsize=10, va="center", color=C["blue"])

# 이온 가지: 전도도(위) + 전지(아래)
# 긴 선이 +극. E_K < 0이면 바깥쪽(위)이 +, E_Na > 0이면 안쪽(아래)이 +.
for x, name, col, plus_up, var in [(xs[1], "K", C["green"], True, True),
                                    (xs[2], "Na", C["red"], False, True),
                                    (xs[3], "L", C["gray"], True, False)]:
    resistor_v(a1, x, top, 1.5, variable=var, color=col)
    battery_v(a1, x, 1.5, bot + 0.2, plus_up=plus_up, color=col)
    wire(a1, (x, bot + 0.2), (x, bot))
    a1.text(x + 0.22, 2.35, f"$g_{{{name}}}$", fontsize=10, va="center", color=col)
    a1.text(x + 0.3, 0.85, f"$E_{{{name}}}$", fontsize=10, va="center", color=col)
a1.text(2.05, -0.95, "화살표 = 열리고 닫히며 변하는 전도도", ha="center", fontsize=8, color=C["gray"])
a1.set_xlim(-0.2, 4.4)
a1.set_ylim(-1.2, 3.5)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("(가) 세포막 등가 회로", fontsize=10)

# (나) 가중 평균 수직선
a2.set_xlim(0, 1)
a2.set_ylim(-100, 75)
a2.axis("off")
xl = 0.32
a2.plot([xl, xl], [-95, 68], color=C["gray"], lw=1.2)
for v in (-90, -60, -30, 0, 30, 60):
    a2.plot([xl - 0.02, xl], [v, v], color=C["gray"], lw=0.8)
    a2.text(xl - 0.04, v, f"{v:+d}" if v else "0", ha="right", va="center", fontsize=7.5, color=C["gray"])
a2.text(xl - 0.04, 72, "mV", ha="right", fontsize=7.5, color=C["gray"])
marks = [(-90, "$E_K$ = −90", C["green"]), (60, "$E_{Na}$ = +60", C["red"])]
for v, lab, col in marks:
    a2.plot([xl], [v], "o", color=col, ms=6)
    a2.text(xl + 0.06, v, lab, va="center", fontsize=8.5, color=col)
a2.annotate("휴지: $g_{Na}/g_K$ ≈ 0.15\n→ 약 −70", xy=(xl, -70), xytext=(xl + 0.08, -52),
            fontsize=8, va="center", color=C["ink"],
            arrowprops=dict(arrowstyle="->", color=C["green"]))
a2.annotate("최고점: $g_{Na}/g_K$ ≈ 4\n→ 약 +30", xy=(xl, 30), xytext=(xl + 0.08, 12),
            fontsize=8, va="center", color=C["ink"],
            arrowprops=dict(arrowstyle="->", color=C["red"]))
a2.plot([xl], [-70], "s", color=C["blue"], ms=5)
a2.plot([xl], [30], "s", color=C["blue"], ms=5)
a2.set_title("(나) 막전위는 전도도 가중 평균", fontsize=10)
fig.tight_layout()
save(fig, __file__)
