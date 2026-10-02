from figstyle import plt, np, save, C
from matplotlib.colors import LinearSegmentedColormap

# 구형 머리 모형(사바스 식)에서 전류 쌍극자가 만드는 바깥 자기장의 지름 성분 B_r.
# 머리 중심이 원점, 센서는 반지름 11 cm 구면 위에 있다.
mu0 = 4e-7 * np.pi
R_SENS = 0.11


def sarvas(r, r0, Q):
    """r: (...,3) 측정점, r0: (3,) 쌍극자 위치, Q: (3,) 쌍극자 모멘트(A·m)."""
    a_vec = r - r0
    a = np.linalg.norm(a_vec, axis=-1)
    rn = np.linalg.norm(r, axis=-1)
    adr = np.sum(a_vec * r, axis=-1)
    F = a * (rn * a + rn**2 - np.sum(r0 * r, axis=-1))
    gF = ((a**2 / rn + adr / a + 2 * a + 2 * rn)[..., None] * r
          - (a + 2 * rn + adr / a)[..., None] * r0)
    Qxr0 = np.cross(Q, r0)
    B = mu0 / (4 * np.pi * F[..., None] ** 2) * (F[..., None] * Qxr0 - np.sum(Qxr0 * r, axis=-1)[..., None] * gF)
    return B


# 정수리 위에서 내려다본 투영 좌표 (방위 등거리 투영)
u = np.linspace(-1, 1, 241)
U, V = np.meshgrid(u, u)
rho = np.hypot(U, V)
theta = rho * np.deg2rad(80)            # 정수리에서 80도까지
ph = np.arctan2(V, U)
pts = R_SENS * np.stack([np.sin(theta) * np.cos(ph), np.sin(theta) * np.sin(ph), np.cos(theta)], axis=-1)
rhat = pts / R_SENS

r0 = np.array([0, 0, 0.07])             # 머리 중심에서 7 cm (피질 깊이 어림)
cases = [("(가) 접선 방향 쌍극자", np.array([10e-9, 0, 0])),
         ("(나) 지름 방향 쌍극자", np.array([0, 0, 10e-9]))]

cmap = LinearSegmentedColormap.from_list("bwr_book", [C["blue"], "white", C["red"]])
lim = 200
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5))
for ax, (title, Q) in zip(axes, cases):
    B = sarvas(pts, r0, Q)
    Br = np.sum(B * rhat, axis=-1) * 1e15          # fT
    Br[rho > 1] = np.nan
    print(title, "최대 |Br| =", np.nanmax(np.abs(Br)), "fT")
    im = ax.contourf(U, V, Br, levels=np.linspace(-lim, lim, 16), cmap=cmap, extend="both")
    if np.nanmax(np.abs(Br)) > 1:
        ax.contour(U, V, Br, levels=[-150, -100, -50, 50, 100, 150],
                   colors=C["gray"], linewidths=0.5)
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=C["ink"], lw=0.8))
    ax.text(0, 1.03, "앞", ha="center", va="bottom", fontsize=8, color=C["gray"])
    # 쌍극자 화살표 (위에서 본 모습)
    if Q[0] != 0:
        ax.annotate("", xy=(0.12, 0), xytext=(-0.12, 0),
                    arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.6))
    else:
        ax.plot(0, 0, "o", ms=8, mfc="white", color=C["ink"])
        ax.plot(0, 0, ".", ms=4, color=C["ink"])
        ax.text(0, -0.35, "바깥 자기장 0", ha="center", fontsize=9)
    ax.set_title(title, fontsize=10.5, pad=12)
    ax.set_aspect("equal")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.axis("off")
axes[0].text(0.62, 0.55, "나오는\n자기장", ha="center", fontsize=8.5,
             bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
axes[0].text(0.62, -0.6, "들어가는\n자기장", ha="center", fontsize=8.5,
             bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
cb = fig.colorbar(im, ax=axes, shrink=0.75, pad=0.03)
cb.set_label("자기장 지름 성분 (fT)")
cb.set_ticks([-200, -100, 0, 100, 200])
save(fig, __file__)
