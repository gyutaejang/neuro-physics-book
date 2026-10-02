from figstyle import plt, np, save, C
from scipy.optimize import nnls

# 교차 섬유 복셀에서 텐서와 구면 디컨볼루션(섬유 방향 분포)을 비교한다.
# b = 3000 s/mm², 64방향, SNR 30. 각 다발: λ = (1.7, 0.3, 0.3) × 10⁻³ mm²/s, 같은 양으로 섞음.
rng = np.random.default_rng(3)


def fib_hemisphere(k):
    i = np.arange(k) + 0.5
    z = i / k
    phi = np.pi * (1 + 5 ** 0.5) * i
    r = np.sqrt(1 - z ** 2)
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], 1)


g = fib_hemisphere(64)
b, lpar, lper = 3.0, 1.7, 0.3
cand = fib_hemisphere(400)  # 후보 섬유 방향
A = np.exp(-b * (lper + (lpar - lper) * (g @ cand.T) ** 2))  # 응답 함수 행렬


def unit(a):
    a = np.radians(a)
    return np.array([np.cos(a), np.sin(a), 0.0])


def signal(angs, snr=30):
    S = sum(np.exp(-b * (lper + (lpar - lper) * (g @ unit(a)) ** 2)) for a in angs) / len(angs)
    s = 1 / snr
    return np.abs(S + s * rng.standard_normal(len(g)) + 1j * s * rng.standard_normal(len(g)))


def tensor(S):
    B = np.c_[np.ones(len(g)), -b * np.c_[g[:, 0] ** 2, g[:, 1] ** 2, g[:, 2] ** 2,
                                          2 * g[:, 0] * g[:, 1], 2 * g[:, 0] * g[:, 2], 2 * g[:, 1] * g[:, 2]]]
    c = np.linalg.lstsq(B, np.log(S), rcond=None)[0][1:]
    T = np.array([[c[0], c[3], c[4]], [c[3], c[1], c[5]], [c[4], c[5], c[2]]])
    w = np.linalg.eigvalsh(T)
    fa = np.sqrt(1.5 * ((w - w.mean()) ** 2).sum() / (w ** 2).sum())
    return T, fa


def deconv(S, mu=0.02):
    M = np.r_[A, np.sqrt(mu) * np.eye(len(cand))]  # 음이 아닌 최소제곱 + 약한 정칙화
    w, _ = nnls(M, np.r_[S, np.zeros(len(cand))])
    return w


phi = np.radians(np.arange(0, 360, 1.0))
E = np.stack([np.cos(phi), np.sin(phi), 0 * phi], 1)


def odf(w, k=25):
    return (np.exp(k * ((E @ cand.T) ** 2 - 1)) * w).sum(1)


def peaks(f):
    half = f[:180]
    n = len(half)
    return [i for i in range(n) if half[i] > half[i - 1] and half[i] >= half[(i + 1) % n]
            and half[i] > 0.3 * half.max()]


cases = [([0], "한 다발"), ([0, 90], "90° 교차"), ([0, 45], "45° 교차"), ([0, 30], "30° 교차")]
fig, axes = plt.subplots(2, 4, figsize=(7.3, 4.0))
for j, (angs, name) in enumerate(cases):
    S = signal(angs)
    T, fa = tensor(S)
    f = odf(deconv(S))
    pk = peaks(f)
    a1, a2 = axes[0, j], axes[1, j]
    for ax in (a1, a2):
        for a in angs:
            u = unit(a)
            ax.plot([-1.25 * u[0], 1.25 * u[0]], [-1.25 * u[1], 1.25 * u[1]], color=C["gray"], lw=0.8, ls=":")
        ax.set_aspect("equal")
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.axis("off")
    # 텐서: xy 평면 2 x 2 블록의 타원(축 길이 ∝ 고윳값)
    w2, v2 = np.linalg.eigh(T[:2, :2])
    sc = 1.0 / max(w2)
    ell = (v2 @ np.diag(w2 * sc) @ np.stack([np.cos(phi), np.sin(phi)]))
    a1.fill(ell[0], ell[1], color=C["blue"], alpha=0.25, lw=0)
    a1.plot(ell[0], ell[1], color=C["blue"], lw=1.4)
    e = v2[:, -1]
    a1.plot([-e[0], e[0]], [-e[1], e[1]], color=C["red"], lw=1.6)
    a1.set_title(name, fontsize=9.5)
    a1.text(0, -1.42, f"FA {fa:.2f}", ha="center", va="top", fontsize=8.5)
    # 섬유 방향 분포(ODF) 극좌표 곡선
    r = f / f.max()
    a2.fill(r * np.cos(phi), r * np.sin(phi), color=C["green"], alpha=0.25, lw=0)
    a2.plot(r * np.cos(phi), r * np.sin(phi), color=C["green"], lw=1.4)
    for p in pk:
        u = E[p]
        a2.plot([-u[0] * r[p], u[0] * r[p]], [-u[1] * r[p], u[1] * r[p]], color=C["red"], lw=1.4)
    a2.text(0, -1.42, f"봉우리 {len(pk)}개", ha="center", va="top", fontsize=8.5)
    print(name, "FA", round(fa, 2), "봉우리 각도", pk, "텐서 주방향",
          round(np.degrees(np.arctan2(e[1], e[0])) % 180, 1))
fig.text(0.0, 0.73, "텐서", rotation=90, va="center", fontsize=9.5, color=C["blue"])
fig.text(0.0, 0.28, "섬유 방향 분포", rotation=90, va="center", fontsize=9.5, color=C["green"])
fig.tight_layout(rect=(0.035, 0, 1, 1), h_pad=1.6)
save(fig, __file__)
