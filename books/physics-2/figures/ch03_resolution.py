from figstyle import plt, np, save, C

# (가) 동위원소별 물속 양전자 평균 비정, (나) 공간 해상도 예산(제곱합의 제곱근)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2), gridspec_kw=dict(width_ratios=[1, 1.15]))

iso = [("¹⁸F", 0.634, 0.6), ("¹¹C", 0.960, 1.2), ("¹³N", 1.199, 1.8),
       ("¹⁵O", 1.732, 3.0), ("⁸²Rb", 3.378, 5.9)]
y = np.arange(len(iso))[::-1]
a1.barh(y, [r for _, _, r in iso], color=[C["red"] if n == "¹⁸F" else C["blue"] for n, _, _ in iso],
        height=0.6)
for yy, (n, e, r) in zip(y, iso):
    a1.text(r + 0.12, yy, f"{r:.1f} mm  (최대 {e:.2f} MeV)", va="center", fontsize=8)
a1.set_yticks(y)
a1.set_yticklabels([n for n, _, _ in iso])
a1.set_xlim(0, 10.5)
a1.set_ylim(-0.6, len(iso) - 0.4)
a1.set_xlabel("물속 평균 비정 (mm)")
a1.set_title("(가) 양전자가 소멸 전에 가는 거리", fontsize=9.5)

# (나) 해상도 예산
cases = [("임상 전신 PET\n결정 4 mm, 지름 80 cm", 4.0, 800),
         ("뇌 전용 PET\n결정 2 mm, 지름 40 cm", 2.0, 400)]
r18 = 0.5  # ¹⁸F 양전자 비정의 실효 FWHM 기여 (mm)
names = ["검출기 (d/2)", "비공선성 (0.0022 D)", "양전자 비정 (¹⁸F)", "합 × 1.25 (재구성)"]
cols = [C["blue"], C["purple"], C["red"], C["ink"]]
w = 0.18
for i, (lab, d, D) in enumerate(cases):
    comps = [d / 2, 0.0022 * D, r18]
    tot = 1.25 * np.sqrt(sum(c * c for c in comps))
    vals = comps + [tot]
    for j, v in enumerate(vals):
        x = i + (j - 1.5) * w
        a2.bar(x, v, width=w * 0.9, color=cols[j], label=names[j] if i == 0 else None)
        a2.text(x, v + 0.07, f"{v:.1f}", ha="center", fontsize=7.6)
a2.set_xticks([0, 1])
a2.set_xticklabels([c[0] for c in cases], fontsize=8)
a2.set_ylabel("FWHM 기여 (mm)")
a2.set_ylim(0, 4.6)
a2.legend(fontsize=7.6, loc="upper right")
a2.set_title("(나) 영상 중심의 해상도 어림", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
