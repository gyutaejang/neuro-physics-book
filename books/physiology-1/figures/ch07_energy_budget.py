from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[2.3, 1]))

# 왼쪽: 신호 전달 에너지의 항목별 몫(%). 설치류 회백질 상향식 계산, 대략값.
items = ["시냅스 후 전류", "활동전위", "휴지 전위 유지", "시냅스 앞 Ca$^{2+}$·소포", "글루탐산 재활용"]
cols = [C["blue"], C["red"], C["green"], C["purple"], C["gray"]]
al2001 = [34, 47, 13, 3, 3]
rev = [50, 22, 20, 6, 2]
rows = [("Attwell & Laughlin\n(2001)", al2001), ("개정 계산\n(2012 무렵)", rev)]
for j, (name, vals) in enumerate(rows):
    y = 1 - j
    left = 0
    for v, c in zip(vals, cols):
        a1.barh(y, v, left=left, color=c, alpha=0.85, height=0.55, edgecolor="white")
        if v >= 10:
            a1.text(left + v / 2, y, f"{v}", ha="center", va="center", fontsize=8.5, color="white",
                    weight="bold")
        left += v
    a1.text(-2, y, name, ha="right", va="center", fontsize=8.5)
a1.set_xlim(0, 100)
a1.set_ylim(-0.75, 1.75)
a1.set_yticks([])
a1.spines["left"].set_visible(False)
a1.set_xlabel("신호 전달 에너지 중 몫 (%)")
handles = [plt.Rectangle((0, 0), 1, 1, color=c, alpha=0.85) for c in cols]
a1.legend(handles, items, fontsize=7.5, ncol=3, loc="upper center", bbox_to_anchor=(0.42, 1.27),
          handlelength=1.0, columnspacing=0.9)

# 오른쪽: 사람 회백질과 백질의 포도당 대사율(PET, 대략)
names = ["회백질", "뇌 전체\n평균", "백질"]
vals = [0.40, 0.28, 0.15]
a2.bar(range(3), vals, 0.6, color=[C["blue"], C["gray"], C["blue"]], alpha=[0.9, 0.6, 0.45][0])
for i, v in enumerate(vals):
    a2.text(i, v + 0.01, f"약 {v:.2f}", ha="center", va="bottom", fontsize=8)
a2.set_xticks(range(3))
a2.set_xticklabels(names, fontsize=8.5)
a2.set_ylabel("CMRglc (μmol/g/분)")
a2.set_ylim(0, 0.5)
a2.set_title("사람 뇌 (PET)", fontsize=9.5)
fig.tight_layout(w_pad=4)
save(fig, __file__)
