from figstyle import log_scale_map, save, C

items = [
    (2e-12, "이온 통로 하나\n~1–10 pA"),
    (5e-11, "시냅스 하나의\n전류 ~수십 pA"),
    (2e-9, "활동전위 때\n세포 전체 ~nA"),
    (1.5e-3, "tDCS 자극\n1–2 mA"),
    (1e-1, "심장에 위험한\n감전 ~0.1 A"),
    (1, "가정용 전기\n기구 ~1 A"),
    (5e3, "TMS 코일\n펄스 수 kA"),
]
ticks = [(1e-12, "1 pA"), (1e-9, "1 nA"), (1e-6, "1 μA"), (1e-3, "1 mA"), (1, "1 A"), (1e3, "1 kA")]
fig, ax = log_scale_map(items, "전류 (암페어, 로그 눈금)", (2e-13, 5e4), figsize=(7.5, 3.4),
                        color=C["blue"], ticks=ticks)
ax.set_ylim(-2.3, 1.6)
ax.spines["bottom"].set_position(("data", -2.3))
ax.annotate("", xy=(5e3, -1.8), xytext=(2e-12, -1.8),
            arrowprops=dict(arrowstyle="<->", color=C["blue"], lw=1))
ax.text(3e-4, -1.9, "약 10¹⁵배 차이", ha="center", va="top", fontsize=8.5, color=C["blue"])
save(fig, __file__)
