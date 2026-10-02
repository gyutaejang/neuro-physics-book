from figstyle import log_scale_map, save, C

items = [
    (1e-8, "축삭 속 소포\n~10⁻⁸"),
    (3e-5, "헤엄치는 세균\n~10⁻⁵"),
    (1e-3, "모세혈관 속\n적혈구 ~10⁻³"),
    (1e-2, "정자\n~10⁻²"),
    (1e2, "중뇌수도관의\n뇌척수액 ~10²"),
    (2e3, "대동맥 혈류\n~10³"),
    (1e6, "헤엄치는 사람\n~10⁶"),
]
ticks = [(10.0 ** k, f"10$^{{{k}}}$") for k in range(-9, 8, 2)]
fig, ax = log_scale_map(items, "레이놀즈 수 Re = ρvL/η (로그 눈금)", (1e-9, 1e8), figsize=(7.5, 3.5),
                        ticks=ticks)
ax.axvspan(1e-9, 1, color=C["green"], alpha=0.08, zorder=0)
ax.axvspan(1, 1e8, color=C["blue"], alpha=0.06, zorder=0)
ax.axvline(1, color=C["gray"], lw=0.8, ls="--")
ax.text(3e-5, 1.45, "점성이 지배 (Re ≪ 1): 미는 힘을 멈추면 즉시 선다", ha="center", fontsize=8,
        color=C["green"])
ax.text(1e4, 1.45, "관성이 지배 (Re ≫ 1): 미끄러져 나아간다", ha="center", fontsize=8, color=C["blue"])
ax.set_ylim(-1.6, 1.75)
save(fig, __file__)
