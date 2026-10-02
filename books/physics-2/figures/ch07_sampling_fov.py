from figstyle import plt, np, save, C

# 표본화는 스펙트럼을 주기적으로 복제한다. 공간에서는 k-공간 간격 Δk = 1/FOV가 시야를 정하고,
# 시야보다 큰 물체는 반대편으로 접혀 들어온다.
fig = plt.figure(figsize=(7.4, 3.1))
gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1], wspace=0.3)
a0 = fig.add_subplot(gs[0])

# (가) 스펙트럼 복제: 신호 대역이 ±0.65 f_s로 f_s/2를 넘는다
f = np.linspace(-2.5, 2.5, 2000)
band = lambda f0, B: np.clip(1 - np.abs(f - f0) / B, 0, None)
fs, B = 1.0, 0.65
a0.axvspan(-0.5, 0.5, color=C["light"], zorder=0)
for kk in range(-2, 3):
    col = C["blue"] if kk == 0 else C["gray"]
    a0.fill_between(f, 0, band(kk * fs, B), color=col, alpha=0.6 if kk == 0 else 0.3, lw=0)
for kk in (-1, 0):
    lo, hi = kk + 0.35, kk + 0.65
    a0.fill_between(f, 0, np.minimum(band(kk, B), band(kk + 1, B)), where=(f > lo) & (f < hi),
                    color=C["red"], alpha=0.85, lw=0)
for xv in (-0.5, 0.5):
    a0.axvline(xv, color=C["red"], lw=0.8, ls="--")
a0.text(0.53, 1.33, "$f_s/2$", color=C["red"], ha="left", fontsize=8.5)
a0.text(-0.53, 1.33, "$-f_s/2$", color=C["red"], ha="right", fontsize=8.5)
a0.text(0, 1.05, "원래", ha="center", fontsize=8, color=C["blue"])
a0.text(-2, 1.05, "복제본", ha="center", fontsize=8, color=C["gray"])
a0.annotate("겹친 부분 =\n에일리어싱", xy=(0.5, 0.2), xytext=(1.3, 1.2), fontsize=8, ha="left",
            color=C["red"], arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
a0.set_xlim(-2.5, 2.5)
a0.set_ylim(0, 1.5)
a0.set_yticks([])
a0.spines["left"].set_visible(False)
a0.set_xticks([-2, -1, 0, 1, 2])
a0.set_xticklabels(["$-2f_s$", "$-f_s$", "0", "$f_s$", "$2f_s$"])
a0.set_xlabel("주파수")
a0.set_title("(가) 스펙트럼의 복제", fontsize=9.5)

# (나), (다) 시야와 접힘: 머리 모형 (위아래 190 mm)을 1 mm 격자, 320 mm 시야에서 만든다.
N = 320
y, x = np.mgrid[-160:160, -160:160] + 0.5
head = ((x / 72) ** 2 + (y / 95) ** 2 <= 1).astype(float)
brain = ((x / 64) ** 2 + ((y + 3) / 86) ** 2 <= 1)
img = 0.35 * head
img[brain] = 0.7
img[((x + 22) ** 2 + (y + 45) ** 2) <= 14 ** 2] = 1.0      # 밝은 점: 위아래를 구별하는 표지
img[((x / 10) ** 2 + ((y + 3) / 30) ** 2) <= 1] = 1.0       # 가운데 뇌실 모양
K = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(img)))
# 위아래(위상 부호화) 방향으로 k-공간 줄을 하나 건너 하나만 쓰면 Δk가 두 배 → 시야 160 mm
Ks = K[::2, :]
img2 = np.abs(np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(Ks))))

a1 = fig.add_subplot(gs[1])
a1.imshow(img, cmap="gray", extent=(-160, 160, -160, 160), vmin=0, vmax=1)
a1.set_title("(나) 시야 320 mm", fontsize=9.5)
a2 = fig.add_subplot(gs[2])
a2.imshow(img2, cmap="gray", extent=(-160, 160, -80, 80), vmin=0, vmax=1, aspect="equal")
a2.set_ylim(-160, 160)
from matplotlib.patches import Rectangle
a2.add_patch(Rectangle((-160, -80), 320, 160, fill=False, ec=C["gray"], lw=0.8))
a2.set_title("(다) 시야 160 mm", fontsize=9.5)
a1.axhline(80, color=C["red"], lw=0.8, ls="--")
a1.axhline(-80, color=C["red"], lw=0.8, ls="--")
a1.text(150, 84, "160 mm 시야", color=C["red"], fontsize=7.5, ha="right", va="bottom")
a2.annotate("아래 끝이 위로\n접혀 들어옴", xy=(0, 72), xytext=(0, 125), fontsize=7.5,
            color=C["red"], ha="center", arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
a2.annotate("위 끝이 아래로", xy=(0, -72), xytext=(0, -130), fontsize=7.5,
            color=C["red"], ha="center", arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
for a in (a1, a2):
    a.set_xticks([])
    a.set_yticks([-80, 0, 80])
    a.tick_params(labelsize=7.5)
    for s in a.spines.values():
        s.set_visible(False)
a1.set_ylabel("위상 부호화 방향 (mm)", fontsize=8)
save(fig, __file__)
