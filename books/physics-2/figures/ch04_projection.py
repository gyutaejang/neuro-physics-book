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
p0, p90 = project(mu, [0.0, 90.0])
# 출혈이 없을 때와의 차이
q0 = project(to_mu(head_phantom(PARTS[:-1])), [0.0])[0]
print("투영 최대", p0.max(), p90.max(), "출혈에 의한 최대 차이", (p0 - q0).max())

fig = plt.figure(figsize=(7.2, 3.6))
ax = fig.add_axes([0.0, 0.0, 0.52, 1.0])
ax.imshow(hu, cmap="gray", vmin=-20, vmax=100, extent=(-12, 12, -12, 12))
sc = 1.1   # 투영값 1당 그림 위 길이 (cm)
# θ = 0°: 위에서 아래로 가는 빛줄기, 아래에 검출기
for xs in np.linspace(-9, 9, 7):
    ax.annotate("", xy=(xs, -11.6), xytext=(xs, 11.6),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=0.6, alpha=0.7))
ax.plot([-12, 12], [-12.4, -12.4], color=C["ink"], lw=2)
ax.plot(XC, -12.6 - p0 * sc, color=C["blue"], lw=1.5)
ax.text(-12, -18.8, "θ = 0°의 투영", fontsize=9, color=C["blue"])
# θ = 90°: 왼쪽에서 오른쪽으로 가는 빛줄기, 오른쪽에 검출기
ax.plot([12.4, 12.4], [-12, 12], color=C["ink"], lw=2)
ax.plot(12.6 + p90 * sc, XC, color=C["blue"], lw=1.5)
ax.text(13.0, 13.0, "θ = 90°의 투영", fontsize=9, color=C["blue"])
ax.text(0, 12.8, "X선관 쪽", fontsize=8.5, ha="center", color=C["red"])
ax.text(3.0, -5.2, "출혈", fontsize=8, color="white", ha="center")
ax.set_xlim(-13, 19.5); ax.set_ylim(-19.5, 14.5)
ax.set_aspect("equal"); ax.axis("off")
ax.text(-13, 14.0, "(가) 두 방향의 그림자", fontsize=10.5)

a1 = fig.add_axes([0.62, 0.58, 0.36, 0.33])
a2 = fig.add_axes([0.62, 0.14, 0.36, 0.33])
a1.plot(XC, np.exp(-p0), color=C["gray"], lw=1.5)
a1.set_ylabel("I / I₀")
a1.set_xticklabels([])
a1.set_ylim(0, 1.05); a1.set_xlim(-12, 12)
a1.set_title("(나) 검출기 신호와 투영값 (θ = 0°)", fontsize=10.5, loc="left", x=-0.25)
a2.plot(XC, p0, color=C["blue"], lw=1.5)
a2.set_ylabel("p = ln(I₀/I)")
a2.set_xlabel("검출기 위치 s (cm)")
a2.set_xlim(-12, 12); a2.set_ylim(0, 4.6)
a2.annotate("머리뼈를 길게\n스치는 줄", xy=(-6.9, p0[np.argmin(abs(XC + 6.9))]), xytext=(-11.5, 4.0),
            fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.6))
a1.text(0, 0.45, "가운데에서는 약 2%만 남는다", fontsize=8, ha="center", color=C["gray"])
save(fig, __file__)
