from figstyle import plt, np, save, C

# 해상도 행렬 R = K L 의 열(점 퍼짐 함수, PSF). 잡음 없이 한 자리에만 단위 소스를 두었을 때
# 최소 노름 추정이 그리는 지도다. 장난감 모형과 λ² = 0.3은 앞 그림과 같다.
xs = (np.arange(32) - 15.5) * 0.75
xg = np.arange(-10, 10.01, 0.5)
dg = np.arange(2.0, 6.01, 0.5)
X, D = np.meshgrid(xg, dg)
sx, sd = X.ravel(), D.ravel()
dx = (xs[:, None] - sx[None, :]) * 1e-2
L = 2 * 1e-9 * sd[None, :] * 1e-2 / (4 * np.pi * 0.33 * (dx**2 + (sd[None, :] * 1e-2) ** 2) ** 1.5) * 1e6
K = L.T @ np.linalg.inv(L @ L.T + 0.3 * np.eye(32))
Rm = K @ L
idx = lambda x, d: int(np.where(np.isclose(sx, x) & np.isclose(sd, d))[0][0])

fig = plt.figure(figsize=(7.3, 3.4))
gs = fig.add_gridspec(3, 2, width_ratios=[1.35, 1], hspace=0.55, wspace=0.3)
for i, d in enumerate([2.5, 4.0, 5.5]):
    a = fig.add_subplot(gs[i, 0])
    psf = Rm[:, idx(0, d)].reshape(D.shape)
    a.imshow(psf / psf.max(), cmap="Blues", vmin=0, vmax=1, extent=[-10.25, 10.25, -6.25, -1.75],
             aspect="equal", interpolation="nearest")
    a.plot(0, -d, "x", color=C["red"], ms=7, mew=2)
    a.set_yticks([-2, -4, -6])
    a.set_yticklabels(["2", "4", "6"], fontsize=7)
    a.tick_params(axis="x", labelsize=7)
    a.set_title(f"실제 깊이 {d:g} cm의 점 → 최대 R = {psf.max():.2f}", fontsize=8.5, loc="left", pad=3)
    if i < 2:
        a.set_xticklabels([])
    else:
        a.set_xlabel("x (cm)", fontsize=8.5)
    if i == 1:
        a.set_ylabel("깊이 (cm)", fontsize=8.5)
fig.text(0.1, 0.97, "(가) 최소 노름의 점 퍼짐 함수 (최댓값으로 나눔)", fontsize=9.5)

a = fig.add_subplot(gs[:, 1])
peak, spread, peak_s = [], [], []
for d in dg:
    k = idx(0, d)
    psf = Rm[:, k]
    m = np.argmax(np.abs(psf))
    peak.append(sd[m])
    dist = np.hypot(sx - 0, sd - d)
    spread.append(np.sqrt(np.sum(psf**2 * dist**2) / np.sum(psf**2)))
    s = psf**2 / np.diag(Rm)                    # sLORETA로 표준화한 PSF
    peak_s.append(sd[np.argmax(s)])
print("깊이", dg, "\nMNE 최댓값 깊이", peak, "\nsLORETA", peak_s, "\n퍼짐", np.round(spread, 2))
a.plot(dg, dg, color=C["gray"], lw=0.8, ls=":", label="오차 없음")
a.plot(dg, peak, "o-", color=C["blue"], ms=4, lw=1.4, label="MNE 최댓값의 깊이")
a.plot(dg, peak_s, "s--", color=C["red"], ms=4, lw=1.2, mfc="none", label="sLORETA 최댓값의 깊이")
a.plot(dg, spread, "^-", color=C["purple"], ms=4, lw=1.2, label="MNE 퍼짐 (cm)")
a.set_xlabel("실제 소스 깊이 (cm)")
a.set_ylabel("cm")
a.set_xlim(1.8, 6.2)
a.set_ylim(0, 6.5)
a.legend(fontsize=7.5, loc="upper left")
a.set_title("(나) 깊을수록 위로 끌리고 넓게 퍼진다", fontsize=9.5)
save(fig, __file__)
