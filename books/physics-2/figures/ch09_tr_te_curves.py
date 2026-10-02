from figstyle import plt, np, save, C

# 3 T 어림값: (T1 ms, T2 ms, 양성자 밀도)
tissues = {
    "백질": (850, 75, 0.70, C["blue"], "-"),
    "회백질": (1400, 100, 0.80, C["red"], "-"),
    "뇌척수액": (4000, 2000, 1.00, C["green"], "--"),
}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
TR = np.linspace(0, 6000, 600)
for name, (T1, T2, PD, col, ls) in tissues.items():
    a1.plot(TR, PD * (1 - np.exp(-TR / T1)), color=col, ls=ls, label=name)
a1.axvspan(400, 700, color=C["light"], zorder=0)
a1.text(550, 1.02, "T1 강조\n(짧은 TR)", ha="center", va="bottom", fontsize=8)
a1.axvline(4000, color=C["gray"], lw=0.6, ls=":")
a1.text(4080, 1.1, "긴 TR", fontsize=8, color=C["gray"])
a1.set_xlim(0, 6000)
a1.set_ylim(0, 1.2)
a1.set_xlabel("TR (ms)")
a1.set_ylabel("다음 펄스 직전의 $M_z$ / $M_0$(물)")
a1.set_title("(가) TR: 세로 자화가 얼마나 돌아왔나", fontsize=9.5, loc="left")

TE = np.linspace(0, 300, 600)
for name, (T1, T2, PD, col, ls) in tissues.items():
    a2.plot(TE, PD * (1 - np.exp(-4000 / T1)) * np.exp(-TE / T2), color=col, ls=ls, label=name)
a2.axvspan(5, 15, color=C["light"], zorder=0)
a2.axvspan(80, 110, color=C["light"], zorder=0)
a2.text(17, 0.8, "PD 강조", ha="left", va="bottom", fontsize=8)
a2.text(95, 0.78, "T2 강조", ha="center", va="bottom", fontsize=8)
a2.set_xlim(0, 300)
a2.set_ylim(0, 0.9)
a2.set_xlabel("TE (ms)")
a2.set_ylabel("신호 (TR = 4000 ms)")
a2.legend(fontsize=8, loc="center right", bbox_to_anchor=(1.0, 0.42))
a2.set_title("(나) TE: 가로 자화가 얼마나 남았나", fontsize=9.5, loc="left")
fig.tight_layout(w_pad=2)
save(fig, __file__)
