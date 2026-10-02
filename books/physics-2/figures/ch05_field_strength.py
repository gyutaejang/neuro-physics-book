from figstyle import plt, np, save, C

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.1, 1]))

# (가) 3 T를 1로 놓은 상대값
B = np.array([1.5, 3.0, 7.0])
rows = [("알짜 자화 M₀ ∝ B₀", B / 3, C["purple"]),
        ("유도 신호 ∝ B₀²", (B / 3) ** 2, C["blue"]),
        ("SNR (측정: B₀의 약 1.65제곱)", (B / 3) ** 1.65, C["green"]),
        ("같은 숙임각의 SAR ∝ B₀²", (B / 3) ** 2, C["red"])]
w = 0.2
x = np.arange(3)
for i, (lab, v, col) in enumerate(rows):
    bars = ax1.bar(x + (i - 1.5) * w, v, w * 0.92, color=col, label=lab,
                   hatch="//" if i == 3 else None, edgecolor="white" if i < 3 else col,
                   fill=i < 3, lw=0.8)
    for xx, vv in zip(x + (i - 1.5) * w, v):
        if xx > 1.5:
            ax1.text(xx, vv + 0.08, f"{vv:.1f}", ha="center", fontsize=7.5)
ax1.axhline(1, color=C["gray"], lw=0.6, ls=":")
ax1.set_xticks(x)
ax1.set_xticklabels(["1.5 T", "3 T", "7 T"])
ax1.set_ylabel("3 T 대비 상대값")
ax1.set_ylim(0, 7.6)
ax1.legend(loc="upper left", fontsize=7.6)
ax1.set_title("(가) 장 세기가 바꾸는 것", fontsize=10.5)

# (나) 뇌에서 얻는 신호의 상대 크기 (물 ¹H = 1): 핵 감도 × 농도
items = [("물의 ¹H\n(약 90 M)", 1.0 * 90, C["blue"]),
         ("NAA의 ¹H\n(메틸기, 약 30 mM)", 1.0 * 0.03, C["blue"]),
         ("²³Na\n(약 45 mM)", 0.093 * 0.045, C["green"]),
         ("³¹P (PCr)\n(약 4.5 mM)", 0.066 * 0.0045, C["purple"])]
vals = np.array([v for _, v, _ in items]) / 90
ax2.barh(np.arange(4)[::-1], vals, color=[c for *_, c in items], height=0.6)
for yy, v in zip(np.arange(4)[::-1], vals):
    if v < 1:
        m, ex = f"{v:.0e}".split("e")
        lab = f"${m}\\times10^{{{int(ex)}}}$"
    else:
        lab = "1"
    ax2.text(v * 1.6, yy, lab, va="center", fontsize=8.5)
ax2.set_yticks(np.arange(4)[::-1])
ax2.set_yticklabels([n for n, *_ in items], fontsize=8.3)
ax2.set_xscale("log")
ax2.set_xlim(1e-7, 30)
ax2.set_xlabel("신호 상대 크기 (물 ¹H = 1, 로그 눈금)")
ax2.set_title("(나) 핵 감도 × 뇌 속 농도", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
