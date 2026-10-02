from figstyle import plt, np, save, C

# 30방향, b = 1000 s/mm² 모의 데이터에서 텐서를 맞추고 타원체로 그린다.
rng = np.random.default_rng(11)
n = 30
k = np.arange(n) + 0.5
z = 1 - k / n                                     # 위쪽 반구에 고르게 (나선 배치)
phi = np.pi * (1 + 5 ** 0.5) * k
g = np.c_[np.sqrt(1 - z ** 2) * np.cos(phi), np.sqrt(1 - z ** 2) * np.sin(phi), z]
b = 1000.0
snr = 30


def rot(axis_angle_deg):
    a = np.radians(axis_angle_deg)
    return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])


def tensor(l, ang=0):
    R = rot(ang)
    return R @ np.diag(l) @ R.T * 1e-3


def simulate(Ds, fr):
    S = sum(f * np.exp(-b * np.einsum("ij,jk,ik->i", g, D, g)) for D, f in zip(Ds, fr))
    noisy = np.abs(S + rng.normal(0, 1 / snr, n) + 1j * rng.normal(0, 1 / snr, n))
    s0 = abs(1 + rng.normal(0, 1 / snr) + 1j * rng.normal(0, 1 / snr))
    return s0, noisy


def fit(s0, S):
    # ln(S/S0) = -b gᵀ D g, 미지수 6개 (Dxx, Dyy, Dzz, Dxy, Dxz, Dyz)
    A = -b * np.c_[g[:, 0] ** 2, g[:, 1] ** 2, g[:, 2] ** 2,
                   2 * g[:, 0] * g[:, 1], 2 * g[:, 0] * g[:, 2], 2 * g[:, 1] * g[:, 2]]
    d = np.linalg.lstsq(A, np.log(S / s0), rcond=None)[0]
    return np.array([[d[0], d[3], d[4]], [d[3], d[1], d[5]], [d[4], d[5], d[2]]])


def fa_md(l):
    md = l.mean()
    return np.sqrt(1.5 * ((l - md) ** 2).sum() / (l ** 2).sum()), md


cases = [("뇌척수액", [tensor([3.0, 3.0, 3.0])], [1.0], C["blue"]),
         ("회백질", [tensor([0.95, 0.8, 0.7], 20)], [1.0], C["green"]),
         ("백질 한 다발", [tensor([1.7, 0.3, 0.3], 30)], [1.0], C["purple"]),
         ("직각 교차", [tensor([1.7, 0.3, 0.3], 30), tensor([1.7, 0.3, 0.3], 120)], [0.5, 0.5], C["red"])]

fig = plt.figure(figsize=(7.4, 2.7))
u = np.linspace(0, 2 * np.pi, 40)
v = np.linspace(0, np.pi, 20)
sph = np.array([np.outer(np.cos(u), np.sin(v)), np.outer(np.sin(u), np.sin(v)),
                np.outer(np.ones_like(u), np.cos(v))])

# (가) 방향 배치와 백질 복셀의 신호
ax = fig.add_subplot(1, 5, 1, projection="3d")
s0, Swm = simulate(cases[2][1], cases[2][2])
sc = ax.scatter(g[:, 0], g[:, 1], g[:, 2], c=Swm / s0, cmap="Blues_r", vmin=0, vmax=1, s=16,
                edgecolor=C["ink"], linewidth=0.3, depthshade=False)
ax.plot_wireframe(*sph, color=C["gray"], lw=0.2, alpha=0.4, rstride=2, cstride=4)
ax.set_title("30방향 (백질 신호)", fontsize=9.5, pad=-2)
cb = fig.colorbar(sc, ax=ax, shrink=0.45, pad=0.02, location="bottom")
cb.set_label("$S/S_0$", fontsize=8.5)
cb.ax.tick_params(labelsize=8)

for i, (name, Ds, fr, col) in enumerate(cases):
    s0, S = simulate(Ds, fr)
    Dfit = fit(s0, S)
    lam, vec = np.linalg.eigh(Dfit)
    lam = np.clip(lam[::-1], 1e-6, None)
    vec = vec[:, ::-1]
    fa, md = fa_md(lam * 1e3)
    pts = vec @ (np.sqrt(lam * 1e3)[:, None] * sph.reshape(3, -1))
    X, Y, Z = (pts.reshape(3, *sph.shape[1:]))
    ax = fig.add_subplot(1, 5, i + 2, projection="3d")
    ax.plot_surface(X, Y, Z, color=col, alpha=0.55, linewidth=0, shade=True)
    if name == "직각 교차":
        for D in Ds:
            e = np.linalg.eigh(D)[1][:, -1] * 1.6
            ax.plot([-e[0], e[0]], [-e[1], e[1]], [0, 0], color=C["ink"], lw=1.0, ls="--")
    elif name.startswith("백질"):
        e = vec[:, 0] * 1.6
        ax.plot([-e[0], e[0]], [-e[1], e[1]], [-e[2], e[2]], color=C["ink"], lw=1.0, ls="--")
    ax.set_title(name, fontsize=9.5, pad=-2)
    tl = np.linalg.eigvalsh(Ds[0]) * 1e3
    tfa, tmd = fa_md(tl)
    tag = "한 다발 " if len(Ds) > 1 else "참 "
    ax.text2D(0.5, 0.02, f"FA {fa:.2f} ({tag}{tfa:.2f})\nMD {md:.2f} ({tag}{tmd:.2f})", transform=ax.transAxes, ha="center",
              va="top", fontsize=8.5)
for a in fig.axes:
    if hasattr(a, "set_zlim"):
        r = 1.8
        a.set_xlim(-r, r); a.set_ylim(-r, r); a.set_zlim(-r, r)
        a.set_box_aspect((1, 1, 1), zoom=1.45)
        a.view_init(elev=28, azim=-60)
        a.set_axis_off()
fig.subplots_adjust(left=0, right=1, wspace=0.05, top=0.9, bottom=0.17)
save(fig, __file__)
