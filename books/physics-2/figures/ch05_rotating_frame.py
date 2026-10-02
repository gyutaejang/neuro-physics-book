from figstyle import plt, np, save, C

# 90° 펄스 동안 자화 M의 운동을 블로흐 식 dM/dt = γ M × B 로 직접 적분한다(이완 없음).
# 실제 3 T에서는 ω₀/ω₁ ≈ 30만이지만, 그림에서는 ω₀/ω₁ = 12로 줄였다.
w1 = 1.0
w0 = 12.0
tp = (np.pi / 2) / w1
t = np.linspace(0, tp, 4000)
dt = t[1] - t[0]


def rot(v, axis, ang):
    axis = axis / np.linalg.norm(axis)
    return (v * np.cos(ang) + np.cross(axis, v) * np.sin(ang)
            + axis * np.dot(axis, v) * (1 - np.cos(ang)))


M = np.array([0.0, 0.0, 1.0])
lab = [M]
for ti in t[:-1]:
    # 양성자는 B₀ 둘레를 −z 방향 감기(위에서 보아 시계 방향)로 돈다. B₁도 같은 방향으로 돌린다.
    b = np.array([w1 * np.cos(-w0 * ti), w1 * np.sin(-w0 * ti), w0])
    # dM/dt = M × b  (γ = 1 단위) → 축 −b 둘레의 회전
    M = rot(M, -b, np.linalg.norm(b) * dt)
    lab.append(M)
lab = np.array(lab)
# 회전 좌표계: z축 둘레로 +ω₀t 만큼 되돌린다
c, s = np.cos(w0 * t), np.sin(w0 * t)
rf = np.stack([c * lab[:, 0] - s * lab[:, 1], s * lab[:, 0] + c * lab[:, 1], lab[:, 2]], axis=1)

fig = plt.figure(figsize=(7.2, 3.5))
u = np.linspace(0, 2 * np.pi, 60)
for i, (P, title) in enumerate([(lab, "(가) 실험실 좌표계"), (rf, "(나) 회전 좌표계 (ω₀로 함께 돈다)")]):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d", computed_zorder=False)
    ax.plot(np.cos(u), np.sin(u), 0 * u, color=C["gray"], lw=0.6)
    ax.plot(np.cos(u), 0 * u, np.sin(u), color=C["gray"], lw=0.4, alpha=0.6)
    ax.plot(0 * u, np.cos(u), np.sin(u), color=C["gray"], lw=0.4, alpha=0.6)
    for d, lab_ in [((1.25, 0, 0), "x"), ((0, 1.25, 0), "y"), ((0, 0, 1.3), "z")]:
        ax.plot([0, d[0]], [0, d[1]], [0, d[2]], color=C["gray"], lw=0.7)
        ax.text(d[0] * 1.06, d[1] * 1.06, d[2] * 1.04, lab_ + ("′" if i == 1 and lab_ != "z" else ""),
                fontsize=9, color=C["gray"])
    ax.plot(P[:, 0], P[:, 1], P[:, 2], color=C["blue"], lw=1.4, zorder=5)
    e = P[-1]
    ax.quiver(0, 0, 0, e[0], e[1], e[2], color=C["red"], lw=2, arrow_length_ratio=0.15, zorder=6)
    ax.text(e[0] + 0.1, e[1] - 0.15, e[2] - 0.3, "M (끝)", color=C["red"], fontsize=9, zorder=7)
    ax.quiver(0, 0, 0, 0, 0, 1.0, color=C["red"], lw=1, arrow_length_ratio=0.12, alpha=0.4, zorder=6)
    if i == 1:
        ax.quiver(0, 0, 0, 0.9, 0, 0, color=C["purple"], lw=2.2, arrow_length_ratio=0.2, zorder=6)
        ax.text(0.8, -0.1, -0.35, "$B_1$ (정지)", color=C["purple"], fontsize=9.5, zorder=7)
    else:
        ax.text(0.12, 0, 1.15, "B₀", color=C["purple"], fontsize=10)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-0.45, 1.15)
    ax.set_box_aspect((1, 1, 0.85))
    ax.view_init(elev=22, azim=-58)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10.5, y=0.97)
fig.subplots_adjust(left=0, right=1, bottom=0, top=0.95, wspace=0)
save(fig, __file__)
