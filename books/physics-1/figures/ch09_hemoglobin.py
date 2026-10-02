from figstyle import plt, np, save, C


def smooth_log(xk, yk, x):
    # 로그 값을 선형 보간한 뒤 이동 평균으로 매끄럽게 한다.
    y = np.interp(x, xk, np.log(yk))
    k = 5
    pad = np.pad(y, k, mode="edge")
    return np.exp(np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k])

# 도식. 표준 문헌 값(몰 흡광 계수)의 모양을 따랐지만 측정 데이터가 아니다.
lam_k = np.array([600, 620, 650, 680, 700, 730, 757, 780, 800, 830, 860, 900, 930, 960, 1000])
hbo = np.array([3200, 940, 370, 285, 290, 390, 560, 710, 815, 975, 1100, 1200, 1210, 1170, 1050])
hbr = np.array([14600, 6500, 3750, 2400, 1800, 1100, 1600, 1075, 762, 700, 700, 760, 820, 820, 760])
lam = np.linspace(600, 1000, 400)
# 물의 흡수 (도식): 900 nm 이후 가파르게 오르고 약 970 nm에서 봉우리.
wk = np.array([600, 700, 800, 850, 900, 930, 960, 975, 1000])
wv = np.array([0.0023, 0.006, 0.02, 0.043, 0.068, 0.15, 0.40, 0.45, 0.36])

fig, ax = plt.subplots(figsize=(6.6, 3.3))
ax.axvspan(650, 950, color=C["light"], lw=0)
ax.text(655, 2.6e4, "근적외선 창 (약 650–950 nm)", fontsize=8.5, color=C["blue"], va="top")
ax.semilogy(lam, smooth_log(lam_k, hbr, lam), color=C["blue"], lw=2, label="탈산소헤모글로빈 (HbR)")
ax.semilogy(lam, smooth_log(lam_k, hbo, lam), color=C["red"], lw=2, label="산소헤모글로빈 (HbO₂)")
ax.semilogy(lam, smooth_log(wk, wv, lam) * 8000, color=C["gray"], lw=1.4, ls="--", label="물 (세로 위치 임의)")
ax.axvline(800, color=C["ink"], lw=0.6, ls=":")
ax.annotate("등흡광점 (약 800 nm)", xy=(800, 790), xytext=(655, 150), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.text(690, 560, "800 nm 아래:\nHbR이 더 흡수", fontsize=8.5, color=C["blue"], ha="center")
ax.text(880, 2.6e3, "800 nm 위:\nHbO₂가 더 흡수", fontsize=8.5, color=C["red"], ha="center")
ax.set_xlim(600, 1000)
ax.set_ylim(120, 3e4)
ax.set_xlabel("파장 (nm)")
ax.set_ylabel("흡수 세기 (상대값, 로그 눈금)")
ax.set_yticks([])
ax.minorticks_off()
ax.legend(fontsize=8, loc="upper right")
save(fig, __file__)
