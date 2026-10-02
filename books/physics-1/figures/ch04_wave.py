from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 3.9), gridspec_kw={"height_ratios": [1.3, 1]})

x = np.linspace(0, 3.2, 600)
a1.plot(x, np.sin(2 * np.pi * x), color=C["blue"], lw=1.8, label="지금")
a1.plot(x, np.sin(2 * np.pi * (x - 0.15)), color=C["blue"], lw=1, ls="--", alpha=0.6, label="조금 뒤")
a1.axhline(0, color=C["gray"], lw=0.5)
a1.annotate("", xy=(0.25, 1.3), xytext=(1.25, 1.3), arrowprops=dict(arrowstyle="<->", color=C["red"]))
a1.text(0.75, 1.38, "파장 λ", ha="center", va="bottom", fontsize=9, color=C["red"])
a1.annotate("", xy=(2.75, 1.35), xytext=(2.25, 1.35), arrowprops=dict(arrowstyle="->", color=C["ink"]))
a1.text(2.5, 1.43, "진행 방향, 속력 v", ha="center", va="bottom", fontsize=9)
a1.annotate("", xy=(1.75, 0.95), xytext=(1.75, -0.95), arrowprops=dict(arrowstyle="<->", color=C["green"]))
a1.text(1.75, -1.18, "매질은 위아래로만", fontsize=8.5, color=C["green"], ha="center", va="top")
a1.set_ylim(-1.6, 1.9)
a1.set_xlim(0, 3.2)
a1.axis("off")
a1.set_title("횡파: 매질의 떨림이 진행 방향과 수직 (줄, 전자기파)", fontsize=9.5, loc="left")
a1.legend(fontsize=8, loc="lower right", ncol=2, bbox_to_anchor=(1.0, -0.12))

n = 90
x0 = np.linspace(0, 3.2, n)
xs = x0 + 0.045 * np.cos(2 * np.pi * x0)  # 0.25, 1.25, 2.25에서 빽빽(밀)
for xi in xs:
    a2.plot([xi, xi], [0, 1], color=C["blue"], lw=1.1)
for c in (0.25, 1.25, 2.25):
    a2.text(c, -0.15, "밀", ha="center", va="top", fontsize=8.5, color=C["red"])
for c in (0.75, 1.75, 2.75):
    a2.text(c, -0.15, "소", ha="center", va="top", fontsize=8.5, color=C["gray"])
a2.annotate("", xy=(0.25, 1.25), xytext=(1.25, 1.25), arrowprops=dict(arrowstyle="<->", color=C["red"]))
a2.text(0.75, 1.3, "λ", ha="center", va="bottom", fontsize=9, color=C["red"])
a2.annotate("", xy=(2.05, 1.3), xytext=(1.85, 1.3), arrowprops=dict(arrowstyle="<->", color=C["green"]))
a2.text(2.15, 1.3, "매질은 앞뒤로", fontsize=8.5, color=C["green"], va="center")
a2.set_xlim(0, 3.2)
a2.set_ylim(-0.55, 1.7)
a2.axis("off")
a2.set_title("종파: 떨림이 진행 방향과 나란함 (소리, 초음파)", fontsize=9.5, loc="left")
fig.tight_layout()
save(fig, __file__)
