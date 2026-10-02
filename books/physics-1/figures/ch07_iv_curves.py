from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1))

# (가) 옴 소자: 전도도가 기울기
V = np.linspace(-1, 1, 50)
for g, ls, lab in [(2.0, "-", "g = 2 S (R = 0.5 Ω)"), (1.0, "--", "g = 1 S (R = 1 Ω)"),
                   (0.5, ":", "g = 0.5 S (R = 2 Ω)")]:
    a1.plot(V, g * V, color=C["blue"], ls=ls, label=lab)
a1.axhline(0, color=C["gray"], lw=0.6)
a1.axvline(0, color=C["gray"], lw=0.6)
a1.set_xlabel("전압 V (V)")
a1.set_ylabel("전류 I (A)")
a1.set_title("(가) 옴의 법칙: 기울기 = 전도도", fontsize=10)
a1.legend(fontsize=7.5, loc="upper left")
a1.set_ylim(-2.1, 2.1)

# (나) 이온 통로: I = g (V - E)
Vm = np.linspace(-120, 80, 200)
EK, ENa = -90, 60
gK, gNa = 10e-12, 20e-12
IK = gK * (Vm - EK) * 1e-3 * 1e12   # pA
INa = gNa * (Vm - ENa) * 1e-3 * 1e12
a2.plot(Vm, IK, color=C["green"], label="K⁺ 통로 (10 pS)")
a2.plot(Vm, INa, color=C["red"], label="Na⁺ 통로 (20 pS)")
a2.axhline(0, color=C["gray"], lw=0.6)
a2.axvline(-70, color=C["gray"], lw=0.6, ls=":")
a2.scatter([EK, ENa], [0, 0], color=[C["green"], C["red"]], zorder=3, s=22)
a2.annotate("$E_K$ = −90 mV", xy=(EK, 0), xytext=(-112, 0.9), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.annotate("$E_{Na}$ = +60 mV", xy=(ENa, 0), xytext=(18, -1.6), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.text(-68, -3.3, "휴지 −70 mV", fontsize=7.5, color=C["gray"])
a2.text(-118, 2.0, "↑ 바깥향 전류 (+)", fontsize=7.5, va="top", color=C["ink"])
a2.text(-118, -1.2, "↓ 안쪽향 전류 (−)", fontsize=7.5, color=C["ink"])
a2.set_xlabel("막전위 V (mV)")
a2.set_ylabel("통로 전류 (pA)")
a2.set_title("(나) 이온 통로: I = g (V − E)", fontsize=10)
a2.legend(fontsize=7.5, loc="lower right")
a2.set_ylim(-3.8, 2.2)
fig.tight_layout()
save(fig, __file__)
