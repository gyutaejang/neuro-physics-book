from figstyle import plt, np, save, C
from matplotlib.patches import Ellipse


def fa(l):
    l = np.array(l, float)
    return np.sqrt(0.5) * np.sqrt(((l[0] - l[1]) ** 2 + (l[1] - l[2]) ** 2 + (l[2] - l[0]) ** 2)
                                  / (l ** 2).sum())


cases = [("뇌척수액", [3.0, 3.0, 3.0], C["blue"]),
         ("회백질", [0.95, 0.8, 0.7], C["green"]),
         ("백질 (뇌량)", [1.7, 0.3, 0.3], C["purple"])]
fig, ax = plt.subplots(figsize=(7.0, 2.9))
for i, (name, l, col) in enumerate(cases):
    x0 = i * 3.2
    w, h = np.sqrt(l[0]) * 1.25, np.sqrt(l[1]) * 1.25
    ax.add_patch(Ellipse((x0, 0), w, h, facecolor=col, alpha=0.25, edgecolor=col, lw=1.5))
    md = np.mean(l)
    ax.text(x0, 1.45, name, ha="center", fontsize=10, weight="bold")
    ax.text(x0, -1.35, f"λ = {l[0]:.2f}, {l[1]:.2f}, {l[2]:.2f}", ha="center", fontsize=8.5)
    ax.text(x0, -1.75, f"평균 확산도 {md:.2f}   FA {fa(l):.2f}", ha="center", fontsize=8.5)
ax.text(6.4 + 1.75, 0, "섬유\n방향 →", fontsize=8.5, va="center", color=C["purple"])
ax.text(3.2, -2.25, "λ와 평균 확산도의 단위는 10⁻³ mm²/s. 타원의 축 길이는 그 방향으로 퍼지는 거리(√λ)에 비례한다.",
        ha="center", fontsize=8, color=C["gray"])
ax.set_xlim(-1.7, 8.9)
ax.set_ylim(-2.45, 1.8)
ax.set_aspect("equal")
ax.axis("off")
save(fig, __file__)
