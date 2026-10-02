from figstyle import plt, np, save, C

t = np.linspace(0, 10, 1001)          # 분
dt = t[1] - t[0]
D = 0.1                                # mmol/kg
Cp = D * (3.99 * np.exp(-0.144 * t) + 4.78 * np.exp(-0.0111 * t))   # 혈장 농도 (mM), 바이크스포넨셜 모형
Cp[0] = 0


def tofts(ktrans, ve, vp):
    kep = ktrans / ve if ve > 0 else 0
    conv = np.array([np.sum(Cp[:i + 1] * np.exp(-kep * (t[i] - t[:i + 1]))) * dt for i in range(len(t))])
    return vp * Cp + ktrans * conv


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
for k, ve, vp, col, lab in ((0.0, 0.2, 0.03, C["gray"], "정상 회백질 (Ktrans ≈ 0)"),
                            (0.01, 0.2, 0.03, C["purple"], "활성 탈수초 병변 0.01/분"),
                            (0.10, 0.3, 0.06, C["red"], "고등급 종양 0.10/분")):
    a1.plot(t, tofts(k, ve, vp), color=col, lw=1.7, label=lab)
a1.plot(t, Cp * 0.1, color=C["blue"], lw=1.0, ls="--", label="혈장 농도 × 0.1")
a1.set_xlabel("주사 뒤 시간 (분)")
a1.set_ylabel("조직 조영제 농도 (mM)")
a1.set_title("조직에 쌓이는 조영제 (토프츠 모형)", fontsize=10)
a1.set_xlim(0, 10)
a1.set_ylim(0, 0.25)
a1.legend(fontsize=7.2, loc="center right", bbox_to_anchor=(1.0, 0.5))

# 오른쪽: Ktrans = Fp (1 - exp(-PS/Fp)) — 혈류 제한과 투과 제한
PS = np.logspace(-3, 1, 300)          # 1/분
for Fp, col in ((0.15, C["purple"]), (0.30, C["blue"])):
    a2.plot(PS, Fp * (1 - np.exp(-PS / Fp)), color=col, lw=1.8, label=f"혈장 흐름 Fp = {Fp:.2f}/분")
a2.plot(PS, PS, color=C["gray"], lw=0.8, ls=":")
a2.text(0.0013, 0.03, "Ktrans ≈ PS\n(투과 제한)", fontsize=7.5, color=C["gray"])
a2.text(1.3, 0.42, "Ktrans ≈ Fp\n(혈류 제한)", fontsize=7.5, color=C["gray"], ha="center")
a2.set_xscale("log")
a2.set_yscale("log")
a2.set_xlim(1e-3, 10)
a2.set_ylim(1e-3, 1)
a2.set_xlabel("투과도·표면적 곱 PS (1/분)")
a2.set_ylabel("Ktrans (1/분)")
a2.set_title("Ktrans는 투과와 혈류의 혼합", fontsize=10)
a2.legend(fontsize=7.2, loc="lower right")
fig.tight_layout()
save(fig, __file__)
