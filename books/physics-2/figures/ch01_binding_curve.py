from figstyle import plt, np, save, C

# 핵자당 결합 에너지. 점은 측정값(원자 질량 평가표 AME 기준, MeV),
# 회색 선은 반경험적 질량 공식(액체 방울 모형)으로 안정선 위를 계산한 것.
data = {"²H": (2, 1.112), "³He": (3, 2.573), "⁴He": (4, 7.074), "⁶Li": (6, 5.332), "⁷Li": (7, 5.606),
        "⁹Be": (9, 6.463), "¹⁰B": (10, 6.475), "¹²C": (12, 7.680), "¹⁴N": (14, 7.476), "¹⁶O": (16, 7.976),
        "¹⁹F": (19, 7.779), "²⁰Ne": (20, 8.032), "²³Na": (23, 8.112), "²⁴Mg": (24, 8.261), "²⁸Si": (28, 8.448),
        "³¹P": (31, 8.481), "⁴⁰Ca": (40, 8.551), "⁵⁶Fe": (56, 8.790), "⁶²Ni": (62, 8.795), "⁹⁰Zr": (90, 8.710),
        "¹²⁰Sn": (120, 8.505), "¹⁵⁸Gd": (158, 8.202), "²⁰⁸Pb": (208, 7.867), "²³⁵U": (235, 7.591), "²³⁸U": (238, 7.570)}
A = np.arange(10, 261)
Z = A / (2 + 0.0155 * A ** (2 / 3))
B = 15.75 * A - 17.8 * A ** (2 / 3) - 0.711 * Z ** 2 / A ** (1 / 3) - 23.7 * (A - 2 * Z) ** 2 / A

fig, ax = plt.subplots(figsize=(6.8, 3.4))
ax.plot(A, B / A, color=C["gray"], lw=1.2, label="액체 방울 모형")
xs = [v[0] for v in data.values()]
ys = [v[1] for v in data.values()]
ax.scatter(xs, ys, s=16, color=C["blue"], zorder=3, label="측정값")
show = {"²H": (1.12, 0), "³He": (1.12, 0), "⁴He": (0.75, 0.25), "⁶Li": (1.1, -0.25), "¹²C": (0.97, 0.33),
        "¹⁴N": (1.0, -0.38), "¹⁶O": (1.0, 0.33), "²³Na": (1.0, -0.38), "³¹P": (1.0, -0.38),
        "⁵⁶Fe": (1.0, 0.3), "¹⁵⁸Gd": (1.0, 0.3), "²³⁸U": (0.97, 0.3)}
for k, (fx, dy) in show.items():
    x, y = data[k]
    ax.text(x * fx, y + dy, k, fontsize=8, ha="left" if fx > 1.05 else "center", va="center")
ax.set_xscale("log")
ax.set_xticks([2, 5, 10, 20, 50, 100, 200])
ax.set_xticklabels(["2", "5", "10", "20", "50", "100", "200"])
ax.minorticks_off()
ax.annotate("", xy=(30, 4.6), xytext=(4.5, 4.6), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4))
ax.text(5, 4.25, "핵융합 (가벼운 핵을 합침)", fontsize=8.5, color=C["red"], va="top")
ax.annotate("", xy=(100, 6.6), xytext=(235, 6.6), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4))
ax.text(235, 6.25, "핵분열 (무거운 핵을 쪼갬)", fontsize=8.5, color=C["red"], va="top", ha="right")
ax.text(30, 9.25, "가장 단단한 핵: 철·니켈 근처 (약 8.8 MeV)", fontsize=8.5, ha="center")
ax.set_xlim(1.6, 300)
ax.set_ylim(0.5, 9.6)
ax.set_xlabel("질량수 A (로그 눈금)")
ax.set_ylabel("핵자당 결합 에너지 (MeV)")
ax.legend(fontsize=8, loc="lower right", bbox_to_anchor=(1.0, 0.05))
fig.tight_layout()
save(fig, __file__)
