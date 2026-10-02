from figstyle import plt, np, save, C

# MNI 좌표를 탈라이라크 좌표로 바꾸는 근사 변환(Brett의 mni2tal)으로 본 두 공간의 차이.
UP = np.array([[0.9900, 0, 0], [0, 0.9688, 0.0460], [0, -0.0485, 0.9189]])   # z ≥ 0
LO = np.array([[0.9900, 0, 0], [0, 0.9688, 0.0420], [0, -0.0485, 0.8390]])   # z < 0


def mni2tal(p):
    p = np.asarray(p, float)
    out = np.where(p[..., 2:3] >= 0, p @ UP.T, p @ LO.T)
    return out


Y, Z = np.meshgrid(np.linspace(-105, 72, 200), np.linspace(-50, 80, 160))
P = np.stack([np.zeros_like(Y), Y, Z], -1)
D = mni2tal(P) - P
mag = np.linalg.norm(D, axis=-1)
inside = ((Y + 17) / 88) ** 2 + ((Z - 15) / 65) ** 2 <= 1      # 대략의 뇌 윤곽(시상면)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[2.3, 1], wspace=0.8))
im = a1.imshow(np.where(inside, mag, np.nan), origin="lower", extent=[Y.min(), Y.max(), Z.min(), Z.max()],
               cmap="Blues", vmin=0, vmax=10)
g = np.meshgrid(np.arange(-90, 61, 20), np.arange(-40, 76, 15))
gp = np.stack([np.zeros_like(g[0], float), g[0], g[1]], -1)
ins = ((g[0] + 17) / 88) ** 2 + ((g[1] - 15) / 65) ** 2 <= 0.95
gd = mni2tal(gp) - gp
a1.quiver(g[0][ins], g[1][ins], gd[..., 1][ins], gd[..., 2][ins], color=C["red"], angles="xy",
          scale_units="xy", scale=0.5, width=0.005)
a1.axhline(0, color=C["gray"], lw=0.6, ls=":")
a1.plot(0, 0, "+", color=C["ink"], ms=8)
a1.text(2, 2.5, "AC", fontsize=8)
a1.set_xlabel("y (mm, 앞쪽 +)")
a1.set_ylabel("z (mm, 위쪽 +)")
a1.set_title("(가) 정중 시상면, x = 0", fontsize=10)
cb = fig.colorbar(im, ax=a1, shrink=0.85, pad=0.02)
cb.set_label("어긋남 (mm)", fontsize=9)

pts = [("브로카 부근\n(−48, 16, 12)", (-48, 16, 12)), ("보조운동영역\n(0, −10, 65)", (0, -10, 65)),
       ("편도체\n(−22, −4, −18)", (-22, -4, -18)), ("소뇌\n(20, −62, −30)", (20, -62, -30)),
       ("쐐기앞소엽\n(0, −60, 40)", (0, -60, 40))]
vals = [np.linalg.norm(mni2tal(p) - np.array(p, float)) for _, p in pts]
a2.barh(range(len(pts)), vals, color=C["blue"], height=0.6)
for k, v in enumerate(vals):
    a2.text(v + 0.15, k, f"{v:.1f}", va="center", fontsize=8.5)
a2.set_yticks(range(len(pts)))
a2.set_yticklabels([s for s, _ in pts], fontsize=8)
a2.invert_yaxis()
a2.set_xlim(0, 9)
a2.set_xlabel("어긋남 (mm)")
a2.set_title("(나) 같은 숫자, 다른 자리", fontsize=10)
save(fig, __file__)
