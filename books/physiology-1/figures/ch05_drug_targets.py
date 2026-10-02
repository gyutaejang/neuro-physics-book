from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Rectangle

fig, ax = plt.subplots(figsize=(7.3, 4.0))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

# 시냅스 앞 종말과 시냅스 뒤 세포
ax.add_patch(FancyBboxPatch((0.6, 3.6), 6.0, 3.0, boxstyle="round,pad=0.05,rounding_size=0.9",
                            facecolor="#eef3f9", edgecolor=C["gray"], lw=1))
ax.add_patch(Rectangle((0.6, 0.2), 6.0, 2.1, facecolor="#eef6ee", edgecolor=C["gray"], lw=1))
ax.text(0.85, 6.25, "시냅스 앞 종말", fontsize=9.2, color=C["blue"])
ax.text(0.85, 0.45, "시냅스 뒤 세포", fontsize=9.2, color=C["green"])
ax.text(6.45, 2.95, "시냅스 틈", fontsize=8.1, color=C["gray"], ha="right", va="center")

# 소포와 전달물질
for x, y in ((2.6, 5.2), (3.5, 5.6), (4.3, 5.0), (3.2, 4.5)):
    ax.add_patch(Circle((x, y), 0.32, facecolor="white", edgecolor=C["blue"], lw=1))
    for dx, dy in ((-0.1, 0.05), (0.1, -0.05), (0.0, 0.12)):
        ax.add_patch(Circle((x + dx, y + dy), 0.045, color=C["blue"]))
# 미토콘드리아 위 MAO
ax.add_patch(Ellipse((1.6, 4.6), 1.1, 0.55, facecolor="#f6e9df", edgecolor=C["red"], lw=0.9))
ax.text(1.6, 4.6, "MAO", fontsize=7.6, ha="center", va="center", color=C["red"])
# 방출 중인 전달물질
rng = np.random.default_rng(1)
for x, y in zip(rng.uniform(3.0, 5.0, 14), rng.uniform(2.5, 3.4, 14)):
    ax.add_patch(Circle((x, y), 0.045, color=C["blue"]))
# 운반체 (재흡수)
ax.add_patch(Rectangle((5.35, 3.45), 0.35, 0.3, facecolor=C["purple"], edgecolor="none"))
ax.annotate("", xy=(5.52, 4.25), xytext=(5.25, 3.0),
            arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.1, connectionstyle="arc3,rad=-0.3"))
# 자가 수용체
ax.add_patch(Rectangle((1.9, 3.45), 0.4, 0.3, facecolor=C["gray"], edgecolor="none"))
# 시냅스 뒤 수용체
for x in (2.6, 3.4, 4.2, 5.0):
    ax.add_patch(Rectangle((x - 0.18, 2.15), 0.36, 0.3, facecolor=C["green"], edgecolor="none"))
# 효소 분해 (AChE 같은 틈 속 효소)
ax.add_patch(Circle((1.4, 2.95), 0.2, facecolor="#f6e9df", edgecolor=C["red"], lw=0.9))


def mark(x, y, n):
    ax.add_patch(Circle((x, y), 0.22, facecolor=C["ink"], edgecolor="white", zorder=6))
    ax.text(x, y, str(n), color="white", fontsize=8.1, ha="center", va="center", zorder=7)


marks = [(2.0, 5.9, 1), (4.55, 5.75, 2), (5.15, 4.15, 3), (6.0, 3.6, 4), (1.1, 4.1, 5),
         (1.6, 3.95, 6), (2.0, 1.7, 7), (0.95, 2.95, 8)]
for x, y, n in marks:
    mark(x, y, n)

items = [
    ("합성", "전구체 공급 (L-DOPA), 합성 효소 억제"),
    ("소포 저장", "VMAT 억제 (레세르핀, 테트라베나진)"),
    ("방출 · 역수송", "암페타민: 운반체를 거꾸로 돌린다"),
    ("재흡수", "SERT·NET·DAT 억제 (SSRI, 코카인)"),
    ("세포 안 분해", "MAO-A/B 억제"),
    ("자가 수용체", "D2·α2·5-HT1A 자가 수용체: 방출 조절"),
    ("시냅스 뒤 수용체", "작용제, 길항제, 부분 작용제,\n다른 자리 조절제 (벤조디아제핀)"),
    ("틈 속 분해", "AChE 억제 (도네페질)"),
]
y = 6.55
for i, (head, body) in enumerate(items, 1):
    mark(7.25, y, i)
    ax.text(7.6, y, head, fontsize=8.6, va="center", weight="bold")
    ax.text(9.4, y, body, fontsize=8.1, va="center")
    y -= 0.82 if "\n" not in body else 0.95
fig.tight_layout()
save(fig, __file__)
