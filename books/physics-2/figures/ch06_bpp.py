from figstyle import plt, np, save, C

# BPP(블룸베르헌-퍼셀-파운드) 모형: 쌍극자 상호작용의 상관 시간 τc에 따른 T1, T2.
# 상수 K는 τc = 3 ps에서 T1 ≈ 4 s(자유 물, 뇌척수액 어림)가 되도록 맞췄다.
K = 1 / (5 * 3e-12 * 4.0)
gam = 2 * np.pi * 42.58e6
tc = np.logspace(-12, -5, 600)


def J(w):
    return tc / (1 + (w * tc) ** 2)


fig, ax = plt.subplots(figsize=(6.6, 3.4))
for B, col, ls in ((1.5, C["gray"], "-"), (3.0, C["blue"], "-"), (7.0, C["red"], "-")):
    w0 = gam * B
    R1 = K * (J(w0) + 4 * J(2 * w0))
    ax.loglog(tc, 1 / R1, color=col, ls=ls, label=f"T1 ({B:g} T)")
    if B == 3.0:
        R2 = K / 2 * (3 * tc + 5 * J(w0) + 2 * J(2 * w0))
        ax.loglog(tc, 1 / R2, color=C["purple"], lw=1.8, label="T2 (3 T)")
        k = np.argmax(R1)
        ax.plot(tc[k], 1 / R1[k], "o", ms=4, color=col)
        ax.annotate(f"3 T의 T1 최소\nτc ≈ {tc[k]*1e9:.1f} ns", (tc[k], 1 / R1[k]),
                    xytext=(tc[k] * 0.06, 1 / R1[k] * 0.04), fontsize=8, color=col,
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.6))
        print("T1 min", tc[k], 1 / R1[k])
ax.axvspan(1e-12, 1e-11, color=C["light"], zorder=0)
ax.text(3e-12, 2.2e-5, "자유 물\n(ps)", ha="center", fontsize=8.5)
ax.text(3e-9, 2.2e-5, "거대분자에\n붙은 물 (ns)", ha="center", fontsize=8.5)
ax.text(6e-8, 2.2e-5, "거대분자 자신의\n수소 (μs)", ha="center", fontsize=8.5)
ax.text(2e-12, 6, "T1 ≈ T2", fontsize=8.5, color=C["ink"])
ax.set_xlim(1e-12, 1e-5)
ax.set_ylim(1e-5, 30)
ax.set_xlabel("상관 시간 τc (s): 오른쪽일수록 느린 움직임")
ax.set_ylabel("이완 시간 (s)")
ax.legend(fontsize=8, loc="lower left", bbox_to_anchor=(0.0, 0.2), ncol=1)
save(fig, __file__)
