from figstyle import plt, np, save, C

RT = 2.58  # kJ/mol, 37 °C에서 kT 하나를 몰당으로 쓴 값
# (이름, 최소 kJ/mol, 최대 kJ/mol, 색)
rows = [
    ("공유 결합 (C–C, O–H 등)", 150, 500, C["blue"]),
    ("이온 쌍 Na⁺–Cl⁻, 진공 (0.3–0.5 nm)", 278, 463, C["red"]),
    ("이온–물 분자 하나 (Na⁺, K⁺, 기체 상태)", 70, 100, C["green"]),
    ("수소 결합 하나", 10, 40, C["blue"]),
    ("쌍극자–쌍극자 (돌아다니는 극성 분자)", 1, 5, C["purple"]),
    ("이온 쌍 Na⁺–Cl⁻, 물속 (0.3–0.5 nm)", 278 / 80, 463 / 80, C["red"]),
    ("분산력 (원자 한 쌍)", 0.5, 1.5, C["gray"]),
]
fig, ax = plt.subplots(figsize=(6.8, 3.2))
y = np.arange(len(rows))[::-1]
for yi, (name, lo, hi, col) in zip(y, rows):
    a, b = lo / RT, hi / RT
    ax.barh(yi, b - a, left=a, color=col, alpha=0.75, height=0.55)
    txt = f"{a:.1f}–{b:.1f} kT" if b < 3 else f"{a:.0f}–{b:.0f} kT"
    ax.text(b * 1.12, yi, txt, va="center", fontsize=8.5)
ax.set_xscale("log")
ax.set_xlim(0.1, 900)
ax.set_yticks(y)
ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
ax.set_xticks([0.1, 1, 10, 100])
ax.set_xticklabels(["0.1", "1", "10", "100"])
ax.minorticks_off()
ax.axvline(1, color=C["red"], lw=0.9, ls="--")
ax.text(1.08, len(rows) - 0.45, "kT (37 °C)", color=C["red"], fontsize=8.5, va="center")
ax.set_ylim(-0.6, len(rows) - 0.1)
ax.set_xlabel("에너지 (kT의 몇 배인가, 로그 눈금; 1 kT ≈ 2.6 kJ/mol)")
fig.tight_layout()
save(fig, __file__)
