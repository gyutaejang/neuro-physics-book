from figstyle import plt, np, save, C

# A ⇌ B, kf = 0.3 /s, kr = 0.1 /s → K = 3, 평형에서 B 75 %
kf, kr = 0.3, 0.1
t = np.linspace(0, 15, 300)
beq = kf / (kf + kr)
lam = kf + kr

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0))

# 왼쪽: 두 출발점에서 같은 평형으로
for b0, ls, lab in ((0.0, "-", "A만 넣고 시작"), (1.0, "--", "B만 넣고 시작")):
    b = beq + (b0 - beq) * np.exp(-lam * t)
    a1.plot(t, b, color=C["blue"], ls=ls, lw=1.6, label=f"[B], {lab}")
    a1.plot(t, 1 - b, color=C["red"], ls=ls, lw=1.2, alpha=0.8)
a1.axhline(beq, color=C["gray"], lw=0.6, ls=":")
a1.axhline(1 - beq, color=C["gray"], lw=0.6, ls=":")
a1.text(15, beq + 0.03, "평형 [B] = 0.75", ha="right", va="bottom", fontsize=8.5, color=C["blue"])
a1.text(15, 1 - beq + 0.03, "평형 [A] = 0.25", ha="right", va="bottom", fontsize=8.5, color=C["red"])
a1.set_xlabel("시간 (s)")
a1.set_ylabel("농도 (상대값)")
a1.set_title("농도: 출발점과 상관없이 같은 곳으로")
a1.set_ylim(-0.03, 1.1)
a1.legend(fontsize=7.5, loc="center right", bbox_to_anchor=(1.0, 0.58))

# 오른쪽: 정반응과 역반응 속도
b = beq * (1 - np.exp(-lam * t))
a2.plot(t, kf * (1 - b), color=C["blue"], lw=1.6, label="정반응 속도  $k_f$[A]")
a2.plot(t, kr * b, color=C["red"], lw=1.6, label="역반응 속도  $k_r$[B]")
a2.axvspan(9, 15, color=C["light"], lw=0)
a2.text(12, 0.14, "두 속도가 같다\n= 동적 평형", ha="center", va="center", fontsize=8.5)
a2.set_xlabel("시간 (s)")
a2.set_ylabel("속도 (상대값/s)")
a2.set_title("속도: A만 넣고 시작한 경우")
a2.set_ylim(0, 0.32)
a2.legend(fontsize=8, loc="upper right")
fig.tight_layout()
save(fig, __file__)
