from figstyle import plt, np, save, C

# 순수 지질 이중층의 투과 계수 (cm/s). 측정마다 차이가 커서 자릿수 범위로 나타낸다.
rows = [
    ("O₂ (작은 비극성 기체)", 1e0, 1e2, C["gray"]),
    ("물 H₂O", 1e-4, 1e-2, C["blue"]),
    ("요소, 글리세롤", 1e-6, 1e-5, C["purple"]),
    ("포도당", 1e-10, 1e-7, C["purple"]),
    ("Cl⁻", 1e-12, 1e-10, C["green"]),
    ("K⁺, Na⁺", 1e-14, 1e-12, C["green"]),
]
fig, ax = plt.subplots(figsize=(6.4, 2.9))
y = np.arange(len(rows))[::-1]
for yi, (name, lo, hi, col) in zip(y, rows):
    ax.barh(yi, hi - lo, left=lo, color=col, alpha=0.75, height=0.55)
ax.set_xscale("log")
ax.set_xlim(1e-15, 1e3)
ax.set_yticks(y)
ax.set_yticklabels([r[0].replace("H₂O", "H$_2$O").replace("O₂", "O$_2$") for r in rows], fontsize=9)
ticks = [1e-14, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1, 1e2]
ax.set_xticks(ticks)
ax.set_xticklabels(["10⁻¹⁴", "10⁻¹²", "10⁻¹⁰", "10⁻⁸", "10⁻⁶", "10⁻⁴", "10⁻²", "1", "10²"])
ax.minorticks_off()
ax.set_xlabel("지질 이중층 투과 계수 (cm/s, 로그 눈금)")
ax.annotate("", xy=(1e-13, 0.5), xytext=(1e-3, 0.5),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1))
ax.text(1e-8, 0.58, "약 10⁹–10¹⁰배", color=C["red"], fontsize=8.5, ha="center", va="bottom")
ax.set_ylim(-0.6, len(rows) - 0.4)
fig.tight_layout()
save(fig, __file__)
