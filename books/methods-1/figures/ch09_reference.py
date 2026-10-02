from matplotlib.colors import LinearSegmentedColormap

from figstyle import plt, np, save, C

# 구 모양 머리(반지름 1) 속 쌍극자 두 개(좌우 후두-측두, N170 같은 반응)가 만드는 두피 전위.
# 무한 균질 매질 근사로 모양만 본다. x는 오른쪽, y는 코 쪽, z는 정수리 쪽.


def sph(th, ph):
    """th: 정수리에서 잰 극각, ph: 코에서 오른쪽으로 잰 방위각."""
    return np.stack([np.sin(th) * np.sin(ph), np.sin(th) * np.cos(ph), np.cos(th)], -1)


dips = []
for s in (1, -1):
    loc = 0.72 * sph(np.deg2rad(100), np.deg2rad(s * 125))
    mom = np.array([-s * 0.3, 0.6, 0.75])
    dips.append((loc, mom / np.linalg.norm(mom)))


def pot(r):
    out = 0
    for loc, mom in dips:
        d = r - loc
        out = out + (d @ mom) / np.linalg.norm(d, axis=-1) ** 3
    return out


# 전극 약 64개(정수리에서 112°까지 고르게), 유양돌기 두 곳, Cz
n = 94
i = np.arange(n) + 0.5
th_e = np.arccos(1 - 2 * i / n)
ph_e = np.pi * (1 + 5 ** 0.5) * i
keep = th_e <= np.deg2rad(112)
th_e, ph_e = th_e[keep], ph_e[keep]
E = sph(th_e, ph_e)
M = sph(np.deg2rad(np.array([118, 118])), np.deg2rad(np.array([-105, 105])))
Cz = sph(np.array(0.0), np.array(0.0))
P8 = sph(np.deg2rad(np.array(105.0)), np.deg2rad(np.array(118.0)))

# 눈금: 무한 기준에서 P8 근처가 −6 μV가 되도록 맞춘다.
scale = -6.0 / pot(P8)

# 그림 격자: 방위 등거리 투영. 반지름 1이 극각 90°(귀 높이)다.
gx, gy = np.meshgrid(np.linspace(-1.3, 1.3, 261), np.linspace(-1.3, 1.3, 261))
rr = np.hypot(gx, gy)
th_g = rr * np.pi / 2
ph_g = np.arctan2(gx, gy)
inside = th_g <= np.deg2rad(115)
G = sph(np.where(inside, th_g, 0.5), ph_g)
Vg = pot(G) * scale
Ve = pot(E) * scale

refs = [
    ("(가) 무한 기준 (참값)", 0.0),
    ("(나) Cz 기준", pot(Cz) * scale),
    ("(다) 연결 유양돌기 기준", pot(M).mean() * scale),
    ("(라) 평균 기준 (전극 %d개)" % len(Ve), Ve.mean()),
]

cmap = LinearSegmentedColormap.from_list("rb", [C["red"], "#ffffff", C["blue"]])
fig, axes = plt.subplots(1, 4, figsize=(7.5, 2.55))
lim = 9
for ax, (title, ref) in zip(axes, refs):
    Z = np.where(inside, Vg - ref, np.nan)
    ax.contourf(gx, gy, Z, levels=np.linspace(-lim, lim, 19), cmap=cmap, extend="both")
    ax.contour(gx, gy, Z, levels=[0], colors=[C["ink"]], linewidths=0.6)
    # 머리 윤곽, 코, 귀
    a = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(a), np.sin(a), color=C["ink"], lw=0.9)
    ax.plot([-0.12, 0, 0.12], [0.99, 1.15, 0.99], color=C["ink"], lw=0.9)
    for s in (1, -1):
        ax.plot(s * (1 + 0.06 * np.sin(np.linspace(0, np.pi, 30))), np.linspace(0.18, -0.18, 30),
                color=C["ink"], lw=0.9)
    ex = th_e / (np.pi / 2) * np.sin(ph_e)
    ey = th_e / (np.pi / 2) * np.cos(ph_e)
    ax.scatter(ex, ey, s=1.5, color=C["ink"], zorder=3)
    vp8 = pot(P8) * scale - ref
    px, py = 105 / 90 * np.sin(np.deg2rad(118)), 105 / 90 * np.cos(np.deg2rad(118))
    ax.scatter([px], [py], s=14, facecolor="none", edgecolor=C["ink"], lw=0.8, zorder=4)
    ax.text(0, -1.42, f"P8 부근: {vp8:+.1f} μV", ha="center", fontsize=7.8)
    if "Cz" in title:
        ax.scatter([0], [0], marker="x", s=18, color=C["ink"], zorder=4)
    if "유양" in title:
        for s in (1, -1):
            mx, my = 118 / 90 * np.sin(np.deg2rad(s * 105)), 118 / 90 * np.cos(np.deg2rad(s * 105))
            ax.scatter([mx], [my], marker="x", s=18, color=C["ink"], zorder=4)
    ax.set_title(title, fontsize=8.6)
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.55, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")

sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(-lim, lim))
cb = fig.colorbar(sm, ax=axes, orientation="vertical", fraction=0.018, pad=0.01)
cb.set_label("전위 (μV)", fontsize=8, labelpad=6)
cb.ax.tick_params(labelsize=7)
save(fig, __file__)
