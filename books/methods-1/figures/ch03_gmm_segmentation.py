from figstyle import plt, np, save, C
from ch03_bias_field import phantom, t1_image, brain_mask

# 뇌 안 밝기 히스토그램에 3-성분 혼합 가우스 모형(GMM)을 EM으로 맞춘다.
frac = phantom()
img = t1_image(frac)
mask = brain_mask(frac)
x = img[mask]


def gmm_em(x, mu, sd, w, n_iter=200):
    for _ in range(n_iter):
        lik = w * np.exp(-0.5 * ((x[:, None] - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        r = lik / lik.sum(axis=1, keepdims=True)          # E 단계: 복셀별 소속 확률
        nk = r.sum(axis=0)                                 # M 단계: 가중 평균과 분산
        w = nk / len(x)
        mu = (r * x[:, None]).sum(axis=0) / nk
        sd = np.sqrt((r * (x[:, None] - mu) ** 2).sum(axis=0) / nk)
    return mu, sd, w


mu, sd, w = gmm_em(x, np.array([0.2, 0.5, 0.8]), np.full(3, 0.1), np.full(3, 1 / 3))


def post(v):
    lik = w * np.exp(-0.5 * ((np.atleast_1d(v)[:, None] - mu) / sd) ** 2) / sd
    return lik / lik.sum(axis=1, keepdims=True)


if __name__ == "__main__":
    print("mu", mu.round(3), "sd", sd.round(3), "w", w.round(3))
    true_w = [frac[k][mask].sum() / mask.sum() for k in ("csf", "gm", "wm")]
    print("참 분율", np.round(true_w, 3))
    for v in (0.60, 0.65, 0.70):
        print(v, "사후", post(v).round(3), "선형 GM 분율", round((mu[2] - v) / (mu[2] - mu[1]), 3))
    pvm = (frac["gm"] > 0.05) & (frac["gm"] < 0.95) & mask
    print("부분 용적 복셀 비율", round(pvm.sum() / mask.sum(), 3))
    pg = post(x)[:, 1]
    print("GM 부피: 참 분율 합", round(frac["gm"][mask].sum()), "사후확률 합", round(pg.sum()),
          "문턱>0.5 개수", int((pg > 0.5).sum()))

    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.8), gridspec_kw=dict(width_ratios=[1.2, 1.2, 1.0], wspace=0.36))
    ax = axs[0]
    bins = np.linspace(0, 1, 81)
    ax.hist(x, bins=bins, density=True, color="#c9d6e8", edgecolor="none")
    g = np.linspace(0, 1, 400)
    cols = [C["gray"], C["red"], C["blue"]]
    names = ["CSF", "GM", "WM"]
    comp = w * np.exp(-0.5 * ((g[:, None] - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
    for k in range(3):
        ax.plot(g, comp[:, k], color=cols[k], lw=1.3)
        ax.text(mu[k], comp[:, k].max() + 0.15, names[k], ha="center", fontsize=8, color=cols[k])
    ax.plot(g, comp.sum(axis=1), color=C["ink"], lw=0.8, ls="--")
    ax.axvspan(mu[1] + 1.5 * sd[1], mu[2] - 1.5 * sd[2], color=C["purple"], alpha=0.12, lw=0)
    ax.annotate("부분 용적\n(GM+WM)", xy=(0.64, 0.5), xytext=(0.47, 3.1), fontsize=7.5, color=C["purple"],
                ha="center", arrowprops=dict(arrowstyle="-", color=C["purple"], lw=0.6))
    ax.set_xlabel("밝기")
    ax.set_ylabel("확률 밀도")
    ax.set_xlim(0, 1)
    ax.set_title("(가) 히스토그램과 GMM", fontsize=9.5)

    ax = axs[1]
    P = post(g)
    for k in range(3):
        ax.plot(g, P[:, k], color=cols[k], lw=1.5, label=f"P({names[k]} | 밝기)")
    lin = np.clip((mu[2] - g) / (mu[2] - mu[1]), 0, 1)
    sel = (g > mu[1]) & (g < mu[2])
    ax.plot(g[sel], lin[sel], color=C["red"], lw=1.0, ls=":", label="GM 분율(선형 혼합)")
    ax.set_xlabel("밝기")
    ax.set_ylabel("확률 또는 분율")
    ax.set_xlim(0, 1); ax.set_ylim(-0.02, 1.25)
    ax.set_yticks([0, 0.5, 1])
    ax.legend(fontsize=6.8, loc="upper center", ncol=2, handlelength=1.4, columnspacing=0.8)
    ax.set_title("(나) 사후 확률 대 분율", fontsize=9.5)

    ax = axs[2]
    pmap = np.zeros(img.shape)
    pmap[mask] = pg
    ax.imshow(pmap[8:108, 46:146], cmap="magma", vmin=0, vmax=1)
    ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values():
        s_.set_visible(False)
    ax.set_title("(다) GM 확률 지도", fontsize=9.5)
    save(fig, __file__)
