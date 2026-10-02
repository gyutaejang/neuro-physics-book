from figstyle import plt, np, save, C

bands = [  # (긴 쪽 파장 m, 짧은 쪽 파장 m, 이름)
    (1e3, 1, "전파"),
    (1, 1e-3, "마이크로파"),
    (1e-3, 7.5e-7, "적외선"),
    (7.5e-7, 3.8e-7, ""),
    (3.8e-7, 1e-8, "자외선"),
    (1e-8, 1e-11, "X선"),
    (1e-11, 1e-14, "감마선"),
]
fig, ax = plt.subplots(figsize=(7.4, 3.3))
ax.set_xscale("log")
ax.set_xlim(1e3, 1e-14)  # 왼쪽이 긴 파장
ax.set_ylim(-1.7, 2.0)
for i, (a, b, name) in enumerate(bands):
    col = C["light"] if i % 2 == 0 else "#d5dfee"
    if name == "":
        col = C["red"]
    ax.axvspan(b, a, ymin=0.42, ymax=0.58, color=col, alpha=1 if name else 0.55, lw=0)
    if name:
        xm = np.sqrt(a * b)
        ax.text(xm, 0.15, name, ha="center", va="center", fontsize=8.5, color=C["ink"])
ax.annotate("가시광\n380–750 nm", xy=(5.3e-7, 0.35), xytext=(5.3e-7, 1.35), ha="center", fontsize=8.5,
            color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
uses = [  # (파장 m, 글자, 위/아래)
    (2.35, "3 T MRI RF\n128 MHz, 2.3 m", 1),
    (0.12, "휴대전화\n~2.5 GHz", -1),
    (8e-7, "fNIRS\n650–950 nm", -1),
    (4.7e-7, "", 0),
    (5e-11, "CT X선\n수십 keV", 1),
    (2.4e-12, "PET 감마선\n511 keV", -1),
]
for lam, txt, up in uses:
    if not txt:
        continue
    y = 1.05 if up > 0 else -0.9
    ax.plot([lam, lam], [0.32 if up > 0 else -0.32, y - 0.1 * up], color=C["gray"], lw=0.7)
    ax.scatter([lam], [0.32 if up > 0 else -0.32], s=14, color=C["blue"], zorder=3)
    ax.text(lam, y, txt, ha="center", va="bottom" if up > 0 else "top", fontsize=8, color=C["ink"])
ax.annotate("", xy=(1e-14, -1.55), xytext=(1e3, -1.55),
            arrowprops=dict(arrowstyle="->", color=C["purple"], lw=1))
ax.text(3e-6, -1.47, "파장이 짧을수록 진동수와 광자 에너지가 크다", ha="center", va="bottom",
        fontsize=8.5, color=C["purple"])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -1.7))
ticks = [1e3, 1, 1e-3, 1e-6, 1e-9, 1e-12]
ax.set_xticks(ticks)
ax.set_xticklabels(["1 km", "1 m", "1 mm", "1 μm", "1 nm", "1 pm"])
ax.minorticks_off()
ax.set_xlabel("파장 (로그 눈금, 왼쪽이 긴 파장)")
save(fig, __file__)
