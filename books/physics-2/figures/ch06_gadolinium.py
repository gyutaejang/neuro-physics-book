from figstyle import plt, np, save, C

# 가돌리늄 조영제: 1/T1 = 1/T1,0 + r1·C. r1 = 4 L/(mmol·s) (3 T, 제제에 따라 대략 3–5).
r1 = 4.0
c = np.linspace(0, 2, 401)                        # mM
tis = [("혈액 (T1,0 = 1.65 s)", 1.65, C["red"]), ("회백질 (T1,0 = 1.35 s)", 1.35, C["green"]),
       ("백질 (T1,0 = 0.85 s)", 0.85, C["blue"])]
TR = 0.5
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(wspace=0.32))
for name, T10, col in tis:
    R1 = 1 / T10 + r1 * c
    a1.plot(c, R1, color=col, label=name)
    a2.plot(c, 1 - np.exp(-TR * R1), color=col)
a1.set_xlabel("조영제 농도 (mM)")
a1.set_ylabel("$R_1 = 1/T_1$ (s$^{-1}$)")
a1.set_title("(가) 이완율은 농도에 비례해 는다", fontsize=10)
a1.text(1.0, 2.0, "기울기 = $r_1$\n= 4 s$^{-1}$ mM$^{-1}$", fontsize=8.5, color=C["ink"])
a1.legend(fontsize=7.8, loc="upper left")
a1.set_xlim(0, 2); a1.set_ylim(0, 10)
a2.set_xlabel("조영제 농도 (mM)")
a2.set_ylabel("$M_z/M_0$ (TR 0.5 s)")
a2.set_title("(나) T1 강조 신호는 포화된다", fontsize=10)
a2.set_xlim(0, 2); a2.set_ylim(0, 1.05)
a2.axvline(0.2, color=C["gray"], lw=0.7, ls=":")
a2.text(0.24, 0.08, "0.2 mM", fontsize=8, color=C["gray"])
save(fig, __file__)
