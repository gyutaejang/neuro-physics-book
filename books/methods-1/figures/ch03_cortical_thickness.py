from figstyle import plt, np, save, C

# 피질 두께: 두 표면(백질 경계, 연질막 경계) 사이의 거리. 영상 격자 방향으로 재면 기울어진 곳에서 두껍게 나온다.
L = 24.0                                    # 이랑 한 주기 (mm)
xs = np.linspace(-L, L, 4001)
pial = 6.0 - 15.0 * sum(np.exp(-((xs - c) / 3.2) ** 2) for c in (-L, 0, L))   # 넓은 이랑 마루, 좁고 깊은 고랑
dy = np.gradient(pial, xs)
nx, ny = dy / np.sqrt(1 + dy ** 2), -1 / np.sqrt(1 + dy ** 2)   # 조직 안쪽(아래) 법선
t_true = 2.0 + 1.0 * (pial - pial.min()) / (pial.max() - pial.min())   # 마루 약 3 mm, 바닥 약 2 mm
wx, wy = xs + t_true * nx, pial + t_true * ny                   # 백질 경계 = 법선 방향으로 두께만큼 안쪽


def vertical_thickness(i):
    """연질막 점에서 세로(격자) 방향으로 내려가 백질 경계를 만날 때까지의 길이."""
    x0, y0 = xs[i], pial[i]
    sgn = np.sign(wx - x0)
    k = np.where((sgn[:-1] != sgn[1:]) & (wy[:-1] < y0))[0]
    yw = [wy[j] + (wy[j + 1] - wy[j]) * (x0 - wx[j]) / (wx[j + 1] - wx[j]) for j in k]
    yw = [v for v in yw if v < y0]
    return y0 - max(yw)


if __name__ == "__main__":
    ang = np.degrees(np.arctan(np.abs(dy)))
    for a in (0, 30, 45, 60):
        print(a, "° → 1/cos = %.2f" % (1 / np.cos(np.radians(a))))
    idx = np.arange(200, 4000, 70)
    sel = list(idx)
    vt = np.array([vertical_thickness(i) for i in sel])
    rat = vt / t_true[sel]
    print("비 범위 %.2f–%.2f, 각도 최대 %.0f°" % (rat.min(), rat.max(), ang[sel].max()))

    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw=dict(width_ratios=[1.45, 1], wspace=0.3))
    ax = axs[0]
    ax.fill_between(xs, pial, 9, color="#dfe7f1", lw=0)
    poly_x = np.concatenate([xs, wx[::-1]]); poly_y = np.concatenate([pial, wy[::-1]])
    ax.fill(poly_x, poly_y, color="#f1c9b4", lw=0)
    ax.fill_between(wx, wy, -16, color="#f4f4f4", lw=0)
    ax.plot(xs, pial, color=C["red"], lw=1.3)
    ax.plot(wx, wy, color=C["blue"], lw=1.3)
    for i in (3000, 2400, 2000):
        ax.annotate("", xy=(wx[i], wy[i]), xytext=(xs[i], pial[i]),
                    arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=1.0, mutation_scale=7, shrinkA=0, shrinkB=0))
    i = 2400
    ax.plot([xs[i], xs[i]], [pial[i], pial[i] - vertical_thickness(i)], color=C["gray"], lw=1.3, ls="--")
    ax.annotate("격자 방향", xy=(xs[i], pial[i] - 5), xytext=(8.5, -6.5), fontsize=7.5, color=C["gray"],
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
    ax.text(12, 6.6, "이랑 마루", ha="center", fontsize=8)
    ax.text(0, -14.8, "고랑 바닥", ha="center", fontsize=8)
    ax.text(0, 6.8, "뇌척수액", fontsize=7.5, color=C["gray"], ha="center")
    ax.text(-12, -9, "백질", fontsize=8, color=C["gray"], ha="center")
    ax.text(-12, 6.6, "연질막 표면", fontsize=7.5, color=C["red"], ha="center")
    ax.text(-12, 0.6, "백질 표면", fontsize=7.5, color=C["blue"], ha="center", va="top")
    ax.set_xlim(-L, L); ax.set_ylim(-16, 9)
    ax.set_aspect("equal")
    ax.set_xlabel("mm"); ax.set_ylabel("mm")
    ax.set_title("(가) 두 표면 사이의 거리", fontsize=9.5)

    ax = axs[1]
    ii = np.arange(1500, 3001, 10)
    vt = np.array([vertical_thickness(i) for i in ii])
    ax.plot(xs[ii], t_true[ii], color=C["ink"], lw=1.6, label="표면 사이 거리(참)")
    ax.plot(xs[ii], vt, color=C["gray"], lw=1.4, ls="--", label="격자 방향 길이")
    ax.set_xlabel("가로 위치 (mm)")
    ax.set_ylabel("두께 (mm)")
    ax.set_xlim(-6, 12); ax.set_ylim(0, 10)
    ax.text(0, 0.6, "고랑 바닥", ha="center", fontsize=7.5, color=C["gray"])
    ax.text(12, 0.6, "마루", ha="right", fontsize=7.5, color=C["gray"])
    ax.legend(fontsize=7.5, loc="upper right")
    ax.set_title("(나) 위치에 따른 두께", fontsize=9.5)
    save(fig, __file__)
