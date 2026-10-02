from figstyle import plt, np, save, C

# 2차원 합성 섬유 장: 활 모양 다발 A(뇌량처럼 휘는 다발)와 세로 다발 B가 꼭대기에서 직각으로 교차한다.
# 복셀 2 mm, 시야 60 x 50 mm. 교차 복셀에서 B의 몫이 조금 더 크다(0.55 : 0.45).
VOX = 2.0
NX, NY = 30, 25
CEN, RAD, HW = np.array([30.0, 5.0]), 30.0, 3.0  # 활의 중심, 반지름, 반폭(mm)
BX0, BX1, BY0 = 27.0, 33.0, 10.0  # 세로 다발 범위
LPAR, LPER = 1.7, 0.3


def memberships(x, y):
    """점 (x, y) mm가 다발 A, B에 속하는지와 그 자리의 섬유 방향."""
    d = np.hypot(x - CEN[0], y - CEN[1])
    ang = np.arctan2(y - CEN[1], x - CEN[0])
    inA = (np.abs(d - RAD) < HW) & (ang > np.radians(10)) & (ang < np.radians(170))
    inB = (x > BX0) & (x < BX1) & (y > BY0)
    tA = np.stack([-np.sin(ang), np.cos(ang)], -1)  # 활의 접선
    return inA, inB, tA


def build_field():
    """복셀마다 (A 비율, B 비율, A 방향)과 2 x 2 확산 텐서."""
    sub = (np.arange(4) + 0.5) / 4 * VOX
    fA = np.zeros((NX, NY))
    fB = np.zeros((NX, NY))
    tA = np.zeros((NX, NY, 2))
    for i in range(NX):
        for j in range(NY):
            xs, ys = np.meshgrid(i * VOX + sub, j * VOX + sub)
            a, bb, t = memberships(xs, ys)
            fA[i, j], fB[i, j] = a.mean(), bb.mean()
            both = a & bb
            fA[i, j] = np.where(both, 0.45, a).mean()
            fB[i, j] = np.where(both, 0.55, bb).mean()
            xc, yc = (i + 0.5) * VOX, (j + 0.5) * VOX
            tA[i, j] = memberships(np.array(xc), np.array(yc))[2]
    tot = fA + fB
    T = np.zeros((NX, NY, 2, 2))
    uB = np.array([0.0, 1.0])
    for i in range(NX):
        for j in range(NY):
            if tot[i, j] == 0:
                T[i, j] = 3.0 * np.eye(2) * 0 + 0.8 * np.eye(2)
                continue
            u = tA[i, j]
            Ti = fA[i, j] * (LPER * np.eye(2) + (LPAR - LPER) * np.outer(u, u))
            Ti += fB[i, j] * (LPER * np.eye(2) + (LPAR - LPER) * np.outer(uB, uB))
            T[i, j] = Ti / tot[i, j]
    return fA, fB, tA, T


def fa2(T):
    """평면 두 고윳값과 지름 방향 고윳값 LPER로 계산한 FA."""
    w = np.r_[np.linalg.eigvalsh(T), LPER]
    return np.sqrt(1.5 * ((w - w.mean()) ** 2).sum() / (w ** 2).sum())


def voxel(p):
    i, j = int(p[0] // VOX), int(p[1] // VOX)
    if 0 <= i < NX and 0 <= j < NY:
        return i, j
    return None


def interp_tensor(T, p):
    """텐서를 이웃 네 복셀에서 쌍선형 보간한다."""
    x, y = p[0] / VOX - 0.5, p[1] / VOX - 0.5
    i0, j0 = int(np.floor(x)), int(np.floor(y))
    out = np.zeros((2, 2))
    for di in (0, 1):
        for dj in (0, 1):
            i, j = min(max(i0 + di, 0), NX - 1), min(max(j0 + dj, 0), NY - 1)
            w = (1 - abs(x - (i0 + di))) * (1 - abs(y - (j0 + dj)))
            out += w * T[i, j]
    return out


def track(p0, d0, field, mode, step=0.5, max_angle=45.0, rng=None, disp=0.0, max_len=150.0):
    """mode: 'tensor'은 주 고유벡터, 'peak'은 이전 방향에 가장 가까운 섬유 봉우리를 따른다.
    disp > 0이면 매 걸음 방향을 그 표준편차(°)로 흔든다(확률적 추적)."""
    fA, fB, tA, T = field
    p, d = np.array(p0, float), np.array(d0, float) / np.linalg.norm(d0)
    pts = [p.copy()]
    cosmax = np.cos(np.radians(max_angle))
    for _ in range(int(max_len / step)):
        v = voxel(p)
        if v is None or fA[v] + fB[v] < 0.3:
            break  # 백질 마스크 밖
        if mode == "tensor":
            Tp = interp_tensor(T, p)
            if fa2(Tp) < 0.2:
                break
            w, vec = np.linalg.eigh(Tp)
            nd = vec[:, -1]
        else:
            cands = []
            if fA[v] > 0.1:
                cands.append(tA[v])
            if fB[v] > 0.1:
                cands.append(np.array([0.0, 1.0]))
            nd = max(cands, key=lambda c: abs(c @ d))
        if nd @ d < 0:
            nd = -nd
        if disp > 0:
            a = np.radians(disp) * rng.standard_normal()
            c, s = np.cos(a), np.sin(a)
            nd = np.array([c * nd[0] - s * nd[1], s * nd[0] + c * nd[1]])
        if nd @ d < cosmax:
            break  # 너무 급히 꺾임
        d = nd
        p = p + step * d
        pts.append(p.copy())
    return np.array(pts)


def seeds_A(n=5):
    a = np.radians(158)
    out = []
    for r in np.linspace(RAD - 1.6, RAD + 1.6, n):
        p = CEN + r * np.array([np.cos(a), np.sin(a)])
        out.append((p, np.array([np.sin(a), -np.cos(a)])))  # 시계 방향(꼭대기 쪽)
    return out


def seeds_B(n=5):
    return [(np.array([x, 12.0]), np.array([0.0, 1.0])) for x in np.linspace(28.0, 32.0, n)]


def draw_field(ax, field):
    fA, fB, tA, T = field
    for i in range(NX):
        for j in range(NY):
            xc, yc = (i + 0.5) * VOX, (j + 0.5) * VOX
            for f, u in ((fA[i, j], tA[i, j]), (fB[i, j], np.array([0.0, 1.0]))):
                if f > 0.1:
                    L = 0.85 * f / max(fA[i, j] + fB[i, j], 1e-9) + 0.25
                    ax.plot([xc - L * u[0], xc + L * u[0]], [yc - L * u[1], yc + L * u[1]],
                            color="#b9b9b9", lw=1.0)
    ax.set_xlim(0, NX * VOX)
    ax.set_ylim(0, NY * VOX)
    ax.set_aspect("equal")
    ax.set_xticks([0, 20, 40, 60])
    ax.set_yticks([0, 20, 40])


if __name__ == "__main__":
    field = build_field()
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for ax, mode, title in ((axes[0], "tensor", "(가) 텐서 주방향을 따라감"),
                            (axes[1], "peak", "(나) 섬유 봉우리를 골라 따라감")):
        draw_field(ax, field)
        ends = []
        for p0, d0 in seeds_A():
            s = track(p0, d0, field, mode)
            ax.plot(s[:, 0], s[:, 1], color=C["blue"], lw=1.3)
            ends.append(s[-1])
        for p0, d0 in seeds_B():
            s = track(p0, d0, field, mode)
            ax.plot(s[:, 0], s[:, 1], color=C["red"], lw=1.1, alpha=0.9)
        for p0, _ in seeds_A() + seeds_B():
            ax.plot(*p0, "o", ms=2.6, color=C["ink"])
        ends = np.array(ends)
        print(mode, "A 끝점", np.round(ends, 1).tolist())
        ax.set_title(title, fontsize=9.5)
        ax.set_xlabel("x (mm)")
    axes[0].set_ylabel("y (mm)")
    axes[0].annotate("활 다발이 세로 다발로\n갈아탄다", xy=(31, 47), xytext=(37, 44), fontsize=8,
                     color=C["blue"], arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7))
    axes[1].annotate("교차를 지나\n활을 끝까지 따른다", xy=(52, 24), xytext=(38, 6), fontsize=8,
                     color=C["blue"], arrowprops=dict(arrowstyle="->", color=C["gray"], lw=0.7))
    fig.tight_layout()
    save(fig, __file__)
