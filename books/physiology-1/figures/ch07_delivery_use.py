from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1, 1.25]))

# 왼쪽: 혈액이 실어 오는 양과 뇌가 쓰는 양 (μmol/100 g/분)
CBF = 0.050           # L/100 g/분
glc_in = CBF * 5.0 * 1000     # 혈장 포도당 5 mM
o2_in = CBF * (200 / 22.4) * 1000  # 동맥혈 O₂ 20 mL/dL
glc_use, o2_use = 28, 155
x = np.arange(2)
w = 0.36
a1.bar(x - w / 2, [glc_in, o2_in], w, color=C["gray"], alpha=0.45, label="혈액이 실어 옴")
a1.bar(x + w / 2, [glc_use, o2_use], w, color=[C["blue"], C["red"]], alpha=0.85, label="뇌가 씀")
for i, (s, u) in enumerate(((glc_in, glc_use), (o2_in, o2_use))):
    a1.text(i - w / 2, s + 8, f"{s:.0f}", ha="center", va="bottom", fontsize=8)
    a1.text(i + w / 2, u + 8, f"{u:.0f}", ha="center", va="bottom", fontsize=8)
    a1.text(i, max(s, u) + 62, f"추출 약 {u / s * 100:.0f}%", ha="center", fontsize=8.5,
            color=C["ink"], weight="bold")
a1.set_xticks(x)
a1.set_xticklabels(["포도당", "산소"])
a1.set_ylabel("μmol / 100 g / 분")
a1.set_ylim(0, 590)
a1.legend(fontsize=7.5, loc="upper left")
a1.set_title("공급과 사용 (휴지기 성인)", fontsize=10)

# 오른쪽: 상황별 혈중 β-히드록시부티르산 범위 (대략, 로그 눈금)
rows = [
    ("식사 후", 0.03, 0.1),
    ("밤사이 공복", 0.1, 0.4),
    ("단식 2–3일", 1.0, 2.5),
    ("케톤 식이 치료", 2.0, 5.0),
    ("단식 수 주", 4.0, 7.0),
]
for i, (name, lo, hi) in enumerate(rows):
    y = len(rows) - 1 - i
    a2.plot([lo, hi], [y, y], color=C["green"], lw=7, solid_capstyle="round", alpha=0.85)
    a2.text(0.022, y, name, ha="right", va="center", fontsize=8.5)
a2.set_xscale("log")
a2.set_xlim(0.025, 12)
a2.set_ylim(-1.0, len(rows) - 0.4)
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xticks([0.03, 0.1, 0.3, 1, 3, 10])
a2.set_xticklabels(["0.03", "0.1", "0.3", "1", "3", "10"])
a2.minorticks_off()
a2.set_xlabel("혈중 β-히드록시부티르산 (mM, 대략)")
a2.text(2.6, -0.32, "이때 뇌 에너지의 최대 약 60%", ha="center", va="top", fontsize=8, color=C["green"])
a2.set_title("케톤체는 공복이 길수록 는다", fontsize=10)
fig.tight_layout(w_pad=6.5)
save(fig, __file__)
