from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(width_ratios=[1.15, 1]))

# 왼쪽: 얼음 융해. ΔH(일정)와 TΔS(온도에 비례)를 겹쳐 그리면 ΔG는 두 선의 간격이다.
dH, dS = 6.01, 22.0e-3  # kJ/mol, kJ/(mol·K)
T = np.linspace(240, 320, 200)
a1.plot(T, np.full_like(T, dH), color=C["red"], lw=1.8, label="ΔH (+6.0 kJ/mol)")
a1.plot(T, T * dS, color=C["purple"], lw=1.8, label="TΔS")
a1.fill_between(T, dH, T * dS, where=T < 273.15, color=C["red"], alpha=0.12, lw=0)
a1.fill_between(T, dH, T * dS, where=T > 273.15, color=C["blue"], alpha=0.15, lw=0)
a1.axvline(273.15, color=C["gray"], lw=0.7, ls=":")
a1.text(271.5, 7.05, "0 °C\nΔG = 0", fontsize=8, color=C["gray"], ha="right", va="top")
a1.text(252, 6.06, "ΔG > 0\n얼음이 안정", fontsize=8.5, color=C["red"], ha="center", va="bottom")
a1.text(300, 6.25, "ΔG < 0\n물이 안정", fontsize=8.5, color=C["blue"], ha="center")
# 37 °C에서의 간격
t37 = 310.15
a1.annotate("", xy=(t37, t37 * dS), xytext=(t37, dH),
            arrowprops=dict(arrowstyle="<->", color=C["blue"], lw=1))
a1.text(t37 + 1.2, (dH + t37 * dS) / 2, "37 °C\nΔG ≈ −0.8", fontsize=8, color=C["blue"], va="center")
a1.set_xlabel("온도 (K)")
a1.set_ylabel("kJ/mol")
a1.set_xlim(240, 325)
a1.set_ylim(5.2, 7.3)
a1.legend(fontsize=7.5, loc="upper left")
a1.set_title("얼음이 녹는 반응: ΔG = ΔH − TΔS", fontsize=10)

# 오른쪽: ΔH와 ΔS의 부호에 따른 네 경우
a2.set_xlim(-1, 1)
a2.set_ylim(-1, 1)
a2.axhline(0, color=C["gray"], lw=0.8)
a2.axvline(0, color=C["gray"], lw=0.8)
cells = [
    (0.5, 0.5, "높은 온도에서만\n자발적", "얼음 융해, 소수성 효과", C["purple"]),
    (-0.5, 0.5, "언제나 자발적", "포도당 연소", C["green"]),
    (-0.5, -0.5, "낮은 온도에서만\n자발적", "물이 어는 것", C["blue"]),
    (0.5, -0.5, "언제나\n비자발적", "연소의 역반응", C["red"]),
]
for x, y, t, ex, col in cells:
    a2.text(x, y + 0.12, t, ha="center", va="center", fontsize=8.8, color=col, weight="bold")
    a2.text(x, y - 0.3, ex, ha="center", va="center", fontsize=7.5, color=C["ink"])
a2.set_xticks([-0.5, 0.5])
a2.set_xticklabels(["ΔH < 0", "ΔH > 0"])
a2.set_yticks([-0.5, 0.5])
a2.set_yticklabels(["ΔS < 0", "ΔS > 0"])
a2.tick_params(length=0)
for s in a2.spines.values():
    s.set_visible(False)
a2.set_title("ΔG < 0 이 되는 조건", fontsize=10)
fig.tight_layout()
save(fig, __file__)
