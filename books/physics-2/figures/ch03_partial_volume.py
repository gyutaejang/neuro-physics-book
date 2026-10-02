import math

from figstyle import plt, np, save, C

# 얇은 피질의 부분 용적 효과: 1차원 단면(두께 방향)만 가우스 점 퍼짐으로 흐린다.
dx = 0.02
x = np.arange(-30, 40, dx)


def blur(f, fwhm):
    s = fwhm / 2.3548
    k = np.arange(-4 * s, 4 * s + dx, dx)
    g = np.exp(-k ** 2 / (2 * s ** 2))
    g /= g.sum()
    return np.convolve(f, g, mode="same")


def profile(th):
    # 왼쪽부터 뇌척수액(0) | 회백질(4) | 백질(1)
    f = np.zeros_like(x)
    f[(x >= 0) & (x < th)] = 4.0
    f[x >= th] = 1.0
    return f


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2), gridspec_kw=dict(width_ratios=[1.15, 1]))
true = profile(2.5)
a1.fill_between(x, 0, true, step="mid", color=C["light"], label="참 분포 (피질 2.5 mm)")
a1.plot(x, blur(true, 5), color=C["blue"], lw=1.8, label="측정 (FWHM 5 mm)")
a1.plot(x, blur(profile(2.0), 5), color=C["red"], lw=1.5, ls="--", label="피질이 2.0 mm로 얇아지면")
a1.axhline(4, color=C["gray"], lw=0.6, ls=":")
pk = blur(true, 5).max()
a1.annotate(f"정점 {pk:.1f}\n(참값 4의 {pk / 4 * 100:.0f}%)", xy=(1.3, pk), xytext=(6.5, 3.2), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a1.text(-7.5, 0.25, "뇌척수액", fontsize=8, ha="center", color=C["gray"])
a1.text(1.25, 4.15, "회백질", fontsize=8, ha="center", color=C["gray"])
a1.text(13, 0.55, "백질", fontsize=8, ha="center", color=C["gray"])
a1.set_xlim(-12, 18)
a1.set_ylim(0, 5.3)
a1.set_xlabel("피질 표면에 수직인 거리 (mm)")
a1.set_ylabel("방사능 농도 (상대값)")
a1.legend(fontsize=7.6, loc="upper right")
a1.set_title("(가) 얇은 피질은 흐려지며 낮아진다", fontsize=9.5)

w = np.linspace(0.2, 12, 300)
for F, col in ((2.5, C["purple"]), (5, C["blue"]), (8, C["red"])):
    s = F / 2.3548
    rc = [math.erf(v / (2 * math.sqrt(2) * s)) for v in w]
    a2.plot(w, rc, color=col, lw=1.8, label=f"FWHM {F:g} mm")
a2.axvspan(2, 4, color=C["light"], zorder=0)
a2.text(3, 0.04, "피질\n두께", ha="center", fontsize=8, color=C["gray"])
a2.set_xlim(0, 12)
a2.set_ylim(0, 1.05)
a2.set_xlabel("구조의 두께 (mm)")
a2.set_ylabel("회복 계수 (측정 정점 / 참값)")
a2.legend(fontsize=7.8, loc="lower right")
a2.set_title("(나) 두께와 회복 계수", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
