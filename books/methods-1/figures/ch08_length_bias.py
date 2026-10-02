from figstyle import plt, np, save, C

# 스트림라인 수의 길이 편향. 모든 다발은 굵기(축삭 수)가 같고 길이만 다르다.
# 추적은 1 mm마다 일정한 확률로 일찍 멈춘다(평균 생존 길이 λ = 40 mm).
rng = np.random.default_rng(13)
lam = 40.0
q = 1 - np.exp(-1 / lam)  # 1 mm당 멈출 확률
Ls = np.array([10, 20, 30, 45, 60, 80, 100, 120, 150])
L = np.linspace(8, 160, 200)


def mc_roi(Lk, n=4000):
    """한쪽 끝 영역에서 씨앗 n개: 반대쪽 끝까지 살아남은 수."""
    return (rng.geometric(q, n) > Lk).sum()


def mc_wm(Lk, rho=30):
    """백질 전체에 고르게 씨앗(1 mm당 rho개): 양쪽 끝까지 모두 살아남아야 연결로 센다."""
    ns = rng.poisson(rho * Lk)
    s = rng.uniform(0, Lk, ns)
    return ((rng.geometric(q, ns) > s) & (rng.geometric(q, ns) > Lk - s)).sum()


roi = np.array([mc_roi(Lk) for Lk in Ls], float)
wm = np.array([mc_wm(Lk) for Lk in Ls], float)
ref = 20
roi_th = np.exp(-L / lam) / np.exp(-ref / lam)
wm_th = L * np.exp(-L / lam) / (ref * np.exp(-ref / lam))
roi /= roi[Ls == ref]
wm /= wm[Ls == ref]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw=dict(width_ratios=[1.45, 1]))
a1.axhline(1, color=C["ink"], lw=1.2, ls="--")
a1.text(158, 1.6, "참값(점선): 모든 다발의 축삭 수가 같다", ha="right", fontsize=8)
a1.plot(L, wm_th, color=C["blue"], lw=1.7, label="백질 전체 씨앗 ($\\propto L\\,e^{-L/\\lambda}$)")
a1.plot(L, roi_th, color=C["red"], lw=1.7, label="끝 영역 씨앗 ($\\propto e^{-L/\\lambda}$)")
a1.plot(Ls, wm, "o", ms=4, color=C["blue"])
a1.plot(Ls, roi, "o", ms=4, color=C["red"])
a1.set_yscale("log")
a1.set_ylim(0.01, 3)
a1.set_xlim(0, 160)
a1.set_xlabel("다발 길이 L (mm)")
a1.set_ylabel("스트림라인 수 (20 mm 다발 = 1)")
a1.set_title("(가) 같은 굵기, 다른 길이", fontsize=9.5)
a1.legend(fontsize=7.8, loc="lower left")

# (나) 20 mm와 100 mm 다발의 비
r_roi = np.exp(-20 / lam) / np.exp(-100 / lam)
r_wm = (20 * np.exp(-20 / lam)) / (100 * np.exp(-100 / lam))
vals = [1.0, r_wm, r_roi]
labs = ["참값", "백질 전체\n씨앗", "끝 영역\n씨앗"]
cols = [C["gray"], C["blue"], C["red"]]
bars = a2.bar(range(3), vals, color=cols, width=0.6)
for k, v in enumerate(vals):
    a2.text(k, v + 0.15, f"{v:.1f}배", ha="center", fontsize=8.5)
a2.set_xticks(range(3))
a2.set_xticklabels(labs, fontsize=8.5)
a2.set_ylabel("짧은 다발 ÷ 긴 다발")
a2.set_title("(나) 20 mm 대 100 mm 다발", fontsize=9.5)
a2.set_ylim(0, 8.6)
print("비: 백질 씨앗", r_wm, "끝 영역", r_roi, "봉우리 L", lam)
fig.tight_layout()
save(fig, __file__)
