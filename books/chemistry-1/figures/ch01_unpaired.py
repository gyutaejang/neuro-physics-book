from figstyle import plt, np, save, C

# (이름, 오비탈 이름, 상자 수, 전자 수, 비고)
rows = [
    ("산소 원자 O", "2p", 3, 4, ""),
    ("아연 이온 Zn²⁺", "3d", 5, 10, "반자성"),
    ("구리 이온 Cu²⁺", "3d", 5, 9, "상자성"),
    ("철 이온 Fe²⁺ (고스핀)", "3d", 5, 6, "상자성"),
    ("철 이온 Fe³⁺ (고스핀)", "3d", 5, 5, "상자성"),
    ("망간 이온 Mn²⁺", "3d", 5, 5, "상자성"),
    ("가돌리늄 이온 Gd³⁺", "4f", 7, 7, "상자성"),
]
fig, ax = plt.subplots(figsize=(6.8, 3.9))
w, gap = 0.62, 0.08
x0 = 3.3
for i, (name, orb, nbox, ne, note) in enumerate(rows):
    y = -i
    # 훈트 규칙: 먼저 한 칸에 하나씩(위 화살표), 남으면 짝을 채운다
    occ = [0] * nbox
    for k in range(ne):
        occ[k % nbox] += 1
    unpaired = sum(1 for o in occ if o == 1)
    ax.text(0, y, name, va="center", fontsize=9)
    ax.text(x0 - 0.15, y, orb, va="center", ha="right", fontsize=8.5, color=C["gray"])
    for b in range(nbox):
        bx = x0 + b * (w + gap)
        ax.add_patch(plt.Rectangle((bx, y - 0.32), w, 0.64, fill=False, edgecolor=C["gray"], lw=0.9))
        if occ[b] >= 1:
            ax.annotate("", xy=(bx + 0.22, y + 0.26), xytext=(bx + 0.22, y - 0.26),
                        arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.3, mutation_scale=8))
        if occ[b] == 2:
            ax.annotate("", xy=(bx + 0.42, y - 0.26), xytext=(bx + 0.42, y + 0.26),
                        arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=1.3, mutation_scale=8))
    xe = x0 + 7 * (w + gap) + 0.25
    ax.text(xe, y, f"홀전자 {unpaired}", va="center", fontsize=9,
            color=C["purple"] if unpaired else C["gray"], weight="bold" if unpaired >= 4 else "normal")
    if note:
        ax.text(xe + 1.25, y, note, va="center", fontsize=8.5, color=C["gray"])
ax.text(x0, 0.75, "↑ 짝 없는 전자 (보라)   ↑↓ 짝지은 전자", fontsize=8.5, color=C["ink"], va="bottom")
ax.set_xlim(-0.1, 11.4)
ax.set_ylim(-len(rows) + 0.4, 1.2)
ax.axis("off")
save(fig, __file__)
