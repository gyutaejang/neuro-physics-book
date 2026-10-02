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
ang = np.arange(0, 180, 0.5)
f = backproject(ramp_filter(project(to_mu(hu), ang)), ang)
img = 1000 * (f - MU_W) / MU_W

fig = plt.figure(figsize=(7.4, 3.5))
# (가) 전체 HU 눈금
a1 = fig.add_axes([0.05, 0.62, 0.42, 0.22])
a2 = fig.add_axes([0.05, 0.13, 0.42, 0.22])
full = [(-1000, -1000, "공기"), (-100, -50, "지방"), (0, 0, "물"), (700, 2000, "뼈")]
for i, (lo, hi, name) in enumerate(full):
    if lo == hi:
        a1.plot([lo], [0], "o", color=C["blue"], ms=5)
    else:
        a1.plot([lo, hi], [0, 0], color=C["blue"], lw=6, solid_capstyle="butt")
    a1.text((lo + hi) / 2 + (-60 if name == "지방" else 0), -0.6 if name == "지방" else 0.35, name,
            ha="center", fontsize=8.5)
a1.set_xlim(-1150, 2100); a1.set_ylim(-0.75, 0.8)
a1.set_yticks([]); a1.spines["left"].set_visible(False)
a1.set_xticks([-1000, 0, 1000, 2000])
a1.set_title("(가) HU 눈금: 전체와 확대", fontsize=10.5, loc="left")
a1.axvspan(-5, 95, color=C["red"], alpha=0.15)
brain = [(0, 15, "뇌척수액"), (20, 30, "백질"), (35, 45, "회백질"), (50, 80, "급성 출혈")]
for i, (lo, hi, name) in enumerate(brain):
    col = C["red"] if "출혈" in name else C["green"]
    a2.plot([lo, hi], [0, 0], color=col, lw=6, solid_capstyle="butt")
    a2.text((lo + hi) / 2, 0.35 if i % 2 == 0 else -0.55, name, ha="center", fontsize=8.5)
a2.set_xlim(-5, 95); a2.set_ylim(-0.75, 0.8)
a2.set_yticks([]); a2.spines["left"].set_visible(False)
a2.set_xticks([0, 20, 40, 60, 80])
a2.set_xlabel("HU")
# 확대 표시선
fig.add_artist(plt.Line2D([0.05 + 0.42 * (1145 / 3250), 0.05], [0.62, 0.35], color=C["red"], lw=0.6, alpha=0.6))
fig.add_artist(plt.Line2D([0.05 + 0.42 * (1245 / 3250), 0.47], [0.62, 0.35], color=C["red"], lw=0.6, alpha=0.6))

for k, (W, L, title) in enumerate([(80, 40, "(나) 뇌 창 W 80 / L 40"), (2000, 500, "(다) 뼈 창 W 2000 / L 500")]):
    ax = fig.add_axes([0.52 + k * 0.245, 0.1, 0.23, 0.74])
    ax.imshow(img, cmap="gray", vmin=L - W / 2, vmax=L + W / 2)
    ax.set_title(title, fontsize=9.5)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.text(N / 2, N + 14, f"{L - W // 2} ~ {L + W // 2} HU를 검정~흰색에", fontsize=8, ha="center", va="top")
    ax.set_ylim(N + 40, -2)
save(fig, __file__)
