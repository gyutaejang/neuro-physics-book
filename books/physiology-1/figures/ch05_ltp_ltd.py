from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
t = np.arange(-20, 61, 1.0)

def noisy(y, s=4):
    return y + rng.normal(0, s, y.size)

# 왼쪽: 고빈도 자극(100 Hz, 1 s) 뒤의 LTP와 NMDA 길항제(APV) 조건
after = t > 0
ltp = np.where(after, 150 + 70 * np.exp(-t / 4), 100)
apv = np.where(after, 100 + 60 * np.exp(-t / 3), 100)

# 오른쪽: 저빈도 자극(1 Hz, 15분) 뒤의 LTD
lfs_on = (t >= 0) & (t < 15)
ltd = np.where(t < 0, 100, np.where(lfs_on, 100 - 25 * (1 - np.exp(-t / 5)), 75 + 2 * np.exp(-(t - 15) / 10)))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), sharey=True)
a1.scatter(t, noisy(ltp), s=9, color=C["red"], label="대조")
a1.scatter(t, noisy(apv), s=9, color=C["gray"], label="NMDA 길항제(APV)")
a1.annotate("고빈도 자극\n100 Hz, 1 s", xy=(0.3, 222), xytext=(8, 218), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["ink"]))
a1.axvline(0, color=C["ink"], lw=0.8, ls=":")
a1.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.0, 0.82))
a1.set_title("LTP", fontsize=10)
a1.set_ylabel("fEPSP 기울기 (기저선 대비 %)")

a2.axvspan(0, 15, color=C["blue"], alpha=0.10, lw=0)
a2.scatter(t, noisy(ltd), s=9, color=C["blue"])
a2.text(7.5, 225, "저빈도 자극\n1 Hz, 15분\n(900회)", ha="center", va="top", fontsize=8)
a2.set_title("LTD", fontsize=10)

for a in (a1, a2):
    a.axhline(100, color=C["gray"], lw=0.7, ls="--")
    a.set_xlabel("시간 (분)")
    a.set_xlim(-21, 61)
a1.set_ylim(50, 250)
fig.tight_layout()
save(fig, __file__)
