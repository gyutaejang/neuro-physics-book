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

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.8))
# (가) 주파수 영역: 단순 역투영의 흐림 1/|k|, 램프 |k|, 그 곱
ax = axes[0]
k = np.linspace(0.02, 1, 300)
ax.plot(k, 0.1 / k, color=C["red"], lw=1.6)
ax.plot(k, k, color=C["blue"], lw=1.6)
ax.plot(k, np.ones_like(k) * 0.1 / 1 * 1, color=C["gray"], lw=1.2, ls="--")
ax.text(0.2, 0.88, "단순 역투영의\n흐림 ∝ 1/|k|", color=C["red"], fontsize=8.5)
ax.text(0.74, 0.42, "램프 필터\n∝ |k|", color=C["blue"], fontsize=8.5)
ax.text(0.32, -0.045, "두 곡선의 곱 = 평평", color=C["gray"], fontsize=8.5)
ax.set_xlim(0, 1); ax.set_ylim(-0.06, 1.05)
ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(["0", "", "최대"])
ax.set_yticks([])
ax.set_xlabel("공간 주파수 |k|")
ax.set_title("(가) 주파수로 본 필터", fontsize=10.5)

# (나) 공간 영역의 램-락 커널
ax = axes[1]
n = np.arange(-8, 9)
h = np.zeros(n.size, dtype=float)
h[n == 0] = 0.25
odd = n % 2 != 0
h[odd] = -1 / (np.pi * n[odd]) ** 2
ml, sl, bl = ax.stem(n, h, basefmt=" ")
plt.setp(sl, color=C["blue"], lw=1.2); plt.setp(ml, color=C["blue"], ms=4)
ax.axhline(0, color=C["gray"], lw=0.6)
ax.set_xlabel("떨어진 검출기 칸 수")
ax.set_title("(나) 같은 필터의 커널", fontsize=10.5)
ax.text(1.0, 0.2, "자기 칸: +", fontsize=8.5, color=C["blue"])
ax.text(-8, -0.075, "이웃 칸: −", fontsize=8.5, color=C["red"])
ax.set_ylim(-0.13, 0.28); ax.set_yticks([0])

# (다) 투영 하나를 필터하면
ax = axes[2]
hu = head_phantom()
p = project(to_mu(hu), [0.0])
q = ramp_filter(p)[0]
ax.plot(XC, p[0] / p[0].max(), color=C["gray"], lw=1.3, label="투영 p(s)")
ax.plot(XC, q / np.abs(q).max(), color=C["blue"], lw=1.1, label="필터한 투영")
ax.axhline(0, color=C["gray"], lw=0.5)
ax.set_xlim(-10, 10); ax.set_ylim(-1.1, 1.5)
ax.set_xlabel("검출기 위치 s (cm)")
ax.set_yticks([0])
ax.legend(fontsize=7.5, loc="upper center", ncol=2, handlelength=1.2, columnspacing=0.8)
ax.set_title("(다) 투영 하나에 적용", fontsize=10.5)
fig.tight_layout(w_pad=1.0)
save(fig, __file__)
