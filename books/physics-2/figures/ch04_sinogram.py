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

hu = head_phantom()
mu = to_mu(hu)
ang = np.arange(0, 180, 1.0)
sino = project(mu, ang)
# 출혈만 따로 투영하면 그 자취가 보인다
blob = np.where(ellipse(3.0, -3.0, 1.1, 0.9, 30), 1.0, 0.0)
sb = project(blob, ang)

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[1, 1.25, 1.25]))
ax = axes[0]
ax.imshow(hu, cmap="gray", vmin=-20, vmax=100, extent=(-12, 12, -12, 12))
ax.add_patch(plt.Circle((3, -3), 1.7, fill=False, color=C["red"], lw=1.2))
ax.plot([0, 3], [0, -3], color=C["red"], lw=0.8, ls="--")
ax.text(0, -13.3, "출혈 중심 (x, y) = (3, −3) cm", color=C["red"], fontsize=8, ha="center", va="top")
ax.axis("off")
ax.set_title("(가) 단면", fontsize=10.5)

ext = (0, 180, -12, 12)
ax = axes[1]
ax.imshow(sino.T, cmap="gray", aspect="auto", origin="lower", extent=ext)
ax.set_title("(나) 사이노그램", fontsize=10.5)
ax.set_xlabel("투영 각도 θ (°)")
ax.set_ylabel("검출기 위치 s (cm)")
ax.set_xticks([0, 45, 90, 135, 180])

ax = axes[2]
ax.imshow(sb.T, cmap="gray_r", aspect="auto", origin="lower", extent=ext)
th = np.linspace(0, 180, 200)
s_pred = 3 * np.cos(np.deg2rad(th)) + (-3) * np.sin(np.deg2rad(th))
ax.plot(th, s_pred, color=C["red"], lw=1, ls="--")
ax.text(95, 6.5, "s = x cos θ + y sin θ", fontsize=8.5, color=C["red"], ha="center")
ax.set_title("(다) 출혈 한 점의 자취", fontsize=10.5)
ax.set_xlabel("투영 각도 θ (°)")
ax.set_xticks([0, 45, 90, 135, 180])
ax.set_yticks([-10, -5, 0, 5, 10])
fig.tight_layout()
save(fig, __file__)
