from figstyle import plt, np, save, C

# 합성 휴지기 자료: TR 2 s, 300 볼륨. 회백질 300 복셀은 독립 네트워크 6개 중 하나를 담고,
# 모든 조직이 구조화된 잡음 원천 4개(호흡 변동, 접힌 심박, 움직임 잔여, 표류)를 나눠 가진다.
TR, NV = 2.0, 300
t = np.arange(NV) * TR
rng = np.random.default_rng(21)


def band(n, fl, fh):
    f = np.fft.rfftfreq(NV, TR)
    X = rng.normal(size=(n, f.size)) + 1j * rng.normal(size=(n, f.size))
    X[:, (f < fl) | (f > fh)] = 0
    x = np.fft.irfft(X, NV, axis=1)
    return x / x.std(axis=1, keepdims=True)


net = band(6, 0.01, 0.1)
resp = band(1, 0.02, 0.05)[0]                                   # 호흡 깊이 변동
card = np.sin(2 * np.pi * 0.15 * t + 0.3 * np.cumsum(rng.normal(0, 0.05, NV)))  # 접힌 심박
mot = np.convolve(rng.normal(0, 1, NV) * (rng.random(NV) < 0.05) * 3, np.exp(-np.arange(8) / 2))[:NV]
drift = (t / t[-1]) ** 2
Nz = np.vstack([resp, card, mot / mot.std(), drift / drift.std()])
nG, nW, nF = 300, 200, 100
lab = rng.integers(0, 6, nG)
LG = np.abs(rng.normal([0.9, 0.3, 0.6, 0.5], 0.25, (nG, 4)))
G = net[lab] * 1.0 + LG @ Nz + rng.normal(0, 0.8, (nG, NV))
LW = np.abs(rng.normal([0.7, 0.2, 0.5, 0.6], 0.25, (nW, 4)))
LF = np.abs(rng.normal([0.6, 1.0, 0.8, 0.3], 0.25, (nF, 4)))
WF = np.vstack([LW @ Nz + rng.normal(0, 0.8, (nW, NV)), LF @ Nz + rng.normal(0, 1.0, (nF, NV))])

# aCompCor: 백질+뇌척수액 시계열을 평균 제거 후 주성분 분석, 상위 5개를 회귀자로.
Wc = WF - WF.mean(1, keepdims=True)
U, S, Vt = np.linalg.svd(Wc, full_matrices=False)
ve = S ** 2 / np.sum(S ** 2)
K = 5
X = np.column_stack([np.ones(NV), Vt[:K].T])
beta = np.linalg.lstsq(X, G.T, rcond=None)[0]
Gc = G - (X @ beta).T + G.mean(1, keepdims=True)
print("var expl top5", ve[:5].round(3), ve[:5].sum().round(2))


def pair_r(D):
    Dz = (D - D.mean(1, keepdims=True)) / D.std(1, keepdims=True)
    R = Dz @ Dz.T / NV
    iu = np.triu_indices(nG, 1)
    diff = lab[iu[0]] != lab[iu[1]]
    return R[iu][diff], R[iu][~diff]


rb_d, rb_s = pair_r(G)
ra_d, ra_s = pair_r(Gc)
print("diff-net r before", np.median(rb_d).round(2), "after", np.median(ra_d).round(2))
print("same-net r before", np.median(rb_s).round(2), "after", np.median(ra_s).round(2))
i0 = 0
print("r with truth before", np.corrcoef(G[i0], net[lab[i0]])[0, 1].round(2),
      "after", np.corrcoef(Gc[i0], net[lab[i0]])[0, 1].round(2))

fig = plt.figure(figsize=(7.4, 4.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], width_ratios=[1, 1.25], hspace=0.55, wspace=0.3)
a = fig.add_subplot(gs[0, :])
z = lambda s: (s - s.mean()) / s.std()
a.plot(t, z(G[i0]) + 3.6, color=C["gray"], lw=0.9)
a.plot(t, z(Gc[i0]), color=C["blue"], lw=1.0)
a.plot(t, z(net[lab[i0]]), color=C["green"], lw=1.2, ls="--")
a.text(605, 3.6, "보정 전", fontsize=8, color=C["gray"], va="center")
a.text(605, 1.1, "CompCor 뒤", fontsize=8, color=C["blue"], va="center")
a.text(605, -1.2, "참 신경 신호(점선)", fontsize=8, color=C["green"], va="center")
a.set_xlim(0, 600)
a.set_yticks([])
a.spines["left"].set_visible(False)
a.set_xlabel("시간 (s)")
a.set_title("(가) 회백질 복셀 하나의 시계열 (각각 z 점수)", fontsize=10, loc="left")

b = fig.add_subplot(gs[1, 0])
m = 12
b.bar(np.arange(1, m + 1), ve[:m] * 100, color=[C["purple"] if i < K else C["gray"] for i in range(m)])
b.set_xlabel("백질·뇌척수액 주성분 번호")
b.set_ylabel("설명 분산 (%)")
b.set_title(f"(나) 상위 {K}개를 회귀자로", fontsize=10, loc="left")

c = fig.add_subplot(gs[1, 1])
bins = np.linspace(-0.4, 1.0, 57)
c.hist(rb_d, bins, color=C["gray"], alpha=0.6, density=True, label="보정 전")
c.hist(ra_d, bins, color=C["blue"], alpha=0.6, density=True, label="CompCor 뒤")
c.axvline(0, color=C["ink"], lw=0.7)
c.set_xlabel("서로 다른 네트워크 복셀 쌍의 상관")
c.set_yticks([])
c.spines["left"].set_visible(False)
c.legend(fontsize=7.5, loc="upper right")
c.set_title("(다) 가짜 연결이 0 근처로", fontsize=10, loc="left")
save(fig, __file__)
