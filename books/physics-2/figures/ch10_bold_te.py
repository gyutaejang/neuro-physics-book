from figstyle import plt, np, save, C

# BOLD 대비와 TE. 신호 S = S0 exp(-TE/T2*), 활성화 때 R2*가 dR만큼 준다.
TE = np.linspace(0, 120, 600) * 1e-3

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1))

# (가) 3 T 회백질: 휴지 신호와 활성-휴지 차이
T2s, dR = 45e-3, 0.4
rest = np.exp(-TE / T2s)
act = np.exp(-TE * (1 / T2s - dR))
diff = (act - rest) * 100
a1.plot(TE * 1e3, rest * 100, color=C["blue"], lw=1.8, label="휴지 신호 (왼쪽 눈금)")
a1.set_ylabel("신호 ($S_0$ 대비 %)")
a1.set_ylim(0, 105)
a1.set_xlabel("에코 시간 TE (ms)")
b1 = a1.twinx()
b1.plot(TE * 1e3, diff, color=C["red"], lw=1.8)
b1.set_ylim(0, 0.8)
b1.set_ylabel("활성 − 휴지 ($S_0$ 대비 %)", color=C["red"])
b1.tick_params(axis="y", colors=C["red"])
b1.spines["right"].set_visible(True)
b1.spines["right"].set_color(C["red"])
b1.spines["top"].set_visible(False)
i = np.argmax(diff)
b1.axvline(TE[i] * 1e3, color=C["gray"], lw=0.7, ls="--")
b1.annotate(f"최대: TE = $T_2^*$ = {TE[i]*1e3:.0f} ms", xy=(TE[i] * 1e3, diff[i]),
            xytext=(52, 0.74), fontsize=8, color=C["ink"],
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
b1.text(108, 0.47, "차이\n(오른쪽 눈금)", fontsize=8, color=C["red"], ha="center")
a1.text(50, 8, "휴지 신호\n(왼쪽 눈금)", fontsize=8, color=C["blue"], ha="left")
a1.set_title("(가) 3 T 회백질 ($T_2^*$ 45 ms)", fontsize=9.5)

# (나) 장 세기별 BOLD 차이 (M0 ∝ B0, 어림 값)
cases = [("1.5 T", 1.5, 60e-3, 0.2, C["gray"]),
         ("3 T", 3.0, 45e-3, 0.4, C["blue"]),
         ("7 T", 7.0, 28e-3, 1.0, C["red"])]
ref = 3.0 * 45e-3 * 0.4 / np.e
for name, B, t2, dr, col in cases:
    d = B * TE * np.exp(-TE / t2) * dr / ref
    a2.plot(TE * 1e3, d, color=col, lw=1.8)
    j = np.argmax(d)
    a2.plot(TE[j] * 1e3, d[j], "o", color=col, ms=4)
    a2.text(66, {"1.5 T": 3.0, "3 T": 3.35, "7 T": 3.7}[name],
            f"{name}: 최적 TE ≈ {t2*1e3:.0f} ms", fontsize=8.5, color=col)
a2.set_xlabel("에코 시간 TE (ms)")
a2.set_ylabel("BOLD 신호 차이 (3 T 최대 = 1)")
a2.set_ylim(0, 4.2)
a2.set_title("(나) 장 세기에 따른 최적 TE", fontsize=9.5)
fig.tight_layout(w_pad=2.2)
save(fig, __file__)
