from figstyle import plt, np, save, C

# Azevedo 등(2009), 성인 남성 4명의 평균 (단위: 10억 개, g)
regions = ["대뇌 피질\n(회백질+백질)", "소뇌", "나머지\n(뇌간, 간뇌, 기저핵)"]
neurons = np.array([16.34, 69.03, 0.69])
others = np.array([60.84, 16.04, 7.73])
mass = np.array([1232.9, 154.0, 118.1])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(width_ratios=[1, 1.15]))

# 왼쪽: 질량 비율 대 뉴런 비율
mp = mass / mass.sum() * 100
npct = neurons / neurons.sum() * 100
cols = [C["blue"], C["green"], C["gray"]]
for row, (vals, lab) in enumerate([(mp, "질량"), (npct, "뉴런 수")]):
    left = 0
    for v, col in zip(vals, cols):
        a1.barh(row, v, left=left, color=col, alpha=0.85, height=0.55, edgecolor="white")
        if v > 6:
            a1.text(left + v / 2, row, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=8.5)
        left += v
a1.set_yticks([0, 1])
a1.set_yticklabels(["질량", "뉴런 수"])
a1.set_ylim(1.6, -0.6)
a1.set_xlim(0, 100)
a1.set_xlabel("뇌 전체에 대한 비율 (%)")
for col, name, xx in zip(cols, ["대뇌 피질", "소뇌", "나머지"], [0, 36, 60]):
    a1.add_patch(plt.Rectangle((xx, -0.55), 4, 0.16, color=col, clip_on=False))
    a1.text(xx + 5, -0.47, name, fontsize=8, va="center")
a1.set_title("(가) 무게는 피질, 뉴런은 소뇌", fontsize=9.5, pad=14)

# 오른쪽: 뉴런 대 비뉴런 세포 수
x = np.arange(3)
w = 0.38
a2.bar(x - w / 2, neurons, w, color=C["blue"], label="뉴런")
a2.bar(x + w / 2, others, w, color=C["green"], alpha=0.8, label="비뉴런 세포 (주로 신경교)")
for i in range(3):
    a2.text(x[i] - w / 2, neurons[i] + 1.2, f"{neurons[i]:.1f}", ha="center", fontsize=7.8)
    a2.text(x[i] + w / 2, others[i] + 1.2, f"{others[i]:.1f}", ha="center", fontsize=7.8)
    a2.text(x[i], 93, f"비 {others[i] / neurons[i]:.1f} : 1", ha="center", fontsize=8, color=C["red"])
a2.set_xticks(x)
a2.set_xticklabels(regions, fontsize=8)
a2.set_ylabel("세포 수 (10억 개)")
a2.set_ylim(0, 100)
a2.legend(fontsize=7.8, loc="upper right", bbox_to_anchor=(1.0, 0.88))
a2.set_title("(나) 부위별 뉴런과 비뉴런 세포", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
