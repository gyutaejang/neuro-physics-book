from figstyle import plt, np, save, C

# 세 기관의 피질 두께. 기관마다 평균(가산)과 퍼짐(곱셈)이 다르다. ComBat식 위치·척도 조정으로 맞춘다.
rng = np.random.default_rng(7)
SITES = ["기관 1", "기관 2", "기관 3"]
GAMMA = [0.00, 0.12, -0.08]          # 기관 평균 차이 (mm)
DELTA = [1.0, 1.6, 0.7]              # 기관 잡음 배율
AGE_RANGE = [(20, 80), (45, 85), (20, 60)]
SLOPE = -0.005                       # 나이 1년당 두께 변화 (mm)


def simulate(n=70):
    age, site, y = [], [], []
    for s, (lo, hi) in enumerate(AGE_RANGE):
        a = rng.uniform(lo, hi, n)
        age.append(a); site.append(np.full(n, s))
        y.append(2.50 + SLOPE * (a - 50) + GAMMA[s] + 0.07 * DELTA[s] * rng.standard_normal(n))
    return np.concatenate(age), np.concatenate(site), np.concatenate(y)


def combat(y, site, X):
    """한 특징에 대한 위치·척도 조정(경험적 베이즈 수축 없이). X: 보존할 공변량 열."""
    S = np.stack([(site == s).astype(float) for s in np.unique(site)], 1)
    D = np.column_stack([S, X])
    b, *_ = np.linalg.lstsq(D, y, rcond=None)
    w = S.mean(0)
    alpha = S.shape[1] and (b[:S.shape[1]] * w).sum()
    fitX = X @ b[S.shape[1]:]
    resid = y - S @ b[:S.shape[1]] - fitX
    sigma = np.sqrt(np.mean(resid ** 2))
    z = (y - alpha - fitX) / sigma
    out = np.empty_like(y)
    for s in np.unique(site):
        m = site == s
        out[m] = (z[m] - z[m].mean()) / z[m].std() * sigma + alpha + fitX[m]
    return out


def ols_slope(x, y):
    A = np.column_stack([np.ones_like(x), x])
    return np.linalg.lstsq(A, y, rcond=None)[0][1]


def confound_demo(reps=400, n=150):
    """기관 1에 환자가 80%, 기관 2에 20%. 참 환자 효과 −0.10 mm, 기관 1 평균 +0.10 mm."""
    est = {"참값": [], "기관 무시": [], "조화, 진단 뺌": [], "조화, 진단 포함": []}
    for _ in range(reps):
        site = np.repeat([0, 1], n)
        pat = np.concatenate([rng.random(n) < 0.8, rng.random(n) < 0.2]).astype(float)
        y = 2.5 - 0.10 * pat + 0.10 * (site == 0) + 0.08 * rng.standard_normal(2 * n)
        est["참값"].append(-0.10)
        est["기관 무시"].append(y[pat == 1].mean() - y[pat == 0].mean())
        h1 = combat(y, site, np.zeros((2 * n, 0)))
        est["조화, 진단 뺌"].append(h1[pat == 1].mean() - h1[pat == 0].mean())
        h2 = combat(y, site, pat[:, None])
        est["조화, 진단 포함"].append(h2[pat == 1].mean() - h2[pat == 0].mean())
    return {k: float(np.mean(v)) for k, v in est.items()}


if __name__ == "__main__":
    age, site, y = simulate()
    yh = combat(y, site, (age - 50)[:, None])
    for s in range(3):
        m = site == s
        print(SITES[s], "평균 %.3f→%.3f, SD %.3f→%.3f" % (y[m].mean(), yh[m].mean(), y[m].std(), yh[m].std()))
    print("나이 기울기(mm/년): 원자료 %.4f, 조화 %.4f, 참 %.4f" % (ols_slope(age, y), ols_slope(age, yh), SLOPE))
    cd = confound_demo()
    print({k: round(v, 3) for k, v in cd.items()})

    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.7), gridspec_kw=dict(width_ratios=[1, 1, 1.0], wspace=0.62))
    cols = [C["blue"], C["red"], C["green"]]
    for ax, data, ttl in [(axs[0], y, "(가) 원자료"), (axs[1], yh, "(나) 조화 뒤")]:
        for s in range(3):
            m = site == s
            ax.scatter(age[m], data[m], s=5, color=cols[s], alpha=0.6, lw=0, label=SITES[s])
            A = np.column_stack([np.ones(m.sum()), age[m]])
            b = np.linalg.lstsq(A, data[m], rcond=None)[0]
            xx = np.array(AGE_RANGE[s])
            ax.plot(xx, b[0] + b[1] * xx, color=cols[s], lw=1.4)
        ax.set_xlabel("나이 (세)")
        ax.set_ylim(2.05, 3.0)
        ax.set_xlim(15, 90)
        ax.set_title(ttl, fontsize=9.5)
    axs[0].set_ylabel("평균 피질 두께 (mm)")
    axs[0].legend(fontsize=7, loc="upper right", markerscale=2, handletextpad=0.2, borderaxespad=0.1)
    ax = axs[2]
    keys = list(cd)
    vals = [cd[k] for k in keys]
    bc = [C["gray"], C["red"], C["red"], C["blue"]]
    ax.barh(range(4), vals, color=bc, height=0.6)
    ax.set_yticks(range(4)); ax.set_yticklabels(keys, fontsize=7.5)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()
    ax.axvline(0, color=C["ink"], lw=0.7)
    ax.axvline(-0.10, color=C["gray"], lw=0.7, ls=":")
    for i, v in enumerate(vals):
        ax.text(0.004, i, f"{v:.3f}", va="center", ha="left", fontsize=7)
    ax.set_xlim(-0.13, 0.045)
    ax.set_xticks([-0.1, -0.05, 0])
    ax.set_xlabel("환자 − 대조 (mm)")
    ax.set_title("(다) 기관과 진단이 엉킬 때", fontsize=9.5)
    save(fig, __file__)
