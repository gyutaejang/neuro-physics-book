from figstyle import plt, np, save, C
from matplotlib.colors import LinearSegmentedColormap

# 정칙화 L-곡선. 앞 그림들과 같은 장난감 모형(센서 32개, 소스 자리 369개)에서
# 깊이 4 cm, x = 2 cm의 10 nA·m 쌍극자 + 센서마다 0.1 μV 잡음.
# 최소 노름 해 ĵ = Lᵀ(LLᵀ + λ²I)⁻¹y를 λ²마다 구해, 잔차 ‖y − Lĵ‖와 해의 크기 ‖ĵ‖를 찍는다.
xs = (np.arange(32) - 15.5) * 0.75
xg = np.arange(-10, 10.01, 0.5)
dg = np.arange(2.0, 6.01, 0.5)
X, D = np.meshgrid(xg, dg)
sx, sd = X.ravel(), D.ravel()
dx = (xs[:, None] - sx[None, :]) * 1e-2
L = 2 * 1e-9 * sd[None, :] * 1e-2 / (4 * np.pi * 0.33 * (dx**2 + (sd[None, :] * 1e-2) ** 2) ** 1.5) * 1e6
j = np.zeros(L.shape[1])
j[int(np.where(np.isclose(sx, 2) & np.isclose(sd, 4))[0][0])] = 10
rng = np.random.default_rng(3)
y = L @ j + rng.normal(0, 0.1, 32)


def mne(lam2):
    return L.T @ np.linalg.solve(L @ L.T + lam2 * np.eye(32), y)


lams = np.geomspace(1e-6, 1e2, 200)
res = np.array([np.linalg.norm(y - L @ mne(l)) for l in lams])
nrm = np.array([np.linalg.norm(mne(l)) for l in lams])
marks = [(1e-5, "너무 작은 λ²", C["red"]), (0.3, "알맞은 λ²", C["blue"]), (30, "너무 큰 λ²", C["gray"])]
ltxt = {1e-5: "10⁻⁵", 0.3: "0.3", 30: "30"}
offs = {1e-5: (8, 4), 0.3: (-62, -26), 30: (4, -26)}

fig = plt.figure(figsize=(7.3, 3.2))
gs = fig.add_gridspec(3, 2, width_ratios=[1, 1.15], hspace=0.6, wspace=0.3, top=0.86)
ax = fig.add_subplot(gs[:, 0])
ax.loglog(res, nrm, color=C["ink"], lw=1.4)
for l, lab, col in marks:
    jh = mne(l)
    r, n = np.linalg.norm(y - L @ jh), np.linalg.norm(jh)
    print(lab, "λ² =", l, "잔차", r, "해 크기", n)
    ax.plot(r, n, "o", ms=7, color=col)
    ax.annotate(f"{lab}\n(λ² = {ltxt[l]})", xy=(r, n), xytext=offs[l], textcoords="offset points",
                fontsize=8, color=col)
ax.axvline(np.sqrt(32) * 0.1, color=C["gray"], ls=":", lw=0.8)
ax.text(np.sqrt(32) * 0.1 * 1.1, 4.5, "잡음 크기\n√32 × 0.1 μV", fontsize=7.5, color=C["gray"], va="top")
ax.set_xlabel("잔차 ‖y − Lĵ‖ (μV)")
ax.set_ylabel("해의 크기 ‖ĵ‖ (nA·m)")
fig.text(0.08, 0.97, "(가) L-곡선", fontsize=9.5, ha="left")
fig.text(0.56, 0.97, "(나) λ²에 따른 추정 지도 (×: 실제 소스)", fontsize=9.5, ha="left")
ax.set_xlim(1e-3, 20)
ax.set_ylim(0.2, 60)

cmap = LinearSegmentedColormap.from_list("bwr_book", [C["blue"], "white", C["red"]])
for i, (l, lab, col) in enumerate(marks):
    a = fig.add_subplot(gs[i, 1])
    jh = mne(l).reshape(D.shape)
    m = np.abs(jh).max()
    a.imshow(jh, cmap=cmap, vmin=-m, vmax=m, extent=[-10.25, 10.25, -6.25, -1.75],
             aspect="equal", interpolation="nearest")
    a.plot(2, -4, "x", color=C["ink"], ms=6, mew=1.5)
    a.set_title(f"{lab}: 최대 |ĵ| = {m:.1f} nA·m", fontsize=8.5, color=col, pad=3)
    a.set_yticks([-2, -4, -6])
    a.set_yticklabels(["2", "4", "6"], fontsize=7)
    a.tick_params(axis="x", labelsize=7)
    if i < 2:
        a.set_xticklabels([])
    else:
        a.set_xlabel("x (cm)", fontsize=8.5)
    if i == 1:
        a.set_ylabel("깊이 (cm)", fontsize=8.5)
save(fig, __file__)
