from figstyle import plt, np, save, C
from matplotlib.colors import LinearSegmentedColormap

# 같은 접선 방향 쌍극자(10 nA·m, 중심에서 7.5 cm, +x 방향)를 EEG와 MEG로 본 지도.
# EEG: 동심 구 3겹(뇌 0.33, 두개골 0.01, 두피 0.43 S/m)의 두피 전위.
# MEG: 사바스 식으로 계산한 반지름 11 cm 센서 구면의 자기장 지름 성분. 전도율과 무관하다.
R = 0.092
b = np.array([0.080, 0.086, 0.092]) / R
sig = np.array([0.33, 0.01, 0.43])
r0n = 0.075 / R
p = 10e-9
NMAX = 200
mu0 = 4e-7 * np.pi


def gains(sig):
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


def eeg_tangential(theta, phi):
    """+x 방향 쌍극자: 각 성분은 sinθ·P_n'(cosθ)·cosφ."""
    g = gains(sig)
    x = np.cos(theta)
    s = np.sin(theta)
    Pm, P = np.ones_like(x), x
    V = np.zeros_like(x)
    for n in range(1, NMAX + 1):
        dP = n * (Pm - x * P) / s                 # sinθ·P_n'(cosθ)
        V += g[n] * r0n ** (n - 1) * dP
        Pm, P = P, ((2 * n + 1) * x * P - n * Pm) / (n + 1)
    return V * np.cos(phi) * p / (4 * np.pi * sig[0]) / R**2 * 1e6   # μV


def sarvas(r, r0, Q):
    a_vec = r - r0
    a = np.linalg.norm(a_vec, axis=-1)
    rn = np.linalg.norm(r, axis=-1)
    adr = np.sum(a_vec * r, axis=-1)
    F = a * (rn * a + rn**2 - np.sum(r0 * r, axis=-1))
    gF = ((a**2 / rn + adr / a + 2 * a + 2 * rn)[..., None] * r
          - (a + 2 * rn + adr / a)[..., None] * r0)
    Qxr0 = np.cross(Q, r0)
    return mu0 / (4 * np.pi * F[..., None] ** 2) * (F[..., None] * Qxr0 - np.sum(Qxr0 * r, axis=-1)[..., None] * gF)


u = np.linspace(-1, 1, 201)
U, Vv = np.meshgrid(u, u)
rho = np.hypot(U, Vv)
TMAX = np.deg2rad(45)
TH = np.clip(rho, 0, 1) * TMAX + 1e-6
PH = np.arctan2(Vv, U)

eeg = eeg_tangential(TH, PH)
R_S = 0.11
pts = R_S * np.stack([np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)], axis=-1)
B = sarvas(pts, np.array([0, 0, 0.075]), np.array([p, 0, 0]))
meg = np.sum(B * pts / R_S, axis=-1) * 1e15
eeg[rho > 1] = np.nan
meg[rho > 1] = np.nan
print("EEG 최대", np.nanmax(eeg), "μV; MEG 최대", np.nanmax(meg), "fT")

cmap = LinearSegmentedColormap.from_list("bwr_book", [C["blue"], "white", C["red"]])
fig = plt.figure(figsize=(7.0, 3.1))
gs = fig.add_gridspec(1, 5, width_ratios=[1, 0.05, 0.28, 1, 0.05], wspace=0.08)
panels = [(0, eeg, 2.0, "μV", "(가) EEG: 두피 전위", [-2, -1, 0, 1, 2]),
          (3, meg, 280, "fT", "(나) MEG: 자기장 지름 성분", [-250, 0, 250])]
for col, Z, lim, unit, title, ticks in panels:
    ax = fig.add_subplot(gs[0, col])
    im = ax.contourf(U, Vv, Z, levels=np.linspace(-lim, lim, 17), cmap=cmap, extend="both")
    ax.contour(U, Vv, Z, levels=[-0.5 * np.nanmax(Z), 0.5 * np.nanmax(Z)], colors=C["ink"],
               linewidths=0.7, linestyles="--")
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=C["ink"], lw=0.8))
    ax.annotate("", xy=(0.16, 0), xytext=(-0.16, 0),
                arrowprops=dict(arrowstyle="-|>", color=C["ink"], lw=1.6))
    ax.set_title(title, fontsize=9.5)
    ax.set_aspect("equal")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.axis("off")
    cax = fig.add_subplot(gs[0, col + 1])
    cb = fig.colorbar(im, cax=cax)
    cb.set_ticks(ticks)
    cb.ax.tick_params(labelsize=7.5)
    cb.ax.set_title(unit, fontsize=8)
save(fig, __file__)
