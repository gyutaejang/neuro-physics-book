from figstyle import plt, np, save, C

# (가) 직교(카테시안) 표본화: TR마다 한 줄. (나) EPI: 한 번의 들뜸으로 지그재그. (다) EPI 경사 파형.
n = 8
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[1, 1, 1.35], wspace=0.35))
a1, a2, a3 = axs
for a in (a1, a2):
    a.set_xlim(-1.25, 1.25)
    a.set_aspect("equal", adjustable="datalim")
    a.axhline(0, color=C["gray"], lw=0.5); a.axvline(0, color=C["gray"], lw=0.5)
    a.set_xticks([]); a.set_yticks([])
    a.set_xlabel("$k_x$"); a.set_ylabel("$k_y$")
ky = np.linspace(-1, 1, n)
for i, y in enumerate(ky):
    a1.annotate("", xy=(1, y), xytext=(-1, y),
                arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.2, mutation_scale=8, shrinkA=0, shrinkB=0))
    a1.plot(np.linspace(-1, 1, 9), np.full(9, y), ".", color=C["blue"], ms=3)
a1.text(1.12, ky[-1], "TR 1", fontsize=7.5, va="center")
a1.text(1.12, ky[0], f"TR {n}", fontsize=7.5, va="center")
a1.set_title("(가) 줄마다 새 들뜸", fontsize=10)

# EPI: 아래 모서리에서 시작, 좌우로 왕복하며 위로 올라간다
xs, ys = [0], [0]
path = [(0, 0), (-1, -1)]
for i, y in enumerate(ky):
    x0, x1 = (-1, 1) if i % 2 == 0 else (1, -1)
    path += [(x0, y), (x1, y)]
P = np.array(path)
a2.plot(P[:2, 0], P[:2, 1], color=C["red"], lw=1, ls="--")
a2.plot(P[1:, 0], P[1:, 1], color=C["red"], lw=1.3)
for i, y in enumerate(ky):
    x0, x1 = (-1, 1) if i % 2 == 0 else (1, -1)
    a2.annotate("", xy=(x1 * 0.98, y), xytext=(x0 * 0.2 + x1 * 0.2, y),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.2, mutation_scale=8, shrinkA=0, shrinkB=0))
a2.text(0.05, -0.32, "시작", fontsize=7.5, color=C["red"])
a2.set_title("(나) EPI: 한 번에 전부", fontsize=10)

# 경사 파형
dt = 1.0
t = []
gx = []
gy = []
tt = 0
# 미리 감기
t += [0, 0.2, 0.8, 1.0]; gx += [0, -0.5, -0.5, 0]; gy += [0, -0.5, -0.5, 0]
tt = 1.0
for i in range(n):
    s = 1 if i % 2 == 0 else -1
    t += [tt + 0.15, tt + 1.85, tt + 2.0]; gx += [s, s, 0]; gy += [0, 0, 0]
    if i < n - 1:
        t += [tt + 2.05, tt + 2.15]; gx += [0, 0]; gy += [0.35, 0]
    tt += 2.2
a3.plot(t, np.array(gx) + 1.6, color=C["blue"], lw=1.2)
a3.plot(t, np.array(gy) - 0.6, color=C["red"], lw=1.2)
a3.text(-0.4, 1.6, "$G_x$", ha="right", va="center", fontsize=9.5, color=C["blue"])
a3.text(-0.4, -0.6, "$G_y$", ha="right", va="center", fontsize=9.5, color=C["red"])
a3.annotate("블립: $k_y$ 한 칸", xy=(3.25, -0.3), xytext=(4.2, -0.95), fontsize=8, va="top", color=C["red"],
            arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
a3.annotate("", xy=(5.4, 2.8), xytext=(3.2, 2.8), arrowprops=dict(arrowstyle="<->", lw=0.8, shrinkA=0, shrinkB=0))
a3.text(4.3, 2.9, "에코 간격", ha="center", va="bottom", fontsize=8)
a3.set_xlim(-1.6, tt + 0.3); a3.set_ylim(-2.0, 3.4)
a3.axis("off")
a3.text(tt, -1.6, "시간 →", ha="right", va="top", fontsize=8.5, color=C["gray"])
a3.set_title("(다) EPI의 경사 파형", fontsize=10)
save(fig, __file__)
