from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.4), gridspec_kw=dict(width_ratios=[0.85, 1.15]))

# 왼쪽: K+ 평형의 도식
rng = np.random.default_rng(7)
a1.add_patch(plt.Rectangle((-0.25, 0), 0.5, 4, color=C["green"], alpha=0.2, lw=0))
for gx in np.linspace(0.85, 2.35, 4):  # 안: K+ 많음 (흔든 격자)
    for gy in np.linspace(0.3, 3.7, 7):
        if abs(gy - 2.0) < 0.45 and abs(gx - 1.6) < 0.6:
            continue  # 농도 글자 자리
        x, y = gx + rng.uniform(-0.12, 0.12), gy + rng.uniform(-0.12, 0.12)
        a1.text(x, y, "K⁺", fontsize=7, color=C["green"], ha="center", va="center")
for x, y in ((-2.0, 3.3), (-1.0, 3.0), (-1.9, 0.8), (-0.9, 0.5)):  # 밖: K+ 적음
    a1.text(x, y, "K⁺", fontsize=7, color=C["green"], ha="center", va="center")
for y in np.linspace(0.3, 3.7, 7):
    a1.text(-0.38, y, "+", fontsize=9, ha="center", va="center", weight="bold")
    a1.text(0.38, y, "−", fontsize=9, ha="center", va="center", weight="bold")
a1.annotate("", xy=(-1.6, 4.5), xytext=(1.6, 4.5),
            arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.6, mutation_scale=12))
a1.text(0, 4.62, "확산: 농도가 낮은 밖으로", ha="center", va="bottom", fontsize=8.5, color=C["green"])
a1.annotate("", xy=(1.6, -0.5), xytext=(-1.6, -0.5),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.6, mutation_scale=12))
a1.text(0, -0.62, "전기력: 음전하가 쌓인 안으로", ha="center", va="top", fontsize=8.5, color=C["red"])
a1.text(-1.5, 2.0, "밖\n5 mM", ha="center", va="center", fontsize=9,
        bbox=dict(facecolor="white", edgecolor="none", pad=1))
a1.text(1.6, 2.0, "안\n140 mM", ha="center", va="center", fontsize=9,
        bbox=dict(facecolor="white", edgecolor="none", pad=1))
a1.set_xlim(-2.6, 2.6)
a1.set_ylim(-1.4, 5.3)
a1.axis("off")

# 오른쪽: 네른스트 전위 대 농도비
f = 26.7
ratio = np.logspace(-2.2, 4.6, 300)
for z, col, lab in ((1, C["blue"], "z = +1"), (2, C["purple"], "z = +2"), (-1, C["red"], "z = −1")):
    a2.semilogx(ratio, f / z * np.log(ratio), color=col, lw=1.2, label=lab)
ions = [("K⁺", 5 / 140, 1, C["blue"], (8, -7)), ("Na⁺", 145 / 15, 1, C["blue"], (-34, 4)),
        ("Ca²⁺", 1.5 / 1e-4, 2, C["purple"], (6, -12)), ("Cl⁻", 115 / 8, -1, C["red"], (6, -4))]
for name, rt, z, col, off in ions:
    E = f / z * np.log(rt)
    a2.scatter([rt], [E], color=col, s=26, zorder=4)
    a2.annotate(f"{name} {E:+.0f} mV".replace("-", "−"), xy=(rt, E), xytext=off, textcoords="offset points",
                fontsize=8.5, ha="left", va="center")
a2.axhspan(-80, -60, color=C["gray"], alpha=0.15, lw=0)
a2.text(40, -57, "휴지 막전위\n−60 ~ −80 mV", fontsize=8, color=C["gray"], va="bottom")
a2.axhline(0, color=C["gray"], lw=0.6, ls=":")
a2.set_xlabel("농도비 (바깥 / 안), 로그 눈금")
a2.set_ylabel("평형 전위 (mV)")
a2.set_ylim(-140, 160)
a2.set_yticks([-100, -50, 0, 50, 100, 150])
a2.set_yticklabels(["−100", "−50", "0", "50", "100", "150"])
a2.set_xlim(10 ** -2.4, 10 ** 6.4)
a2.set_xticks([1e-2, 1, 1e2, 1e4, 1e6])
a2.set_xticklabels(["1/100", "1", "100", "10⁴", "10⁶"])
a2.minorticks_off()
a2.legend(fontsize=8, loc="upper left")
fig.tight_layout()
save(fig, __file__)
