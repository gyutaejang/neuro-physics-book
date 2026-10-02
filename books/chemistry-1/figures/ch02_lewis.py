from figstyle import plt, np, save, C

# 루이스 구조: 원소 기호, 결합선(공유 전자쌍), 점 두 개(비공유 전자쌍)
fig, axes = plt.subplots(1, 5, figsize=(7.4, 2.5))


def atom(ax, x, y, s, color=C["ink"]):
    ax.text(x, y, s, ha="center", va="center", fontsize=15, weight="bold", color=color, zorder=3)


def bond(ax, p, q, n=1, gap=0.09, shrink=0.26):
    p, q = np.array(p, float), np.array(q, float)
    u = (q - p) / np.linalg.norm(q - p)
    v = np.array([-u[1], u[0]])
    a, b = p + u * shrink, q - u * shrink
    for k in range(n):
        off = (k - (n - 1) / 2) * gap
        ax.plot([a[0] + v[0] * off, b[0] + v[0] * off], [a[1] + v[1] * off, b[1] + v[1] * off],
                color=C["ink"], lw=1.6)


def pair(ax, x, y, ang, r=0.37, sep=0.075):
    t = np.radians(ang)
    cx, cy = x + r * np.cos(t), y + r * np.sin(t)
    nx, ny = -np.sin(t), np.cos(t)
    ax.plot([cx + nx * sep, cx - nx * sep], [cy + ny * sep, cy - ny * sep], "o",
            color=C["red"], ms=3.2)


panels = []
# 물
ax = axes[0]
atom(ax, 0, 0, "O"); atom(ax, -0.75, -0.55, "H"); atom(ax, 0.75, -0.55, "H")
bond(ax, (0, 0), (-0.75, -0.55)); bond(ax, (0, 0), (0.75, -0.55))
pair(ax, 0, 0, 55); pair(ax, 0, 0, 125)
panels.append((ax, "물 H$_2$O", "결합 2, 비공유쌍 2"))
# 암모니아
ax = axes[1]
atom(ax, 0, 0, "N"); atom(ax, -0.8, -0.35, "H"); atom(ax, 0.8, -0.35, "H"); atom(ax, 0, -0.85, "H")
bond(ax, (0, 0), (-0.8, -0.35)); bond(ax, (0, 0), (0.8, -0.35)); bond(ax, (0, 0), (0, -0.85))
pair(ax, 0, 0, 90)
panels.append((ax, "암모니아 NH$_3$", "결합 3, 비공유쌍 1"))
# 메테인
ax = axes[2]
atom(ax, 0, -0.2, "C")
for dx, dy in [(-0.8, 0), (0.8, 0), (0, 0.6), (0, -0.8)]:
    atom(ax, dx, -0.2 + dy if dy else -0.2, "H")
    bond(ax, (0, -0.2), (dx, -0.2 + dy if dy else -0.2))
panels.append((ax, "메테인 CH$_4$", "결합 4, 비공유쌍 0"))
# 이산화탄소
ax = axes[3]
atom(ax, 0, 0, "C"); atom(ax, -0.85, 0, "O"); atom(ax, 0.85, 0, "O")
bond(ax, (-0.85, 0), (0, 0), n=2); bond(ax, (0, 0), (0.85, 0), n=2)
for x0, base in [(-0.85, 180), (0.85, 0)]:
    pair(ax, x0, 0, base + 60); pair(ax, x0, 0, base - 60)
panels.append((ax, "이산화탄소 CO$_2$", "이중 결합 2개"))
# 질소
ax = axes[4]
atom(ax, -0.45, 0, "N"); atom(ax, 0.45, 0, "N")
bond(ax, (-0.45, 0), (0.45, 0), n=3, gap=0.08)
pair(ax, -0.45, 0, 180); pair(ax, 0.45, 0, 0)
panels.append((ax, "질소 N$_2$", "삼중 결합 1개"))

for ax, title, sub in panels:
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.75, 0.95)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    ax.text(0, -1.68, sub, ha="center", va="bottom", fontsize=8.5, color=C["gray"])
fig.text(0.5, 0.04, "선 하나 = 공유 전자쌍 하나(전자 2개)     빨간 점 둘 = 비공유 전자쌍", ha="center",
         fontsize=8.5, color=C["ink"])
fig.subplots_adjust(wspace=0.05)
save(fig, __file__)
