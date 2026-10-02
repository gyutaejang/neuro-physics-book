from figstyle import plt, np, save, C
from matplotlib.patches import Circle

# 회전 좌표계에서 본 등색 스핀 묶음(isochromat) 다섯 개.
# 주파수 차이 dw(상대값)에 따라 위상이 벌어지고, 180° 펄스가 위상을 뒤집는다.
dw = np.array([-2, -1, 0, 1, 2]) * 0.32          # rad / (τ 단위)
cols = [C["blue"], C["gray"], C["purple"], C["gray"], C["red"]]
tau = 1.0
stages = [
    ("(가) 90° 펄스 직후", np.zeros(5), "t = 0"),
    ("(나) 180° 펄스 직전", dw * tau, "t = τ"),
    ("(다) 180° 펄스 직후", -dw * tau, "t = τ"),
    ("(라) 에코", -dw * tau + dw * tau, "t = 2τ"),
]

fig, axes = plt.subplots(1, 4, figsize=(7.4, 2.35))
for ax, (title, ph, tl) in zip(axes, stages):
    ax.add_patch(Circle((0, 0), 1, fill=False, color=C["gray"], lw=0.6, ls=":"))
    ax.plot([-1.15, 1.15], [0, 0], color=C["gray"], lw=0.5)
    ax.plot([0, 0], [-1.15, 1.15], color=C["gray"], lw=0.5)
    for p, col in zip(ph, cols):
        # 위상 0은 +y 방향, 양의 위상은 시계 방향(빠른 스핀이 앞선다)
        x, y = np.sin(p), np.cos(p)
        ax.annotate("", xy=(0.95 * x, 0.95 * y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4, mutation_scale=9))
    ax.text(0, -1.42, tl, ha="center", fontsize=8.5, color=C["ink"])
    ax.text(0.06, 1.12, "y′", fontsize=8, color=C["gray"])
    ax.text(1.12, 0.06, "x′", fontsize=8, color=C["gray"])
    ax.set_title(title, fontsize=9.2)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.6, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
for ax, sgn in ((axes[1], 1), (axes[2], -1)):
    ax.text(sgn * 0.6, -0.5, "빠른\n스핀", fontsize=7.5, color=C["red"], ha="center")
    ax.text(-sgn * 0.6, -0.5, "느린\n스핀", fontsize=7.5, color=C["blue"], ha="center")
save(fig, __file__)
