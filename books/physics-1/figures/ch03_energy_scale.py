from figstyle import log_scale_map, save, C

items = [
    (4.3e-21, "열에너지 kT\n(37 °C)"),
    (1.1e-20, "Na⁺ 하나가\n70 mV를 넘음"),
    (8.3e-20, "ATP 하나\n~0.5 eV"),
    (4.2e-19, "청색 광자\n(470 nm)"),
    (1.0, "사과(100 g)를\n1 m 들어 올림"),
    (20, "뇌가 1초에\n쓰는 에너지"),
    (2e5, "72 km/h 승용차의\n운동에너지"),
    (1.7e6, "뇌가 하루에\n쓰는 에너지"),
    (8.4e6, "하루 식사\n2000 kcal"),
]
ticks = [(1e-21, "10⁻²¹"), (1e-18, "10⁻¹⁸"), (1e-15, "10⁻¹⁵"), (1e-12, "10⁻¹²"), (1e-9, "10⁻⁹"),
         (1e-6, "10⁻⁶"), (1e-3, "10⁻³"), (1, "1"), (1e3, "10³"), (1e6, "10⁶")]
fig, ax = log_scale_map(items, "에너지 (J, 로그 눈금)", (2e-22, 1e8), figsize=(7.5, 3.4),
                        color=C["blue"], ticks=ticks)
ax.set_ylim(-2.3, 1.6)
ax.spines["bottom"].set_position(("data", -2.3))
ax.annotate("", xy=(1e-17, -1.85), xytext=(2e-22, -1.85),
            arrowprops=dict(arrowstyle="-", color=C["green"], lw=3, alpha=0.6))
ax.text(5e-20, -1.95, "분자 하나의 세계", ha="center", va="top", fontsize=8.5, color=C["green"])
ax.annotate("", xy=(1e8, -1.85), xytext=(1e-1, -1.85),
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=3, alpha=0.6))
ax.text(3e3, -1.95, "몸과 일상의 세계", ha="center", va="top", fontsize=8.5, color=C["red"])
ax.text(3e-10, 0.75, "이 사이 약 20자릿수.\n분자 하나의 에너지에 아보가드로 수(6×10²³)를\n곱하면 일상 크기의 에너지가 된다.",
        ha="center", va="center", fontsize=8, color=C["gray"])
ax.tick_params(axis="x", labelsize=8)
save(fig, __file__)
