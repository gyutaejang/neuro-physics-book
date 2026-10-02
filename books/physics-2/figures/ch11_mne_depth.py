from figstyle import plt, np, save, C

# 최소 노름 추정(MNE)의 깊이 편향과 sLORETA의 표준화.
# 장난감 모형은 앞 그림과 같다. 실제 소스: x = 2 cm, 깊이 4 cm, 10 nA·m. 센서 잡음 0.1 μV, λ² = 0.3.
xs = (np.arange(32) - 15.5) * 0.75
xg = np.arange(-10, 10.01, 0.5)
dg = np.arange(2.0, 6.01, 0.5)
X, D = np.meshgrid(xg, dg)
sx, sd = X.ravel(), D.ravel()
dx = (xs[:, None] - sx[None, :]) * 1e-2
L = 2 * 1e-9 * sd[None, :] * 1e-2 / (4 * np.pi * 0.33 * (dx**2 + (sd[None, :] * 1e-2) ** 2) ** 1.5) * 1e6
k0 = int(np.where(np.isclose(sx, 2) & np.isclose(sd, 4))[0][0])
j = np.zeros(L.shape[1])
j[k0] = 10
rng = np.random.default_rng(3)
y0 = L @ j
y = y0 + rng.normal(0, 0.1, 32)
lam2 = 0.3
K = L.T @ np.linalg.inv(L @ L.T + lam2 * np.eye(32))      # 역연산자 (369 × 32)
jh = K @ y
Rdiag = np.einsum("ij,ji->i", K, L)                         # 해상도 행렬의 대각 성분
slor = jh**2 / Rdiag
for name, v in (("MNE", np.abs(jh)), ("sLORETA", slor)):
    m = np.argmax(v)
    print(name, "최대 위치 x =", sx[m], "깊이 =", sd[m])
print("MNE 최대 |ĵ|", np.abs(jh).max(), "nA·m (실제 10)")

fig = plt.figure(figsize=(6.6, 4.4))
gs = fig.add_gridspec(3, 2, height_ratios=[0.9, 1, 1], width_ratios=[1, 0.025], hspace=0.8, wspace=0.03)
a = fig.add_subplot(gs[0, 0])
a.plot(xs, y0, color=C["gray"], lw=1.2, label="잡음 없는 값")
a.plot(xs, y, "o", ms=3.5, color=C["blue"], label="측정값 (잡음 0.1 μV)")
a.set_xlim(-12, 12)
a.set_ylabel("μV")
a.set_title("(가) 센서 32개의 측정값 y", fontsize=9.5, loc="left")
a.plot([], [], "x", color=C["red"], ms=7, mew=2, label="실제 소스 자리")
a.plot([], [], "o", ms=7, mfc="none", mec=C["ink"], mew=1.2, label="추정 지도의 최댓값")
a.legend(fontsize=7.6, loc="upper left", ncol=2)
a.set_ylim(-0.3, 7.2)
a.tick_params(labelsize=8)

maps = [(np.abs(jh), "(나) 최소 노름 추정 |ĵ|: 최댓값이 가장 얕은 줄(깊이 2 cm)에 붙는다", "nA·m"),
        (slor / slor.max(), "(다) sLORETA (|ĵ|²을 해상도로 나눈 값): 최댓값이 실제 깊이로 돌아온다", "")]
for i, (v, title, unit) in enumerate(maps):
    a = fig.add_subplot(gs[i + 1, 0])
    Z = v.reshape(D.shape)
    im = a.imshow(Z, cmap="Blues", vmin=0, vmax=Z.max(), extent=[-10.25, 10.25, -6.25, -1.75],
                  aspect="equal", interpolation="nearest")
    a.plot(2, -4, "x", color=C["red"], ms=8, mew=2, label="실제 소스")
    m = np.unravel_index(np.argmax(Z), Z.shape)
    a.plot(xg[m[1]], -dg[m[0]], "o", ms=8, mfc="none", mec=C["ink"], mew=1.2, label="추정 최댓값")
    a.set_xlim(-12, 12)
    a.set_yticks([-2, -4, -6])
    a.set_yticklabels(["2", "4", "6"])
    a.set_ylabel("깊이 (cm)", fontsize=8.5)
    a.set_title(title, fontsize=9, loc="left")
    a.tick_params(labelsize=8)
    if i == 1:
        a.set_xlabel("x (cm)")
    cb = fig.colorbar(im, cax=fig.add_subplot(gs[i + 1, 1]))
    cb.ax.tick_params(labelsize=7)
    if unit:
        cb.ax.set_title(unit, fontsize=7.5)
save(fig, __file__)
