from figstyle import plt, np, save, C
from matplotlib.patches import Ellipse

L1, L2 = 1.7, 0.3   # 섬유 하나의 축 방향, 지름 방향 확산도 (10⁻³ mm²/s)


def fiber(th):
    u = np.array([np.cos(th), np.sin(th), 0.0])
    return L2 * np.eye(3) + (L1 - L2) * np.outer(u, u)


def fa(w):
    return np.sqrt(0.5) * np.sqrt(((w[0] - w[1]) ** 2 + (w[1] - w[2]) ** 2 + (w[2] - w[0]) ** 2) / (w ** 2).sum())


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1.0, 1.0]))

# 왼쪽: 2차원 타원으로 본 텐서
for x0, th2, title in ((0, None, "한 방향 다발"), (3.2, np.pi / 2, "직각으로 교차하는 두 다발")):
    T = fiber(0) if th2 is None else (fiber(0) + fiber(th2)) / 2
    w, v = np.linalg.eigh(T[:2, :2])
    ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
    a1.add_patch(Ellipse((x0, 0), 1.25 * np.sqrt(w[1]), 1.25 * np.sqrt(w[0]), angle=ang,
                         facecolor=C["purple"], alpha=0.25, edgecolor=C["purple"], lw=1.5))
    for th in ([0] if th2 is None else [0, th2]):
        for k in (-0.35, 0, 0.35):
            dxy = np.array([np.cos(th), np.sin(th)])
            nrm = np.array([-dxy[1], dxy[0]]) * k
            p0, p1 = -1.15 * dxy + nrm, 1.15 * dxy + nrm
            a1.plot([x0 + p0[0], x0 + p1[0]], [p0[1], p1[1]], color=C["green"], lw=1.0, alpha=0.7)
    w3 = np.sort(np.linalg.eigvalsh(T))[::-1]
    a1.text(x0, 1.55, title, ha="center", fontsize=9, weight="bold")
    a1.text(x0, -1.5, f"FA {fa(w3):.2f}   MD {w3.mean():.2f}", ha="center", fontsize=8.5)
    a1.text(x0, -1.9, f"지름 방향 확산도 {(w3[1] + w3[2]) / 2:.2f}", ha="center", fontsize=8.5)
a1.text(1.6, -2.45, "섬유(초록)는 두 그림에서 똑같이 멀쩡하다", ha="center", fontsize=8, color=C["gray"])
a1.set_xlim(-1.5, 4.7)
a1.set_ylim(-2.7, 1.9)
a1.set_aspect("equal")
a1.axis("off")

# 오른쪽: 교차 각도에 따른 지표
angs = np.linspace(0, 90, 91)
FA, AD, RD, MD = [], [], [], []
for a in angs:
    w = np.sort(np.linalg.eigvalsh((fiber(0) + fiber(np.radians(a))) / 2))[::-1]
    FA.append(fa(w)); AD.append(w[0]); RD.append((w[1] + w[2]) / 2); MD.append(w.mean())
a2.plot(angs, FA, color=C["red"], lw=2, label="FA")
a2.plot(angs, AD, color=C["blue"], lw=1.4, ls="--", label=r"축 방향 확산도 $\lambda_1$")
a2.plot(angs, RD, color=C["green"], lw=1.4, ls="-.", label="지름 방향 확산도")
a2.plot(angs, MD, color=C["gray"], lw=1.2, ls=":", label="MD")
a2.set_xlim(0, 90)
a2.set_ylim(0, 1.9)
a2.set_xticks([0, 30, 60, 90])
a2.set_xlabel("두 다발 사이의 각도 (°)")
a2.set_ylabel("FA, 또는 확산도 (10⁻³ mm²/s)")
a2.legend(fontsize=7.5, loc="upper right")
fig.tight_layout()
save(fig, __file__)
