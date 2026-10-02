from scipy import ndimage, optimize, stats

from figstyle import plt, np, save, C

# 128×128 잡음장을 여러 FWHM으로 평활화해, 장 전체 최댓값의 95번째 백분위(FWE 5 % 문턱)를 구한다.
L, NSIM = 128, 1000
rng = np.random.default_rng(62)
fwhms = np.array([0, 2, 3, 4, 6, 8, 12, 16])
emp = []
for fw in fwhms:
    mx = np.empty(NSIM)
    if fw == 0:
        for i in range(NSIM):
            mx[i] = rng.standard_normal((L, L)).max()
    else:
        s = fw / np.sqrt(8 * np.log(2))
        d = np.zeros((L, L))
        d[0, 0] = 1
        norm = np.sqrt((ndimage.gaussian_filter(d, s, mode="wrap") ** 2).sum())
        for i in range(NSIM):
            mx[i] = ndimage.gaussian_filter(rng.standard_normal((L, L)), s, mode="wrap").max() / norm
    emp.append(np.quantile(mx, 0.95))
emp = np.array(emp)

bonf = stats.norm.isf(0.05 / L ** 2)


def rft2(fw):
    R = L ** 2 / fw ** 2
    ec = lambda z: R * 4 * np.log(2) * (2 * np.pi) ** -1.5 * z * np.exp(-z ** 2 / 2) - 0.05
    return optimize.brentq(ec, 1.5, 10)


fg = np.linspace(1.5, 16, 200)
rft = np.array([rft2(f) for f in fg])

fig, ax = plt.subplots(figsize=(6.2, 3.1))
ax.axhline(bonf, color=C["gray"], lw=1.4, ls="--")
ax.text(16.3, bonf + 0.05, f"본페로니 z = {bonf:.2f}", color=C["gray"], fontsize=8, ha="right", va="bottom")
ax.plot(fg, rft, color=C["purple"], lw=1.8, label="무작위장 이론 (2차원 오일러 특성 근사)")
ax.plot(fwhms, emp, "o-", color=C["blue"], lw=1.4, ms=5, label=f"시뮬레이션 (장 {NSIM}개의 최댓값 95 %)")
for f, e in zip(fwhms, emp):
    if f in (0, 4, 8, 16):
        ax.text(f + 0.25, e - 0.08, f"{e:.2f}", fontsize=8, color=C["blue"], va="top")
ax.set_xlabel("평활화 FWHM (픽셀)")
ax.set_ylabel("FWE 5 % 문턱 (z)")
ax.set_xlim(-0.5, 16.5)
ax.set_ylim(3.0, 4.9)
ax.legend(fontsize=8, loc="lower left")
ax2 = ax.secondary_xaxis("top", functions=(lambda f: f, lambda f: f))
ticks = [2, 4, 8, 16]
ax2.set_xticks(ticks)
ax2.set_xticklabels([f"{L * L / t ** 2:,.0f}" for t in ticks], fontsize=8)
ax2.set_xlabel("해상 요소(RESEL) 수 = 넓이/FWHM²", fontsize=8.5)
save(fig, __file__)
