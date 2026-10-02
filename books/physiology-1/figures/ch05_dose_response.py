from figstyle import plt, np, save, C

# 블랙-레프 조작 모형: E/Emax = τ[A] / (K_A + (1 + τ)[A]),  점유율 θ = [A]/([A] + K_A)
a = np.logspace(-3, 3, 400)        # K_A의 배수
def resp(a, tau):
    return tau * a / (1 + (1 + tau) * a)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0))
occ = a / (1 + a)
a1.semilogx(a, occ * 100, color=C["gray"], lw=1.2, ls=":", label="점유율 (두 약물 공통)")
a1.semilogx(a, resp(a, 10) * 100, color=C["blue"], lw=1.8, label="완전 작용제 (τ = 10)")
a1.semilogx(a, resp(a, 0.5) * 100, color=C["green"], lw=1.8, label="부분 작용제 (τ = 0.5)")
a1.semilogx(a, resp(a / 10, 10) * 100, color=C["blue"], lw=1.4, ls="--",
            label="완전 작용제 + 경쟁 길항제")
a1.scatter([1 / 11], [100 * resp(1 / 11, 10)], color=C["red"], s=18, zorder=4)
a1.annotate("EC50 = $K_A$/11\n(점유율 약 8 %)", xy=(1 / 11, 100 * resp(1 / 11, 10)), xytext=(0.0012, 50), fontsize=7.8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a1.set_xlabel("작용제 농도 ($K_A$의 배수, 로그 눈금)")
a1.set_ylabel("계의 최대 반응 대비 (%)")
a1.set_ylim(0, 105)
a1.legend(fontsize=7, loc="upper left", bbox_to_anchor=(0.0, 0.93))

th = np.linspace(0, 1, 200)
for tau, col, lab in ((10, C["blue"], "τ = 10"), (0.5, C["green"], "τ = 0.5")):
    a2.plot(th * 100, tau * th / (1 + tau * th) * 100, color=col, lw=1.8, label=lab)
a2.plot([0, 100], [0, 100], color=C["gray"], lw=0.8, ls=":")
a2.scatter([10], [50], color=C["red"], s=18, zorder=4)
a2.annotate("수용체 10 %만 차도\n반응은 절반", xy=(10, 50), xytext=(25, 30), fontsize=7.8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.text(98, 37, "다 채워도 33 %", ha="right", fontsize=7.8, color=C["green"])
a2.set_xlabel("수용체 점유율 (%)")
a2.set_ylabel("계의 최대 반응 대비 (%)")
a2.set_xlim(0, 100)
a2.set_ylim(0, 105)
a2.legend(fontsize=7.5, loc="lower right")
fig.tight_layout()
save(fig, __file__)
