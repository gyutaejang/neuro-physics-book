from figstyle import plt, np, save, C

E = 0.1      # 탄성 계수 (1/mL)
P0 = 10.0    # 출발 두개내압 (mmHg)
dV = np.linspace(-8, 30, 400)
P = P0 * np.exp(E * dV)

fig, ax = plt.subplots(figsize=(6.6, 3.4))
ax.plot(dV, P, color=C["blue"], lw=2)
ax.axhspan(5, 15, color=C["green"], alpha=0.12, lw=0)
ax.text(29.5, 7.5, "정상 범위 5–15 mmHg", ha="right", fontsize=8, color=C["green"])
ax.axhline(22, color=C["red"], lw=0.9, ls="--")
ax.text(-7.5, 23.2, "치료 문턱 약 20–22 mmHg", fontsize=8, color=C["red"])

# 같은 맥박 부피 1 mL가 만드는 압력 진폭
for v0, lab in ((0, "ICP 10에서\n맥박 진폭 약 1 mmHg"), (11, "ICP 30에서\n약 3 mmHg")):
    p_lo, p_hi = P0 * np.exp(E * v0), P0 * np.exp(E * (v0 + 1))
    ax.plot([v0, v0 + 1], [p_lo, p_lo], color=C["gray"], lw=1)
    ax.plot([v0 + 1, v0 + 1], [p_lo, p_hi], color=C["red"], lw=2.2)
    ax.annotate(lab, xy=(v0 + 1, (p_lo + p_hi) / 2), xytext=(v0 + 4, (p_lo + p_hi) / 2 - 1),
                fontsize=8, va="center", arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))

ax.annotate("+10 mL → 약 27 mmHg", xy=(10, P0 * np.e), xytext=(13.5, 17), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.8))
ax.scatter([0, 10], [P0, P0 * np.e], color=C["blue"], s=22, zorder=4)
ax.text(-7.5, 40, "보상 구간:\n뇌척수액과 정맥혈이\n밀려나 압력이 덜 오른다", fontsize=8, color=C["gray"])
ax.text(21, 35, "비보상 구간:\n조금만 늘어도\n압력이 가파르게 오른다", fontsize=8, color=C["gray"])
ax.set_xlim(-8, 30)
ax.set_ylim(0, 62)
ax.set_xlabel("두개 안에 더해진 부피 (mL)")
ax.set_ylabel("두개내압 (mmHg)")
fig.tight_layout()
save(fig, __file__)
