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
ang_full = np.arange(0, 180, 0.5)
sino_full = project(mu, ang_full)

fig, axes = plt.subplots(2, 4, figsize=(7.4, 4.2))
# (가) 단순 역투영: 각도를 늘려 가며
for j, n in enumerate([1, 3, 12, 360]):
    idx = (np.arange(n) * 360 // n).astype(int)
    b = backproject(sino_full[idx], ang_full[idx])
    axes[0, j].imshow(b, cmap="gray", vmin=0, vmax=b.max())
    axes[0, j].set_title(f"단순 역투영, 각도 {n}개", fontsize=9)
b180 = b
# (나) 원본, 필터 역투영(30개, 180개), 가로줄 단면
row = int(N / 2 + 3 / DX)          # y = −3 cm, 출혈을 지나는 줄
axes[1, 0].imshow(hu, cmap="gray", vmin=-20, vmax=100)
axes[1, 0].set_title("원본", fontsize=9)
for j, n in [(1, 30), (2, 360)]:
    idx = (np.arange(n) * 360 // n).astype(int)
    f = backproject(ramp_filter(sino_full[idx]), ang_full[idx])
    fhu = 1000 * (f - MU_W) / MU_W
    axes[1, j].imshow(fhu, cmap="gray", vmin=-20, vmax=100)
    axes[1, j].set_title(f"필터 역투영, 각도 {n}개", fontsize=9)
for a in axes.flat:
    a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values():
        sp.set_visible(False)
axes[1, 0].axhline(row, color=C["red"], lw=0.8, ls="--")
wm = ellipse(0, -0.3, 5.0, 6.8) & ~ellipse(-1, 0.8, 1.2, 2.9, 15) & ~ellipse(1, 0.8, 1.2, 2.9, -15) & ~ellipse(3, -3, 1.6, 1.4, 30)
print("필터 역투영 360개: 백질 평균 HU", fhu[wm].mean().round(1))

ax = axes[1, 3]
for sp in ["left", "bottom"]:
    ax.spines[sp].set_visible(True)
ax.plot(XC, hu[row], color=C["gray"], lw=3.0, alpha=0.5, label="원본")
ax.plot(XC, fhu[row], color=C["blue"], lw=1.0, label="필터")
bs = b180[row] / b180[row].max() * 100
ax.plot(XC, bs, color=C["red"], lw=1.0, label="단순")
ax.set_ylim(-30, 110); ax.set_xlim(-8, 8)
ax.set_xticks([-5, 0, 5]); ax.set_yticks([0, 50, 100])
ax.tick_params(labelsize=7.5)
ax.set_title("빨간 줄을 따라 (HU)", fontsize=9)
ax.legend(fontsize=7, loc="lower center", ncol=3, handlelength=1.0, columnspacing=0.6, borderaxespad=0.1)
axes[0, 0].set_ylabel("(가)", fontsize=10, rotation=0, labelpad=12)
axes[1, 0].set_ylabel("(나)", fontsize=10, rotation=0, labelpad=12)
fig.tight_layout(h_pad=0.8, w_pad=0.4)
save(fig, __file__)
