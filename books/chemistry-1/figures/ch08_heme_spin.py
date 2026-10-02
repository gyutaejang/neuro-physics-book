from figstyle import plt, np, save, C

fig = plt.figure(figsize=(7.4, 3.5))
axL = fig.add_axes([0.0, 0.0, 0.64, 1.0])
axR = fig.add_axes([0.73, 0.17, 0.26, 0.68])
axL.set_xlim(0, 9.6)
axL.set_ylim(-1.0, 5.4)
axL.axis("off")

# (이름, 철, 아래 세 칸, 위 두 칸): 각 칸의 전자 수와 스핀 (u: 위 하나, ud: 짝)
states = [
    ("탈산소헤모글로빈", r"Fe$^{2+}$ (d$^6$), 고스핀", ["ud", "u", "u"], ["u", "u"], 4, "상자성", C["purple"]),
    ("산소헤모글로빈", r"Fe$^{2+}$ (d$^6$), 저스핀", ["ud", "ud", "ud"], ["", ""], 0, "반자성", C["gray"]),
    ("메트헤모글로빈", r"Fe$^{3+}$ (d$^5$), 고스핀", ["u", "u", "u"], ["u", "u"], 5, "상자성", C["purple"]),
]
bw, bh = 0.62, 0.5


def draw_box(x, y, occ):
    axL.add_patch(plt.Rectangle((x, y), bw, bh, fill=False, edgecolor=C["ink"], lw=1))
    if occ == "u":
        axL.annotate("", xy=(x + bw / 2, y + bh - 0.06), xytext=(x + bw / 2, y + 0.06),
                     arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.4, mutation_scale=9))
    elif occ == "ud":
        axL.annotate("", xy=(x + bw * 0.35, y + bh - 0.06), xytext=(x + bw * 0.35, y + 0.06),
                     arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.4, mutation_scale=9))
        axL.annotate("", xy=(x + bw * 0.65, y + 0.06), xytext=(x + bw * 0.65, y + bh - 0.06),
                     arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.4, mutation_scale=9))


for i, (name, fe, low, high, n, mag, col) in enumerate(states):
    cx = 1.55 + i * 3.2
    axL.text(cx, 5.1, name, ha="center", va="center", fontsize=9.5, weight="bold")
    axL.text(cx, 4.6, fe, ha="center", va="center", fontsize=8.5)
    hy = 2.6 if n else 3.5  # 저스핀은 위아래 칸 사이(에너지 간격)가 더 크다
    for k, o in enumerate(high):
        draw_box(cx - bw - 0.05 + k * (bw + 0.1), hy, o)
    for k, o in enumerate(low):
        draw_box(cx - 1.5 * bw - 0.1 + k * (bw + 0.1), 1.3, o)
    axL.text(cx, 0.75, f"홀전자 {n}개", ha="center", va="center", fontsize=9, color=col)
    axL.text(cx, 0.3, mag, ha="center", va="center", fontsize=9, color=col, weight="bold")
axL.annotate("", xy=(0.05, 4.0), xytext=(0.05, 1.3),
             arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=0.9))
axL.text(0.15, 4.05, "에너지", fontsize=8, color=C["gray"], va="bottom")
axL.text(4.75, -0.45, "철의 d 오비탈 다섯 칸에 전자가 앉는 방식 (단순화한 도식)", ha="center",
         fontsize=8.3, color=C["gray"])

# 오른쪽: 상자성의 세기 ∝ n(n+2)
names = ["산소\nHb", "탈산소\nHb", "메트\nHb", r"Gd$^{3+}$"]
vals = [0, 24, 35, 63]
cols = [C["gray"], C["purple"], C["purple"], C["purple"]]
axR.bar(range(4), vals, color=cols, width=0.62)
for k, v in enumerate(vals):
    axR.text(k, v + 1.5, str(v), ha="center", va="bottom", fontsize=8.5)
axR.set_xticks(range(4))
axR.set_xticklabels(names, fontsize=8)
axR.set_ylim(0, 75)
axR.set_yticks([0, 20, 40, 60])
axR.set_ylabel("n(n+2), 분자당 상자성 세기", fontsize=8.5)
axR.set_title("홀전자 n개의 상자성", fontsize=9.5)
save(fig, __file__)
