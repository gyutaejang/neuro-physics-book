from figstyle import plt, np, save, C

# 수소 원자의 에너지 준위 E_n = -13.6 eV / n^2 와 발머 계열(n -> 2) 전이.
Ry = 13.6057
hc = 1239.84
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.3, 3.5), gridspec_kw={"width_ratios": [1.15, 1]})

E = lambda n: -Ry / n ** 2
for n in range(1, 8):
    ax.plot([0, 1], [E(n)] * 2, color=C["ink"], lw=1.2 if n < 6 else 0.6)
    if n <= 3:
        ax.text(1.04, E(n), f"n = {n}   {E(n):.2f} eV", va="center", fontsize=8)
ax.text(1.04, -0.62, "n = 4, 5, …", va="center", fontsize=8)
ax.plot([0, 1], [0, 0], color=C["gray"], lw=0.8, ls="--")
ax.text(1.04, 0.45, "n = ∞  0 eV (전리)", va="bottom", fontsize=8, color=C["gray"])

# 라이먼 α (자외선)
ax.annotate("", xy=(0.12, E(1)), xytext=(0.12, E(2)),
            arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.3))
ax.text(0.15, -7.0, "라이먼 α\n121.5 nm\n(자외선)", fontsize=7.5, color=C["purple"], va="center")
cols = {3: "#c0392b", 4: "#1f9bb5", 5: "#3b4cc0", 6: "#6a3d9a"}
for i, n in enumerate([3, 4, 5, 6]):
    x = 0.5 + 0.11 * i
    ax.annotate("", xy=(x, E(2)), xytext=(x, E(n)),
                arrowprops=dict(arrowstyle="-|>", color=cols[n], lw=1.3))
ax.text(0.47, -3.75, "발머 계열\n(가시광, n → 2)", fontsize=7.5, color=C["ink"], va="top")
ax.set_xlim(0, 1.75)
ax.set_ylim(-14.5, 1.6)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.set_ylabel("전자의 에너지 (eV)")
ax.set_title("(가) 수소의 에너지 준위", fontsize=10.5)

# (나) 선 스펙트럼
for n in [3, 4, 5, 6]:
    lam = hc / (Ry * (0.25 - 1 / n ** 2))
    bx.plot([lam, lam], [0, 1], color=cols[n], lw=3)
    bx.text(lam + (-6 if n == 6 else 6 if n == 5 else 0), 1.05, f"{lam:.0f}", ha="center", va="bottom", fontsize=8)
    bx.text(lam + (-6 if n == 6 else 6 if n == 5 else 0), -0.06, f"{n}→2", ha="center", va="top", fontsize=7.5, color=C["gray"])
bx.set_xlim(380, 700)
bx.set_ylim(-0.3, 1.35)
bx.set_yticks([])
bx.spines["left"].set_visible(False)
bx.set_xlabel("파장 (nm)")
bx.set_facecolor("#1d1d1d")
bx.set_title("(나) 수소 기체가 내는 선 스펙트럼", fontsize=10.5)
for t in bx.texts:
    if t.get_color() == C["gray"]:
        t.set_color("#bbbbbb")
    else:
        t.set_color("white")
fig.tight_layout()
save(fig, __file__)
