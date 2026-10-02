from figstyle import plt, np, save, C

# 참가자 60명(대조군 30, 환자군 30)의 품질 지표: 평균 FD와 tSNR.
rng = np.random.default_rng(11)
n = 30
fd_c = rng.lognormal(np.log(0.12), 0.35, n)
fd_p = rng.lognormal(np.log(0.19), 0.45, n)
fd_p[[3, 17]] = [0.62, 0.81]          # 움직임이 큰 두 명
fd = np.r_[fd_c, fd_p]
grp = np.r_[np.zeros(n), np.ones(n)]
tsnr = 72 - 55 * fd + rng.normal(0, 5, 2 * n)
tsnr[40] = 31                         # 코일 문제 한 명(움직임은 작다)
fd[40] = 0.15

med = np.median(fd)
mad = 1.4826 * np.median(np.abs(fd - med))
cut_fd = med + 3 * mad
med_t = np.median(tsnr)
mad_t = 1.4826 * np.median(np.abs(tsnr - med_t))
cut_t = med_t - 3 * mad_t
flag = (fd > cut_fd) | (tsnr < cut_t)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1.5, 1], wspace=0.35))
for g, col, lab in [(0, C["blue"], "대조군"), (1, C["green"], "환자군")]:
    m = grp == g
    a1.scatter(fd[m & ~flag], tsnr[m & ~flag], s=18, color=col, label=lab, alpha=0.85)
    a1.scatter(fd[m & flag], tsnr[m & flag], s=40, facecolor="none", edgecolor=C["red"], lw=1.4)
    a1.scatter(fd[m & flag], tsnr[m & flag], s=14, color=col)
a1.axvline(cut_fd, color=C["red"], lw=0.9, ls="--")
a1.axhline(cut_t, color=C["red"], lw=0.9, ls="--")
a1.text(cut_fd + 0.01, 84, f"FD 기준 {cut_fd:.2f} mm", color=C["red"], fontsize=8)
a1.text(0.86, cut_t + 1.5, f"tSNR 기준 {cut_t:.0f}", color=C["red"], fontsize=8, ha="right", va="bottom")
a1.set_xlabel("평균 FD (mm)")
a1.set_ylabel("tSNR")
a1.set_ylim(15, 90); a1.set_xlim(0, 0.88)
a1.legend(fontsize=8.5, loc="upper right")
a1.set_title("(가) 지표 둘, 중앙값 + 3 MAD 기준", fontsize=10)

a2.boxplot([fd[grp == 0], fd[grp == 1]], widths=0.5, showfliers=False,
           medianprops=dict(color=C["ink"]), boxprops=dict(color=C["gray"]),
           whiskerprops=dict(color=C["gray"]), capprops=dict(color=C["gray"]))
for g, col in [(0, C["blue"]), (1, C["green"])]:
    v = fd[grp == g]
    a2.scatter(np.full(n, g + 1) + rng.uniform(-0.12, 0.12, n), v, s=10, color=col, alpha=0.8, zorder=3)
a2.set_xticks([1, 2]); a2.set_xticklabels(["대조군", "환자군"])
a2.set_ylabel("평균 FD (mm)")
a2.set_title("(나) 움직임은 집단마다 다르다", fontsize=10)
save(fig, __file__)
