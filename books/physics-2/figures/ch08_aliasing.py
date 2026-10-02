from figstyle import plt, np, save, C
from ch08_phantom_kspace import phantom, N

# 위상 부호화 방향(세로)의 k-공간 줄을 한 줄 건너 하나씩만 얻으면 시야가 절반이 되어 영상이 접힌다.
img = phantom()
K = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(img)))
K2 = K[::2, :]                                # 줄 간격 Δk가 2배 → FOV 절반
r2 = np.abs(np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(K2)))) * 0.5   # 같은 밝기 눈금으로 맞춤
fov = 240

fig, axs = plt.subplots(1, 3, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[0.8, 1, 1], wspace=0.32))
ax = axs[0]
for i, ky in enumerate(range(-5, 6)):
    ax.plot([-6, 6], [ky, ky], color=C["blue"] if ky % 2 == 0 else C["gray"],
            lw=1.6 if ky % 2 == 0 else 0.8, ls="-" if ky % 2 == 0 else ":")
ax.set_xlim(-7, 9); ax.set_ylim(-6, 6)
ax.set_box_aspect(1)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("$k_x$ (읽기)"); ax.set_ylabel("$k_y$ (위상)")
ax.annotate("", xy=(6.6, 2), xytext=(6.6, 0), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1, mutation_scale=7, shrinkA=0, shrinkB=0))
ax.text(7.0, 1, "2Δk", color=C["red"], fontsize=8.5, va="center")
ax.set_title("(가) 한 줄 건너 얻기", fontsize=10)

axs[1].imshow(img, cmap="gray", vmin=0, vmax=1, extent=[-fov / 2, fov / 2, -fov / 2, fov / 2])
axs[1].set_title("(나) 모든 줄: FOV 240 mm", fontsize=10)
axs[2].imshow(r2, cmap="gray", vmin=0, vmax=1, extent=[-fov / 2, fov / 2, -fov / 4, fov / 4])
axs[2].set_ylim(-fov / 2, fov / 2)
axs[2].set_facecolor("white")
axs[2].set_title("(다) 절반의 줄: FOV 120 mm", fontsize=10)
for a in axs[1:]:
    a.set_xticks([-100, 0, 100]); a.set_yticks([-100, -60, 0, 60, 100])
    a.tick_params(labelsize=8)
axs[2].annotate("FOV 밖으로 나간 머리가\n반대쪽에서 겹쳐 들어온다", xy=(0, 52), xytext=(0, 82), ha="center",
                fontsize=8, color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.8))
save(fig, __file__)
