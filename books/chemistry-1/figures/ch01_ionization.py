from figstyle import plt, np, save, C

# 1차 이온화 에너지 (eV), Z = 1–36 (NIST)
ie = [13.598, 24.587, 5.392, 9.323, 8.298, 11.260, 14.534, 13.618, 17.423, 21.565,
      5.139, 7.646, 5.986, 8.152, 10.487, 10.360, 12.968, 15.760,
      4.341, 6.113, 6.561, 6.828, 6.746, 6.767, 7.434, 7.902, 7.881, 7.640, 7.726, 9.394,
      5.999, 7.900, 9.789, 9.752, 11.814, 14.000]
syms = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split()
Z = np.arange(1, 37)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1.45, 1]))
a1.plot(Z, ie, color=C["blue"], lw=1.2, marker="o", ms=3)
for z in (2, 10, 18, 36):
    a1.annotate(syms[z - 1], (z, ie[z - 1]), xytext=(0, 4), textcoords="offset points",
                ha="center", fontsize=8.5, color=C["blue"])
for z in (3, 11, 19):
    a1.annotate(syms[z - 1], (z, ie[z - 1]), xytext=(0, -11), textcoords="offset points",
                ha="center", fontsize=8.5, color=C["red"])
for z, off in ((17, (-9, 3)), (20, (3, -11))):
    a1.annotate(syms[z - 1], (z, ie[z - 1]), xytext=off, textcoords="offset points",
                ha="center", fontsize=8, color=C["ink"])
a1.text(28, 21.5, "비활성 기체 (파랑): 전자를 떼기 가장 어렵다\n알칼리 금속 (빨강): 가장 쉽다",
        ha="center", fontsize=8, color=C["ink"])
a1.set_xlabel("원자번호 Z")
a1.set_ylabel("1차 이온화 에너지 (eV)")
a1.set_xlim(0, 37)
a1.set_ylim(0, 27)
for z0 in (2.5, 10.5, 18.5):
    a1.axvline(z0, color=C["gray"], lw=0.5, ls=":")

# 오른쪽: 차례 이온화 에너지
data = [("Na", [5.14, 47.3, 71.6], C["green"]), ("Mg", [7.65, 15.0, 80.1], C["green"]),
        ("Ca", [6.11, 11.9, 50.9], C["green"])]
w = 0.26
for i, (name, vals, col) in enumerate(data):
    for k, v in enumerate(vals):
        x = i + (k - 1) * w
        valence = 1 if name == "Na" else 2  # 바깥 껍질 전자 수
        a2.bar(x, v, width=w * 0.92, color=C["green"] if k < valence else C["red"],
               alpha=0.9 if k == 0 else 0.6, edgecolor="white")
        a2.text(x, v * 1.08, f"{v:.0f}" if v > 10 else f"{v:.1f}", ha="center", va="bottom", fontsize=7)
a2.set_yscale("log")
a2.set_ylim(2, 300)
a2.set_xticks(range(3))
a2.set_xticklabels(["Na\n(→ Na⁺)", "Mg\n(→ Mg²⁺)", "Ca\n(→ Ca²⁺)"], fontsize=8.5)
a2.set_yticks([3, 10, 30, 100])
a2.set_yticklabels(["3", "10", "30", "100"])
a2.minorticks_off()
a2.set_ylabel("이온화 에너지 (eV, 로그 눈금)")
a2.text(1, 190, "막대: 1번째, 2번째, 3번째 전자\n빨강 = 안쪽 껍질을 깨야 하는 전자",
        ha="center", va="bottom", fontsize=7.5, color=C["ink"])
a2.set_ylim(2, 600)
fig.tight_layout()
save(fig, __file__)
