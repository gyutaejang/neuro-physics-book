from figstyle import plt, np, save, C

# 관심 영역 150개를 머리 모양 타원체 안에 흩뿌리고, 참가자 40명 × 두 집단의 시계열을 합성한다.
# 참 연결: 네트워크 4개, 같은 네트워크 안 상관 0.4. 움직임 잡음: 70%는 거리 상수 20 mm로 공간 상관,
# 30%는 영역마다 독립이며, 분산은 참가자의 평균 FD에 비례한다.
rng = np.random.default_rng(8)
nR, NV, nS = 150, 300, 40
P = rng.uniform(-1, 1, (4000, 3)) * [70, 85, 60]
P = P[np.sum((P / [70, 85, 60]) ** 2, 1) < 1][:nR]
D = np.linalg.norm(P[:, None] - P[None], axis=2)
lab = rng.integers(0, 4, nR)
same = (lab[:, None] == lab[None]).astype(float)
St = 0.4 * same + 0.6 * np.eye(nR)
Km = 0.7 * np.exp(-D / 20.0) + 0.3 * np.eye(nR)   # 공간 상관 몫 + 영역마다 따로인 몫
iu = np.triu_indices(nR, 1)


def group_r(mfd, keep):
    """keep: 잡음 제거 뒤 남는 움직임 잡음의 비율."""
    out = []
    for fd in mfd:
        a2 = (fd / 0.1) * 0.6 * keep ** 2
        Cv = St + a2 * Km + 0.3 * np.eye(nR)
        Y = np.linalg.cholesky(Cv) @ rng.normal(size=(nR, NV))
        out.append(np.corrcoef(Y)[iu])
    return np.mean(out, axis=0)


low = rng.gamma(4, 0.1 / 4, nS)            # 평균 FD 약 0.10 mm
high = rng.gamma(4, 0.35 / 4, nS)          # 평균 FD 약 0.35 mm
print("mean FD", low.mean().round(3), high.mean().round(3))
d = D[iu]
res = {}
for keep, key in ((1.0, "raw"), (0.3, "clean")):
    res[key] = group_r(high, keep) - group_r(low, keep)
bins = np.arange(0, 181, 15)
fig, axs = plt.subplots(1, 2, figsize=(7.3, 3.0), sharey=True, gridspec_kw=dict(wspace=0.08))
for a, key, title in ((axs[0], "raw", "(가) 움직임 회귀만"), (axs[1], "clean", "(나) 강한 잡음 제거 뒤")):
    dr = res[key]
    a.scatter(d, dr, s=2, color=C["gray"], alpha=0.25, lw=0, rasterized=True)
    bc, bm = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (d >= lo) & (d < hi)
        if m.sum() > 30:
            bc.append((lo + hi) / 2)
            bm.append(dr[m].mean())
    a.plot(bc, bm, color=C["red"], lw=2, marker="o", ms=3.5)
    a.axhline(0, color=C["ink"], lw=0.7)
    a.set_xlabel("두 영역 사이 거리 (mm)")
    a.set_title(title, fontsize=10)
    a.set_xlim(0, 170)
    print(key, "short(<30)", dr[d < 30].mean().round(3), "long(>100)", dr[d > 100].mean().round(3))
axs[0].set_ylabel("Δr (많이 − 적게 움직인 집단)", fontsize=9)
axs[0].set_ylim(-0.1, 0.16)
axs[0].text(8, 0.14, "가까운 쌍: 연결이 강해 보임", fontsize=8, color=C["red"])
axs[0].text(165, 0.05, "먼 쌍: 약해 보임", fontsize=8, color=C["red"], ha="right")
save(fig, __file__)
