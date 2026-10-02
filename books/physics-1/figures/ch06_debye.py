from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.2), gridspec_kw=dict(width_ratios=[1, 1.15]))

# 왼쪽: 양이온 주위의 이온 구름 (도식)
rng = np.random.default_rng(3)
lam = 0.8
pts = []
while len(pts) < 70:
    x, y = rng.uniform(-2.6, 2.6, 2)
    r = np.hypot(x, y)
    if r < 0.45:
        continue
    # 가까울수록 음이온이 많고 양이온이 적다
    p_neg = 0.5 + 0.5 * np.exp(-(r - 0.45) / lam)
    pts.append((x, y, -1 if rng.random() < p_neg else +1))
for x, y, s in pts:
    a1.add_patch(plt.Circle((x, y), 0.11, facecolor="white", edgecolor=C["green"], lw=0.9))
    a1.text(x, y, "−" if s < 0 else "+", ha="center", va="center", fontsize=7, color=C["green"])
a1.add_patch(plt.Circle((0, 0), 0.28, facecolor=C["green"], edgecolor=C["green"]))
a1.text(0, 0, "+", ha="center", va="center", fontsize=12, color="white", weight="bold")
a1.add_patch(plt.Circle((0, 0), 1.0, fill=False, ls="--", color=C["gray"], lw=1))
a1.text(0, -1.12, "데바이 길이 (약 1 nm)", ha="center", va="top", fontsize=8.5, color=C["gray"],
        bbox=dict(facecolor="white", edgecolor="none", pad=1))
a1.set_xlim(-2.7, 2.7)
a1.set_ylim(-2.7, 2.7)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("가까이에 음이온이 더 모인다", fontsize=10)

# 오른쪽: 전위의 감소
r = np.linspace(0.3, 5, 300)
bare = 1 / r
scr = np.exp(-r / lam) / r
a2.semilogy(r, bare, color=C["gray"], ls="--", label="가림이 없을 때 (1/r)")
a2.semilogy(r, scr, color=C["green"], lw=2, label="염용액 150 mM (가림)")
a2.axvline(lam, color=C["gray"], lw=0.6, ls=":")
a2.text(lam + 0.08, 2e-3, "데바이 길이 0.8 nm", fontsize=8.5, color=C["gray"])
a2.annotate("5 nm에서는\n가림 없을 때의\n약 500분의 1", xy=(5, scr[-1]), xytext=(1.3, 2.2e-4), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.set_xlabel("이온 중심에서 거리 (nm)")
a2.set_ylabel("전위 (상대값, 로그 눈금)")
a2.set_ylim(1e-4, 5)
a2.set_xlim(0, 5.2)
a2.legend(fontsize=8, loc="upper right")
fig.tight_layout()
save(fig, __file__)
