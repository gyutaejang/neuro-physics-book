from figstyle import plt, np, save, C

# 모형 머리로 흉내 낸 세 가지 인공물. 위상 부호화는 세로(앞뒤), 읽기는 가로(좌우) 방향이다.
N = 256


def head(ny, nx, ymax, xmax=1.3):
    """머리 단위 좌표에서 y ∈ [−ymax, ymax], x ∈ [−xmax, xmax]를 담는 영상."""
    y, x = np.mgrid[ymax:-ymax:ny * 1j, -xmax:xmax:nx * 1j]
    th = np.arctan2(y, x)
    r = np.sqrt((x / 0.7) ** 2 + (y / 0.82) ** 2)
    wav = 1 + 0.025 * np.sin(14 * th)
    water = np.zeros((ny, nx))
    fat = np.zeros((ny, nx))
    fat[(r < 1.0) & (r >= 0.94)] = 1.0          # 두피 지방
    water[r < 0.88] = 0.55                        # 뇌척수액
    water[r < 0.85 * wav] = 0.75                  # 회백질
    water[r < 0.72 * wav] = 0.95                  # 백질
    for sx in (-1, 1):
        rv = np.sqrt(((x - sx * 0.11) / 0.07) ** 2 + ((y - 0.05) / 0.26) ** 2)
        water[rv < 1] = 0.3
    nose = np.sqrt((x / 0.13) ** 2 + ((y - 0.86) / 0.16) ** 2) < 1
    water[nose & (r >= 0.94)] = 0.7               # 코(앞쪽, 위)
    return water, fat


water, fat = head(N, N, 1.3)
img0 = water + fat

# (나) 주기적 움직임: 위상 부호화 줄을 하나씩 얻는 동안
#   ① 뒤쪽 정맥동(밝은 점)의 신호가 심장 박동에 맞춰 출렁이고(f·TR ≈ 0.13),
#   ② 머리 전체가 숨쉬기처럼 앞뒤로 1.5 픽셀 흔들린다(f·TR = 0.3).
yy, xx = np.mgrid[0:N, 0:N]
vessel = (((xx - 128) ** 2 + (yy - 200) ** 2) < 6 ** 2).astype(float) * 1.0
img0 = np.maximum(img0, vessel)
K = np.fft.fftshift(np.fft.fft2(water + fat))
Kv = np.fft.fftshift(np.fft.fft2(vessel))
ky = np.fft.fftshift(np.fft.fftfreq(N))           # 줄마다의 k_y (주기/픽셀)
line = np.arange(N)                               # 줄을 얻는 순서 = 시간
shift = 1.5 * np.sin(2 * np.pi * 0.3 * line)
pulse = 1 + 0.9 * np.sin(2 * np.pi * 0.13 * line)
Km = K * np.exp(-2j * np.pi * ky[:, None] * shift[:, None]) + pulse[:, None] * Kv
img_motion = np.abs(np.fft.ifft2(np.fft.ifftshift(Km)))

# (다) 접힘: 위상 방향 시야를 머리(코 포함)보다 작게, 머리 단위 1.5로 잡는다.
# 같은 픽셀 크기로 시야 세 개 높이를 계산한 뒤, 시야 밖 부분을 시야 안으로 더한다.
fovpx = int(round(N * 1.5 / 2.6))
tall_w, tall_f = head(3 * fovpx, N, 2.25)
tall = tall_w + tall_f
alias = tall[:fovpx] + tall[fovpx:2 * fovpx] + tall[2 * fovpx:]

# (라) 화학적 이동: 지방 신호가 읽기 방향으로 몇 픽셀 밀린다(낮은 대역폭을 과장).
img_cs = np.maximum(water + np.roll(fat, 8, axis=1), vessel)

panels = [(img0, "(가) 원래 영상"), (img_motion, "(나) 움직임 고스트"),
          (alias, "(다) 접힘(에일리어싱)"), (img_cs, "(라) 화학적 이동")]
fig, axs = plt.subplots(2, 2, figsize=(5.4, 5.6))
axes = axs.ravel()
for ax, (im, title) in zip(axes, panels):
    ax.imshow(im, cmap="gray", vmin=0, vmax=1.0, aspect="equal")
    ax.set_title(title, fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
axes[0].annotate("", xy=(14, 70), xytext=(14, 190), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1))
axes[0].text(22, 130, "위상", color=C["red"], fontsize=8.5, va="center")
axes[0].annotate("", xy=(190, 244), xytext=(66, 244), arrowprops=dict(arrowstyle="<->", color=C["blue"], lw=1))
axes[0].text(128, 234, "읽기", color=C["blue"], fontsize=8.5, ha="center")
axes[1].annotate("정맥동 고스트", xy=(124, 236), xytext=(40, 250), va="center", color=C["red"], fontsize=8.5,
                 ha="center", arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
axes[2].annotate("코가 뒤통수에 접힘", xy=(128, fovpx - 10), xytext=(128, fovpx + 38), annotation_clip=False, va="center", color=C["red"],
                 fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
axes[3].annotate("겹쳐 밝음", xy=(214, 128), xytext=(170, 20), color=C["red"], fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
axes[3].annotate("빈틈", xy=(42, 150), xytext=(14, 235), color=C["red"], fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
fig.tight_layout(w_pad=0.6, h_pad=0.8)
save(fig, __file__)
