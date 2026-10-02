from figstyle import plt, np, C, save

# ---- 공통: 머리 팬텀과 평행빔 투영/역투영 (numpy + PIL만 쓴다) ----
from PIL import Image

N = 256                 # 영상 한 변의 화소 수
FOV = 24.0              # 시야 (cm)
DX = FOV / N            # 화소 크기 (cm)
MU_W = 0.19             # 약 70 keV에서 물의 선형 감쇠 계수 (1/cm)
XC = (np.arange(N) - N / 2 + 0.5) * DX
X, Y = np.meshgrid(XC, -XC)


def ellipse(x0, y0, a, b, ang=0.0, X=X, Y=Y):
    c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    xr = (X - x0) * c + (Y - y0) * s
    yr = -(X - x0) * s + (Y - y0) * c
    return (xr / a) ** 2 + (yr / b) ** 2 <= 1


PARTS = [  # (x0, y0, a, b, 각도, HU) 순서대로 덮어쓴다
    (0, 0, 7.6, 9.6, 0, 40),          # 두피
    (0, 0, 7.2, 9.2, 0, 1000),        # 머리뼈
    (0, 0, 6.6, 8.6, 0, 38),          # 회백질 (피질)
    (0, -0.3, 5.4, 7.2, 0, 25),       # 백질
    (-1.0, 0.8, 0.7, 2.4, 15, 5),     # 가쪽 뇌실 (뇌척수액)
    (1.0, 0.8, 0.7, 2.4, -15, 5),
    (3.0, -3.0, 1.1, 0.9, 30, 70),    # 급성 출혈
]


def head_phantom(parts=PARTS, ss=4):
    """HU 값으로 만든 단순한 머리 단면. 화소 안을 ss×ss로 나눠 평균한다(경계의 부분 용적)."""
    acc = np.zeros((N, N))
    for i in range(ss):
        for j in range(ss):
            Xs = X + (i + 0.5 - ss / 2) / ss * DX
            Ys = Y - (j + 0.5 - ss / 2) / ss * DX
            hu = np.full((N, N), -1000.0)
            for x0, y0, a, b, ang, v in parts:
                hu[ellipse(x0, y0, a, b, ang, Xs, Ys)] = v
            acc += hu
    return acc / ss**2


def to_mu(hu):
    return np.clip(MU_W * (1 + hu / 1000.0), 0, None)


def rot(img, deg):
    im = Image.fromarray(np.ascontiguousarray(img, dtype=np.float32), mode="F")
    return np.asarray(im.rotate(deg, resample=Image.BILINEAR), dtype=float)


def project(mu, angles):
    """사이노그램 p(θ, s). s = x cosθ + y sinθ, 단위는 선적분(무차원)."""
    return np.array([rot(mu, -a).sum(axis=0) * DX for a in angles])


def backproject(sino, angles):
    out = np.zeros((N, N))
    for p, a in zip(sino, angles):
        out += rot(np.tile(p, (N, 1)), a)
    return out * np.pi / len(angles)


def ramp_filter(sino):
    """램-락(Ram-Lak) 필터: 공간 영역 이산 커널로 만들어 DC 오차를 없앤다."""
    n = sino.shape[1]
    P = 2 * n
    k = np.arange(-n, n)
    h = np.zeros(P)
    h[k == 0] = 1 / (4 * DX * DX)
    odd = k % 2 == 1
    h[odd] = -1 / (np.pi * k[odd] * DX) ** 2
    H = np.real(np.fft.fft(np.fft.ifftshift(h))) * DX
    S = np.fft.fft(sino, P, axis=1)
    return np.real(np.fft.ifft(S * H, axis=1))[:, :n]
# ---- 공통 끝 ----

# 물과 알루미늄의 질량 감쇠 계수 (NIST XCOM 근삿값, cm²/g)
E_T = np.array([10, 15, 20, 30, 40, 50, 60, 80, 100, 150.])
WATER = np.array([5.329, 1.673, 0.8096, 0.3756, 0.2683, 0.2269, 0.2059, 0.1837, 0.1707, 0.1505])
AL = np.array([26.23, 7.955, 3.441, 1.128, 0.5685, 0.3681, 0.2778, 0.2018, 0.1704, 0.1378])


def li(E, tab):
    return np.exp(np.interp(np.log(E), np.log(E_T), np.log(tab)))


E = np.arange(12, 120, 0.5)
w = (120 - E) / E * np.exp(-li(E, AL) * 2.699 * 0.7)     # 120 kVp, 알루미늄 7 mm
w /= w.sum()
muE = li(E, WATER)                                       # 물, 1/cm


def mean_E(L):
    t = w * np.exp(-muE * L)
    return (E * t).sum() / t.sum()


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
ax = axes[0]
for L, col, ls in [(0, C["gray"], "--"), (20, C["blue"], "-")]:
    t = w * np.exp(-muE * L)
    ax.plot(E, t / t.max(), color=col, lw=1.6, ls=ls)
    m = mean_E(L)
    ax.axvline(m, color=col, lw=0.8, ls=":")
    print("물", L, "cm 뒤 평균 에너지", round(m, 1))
ax.text(12, 1.08, f"들어갈 때\n평균 {mean_E(0):.0f} keV", fontsize=8.5, color=C["gray"], ha="left")
ax.text(88, 1.03, f"물 20 cm 뒤\n평균 {mean_E(20):.0f} keV", fontsize=8.5, color=C["blue"])
ax.set_xlim(10, 125); ax.set_ylim(0, 1.3)
ax.set_yticks([0, 0.5, 1])
ax.set_xlabel("광자 에너지 (keV)")
ax.set_ylabel("광자 수 (각각 최대 = 1)")
ax.set_title("(가) 지나갈수록 빔이 단단해진다", fontsize=10.5)

# (나) 지름 20 cm 물 원기둥을 다색 빔으로 찍고 그대로 재구성
ang = np.arange(0, 180, 0.5)
disk = head_phantom(parts=[(0, 0, 10, 10, 0, 0)])           # 물 = 0 HU
L = project(np.where(disk > -1000, 1.0, 0.0) * (disk + 1000) / 1000, ang)  # 물 길이 (cm)
p_poly = -np.log((w[None, None, :] * np.exp(-muE[None, None, :] * L[..., None])).sum(axis=-1))
f = backproject(ramp_filter(p_poly), ang)
mu_mono = backproject(ramp_filter(L), ang) * f[N // 2, N // 2]   # 중심값에 맞춘 평평한 기준
ax = axes[1]
row = N // 2
ax.plot(XC, mu_mono[row], color=C["gray"], lw=1.4, ls="--", label="단색 빔이라면 (평평)")
ax.plot(XC, f[row], color=C["blue"], lw=1.6, label="다색 빔 (보정 없음)")
ax.set_xlim(-11, 11); ax.set_ylim(0.19, 0.235)
ax.set_xlabel("위치 (cm)")
ax.set_ylabel("재구성한 μ (1/cm)")
ax.set_title("(나) 물 원기둥의 컵 모양 인공물", fontsize=10.5)
ax.legend(fontsize=8, loc="upper center")
c, e = f[row, row], f[row, int(N / 2 + 9 / DX)]
print("중심 μ", c, "가장자리 근처 μ", e, "차이 HU", 1000 * (e - c) / c)
fig.tight_layout()
save(fig, __file__)
