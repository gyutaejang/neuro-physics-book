from figstyle import plt, np, save, C

# 단순한 축상 뇌 모형에 신호 식을 넣어 네 가지 대비를 계산한다.
# 조직: (T1 ms, T2 ms, 양성자 밀도), 3 T 어림값.
P = {
    "fat": (380, 70, 0.9),      # 두피 지방
    "csf": (4000, 2000, 1.0),
    "gm": (1400, 100, 0.8),
    "wm": (850, 75, 0.7),
    "lesion": (1300, 180, 0.85),  # 백질 병변(물이 늘어난 자리)
}


def phantom(N=256):
    y, x = np.mgrid[1:-1:N * 1j, -1:1:N * 1j]
    th = np.arctan2(y, x)
    r = np.sqrt((x / 0.74) ** 2 + (y / 0.9) ** 2)
    lab = np.full((N, N), "", dtype=object)
    wav = 1 + 0.025 * np.sin(14 * th)
    lab[r < 1.0] = "fat"
    lab[r < 0.95] = ""          # 두개골: 신호 없음
    lab[r < 0.89] = "csf"
    lab[r < 0.86 * wav] = "gm"
    lab[r < 0.74 * wav] = "wm"
    for sx in (-1, 1):
        rv = np.sqrt(((x - sx * 0.11) / 0.07) ** 2 + ((y - 0.05) / 0.28) ** 2)
        lab[rv < 1] = "csf"
    lab[np.sqrt((x - 0.33) ** 2 + (y - 0.25) ** 2) < 0.06] = "lesion"
    lab[np.sqrt((x + 0.35) ** 2 + (y + 0.3) ** 2) < 0.04] = "lesion"
    return lab


def image(lab, kind):
    out = np.zeros(lab.shape)
    for k, (T1, T2, PD) in P.items():
        m = lab == k
        if kind == "T1":
            s = PD * (1 - np.exp(-500 / T1)) * np.exp(-10 / T2)
        elif kind == "PD":
            s = PD * (1 - np.exp(-6000 / T1)) * np.exp(-10 / T2)
        elif kind == "T2":
            s = PD * (1 - np.exp(-4000 / T1)) * np.exp(-90 / T2)
        else:  # FLAIR: TR 9000, TI = 뇌척수액 무효화, TE 90
            TR, TE = 9000, 90
            TI = 4000 * np.log(2 / (1 + np.exp(-TR / 4000)))
            s = PD * abs(1 - 2 * np.exp(-TI / T1) + np.exp(-TR / T1)) * np.exp(-TE / T2)
        out[m] = s
    return out / out.max()


lab = phantom()
kinds = [("T1", "T1 강조\nTR 500, TE 10"), ("PD", "PD 강조\nTR 6000, TE 10"),
         ("T2", "T2 강조\nTR 4000, TE 90"), ("FLAIR", "FLAIR\nTR 9000, TI 2370, TE 90")]
fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.5))
for ax, (k, title) in zip(axes, kinds):
    ax.imshow(image(lab, k), cmap="gray", vmin=0, vmax=1)
    ax.set_title(title, fontsize=8.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
axes[0].annotate("병변", xy=(170, 96), xytext=(205, 30), color=C["red"], fontsize=8,
                 arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.7))
axes[3].annotate("병변", xy=(170, 96), xytext=(205, 30), color=C["red"], fontsize=8,
                 arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.7))
fig.tight_layout(w_pad=0.4)
save(fig, __file__)
