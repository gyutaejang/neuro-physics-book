from figstyle import plt, np, save, C

# 비유일성: 반무한 균질 도체(0.33 S/m) 표면의 전위를 세 가지 다른 소스 배치로 똑같이 만든다.
# 수직 쌍극자 p가 깊이 d에 있으면 표면 전위는 (p/σ)·P_d(ρ), P_d(ρ) = d / (2π(ρ² + d²)^{3/2}).
# P_a * P_b = P_{a+b} (포아송 핵의 반군 성질)이므로, 깊이 a의 쌍극자 판에 면밀도 p·P_{5−a}를 주면
# 깊이 5 cm 점 쌍극자와 표면 전위가 정확히 같다. 아래에서 수치 적분으로 확인한다.
sig = 0.33
p = 20e-9                      # A·m
xs = (np.arange(32) - 15.5) * 0.75 * 1e-2    # 센서 위치 (m), 앞 그림과 같다


def P(rho, d):
    return d / (2 * np.pi * (rho**2 + d**2) ** 1.5)


def surface_from_sheet(a, bdepth):
    """깊이 a의 판(면밀도 p·P_b)이 표면 센서에 만드는 전위. 극좌표 수치 적분."""
    r = np.concatenate([[0], np.geomspace(1e-4, 20.0, 1500)])
    t = np.linspace(0, 2 * np.pi, 361)[:-1]
    RR, TT = np.meshgrid(0.5 * (r[1:] + r[:-1]), t, indexing="ij")
    dA = (0.5 * (r[1:]**2 - r[:-1]**2))[:, None] * (2 * np.pi / len(t))
    m = p * P(RR, bdepth) * dA
    xx, yy = RR * np.cos(TT), RR * np.sin(TT)
    V = np.array([np.sum(m * P(np.hypot(x - xx, yy), a)) for x in xs]) / sig
    return V * 1e6


VA = p / sig * P(np.abs(xs), 0.05) * 1e6
VB = surface_from_sheet(0.02, 0.03)
VC = surface_from_sheet(0.035, 0.015)
print("최대", VA.max(), "μV; 상대 차이", np.max(np.abs(VB - VA)) / VA.max(), np.max(np.abs(VC - VA)) / VA.max())

fig = plt.figure(figsize=(7.3, 3.5))
gs = fig.add_gridspec(3, 2, width_ratios=[1.1, 1], hspace=0.35, wspace=0.25)
xx = np.arange(-8, 8.01, 0.5)
configs = [("(가) 깊이 5 cm 점 하나 (20 nA·m)", None, 5.0, C["purple"]),
           ("(나) 깊이 2 cm의 넓은 판 (합 20 nA·m)", 3.0, 2.0, C["red"]),
           ("(다) 깊이 3.5 cm의 판 (합 20 nA·m)", 1.5, 3.5, C["green"])]
for i, (title, bb, depth, col) in enumerate(configs):
    ax = fig.add_subplot(gs[i, 0])
    ax.axhline(0, color=C["ink"], lw=0.8)
    ax.plot(xs * 100, np.zeros_like(xs), "v", ms=3, color=C["blue"])
    if bb is None:
        ax.annotate("", xy=(0, -depth + 1.1), xytext=(0, -depth - 1.1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0))
    else:
        xf = np.linspace(-10, 10, 400)
        h = 1.5 * P(np.abs(xf), bb) / P(0, bb)
        ax.fill_between(xf, -depth, -depth + h, color=col, alpha=0.25, lw=0)
        ax.plot(xf, -depth + h, color=col, lw=1.0)
        ax.plot(xf, -depth + 0 * xf, color=col, lw=0.6, ls=":")
        for x in np.arange(-6, 6.01, 1.5):
            hh = 1.5 * P(abs(x), bb) / P(0, bb)
            if hh > 0.3:
                ax.annotate("", xy=(x, -depth + hh), xytext=(x, -depth),
                            arrowprops=dict(arrowstyle="-|>", color=col, lw=0.9, mutation_scale=7))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-6.4, 0.6)
    ax.set_yticks([0, -2, -4, -6])
    ax.set_yticklabels(["0", "2", "4", "6"], fontsize=7.5)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.set_title(title, fontsize=8.8, loc="left", pad=2)
    if i == 1:
        ax.set_ylabel("깊이 (cm)")
    if i < 2:
        ax.set_xticklabels([])
    else:
        ax.set_xlabel("x (cm)")

ax = fig.add_subplot(gs[:, 1])
ax.plot(xs * 100, VA, color=C["purple"], lw=4.5, alpha=0.35, label="(가) 점 하나")
ax.plot(xs * 100, VB, "o", ms=4, mfc="none", color=C["red"], label="(나) 얕은 판")
ax.plot(xs * 100, VC, "+", ms=6, color=C["green"], label="(다) 중간 판")
ax.set_xlabel("센서 위치 x (cm)")
ax.set_ylabel("표면 전위 (μV)")
ax.set_title("(라) 센서 32개의 값은 세 경우가 같다", fontsize=9.5)
ax.legend(fontsize=8, loc="upper right")
ax.set_ylim(0, 4.6)
save(fig, __file__)
