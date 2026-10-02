from figstyle import plt, np, save, C

# 3 T, 짧은 TE의 뇌 ¹H-MRS를 흉내 낸 도식 스펙트럼. 실제 측정값이 아니다.
ppm = np.linspace(0.8, 4.3, 3000)
W = 0.035  # 선폭(반너비, ppm) — 3 T에서 약 4–5 Hz


def peak(c, h, w=W):
    return h * w ** 2 / ((ppm - c) ** 2 + w ** 2)


def lactate(h):  # 1.33 ppm 이중선, J ≈ 7 Hz ≈ 0.055 ppm (3 T)
    return peak(1.33 - 0.0275, h, 0.025) + peak(1.33 + 0.0275, h, 0.025)


def glx(h):  # 글루탐산·글루타민 다중선 (2.05–2.45, 3.75)
    s = 0
    for c, a in ((2.06, 0.5), (2.12, 0.6), (2.24, 0.35), (2.35, 0.9), (2.44, 0.6)):
        s = s + peak(c, a * h, 0.03)
    for c, a in ((3.72, 0.7), (3.77, 0.8)):
        s = s + peak(c, a * h, 0.03)
    return s


def mi(h):  # 미오이노시톨 3.52, 3.61 부근
    return peak(3.52, h, 0.035) + peak(3.62, 0.8 * h, 0.035)


def spectrum(naa, cr, cho, mio, gl, lac):
    return (peak(2.01, naa) + peak(2.6, 0.08 * naa, 0.05) + peak(3.03, cr) + peak(3.92, 0.7 * cr)
            + peak(3.20, cho) + mi(mio) + glx(gl) + lactate(lac))


fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.6), sharex=True, gridspec_kw=dict(hspace=0.15))
cases = [("(가) 정상 회백질 (도식)", spectrum(1.0, 0.62, 0.48, 0.32, 0.17, 0.0), C["blue"]),
         ("(나) 병변의 예: NAA 감소, 콜린 증가, 젖산 출현 (도식)", spectrum(0.45, 0.5, 0.85, 0.3, 0.12, 0.42),
          C["red"])]
labels = [(2.01, "NAA\n2.01"), (3.03, "Cr\n3.03"), (3.20, "Cho\n3.2"), (3.92, "Cr\n3.9"),
          (3.56, "mI\n3.56"), (2.3, "Glx\n2.1–2.5"), (3.75, "Glx\n3.75"), (1.33, "Lac\n1.33")]
for ax, (title, y, col) in zip(axes, cases):
    ax.plot(ppm, y, color=col, lw=1.2)
    ax.set_xlim(4.3, 0.8)  # 관례대로 ppm은 오른쪽으로 갈수록 작아진다
    ax.set_ylim(-0.03, 1.32)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(4.27, 1.22, title, fontsize=9, va="top", color=col)
    for x, t in labels:
        i = np.argmin(abs(ppm - x))
        h = y[max(i - 40, 0):i + 40].max()
        if t.startswith("Lac") and h < 0.1:
            continue
        ax.text(x, h + 0.03, t, ha="center", va="bottom", fontsize=7.5, color=C["ink"], linespacing=1.0)
axes[1].set_xlabel("화학적 이동 (ppm)")
axes[1].set_xticks([4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0])
save(fig, __file__)
