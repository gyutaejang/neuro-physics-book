import itertools

from scipy import stats

from figstyle import plt, np, C, save

# 한 데이터셋, 54개의 합리적인 분석 경로. 환자가 대조군보다 ROI 연결성이 약간 낮다(참 d = 0.3).
rng = np.random.default_rng(12)
n = 40                                           # 집단당
g = np.r_[np.ones(n), np.zeros(n)]               # 1 = 환자
motion = rng.gamma(2.0, 0.08, 2 * n) * (1 + 0.6 * g)          # 평균 FD (mm), 환자가 더 움직인다
age = 40 + 10 * rng.standard_normal(2 * n) + 4 * g
core = -0.3 * g + rng.standard_normal(2 * n)
rings = [0.5 * core + rng.standard_normal(2 * n) * 0.9 for _ in range(3)]  # 효과 없는 이웃 복셀
art = -2.0 * (motion - motion.mean()) - 0.02 * (age - age.mean())
roi = {"작은 ROI": core, "중간 ROI": (core + rings[0]) / 2, "아틀라스 ROI": (core + sum(rings)) / 4}

choices = {
    "ROI": list(roi),
    "움직임": ["처리 안 함", "공변량", "FD > 0.3 제외"],
    "이상치": ["유지", "|z| > 2.5 제외", "|z| > 2 제외"],
    "나이": ["공변량 없음", "나이 공변량"],
}
rows = []
for combo in itertools.product(*choices.values()):
    r, mo, ou, ag = combo
    yv = roi[r] + art
    keep = np.ones(2 * n, bool)
    if mo == "FD > 0.3 제외":
        keep &= motion <= 0.3
    z = (yv - yv[keep].mean()) / yv[keep].std()
    if ou != "유지":
        keep &= np.abs(z) <= (2.5 if "2.5" in ou else 2.0)
    cols = [np.ones(keep.sum()), g[keep]]
    if mo == "공변량":
        cols.append(motion[keep])
    if ag == "나이 공변량":
        cols.append(age[keep])
    D = np.column_stack(cols)
    yk = yv[keep]
    b, *_ = np.linalg.lstsq(D, yk, rcond=None)
    res = yk - D @ b
    dof = len(yk) - D.shape[1]
    s2 = res @ res / dof
    se = np.sqrt(s2 * np.linalg.inv(D.T @ D)[1, 1])
    sd = np.sqrt(s2)
    t = b[1] / se
    pval = 2 * stats.t.sf(abs(t), dof)
    rows.append((b[1] / sd, 1.96 * se / sd, pval, combo))

rows.sort(key=lambda r: r[0])
eff = np.array([r[0] for r in rows]); ci = np.array([r[1] for r in rows]); pv = np.array([r[2] for r in rows])
sig = pv < 0.05
print("경로 %d개, 효과(표준화) 범위 %.2f ~ %.2f, 유의 %d개 (%.0f %%), p 범위 %.4f ~ %.2f" %
      (len(rows), eff.min(), eff.max(), sig.sum(), 100 * sig.mean(), pv.min(), pv.max()))
for key in choices:
    for opt in choices[key]:
        m = np.array([opt in r[3] for r in rows])
        print("  ", key, opt, "유의 비율 %.2f, 평균 효과 %.2f" % (sig[m].mean(), eff[m].mean()))

fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1], hspace=0.08)
a1 = fig.add_subplot(gs[0]); a2 = fig.add_subplot(gs[1], sharex=a1)
x = np.arange(len(rows))
for i in x:
    col = C["red"] if sig[i] else C["gray"]
    a1.plot([i, i], [eff[i] - ci[i], eff[i] + ci[i]], color=col, lw=0.8, alpha=0.6)
    a1.scatter([i], [eff[i]], s=9, color=col, zorder=3)
a1.axhline(0, color=C["ink"], lw=0.6)
a1.axhline(-0.3, color=C["blue"], lw=1.2, ls="--")
a1.text(len(rows) - 0.5, -0.27, "참 효과 −0.3", fontsize=7.5, color=C["blue"], ha="right", va="bottom")
a1.set_ylabel("집단 차 (표준화)")
a1.text(0.01, 0.97, "빨강: $p$ < 0.05 (%d / %d 경로)" % (sig.sum(), len(rows)),
        transform=a1.transAxes, fontsize=7.8, va="top", color=C["red"])
a1.tick_params(labelbottom=False)
a1.set_title("같은 데이터, 54개의 분석 경로 (효과 크기 순으로 정렬)", fontsize=10)

ylab, yy = [], 0
for key in choices:
    for opt in choices[key]:
        m = np.array([opt in r[3] for r in rows])
        a2.scatter(x[m], np.full(m.sum(), yy), s=5, marker="s",
                   color=np.where(sig[m], C["red"], C["gray"]))
        ylab.append(f"{key}: {opt}")
        yy -= 1
    yy -= 0.5
ticks = []
yy = 0
for key in choices:
    for opt in choices[key]:
        ticks.append(yy); yy -= 1
    yy -= 0.5
a2.set_yticks(ticks); a2.set_yticklabels(ylab, fontsize=6.5)
a2.set_xticks([])
a2.set_xlabel("분석 경로")
a2.spines["left"].set_visible(False)
a2.tick_params(axis="y", length=0)
a2.set_xlim(-1, len(rows))
save(fig, __file__)
