from figstyle import log_scale_map, save, C

items = [
    (3e-14, "뇌 유발 반응\n(MEG) 수십 fT"),
    (1e-12, "알파파 자기장\n~1 pT"),
    (5e-11, "심장 자기장\n~50 pT"),
    (1e-7, "도시의 자기 잡음\n~100 nT"),
    (5e-5, "지구 자기장\n~50 μT"),
    (5e-3, "냉장고 자석\n~5 mT"),
    (3, "3 T MRI\n주자기장"),
]
ticks = [(1e-15, "1 fT"), (1e-12, "1 pT"), (1e-9, "1 nT"), (1e-6, "1 μT"), (1e-3, "1 mT"), (1, "1 T")]
fig, ax = log_scale_map(items, "자기장 세기 (테슬라, 로그 눈금)", (3e-16, 30), figsize=(7.5, 3.4),
                        color=C["purple"], ticks=ticks)
ax.set_ylim(-2.3, 1.6)
ax.spines["bottom"].set_position(("data", -2.3))
ax.annotate("", xy=(3, -1.75), xytext=(1e-14, -1.75),
            arrowprops=dict(arrowstyle="<->", color=C["purple"], lw=1))
ax.text(1e-5, -1.85, "약 10¹⁴배 (100조 배) 차이", ha="center", va="top", fontsize=8.5, color=C["purple"])
save(fig, __file__)
