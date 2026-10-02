from figstyle import plt, np, save, C

# 3 T 세로 자화 회복. (가) 포화(90°) 뒤 회복, (나) 반전(180°) 뒤 회복.
T1 = [("백질", 0.85, C["blue"]), ("회백질", 1.35, C["green"]), ("뇌척수액", 4.0, C["purple"])]
t = np.linspace(0, 6, 600)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(wspace=0.32))
for name, T, col in T1:
    a1.plot(t, 1 - np.exp(-t / T), color=col, label=f"{name} (T1 {T:g} s)")
    a2.plot(t, 1 - 2 * np.exp(-t / T), color=col)
    tn = T * np.log(2)
    a2.plot(tn, 0, "o", ms=4.5, color=col)
    off = {0.85: (-0.62, 0.1), 1.35: (0.2, -0.2), 4.0: (0.2, -0.2)}[T]
    a2.text(tn + off[0], off[1], f"{tn:.2f} s", fontsize=8, color=col,
            va="bottom" if off[1] > 0 else "top")
# 회백질 T1에서 63%
a1.plot([1.35, 1.35], [0, 1 - np.exp(-1)], color=C["gray"], lw=0.7, ls=":")
a1.plot([0, 1.35], [1 - np.exp(-1)] * 2, color=C["gray"], lw=0.7, ls=":")
a1.text(1.9, 0.6, "점선: t = T1에서 63%", fontsize=8, color=C["gray"])
a1.axvline(0.5, color=C["red"], lw=0.8, ls="--")
a1.text(0.55, 0.05, "TR 0.5 s", fontsize=8, color=C["red"])
a1.set_ylim(0, 1.05)
a1.set_title("(가) 90° 펄스 뒤 회복", fontsize=10)
a1.legend(fontsize=8, loc="lower right")
a2.axhline(0, color=C["gray"], lw=0.6)
a2.set_ylim(-1.05, 1.05)
a2.set_title("(나) 180° 펄스 뒤 회복", fontsize=10)
a2.text(3.2, -0.62, "● 0을 지나는 시각\n   TI = T1 ln 2", fontsize=8, color=C["ink"])
for ax in (a1, a2):
    ax.set_xlim(0, 6)
    ax.set_xlabel("시간 (s)")
    ax.set_ylabel("$M_z / M_0$")
save(fig, __file__)
