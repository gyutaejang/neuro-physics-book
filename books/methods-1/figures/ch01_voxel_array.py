from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle

# 64 × 64 축상면 팬텀. 다른 ch01 그림도 이 함수를 쓴다.
N = 64


def brain_slice(n=N, seed=0):
    """두피, 두개골, 뇌척수액, 회백질, 백질, 뇌실을 가진 단순한 T1 강조 단면(int16 눈금)."""
    y, x = np.mgrid[-1:1:1j * n, -1:1:1j * n]
    th = np.arctan2(y, x)
    img = np.zeros((n, n))

    def ell(a, b, x0=0.0, y0=0.0, ang=0.0, wav=0.0, m=0):
        c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
        xr, yr = (x - x0) * c + (y - y0) * s, -(x - x0) * s + (y - y0) * c
        return np.sqrt((xr / a) ** 2 + (yr / b) ** 2) <= 1 + wav * np.cos(m * th)

    img[ell(0.80, 0.95)] = 600      # 두피
    img[ell(0.74, 0.89)] = 60       # 두개골
    img[ell(0.70, 0.85)] = 150      # 뇌척수액
    img[ell(0.67, 0.82, wav=0.03, m=16)] = 450   # 회백질
    img[ell(0.52, 0.66, wav=0.06, m=10)] = 700   # 백질
    img[ell(0.07, 0.22, x0=-0.11, y0=-0.02, ang=-15)] = 150   # 뇌실
    img[ell(0.07, 0.22, x0=0.11, y0=-0.02, ang=15)] = 150
    rng = np.random.default_rng(seed)
    img = img + rng.normal(0, 18, img.shape)
    return np.clip(np.round(img), 0, None).astype(np.int16)


if __name__ == "__main__":
    img = brain_slice()
    r0, c0, w = 30, 14, 6   # 확대할 6 × 6 칸(회백질-백질 경계 부근)

    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.7),
                            gridspec_kw=dict(width_ratios=[1, 1, 1.35], wspace=0.5))
    a = axs[0]
    a.imshow(img, cmap="gray", vmin=0, vmax=800)
    a.add_patch(Rectangle((c0 - 0.5, r0 - 0.5), w, w, fill=False, ec=C["red"], lw=1.5))
    a.set_title("(가) 64 × 64 단면", fontsize=10)
    a.set_xlabel("열 i")
    a.set_ylabel("행 j")
    a.set_xticks([0, 32, 63]); a.set_yticks([0, 32, 63])

    a = axs[1]
    sub = img[r0:r0 + w, c0:c0 + w]
    a.imshow(sub, cmap="gray", vmin=0, vmax=800)
    for (rr, cc), v in np.ndenumerate(sub):
        a.text(cc, rr, f"{v}", ha="center", va="center", fontsize=6.8,
               color="white" if v < 420 else C["ink"])
    a.set_xticks(range(w)); a.set_xticklabels(range(c0, c0 + w), fontsize=7)
    a.set_yticks(range(w)); a.set_yticklabels(range(r0, r0 + w), fontsize=7)
    a.set_title("(나) 복셀 하나 = 정수 하나", fontsize=10)
    for s in a.spines.values():
        s.set_visible(True); s.set_color(C["red"])

    # (다) 4차원: 같은 복셀의 시간축
    a = axs[2]
    rng = np.random.default_rng(3)
    T, TR = 150, 2.0
    t = np.arange(T) * TR
    box = ((t // 20) % 2 == 1).astype(float)
    from scipy.stats import gamma
    h = gamma.pdf(np.arange(0, 30, TR), 6) - gamma.pdf(np.arange(0, 30, TR), 16) / 6
    bold = np.convolve(box, h / h.max())[:T]
    ts = 700 + 12 * bold + rng.normal(0, 4, T) + 0.05 * t
    a.plot(t, ts, color=C["blue"], lw=0.9)
    a.set_xlabel("시간 (s), 4번째 차원")
    a.set_ylabel("복셀 값 (임의 단위)")
    a.set_title("(다) 4차원: 복셀마다 시계열", fontsize=10)
    a.set_xlim(0, t[-1])
    a.set_box_aspect(0.78)
    save(fig, __file__)
