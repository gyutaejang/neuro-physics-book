from figstyle import plt, np, save, C

# 복소 지수 e^{iωt}: 복소평면의 단위원 위를 도는 화살표(페이저).
f = 1.0                      # 1초에 한 바퀴
t = np.linspace(0, 2, 800)
z = np.exp(1j * 2 * np.pi * f * t)

fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1.6], hspace=0.35, wspace=0.28)
a0 = fig.add_subplot(gs[:, 0])
a1 = fig.add_subplot(gs[0, 1])
a2 = fig.add_subplot(gs[1, 1], sharex=a1)

th = np.linspace(0, 2 * np.pi, 300)
a0.plot(np.cos(th), np.sin(th), color=C["gray"], lw=0.8)
a0.axhline(0, color=C["gray"], lw=0.5)
a0.axvline(0, color=C["gray"], lw=0.5)
t0 = 1 / 6
zz = np.exp(1j * 2 * np.pi * f * t0)
a0.annotate("", xy=(zz.real, zz.imag), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.8))
a0.plot([zz.real, zz.real], [0, zz.imag], color=C["red"], lw=1.4, ls="--")
a0.plot([0, 0], [0, zz.imag], color=C["blue"], lw=3, alpha=0.8)
a0.plot([0, zz.real], [0, 0], color=C["red"], lw=3, alpha=0.8)
ang = np.linspace(0, 2 * np.pi * f * t0, 40)
a0.plot(0.28 * np.cos(ang), 0.28 * np.sin(ang), color=C["ink"], lw=0.8)
a0.annotate("위상\nφ = ωt", xy=(0.27, 0.12), xytext=(0.58, 0.3), fontsize=8, va="center",
            arrowprops=dict(arrowstyle="-", color=C["ink"], lw=0.5))
a0.text(zz.real + 0.05, zz.imag + 0.08, "$e^{i\\omega t}$", fontsize=10, color=C["purple"])
a0.text(0.25, -0.1, "실수부\ncos ωt", fontsize=8, color=C["red"], ha="center", va="top")
a0.text(-0.08, 0.45, "허수부\nsin ωt", fontsize=8, color=C["blue"], ha="right", va="center")
a0.annotate("", xy=(-0.62, 0.86), xytext=(-0.86, 0.55),
            arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=0.9,
                            connectionstyle="arc3,rad=-0.25"))
a0.text(-1.12, 1.0, "시계 반대 방향\n1초에 f 바퀴", fontsize=7.5, color=C["gray"], va="bottom")
a0.text(1.25, -0.05, "실수축", fontsize=7.5, color=C["gray"], ha="right", va="top")
a0.text(0.05, 1.15, "허수축", fontsize=7.5, color=C["gray"], va="top")
a0.set_xlim(-1.25, 1.25)
a0.set_ylim(-1.25, 1.35)
a0.set_aspect("equal")
a0.axis("off")
a0.set_title("(가) 복소평면에서 도는 화살표", fontsize=10)

a1.plot(t, z.real, color=C["red"])
a1.set_ylabel("실수부", fontsize=9)
a1.set_title("(나) 그림자 두 개: 코사인과 사인", fontsize=10)
a2.plot(t, z.imag, color=C["blue"])
a2.set_ylabel("허수부", fontsize=9)
a2.set_xlabel("시간 (s)")
for a in (a1, a2):
    a.axhline(0, color=C["gray"], lw=0.5)
    a.set_ylim(-1.3, 1.3)
    a.set_yticks([-1, 0, 1])
    a.axvline(t0, color=C["purple"], lw=0.8, ls=":")
a1.text(t0 + 0.03, 1.08, "(가)의 순간", fontsize=7.5, color=C["purple"])
plt.setp(a1.get_xticklabels(), visible=False)
a2.set_xlim(0, 2)
save(fig, __file__)
