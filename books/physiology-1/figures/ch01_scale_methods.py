from figstyle import plt, np, save, C

fig, ax = plt.subplots(figsize=(7.3, 3.9))
ax.set_xscale("log")
ax.set_xlim(1e-9, 3e-1)
ax.set_ylim(-6.6, 3.4)

# 위: 구조의 크기
structs = [(5e-9, "세포막\n5 nm", 1.0), (2e-8, "시냅스 틈\n20 nm", 2.3), (4.5e-8, "시냅스 소포\n약 40–50 nm", -1.0),
           (7e-7, "가시 머리\n약 0.5–1 μm", 2.3), (1.5e-5, "세포체\n약 10–20 μm", 1.0),
           (5e-5, "모세혈관 간격\n약 50 μm", 2.3), (5e-4, "피질 기둥\n약 0.3–0.6 mm", 1.0),
           (2.5e-3, "피질 두께\n약 2–4 mm", 2.3), (1.6e-1, "뇌 앞뒤 길이\n약 16 cm", 1.0)]
ax.axhline(0, color=C["gray"], lw=1.0)
for x, lab, lv in structs:
    if lv > 0:
        ax.plot([x, x], [0, lv - 0.1], color=C["gray"], lw=0.6)
    ax.scatter([x], [0], s=22, color=C["green"], zorder=3)
    if lv < 0:
        ax.plot([x, x], [0, 0.9], color=C["gray"], lw=0.6)
        ax.text(x * 0.85, 1.0, lab, ha="left", va="bottom", fontsize=7.6)
    else:
        ax.text(x, lv, lab, ha="center", va="bottom", fontsize=7.6)

# 아래: 방법별 공간 해상도(막대 왼쪽 끝)와 한 번에 보는 범위(오른쪽 끝)
methods = [("전자현미경 (연결체학)", 4e-9, 1e-3, C["purple"]),
           ("광학 현미경 · 조직 염색", 2.5e-7, 2e-2, C["green"]),
           ("이광자 현미경 (생체)", 5e-7, 1e-3, C["green"]),
           ("구조 MRI", 7e-4, 2e-1, C["blue"]),
           ("fMRI · 확산 MRI", 1.5e-3, 2e-1, C["blue"]),
           ("PET", 3e-3, 2e-1, C["red"]),
           ("EEG · MEG (원천 추정)", 1e-2, 2e-1, C["gray"])]
for k, (name, lo, hi, col) in enumerate(methods):
    y = -0.9 - 0.78 * k
    ax.plot([lo, hi], [y, y], color=col, lw=6, alpha=0.55, solid_capstyle="butt")
    ax.plot([lo, lo], [y - 0.25, y + 0.25], color=col, lw=1.5)
    if lo < 1e-4:
        ax.text(hi * 1.4, y, name, va="center", fontsize=7.8)
    else:
        ax.text(lo / 1.4, y, name, va="center", ha="right", fontsize=7.8)
ax.text(1.2e-9, -6.35, "막대: 왼쪽 끝 = 대략의 공간 해상도, 오른쪽 끝 = 한 번에 보는 범위", fontsize=7.6, color=C["gray"])
ticks = [(1e-9, "1 nm"), (1e-8, "10 nm"), (1e-7, "100 nm"), (1e-6, "1 μm"), (1e-5, "10 μm"),
         (1e-4, "100 μm"), (1e-3, "1 mm"), (1e-2, "1 cm"), (1e-1, "10 cm")]
ax.set_xticks([t for t, _ in ticks])
ax.set_xticklabels([s for _, s in ticks], fontsize=8)
ax.minorticks_off()
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -6.6))
for x in (1e-6, 1e-3):
    ax.axvline(x, color=C["gray"], lw=0.5, ls=":", zorder=0)
ax.set_xlabel("길이 (로그 눈금)")
save(fig, __file__)
