from figstyle import plt, np, save, C
from matplotlib.colors import LinearSegmentedColormap

# 동심 구 3겹 머리 모형에서 지름 방향 전류 쌍극자(10 nA·m, 중심에서 7.5 cm)가 만드는 두피 전위.
# 각 층에서 전위를 르장드르 급수로 풀고, 층 경계에서 전위와 수직 전류가 이어지게 한다.
R = 0.092                                   # 두피 바깥 반지름 (m)
b = np.array([0.080, 0.086, 0.092]) / R     # 뇌, 두개골, 두피의 바깥 반지름 (R 단위)
r0 = 0.075 / R
p = 10e-9
NMAX = 200


def gains(sig):
    """n차 성분마다 '두피 전위 계수 / 무한 매질 계수'를 구한다."""
    N = len(b)
    g = np.zeros(NMAX + 1)
    for n in range(1, NMAX + 1):
        M = np.zeros((2 * N - 1, 2 * N - 1))
        rhs = np.zeros(2 * N - 1)
        iA = lambda k: 0 if k == 0 else 2 * k - 1
        iB = lambda k: 2 * k
        row = 0
        for k in range(N - 1):
            r = b[k]
            for der, s1, s2 in ((0, 1.0, 1.0), (1, sig[k], sig[k + 1])):
                fa = n * r ** (n - 1) if der else r ** n
                fb = -(n + 1) * r ** (-(n + 2)) if der else r ** (-(n + 1))
                M[row, iA(k)] += s1 * fa
                if k > 0:
                    M[row, iB(k)] += s1 * fb
                else:
                    rhs[row] -= s1 * fb
                M[row, iA(k + 1)] -= s2 * fa
                M[row, iB(k + 1)] -= s2 * fb
                row += 1
        M[row, iA(N - 1)] = n
        M[row, iB(N - 1)] = -(n + 1)
        x = np.linalg.solve(M, rhs)
        g[n] = x[iA(N - 1)] + x[iB(N - 1)]
    return g


def scalp_radial(theta, sig):
    g = gains(sig)
    x = np.cos(theta)
    P0, P1 = np.ones_like(x), x
    V = g[1] * 1 * P1
    for n in range(1, NMAX):
        P0, P1 = P1, ((2 * n + 1) * x * P1 - n * P0) / (n + 1)
        V = V + g[n + 1] * (n + 1) * r0 ** n * P1
    return V * p / (4 * np.pi * sig[0]) / R**2 * 1e6      # μV


cases = [("(가) 두개골이 없다면", np.array([0.33, 0.33, 0.43]), C["gray"]),
         ("(나) 두개골 0.01 S/m", np.array([0.33, 0.01, 0.43]), C["blue"])]

u = np.linspace(-1, 1, 201)
U, Vv = np.meshgrid(u, u)
rho = np.hypot(U, Vv)
TMAX = 0.07 / R                                  # 정점에서 두피를 따라 7 cm까지만 그린다
TH = np.clip(rho, 0, 1) * TMAX + 1e-6
cmap = LinearSegmentedColormap.from_list("bwr_book", [C["blue"], "white", C["red"]])

fig = plt.figure(figsize=(7.3, 2.9))
gs = fig.add_gridspec(1, 5, width_ratios=[1, 1, 0.06, 0.42, 1.35], wspace=0.12)
lim = 16
for i, (title, sig, col) in enumerate(cases):
    ax = fig.add_subplot(gs[0, i])
    V = scalp_radial(TH, sig)
    V[rho > 1] = np.nan
    print(title, "최대", np.nanmax(V), "μV")
    im = ax.contourf(U, Vv, V, levels=np.linspace(-lim, lim, 17), cmap=cmap, extend="both")
    ax.contour(U, Vv, V, levels=[np.nanmax(V) / 2], colors=C["ink"], linewidths=0.8, linestyles="--")
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=C["ink"], lw=0.8))
    ax.plot(0, 0, "o", ms=6, mfc="white", color=C["ink"])
    ax.plot(0, 0, ".", ms=3, color=C["ink"])
    ax.set_title(title, fontsize=9.5, pad=14)
    ax.text(0, -1.22, f"최대 {np.nanmax(V):.1f} μV", ha="center", fontsize=8.5)
    if i == 0:
        ax.annotate("", xy=(-1, 1.02), xytext=(0, 1.02),
                    arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.7))
        ax.text(-0.5, 1.06, "7 cm", ha="center", va="bottom", fontsize=7.5, color=C["gray"])
    ax.set_aspect("equal")
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-1.35, 1.2)
    ax.axis("off")
cax = fig.add_subplot(gs[0, 2])
cb = fig.colorbar(im, cax=cax)
cb.set_ticks([-16, -8, 0, 8, 16])
cb.ax.tick_params(labelsize=7.5)
cb.ax.set_title("μV", fontsize=8)

ax = fig.add_subplot(gs[0, 4])
th = np.linspace(1e-5, np.pi / 2, 1500)
s_cm = th * R * 100                                   # 정수리에서 두피를 따라 잰 거리
for title, sig, col in cases:
    V = scalp_radial(th, sig)
    Vn = V / V[0]
    half = s_cm[np.argmax(Vn < 0.5)]
    print(title, "반값 반지름", half, "cm")
    lab = "두개골 없음" if col == C["gray"] else "두개골 있음"
    ax.plot(s_cm, Vn, color=col, lw=1.8, label=f"{lab} (반값 {half:.1f} cm)")
    ax.plot([half, half], [0, 0.5], color=col, lw=0.8, ls=":")
ax.axhline(0.5, color=C["gray"], lw=0.6, ls="--")
ax.axhline(0, color=C["gray"], lw=0.6)
ax.set_xlim(0, 8)
ax.set_ylim(-0.1, 1.05)
ax.set_xlabel("정점에서 두피를 따라 잰 거리 (cm)")
ax.set_ylabel("최댓값으로 나눈 전위")
ax.set_title("(다) 모양만 비교", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper right")
save(fig, __file__)
