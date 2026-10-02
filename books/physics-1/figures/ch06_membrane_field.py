from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.4), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.25, 1], hspace=0.12))
L, R = 0.0, 5.0  # 막의 두 면 (nm)

# 위: 막 단면, 전하, 전기장
a1.add_patch(plt.Rectangle((L, 0), R - L, 1, color=C["green"], alpha=0.15, lw=0))
for y in np.linspace(0.1, 0.9, 6):
    a1.text(L - 0.35, y, "+", ha="center", va="center", fontsize=11, weight="bold", color=C["ink"])
    a1.text(R + 0.35, y, "−", ha="center", va="center", fontsize=11, weight="bold", color=C["ink"])
for y in np.linspace(0.18, 0.82, 4):
    a1.annotate("", xy=(R - 0.4, y), xytext=(L + 0.4, y),
                arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.4, mutation_scale=12))
a1.text(2.5, 1.07, "지질 이중층 (약 5 nm)", ha="center", va="bottom", fontsize=9, color=C["green"])
a1.text(2.5, 0.5, "E ≈ 1.4×10⁷ V/m", ha="center", va="center", fontsize=9.5, color=C["blue"],
        bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
a1.text(-2.6, 0.5, "세포 밖\n(기준 0 V)", ha="center", va="center", fontsize=9)
a1.text(7.6, 0.5, "세포 안", ha="center", va="center", fontsize=9)
a1.set_ylim(-0.05, 1.35)
a1.axis("off")

# 아래: 전위
x = np.array([-4.5, L, R, 9.5])
v = np.array([0, 0, -70, -70])
a2.plot(x, v, color=C["blue"], lw=2)
a2.axvspan(L, R, color=C["green"], alpha=0.15, lw=0)
a2.axhline(0, color=C["gray"], lw=0.6, ls=":")
a2.set_ylabel("전위 (mV)")
a2.set_xlabel("위치 (nm)")
a2.set_ylim(-85, 12)
a2.set_yticks([0, -35, -70])
a2.set_yticklabels(["0", "−35", "−70"])
a2.set_xlim(-4.5, 9.5)
a2.annotate("기울기 = 70 mV / 5 nm\n→ 전기장의 크기", xy=(2.5, -35), xytext=(5.6, -22), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.text(-4.2, -60, "용액 안에서는 전위가 거의 평평하다\n(전기장 ≈ 0)", fontsize=8.5, color=C["gray"])
save(fig, __file__)
