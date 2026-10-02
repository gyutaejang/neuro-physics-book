from figstyle import plt, np, save, C

# 완전 허혈 뒤의 대략적 시간 경과(설치류 실험을 바탕으로 한 도식). 측정값이 아니다.
t = np.linspace(-0.5, 5, 600)
s = np.clip(t, 0, None)
pcr = 100 * np.exp(-s / 0.35)
sig = lambda x: 1 / (1 + np.exp((x - 1.6) / 0.35))
atp = 100 * (sig(s) - sig(10)) / (sig(0) - sig(10))
t_ad = 2.0  # 무산소 탈분극
k = np.where(t < 0, 3, np.where(t < t_ad, 3 + 9 * (s / t_ad) ** 1.5, 60 - 48 * np.exp(-(t - t_ad) / 0.12)))

fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 4.0), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.2, 1], hspace=0.12))
a1.plot(t, pcr, color=C["purple"], lw=2, label="크레아틴인산 (PCr)")
a1.plot(t, atp, color=C["blue"], lw=2, label="ATP")
a1.set_ylabel("허혈 전 대비 (%)")
a1.set_ylim(-5, 115)
a1.legend(fontsize=8, loc="upper right")
for a in (a1, a2):
    a.axvline(0, color=C["gray"], lw=0.8, ls=":")
    a.axvline(t_ad, color=C["red"], lw=0.8, ls="--")
a1.axvspan(0.15, 0.4, color=C["gray"], alpha=0.15, lw=0)
a1.text(0.45, 80, "← 의식 소실,\n    EEG 평탄", ha="left", va="top", fontsize=7.8, color=C["ink"],
        transform=a1.transData)
a1.text(-0.45, 50, "혈류\n정지", ha="left", va="center", fontsize=8, color=C["gray"])

a2.plot(t, k, color=C["green"], lw=2)
a2.set_ylabel("세포 밖 K$^{+}$ (mM)")
a2.set_ylim(0, 68)
a2.text(t_ad + 0.45, 30, "무산소 탈분극:\n이온 기울기 붕괴,\n세포독성 부종 시작", ha="left", va="center",
        fontsize=8, color=C["red"])
a2.text(0.9, 17, "천천히 증가", ha="center", va="bottom", fontsize=8, color=C["green"])
a2.set_xlabel("혈류가 멎은 뒤 시간 (분)")
a2.set_xlim(-0.5, 5)
save(fig, __file__)
