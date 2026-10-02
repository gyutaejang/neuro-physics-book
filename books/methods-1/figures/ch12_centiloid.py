from figstyle import plt, np, save, C

# 센틸로이드 변환 (Klunk 2015): CL = 100 (SUVR - SUVR_YC) / (SUVR_AD - SUVR_YC).
# PiB 표준 분석의 고정점은 젊은 정상인 1.009, 알츠하이머병 2.076 (전체 소뇌 기준).
# 가상의 ¹⁸F 추적자 X를 같은 사람들에게 찍어 PiB 눈금으로 옮기는 과정을 합성 데이터로 보인다.
YC, AD = 1.009, 2.076
rng = np.random.default_rng(4)
load = np.r_[rng.normal(0, 4, 12), rng.uniform(5, 90, 14), rng.normal(100, 22, 14)]   # 참 아밀로이드 양 (CL)
pib = YC + (AD - YC) * load / 100 + rng.normal(0, 0.03, len(load))
trx = 1.02 + 0.66 * load / 100 + rng.normal(0, 0.022, len(load))
slope, icpt = np.polyfit(trx, pib, 1)
r2 = np.corrcoef(trx, pib)[0, 1] ** 2
to_cl = lambda s_pib: 100 * (s_pib - YC) / (AD - YC)
cl_x = lambda s: to_cl(slope * s + icpt)
print(f"PiB_calc = {slope:.3f} X + {icpt:.3f}, R2 = {r2:.3f}; CL = {100*slope/(AD-YC):.1f} X {100*(icpt-YC)/(AD-YC):+.1f}")
for s in (1.10, 1.20):
    print(s, round(cl_x(s), 1))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(width_ratios=[1, 1.15]))
grp = np.r_[np.zeros(12), np.ones(14), 2 * np.ones(14)].astype(int)
for g, col, lab in [(0, C["green"], "젊은 정상인"), (1, C["gray"], "노인 (다양)"), (2, C["red"], "전형적 AD")]:
    a1.plot(trx[grp == g], pib[grp == g], "o", color=col, ms=4, mfc="none" if g == 1 else col, label=lab)
xx = np.linspace(0.95, 1.9, 10)
a1.plot(xx, slope * xx + icpt, color=C["blue"], lw=1.4)
a1.text(1.30, 1.07, f"PiB = {slope:.2f} × X − {-icpt:.2f}\n$R^2$ = {r2:.2f}", fontsize=7.8, color=C["blue"])
a1.set_xlim(0.95, 1.9)
a1.set_ylim(0.85, 2.6)
a1.set_xlabel("추적자 X SUVR")
a1.set_ylabel("PiB SUVR")
a1.legend(fontsize=7.4, loc="upper left")
a1.set_title("(가) 같은 사람을 두 추적자로", fontsize=9.5)

# (나) 세 눈금을 나란히 놓는다
rows = [("PiB SUVR", lambda c: YC + (AD - YC) * c / 100, [1.0, 1.5, 2.0], "{:.1f}"),
        ("추적자 X SUVR", lambda c: (YC + (AD - YC) * c / 100 - icpt) / slope, [1.0, 1.2, 1.4, 1.6], "{:.1f}"),
        ("센틸로이드 (CL)", lambda c: c, [0, 50, 100], "{:.0f}")]
cmin, cmax = -10, 120
for k, (name, f, ticks, fmt) in enumerate(rows):
    y = 2 - k
    a2.plot([0, 1], [y, y], color=C["ink"], lw=1)
    for tv in ticks:
        c = np.interp(tv, [f(cmin), f(cmax)], [cmin, cmax])
        xp = (c - cmin) / (cmax - cmin)
        a2.plot([xp, xp], [y - 0.05, y + 0.05], color=C["ink"], lw=0.8)
        a2.text(xp, y - 0.1, fmt.format(tv), ha="center", va="top", fontsize=7.4, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.6))
    a2.text(-0.03, y, name, ha="right", va="center", fontsize=8)
for c, col, lab in [(0, C["green"], "0: 젊은 정상인 평균"), (100, C["red"], "100: 전형적 AD 평균"),
                    (12, C["blue"], "")]:
    xp = (c - cmin) / (cmax - cmin)
    a2.plot([xp, xp], [-0.05, 2.12], color=col, lw=1.1, ls="--" if c == 12 else "-", alpha=0.85)
    if lab:
        a2.text(xp, 2.2, lab, ha="center", va="bottom", fontsize=7.4, color=col)
xp12 = (12 - cmin) / (cmax - cmin)
a2.annotate("12 CL", xy=(xp12, -0.05), xytext=(xp12 + 0.12, -0.42), fontsize=7.6, color=C["blue"],
            arrowprops=dict(arrowstyle="-", color=C["blue"], lw=0.6), va="center")
a2.set_xlim(-0.55, 1.05)
a2.set_ylim(-0.6, 2.55)
a2.axis("off")
a2.set_title("(나) 세 눈금, 하나의 척도", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
