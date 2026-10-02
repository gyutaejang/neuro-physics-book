from matplotlib.patches import Rectangle, FancyArrowPatch

from figstyle import plt, np, save, C

# 가벼운 핵종도표 (가로 N, 세로 Z). s = 안정, p = β⁺ 방출, m = β⁻ 방출.
nuc = {
    (5, 5): ("¹⁰B", "s", ""), (5, 6): ("¹¹B", "s", ""), (5, 7): ("¹²B", "m", "20 ms"),
    (6, 4): ("¹⁰C", "p", "19 s"), (6, 5): ("¹¹C", "p", "20 분"), (6, 6): ("¹²C", "s", ""),
    (6, 7): ("¹³C", "s", ""), (6, 8): ("¹⁴C", "m", "5730 년"),
    (7, 5): ("¹²N", "p", "11 ms"), (7, 6): ("¹³N", "p", "10 분"), (7, 7): ("¹⁴N", "s", ""),
    (7, 8): ("¹⁵N", "s", ""), (7, 9): ("¹⁶N", "m", "7 s"),
    (8, 6): ("¹⁴O", "p", "71 s"), (8, 7): ("¹⁵O", "p", "2 분"), (8, 8): ("¹⁶O", "s", ""),
    (8, 9): ("¹⁷O", "s", ""), (8, 10): ("¹⁸O", "s", ""), (8, 11): ("¹⁹O", "m", "27 s"),
    (9, 8): ("¹⁷F", "p", "65 s"), (9, 9): ("¹⁸F", "p", "110 분"), (9, 10): ("¹⁹F", "s", ""),
    (9, 11): ("²⁰F", "m", "11 s"),
}
face = {"s": C["blue"], "p": "#f6d5c3", "m": "#e6e6e6"}
edge = {"s": C["blue"], "p": C["red"], "m": C["gray"]}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw=dict(width_ratios=[1.45, 1]))
for (z, n), (lab, kind, t) in nuc.items():
    a1.add_patch(Rectangle((n - 0.46, z - 0.46), 0.92, 0.92, fc=face[kind], ec=edge[kind], lw=1.0))
    col = "white" if kind == "s" else C["ink"]
    a1.text(n, z + (0.12 if t else 0), lab, ha="center", va="center", fontsize=9.5, color=col)
    if t:
        a1.text(n, z - 0.24, t, ha="center", va="center", fontsize=7, color=col)
for z0, n0 in ((9, 9), (8, 7), (6, 5)):
    a1.add_patch(FancyArrowPatch((n0 + 0.32, z0 - 0.32), (n0 + 0.68, z0 - 0.68), arrowstyle="-|>",
                                 mutation_scale=8, color=C["red"], lw=1.1))
a1.add_patch(FancyArrowPatch((7.68, 6.32), (7.32, 6.68), arrowstyle="-|>", mutation_scale=8,
                             color=C["gray"], lw=1.1))
a1.set_xlim(3.4, 11.6)
a1.set_ylim(4.4, 9.6)
a1.set_xticks(range(4, 12))
a1.set_yticks(range(5, 10))
a1.set_yticklabels(["B 5", "C 6", "N 7", "O 8", "F 9"])
a1.set_xlabel("중성자 수 N")
a1.set_ylabel("양성자 수 Z")
a1.set_aspect("equal")
a1.set_title("(가) 가벼운 원자핵의 핵종도표", fontsize=9.5)
a1.text(3.6, 9.25, "■ 안정", color=C["blue"], fontsize=8)
a1.text(3.6, 8.85, "■ β⁺ 방출", color=C["red"], fontsize=8)
a1.text(3.6, 8.45, "■ β⁻ 방출", color=C["gray"], fontsize=8)

# (나) 붕괴 방식마다 도표 위에서 움직이는 방향
a2.set_xlim(-2.9, 2.9)
a2.set_ylim(-2.9, 2.9)
a2.set_aspect("equal")
for v in range(-2, 3):
    a2.axhline(v, color="#eeeeee", lw=0.6, zorder=0)
    a2.axvline(v, color="#eeeeee", lw=0.6, zorder=0)
a2.add_patch(Rectangle((-0.42, -0.42), 0.84, 0.84, fc=C["light"], ec=C["ink"], lw=1))
a2.text(0, 0, "어미\n핵", ha="center", va="center", fontsize=8.5)
moves = [((-2, -2), "α: Z−2, N−2", C["ink"], (-1.15, -2.55)),
         ((-1, 1), "β⁻: Z+1, N−1", C["gray"], (-1.6, 1.6)),
         ((1, -1), "β⁺, 전자 포획:\nZ−1, N+1", C["red"], (1.55, -1.75))]
for (dn, dz), lab, col, (tx, ty) in moves:
    a2.add_patch(FancyArrowPatch((0.35 * np.sign(dn), 0.35 * np.sign(dz)), (dn, dz),
                                 arrowstyle="-|>", mutation_scale=10, color=col, lw=1.4))
    a2.add_patch(Rectangle((dn - 0.3, dz - 0.3), 0.6, 0.6, fc="white", ec=col, lw=0.9, ls="--"))
    a2.text(tx, ty, lab, ha="center", va="center", fontsize=8, color=col)
a2.text(1.35, 1.25, "γ, 이성질체 전이:\n제자리\n(에너지만 낮아진다)", ha="center", va="center", fontsize=8,
        color=C["purple"])
a2.set_xticks([-2, -1, 0, 1, 2])
a2.set_yticks([-2, -1, 0, 1, 2])
a2.set_xticklabels(["−2", "−1", "0", "+1", "+2"])
a2.set_yticklabels(["−2", "−1", "0", "+1", "+2"])
a2.set_xlabel("N의 변화")
a2.set_ylabel("Z의 변화")
a2.set_title("(나) 붕괴는 정해진 방향으로 옮긴다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
