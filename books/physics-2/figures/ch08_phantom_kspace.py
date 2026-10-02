from figstyle import plt, np, save, C

# 뇌를 닮은 단순한 2차원 팬텀(256 × 256, 시야 240 mm)과 그 k-공간.
N = 256


def phantom(n=N):
    y, x = np.mgrid[-1:1:1j * n, -1:1:1j * n]
    th = np.arctan2(y, x)
    img = np.zeros((n, n))

    def ell(a, b, x0=0, y0=0, ang=0, wav=0.0, m=0):
        c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
        xr, yr = (x - x0) * c + (y - y0) * s, -(x - x0) * s + (y - y0) * c
        r = np.sqrt((xr / a) ** 2 + (yr / b) ** 2)
        return r <= 1 + wav * np.cos(m * th)

    img[ell(0.74, 0.90)] = 0.80                    # 두피(지방, T1에서 밝다)
    img[ell(0.69, 0.85)] = 0.08                    # 두개골
    img[ell(0.66, 0.82)] = 0.15                    # 뇌척수액
    img[ell(0.63, 0.79, wav=0.025, m=18)] = 0.50   # 회백질(겉이 주름진다)
    img[ell(0.50, 0.65, wav=0.06, m=11)] = 0.78    # 백질
    img[ell(0.07, 0.22, x0=-0.11, y0=0.05, ang=-15)] = 0.15   # 뇌실
    img[ell(0.07, 0.22, x0=0.11, y0=0.05, ang=15)] = 0.15
    for (x0, y0) in [(-0.35, -0.35), (0.38, 0.30), (0.25, -0.45)]:
        img[ell(0.025, 0.025, x0=x0, y0=y0)] = 1.0           # 작은 병변
    return img


if __name__ == "__main__":
    img = phantom()
    K = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(img)))
    fov = 240.0  # mm
    dk = 1 / fov  # 1/mm
    kmax = N / 2 * dk

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    a1.imshow(img, cmap="gray", extent=[-fov / 2, fov / 2, -fov / 2, fov / 2], vmin=0, vmax=1)
    a1.set_xlabel("x (mm)")
    a1.set_ylabel("y (mm)")
    a1.set_title("(가) 영상: 양성자 밀도 지도", fontsize=10.5)
    a1.set_xticks([-100, 0, 100])
    a1.set_yticks([-100, 0, 100])

    mag = np.log10(np.abs(K) + 1e-3)
    im = a2.imshow(mag, cmap="magma", extent=[-kmax, kmax, -kmax, kmax], vmin=mag.max() - 5, vmax=mag.max())
    a2.set_xlabel("$k_x$ (1/mm)")
    a2.set_ylabel("$k_y$ (1/mm)")
    a2.set_title("(나) k-공간 크기 (로그 눈금)", fontsize=10.5)
    a2.set_xticks([-0.5, 0, 0.5])
    a2.set_yticks([-0.5, 0, 0.5])
    cb = fig.colorbar(im, ax=a2, fraction=0.046, pad=0.04)
    cb.set_label(r"$\log_{10}|S|$", fontsize=9)
    cb.ax.tick_params(labelsize=8)
    a2.annotate("중심: 큰 값\n(밝기와 대비)", xy=(0.0, 0.0), xytext=(0.06, 0.36), fontsize=8, color="white",
                arrowprops=dict(arrowstyle="->", color="white", lw=0.8))
    a2.text(-0.5, -0.47, "가장자리: 작은 값\n(경계와 세부)", fontsize=8, color="white")
    fig.tight_layout()
    save(fig, __file__)
