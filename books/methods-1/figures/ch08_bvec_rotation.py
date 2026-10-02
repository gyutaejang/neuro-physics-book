from figstyle import plt, np, save, C

# b-벡터를 돌리지 않았을 때 생기는 방향 오차.
# (가) 머리가 돌아간 만큼 영상은 되돌렸지만 b-벡터는 그대로 둔 경우의 주 고유벡터 오차.
# (나) b-벡터의 x 부호가 뒤집힌 경우: 활 모양 다발의 방향이 거울상이 된다.


def fib_hemisphere(k):
    i = np.arange(k) + 0.5
    z = i / k
    phi = np.pi * (1 + 5 ** 0.5) * i
    r = np.sqrt(1 - z ** 2)
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], 1)


g = fib_hemisphere(60)
N = len(g)
u = np.array([0, 1.0, 0])  # 앞뒤 방향 섬유
D = 0.3 * np.eye(3) + 1.4 * np.outer(u, u)  # λ = (1.7, 0.3, 0.3) × 10⁻³ mm²/s, b = 1000


def Rz(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def fit(gs, S):
    B = -np.c_[gs[:, 0] ** 2, gs[:, 1] ** 2, gs[:, 2] ** 2,
               2 * gs[:, 0] * gs[:, 1], 2 * gs[:, 0] * gs[:, 2], 2 * gs[:, 1] * gs[:, 2]]
    c = np.linalg.lstsq(B, np.log(S), rcond=None)[0]
    T = np.array([[c[0], c[3], c[4]], [c[3], c[1], c[5]], [c[4], c[5], c[2]]])
    w, v = np.linalg.eigh(T)
    md = w.mean()
    fa = np.sqrt(1.5 * ((w - md) ** 2).sum() / (w ** 2).sum())
    return fa, np.degrees(np.arccos(min(1.0, abs(v[:, -1] @ u))))


th = np.linspace(0, 15, 31)
err_const, err_drift, err_rot, fa_const = [], [], [], []
for t in th:
    for mode in ("const", "drift"):
        Rs = [Rz(np.radians(t if mode == "const" else t * k / (N - 1))) for k in range(N)]
        gh = np.array([R.T @ gg for R, gg in zip(Rs, g)])  # 머리 좌표에서 본 실제 경사 방향
        S = np.exp(-np.einsum("ki,ij,kj->k", gh, D, gh))
        fa, e = fit(g, S)  # 돌리지 않은 b-벡터로 맞춤
        (err_const if mode == "const" else err_drift).append(e)
        if mode == "const":
            fa_const.append(fa)
        else:
            err_rot.append(fit(gh, S)[1])  # 돌린 b-벡터로 맞춤
print("10도: 일정", np.interp(10, th, err_const), "표류", np.interp(10, th, err_drift),
      "FA", fa_const[0], fa_const[20])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw=dict(width_ratios=[1.15, 1]))
a1.plot(th, err_const, color=C["red"], lw=1.8, label="모든 볼륨이 θ만큼 돌아감")
a1.plot(th, err_drift, color=C["red"], lw=1.6, ls="--", label="0에서 θ까지 서서히 표류")
a1.plot(th, err_rot, color=C["blue"], lw=1.8, label="b-벡터도 함께 돌림")
a1.set_xlabel("머리 회전 θ (°)")
a1.set_ylabel("주 고유벡터 오차 (°)")
a1.set_title("(가) b-벡터를 돌리지 않으면", fontsize=9.5)
a1.legend(fontsize=7.8, loc="upper left")
a1.set_xlim(0, 15)
a1.set_ylim(-0.5, 16)
a1.text(14.6, 1.2, f"FA는 {fa_const[0]:.2f} 그대로", ha="right", fontsize=8, color=C["gray"])

# (나) 활 모양 다발: 올바른 방향(파랑, 왼쪽)과 x 부호가 뒤집힌 방향(빨강, 오른쪽)
R0 = 5.0
ang = np.radians(np.linspace(10, 170, 9))
arc = np.radians(np.linspace(5, 175, 100))
for x0, flip, col in ((-6.0, False, C["blue"]), (6.0, True, C["red"])):
    for a in ang:
        cx, cy = x0 + R0 * np.cos(a), R0 * np.sin(a)
        t = np.array([-np.sin(a), np.cos(a)])  # 접선
        if flip:
            t = np.array([-t[0], t[1]])  # x 성분 부호 반전
        L = 0.75
        a2.plot([cx - L * t[0], cx + L * t[0]], [cy - L * t[1], cy + L * t[1]], color=col, lw=2.4,
                solid_capstyle="round")
    a2.plot(x0 + R0 * np.cos(arc), R0 * np.sin(arc), color=C["gray"], lw=0.6, ls=":")
a2.text(-6, -1.6, "올바른 b-벡터\n방향이 다발을 따라 이어진다", ha="center", va="top", fontsize=8,
        color=C["blue"])
a2.text(6, -1.6, "x 부호가 뒤집힌 b-벡터\n방향이 다발을 가로지른다", ha="center", va="top", fontsize=8,
        color=C["red"])
a2.set_aspect("equal")
a2.set_xlim(-12, 12)
a2.set_ylim(-4.6, 6.6)
a2.axis("off")
a2.set_title("(나) 축 부호 오류: FA는 같고 방향만 틀린다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
