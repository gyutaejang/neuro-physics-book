from figstyle import plt, save, C

rows = [
    ("G", "기가", 9, "10⁹", "MRI 주파수 영역 근처 (3 T는 0.128 GHz)"),
    ("M", "메가", 6, "10⁶", "3 T MRI 공명 주파수 128 MHz"),
    ("k", "킬로", 3, "10³", "EEG 표본화 1 kHz, TMS 코일 전류 수 kA"),
    ("", "(기본)", 0, "10⁰", "1 m, 1 s, 1 V, 1 T"),
    ("m", "밀리", -3, "10⁻³", "막전위 −70 mV, 활동전위 1 ms"),
    ("μ", "마이크로", -6, "10⁻⁶", "EEG 50 μV, 세포체 20 μm"),
    ("n", "나노", -9, "10⁻⁹", "세포막 5 nm, 세포 전류 nA"),
    ("p", "피코", -12, "10⁻¹²", "이온 통로 하나의 전류 pA"),
    ("f", "펨토", -15, "10⁻¹⁵", "MEG 신호 수십 fT"),
]
fig, ax = plt.subplots(figsize=(6.8, 4.2))
for i, (sym, name, e, pw, ex) in enumerate(rows):
    y = -i
    col = C["blue"] if e > 0 else (C["gray"] if e == 0 else C["red"])
    ax.add_patch(plt.Rectangle((0, y - 0.42), 0.9, 0.84, color=col, alpha=0.15 if e else 0.08, lw=0))
    ax.text(0.45, y, sym or "–", ha="center", va="center", fontsize=14, weight="bold", color=col)
    ax.text(1.1, y, name, va="center", fontsize=10)
    ax.text(2.6, y, pw, va="center", fontsize=10, color=C["ink"])
    ax.text(3.6, y, ex, va="center", fontsize=9, color="#444")
ax.annotate("", xy=(-0.25, -8.4), xytext=(-0.25, 0.4),
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.text(-0.38, -4, "한 칸 내려갈 때마다 1000분의 1", rotation=90, ha="center", va="center", fontsize=8.5,
        color=C["gray"])
ax.set_xlim(-0.6, 9.6)
ax.set_ylim(-8.6, 0.6)
ax.axis("off")
save(fig, __file__)
