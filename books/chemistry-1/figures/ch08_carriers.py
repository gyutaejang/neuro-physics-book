from figstyle import plt, np, save, C, molecule_image

# NAD+/NADH의 니코틴아마이드 고리와 FAD/FADH2의 아이소알록사진 고리.
# R(*)은 나머지 부분(리보스-인산-아데노신)이다. 강조한 원자가 전자와 수소를 받는 자리다.
items = [
    ("NC(=O)c1ccc[n+]([*])c1", "NAD⁺ (산화형)", [4]),
    ("NC(=O)C1=CN([*])C=CC1", "NADH (환원형)", [9]),
    ("Cc1cc2c(cc1C)N([*])C1=NC(=O)NC(=O)C1=N2", "FAD (산화형)", [11, 18]),
    ("Cc1cc2c(cc1C)N([*])C1=C(N2)C(=O)NC(=O)N1", r"FADH$_2$ (환원형)", [12, 18]),
]
fig, axes = plt.subplots(1, 4, figsize=(7.4, 2.3), gridspec_kw=dict(width_ratios=[0.8, 0.8, 1.2, 1.2]))
for ax, (smi, name, hl) in zip(axes, items):
    size = (300, 300) if "NAD" in name else (420, 300)
    ax.imshow(molecule_image(smi, size=size, highlight=hl))
    ax.set_title(name, fontsize=9.5)
    ax.axis("off")
fig.text(0.255, 0.04, "H⁻(양성자 1 + 전자 2)를 받는다", ha="center", fontsize=8.5, color=C["red"])
fig.text(0.70, 0.04, "H 원자 2개(양성자 2 + 전자 2)를 받는다", ha="center", fontsize=8.5, color=C["red"])
fig.tight_layout(rect=(0, 0.07, 1, 1))
save(fig, __file__)
