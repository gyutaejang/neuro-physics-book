import math

from matplotlib.patches import Rectangle
from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.3), gridspec_kw=dict(width_ratios=[1, 1.1]))

# (가) 평행 구멍 콜리메이터 도식 (축척은 과장)
a1.add_patch(Rectangle((-3, 3.0), 6, 0.5, facecolor=C["light"], edgecolor=C["gray"]))
a1.text(0, 3.25, "섬광 결정 (NaI)", ha="center", va="center", fontsize=8)
a1.add_patch(Rectangle((-3, 2.0), 6, 1.0, facecolor="#d9d9d9", edgecolor="none"))
hw = 0.16
for xc in np.arange(-2.4, 2.41, 0.6):
    a1.add_patch(Rectangle((xc - hw, 2.0), 2 * hw, 1.0, facecolor="white", edgecolor="none"))
a1.text(3.1, 2.5, "납 격벽\n(길이 L)", fontsize=7.8, va="center")
# 한 구멍(가운데)을 통과할 수 있는 광자의 원뿔
for z, col, lab in ((1.2, C["blue"], "가까운 선원"), (-0.6, C["red"], "먼 선원")):
    # 구멍 x ∈ [-hw, hw], 위 끝 y=3, 아래 끝 y=2. 선원 깊이 z에서 받아들이는 폭
    Lc = 1.0
    half = hw + 2 * hw * (2.0 - z) / Lc
    a1.fill([-hw, hw, half, -half], [3.0, 3.0, z, z], color=col, alpha=0.18, lw=0)
    a1.plot([-hw, -half], [3.0, z], color=col, lw=0.8)
    a1.plot([hw, half], [3.0, z], color=col, lw=0.8)
    a1.plot([-half, half], [z, z], color=col, lw=1.6)
    a1.text(half + 0.4, z, lab + ("\n좁게 퍼진다" if z > 0 else "\n넓게 퍼진다"), fontsize=7.6, color=col, va="center")
a1.annotate("", xy=(-1.0, 3.0), xytext=(-1.0, 4.2),
            arrowprops=dict(arrowstyle="<|-", color=C["ink"], lw=0.8))
a1.text(-0.9, 4.0, "빛 → 광전자증배관", fontsize=7.6)
a1.set_xlim(-3.3, 4.6)
a1.set_ylim(-1.3, 4.4)
a1.set_aspect("equal")
a1.axis("off")
a1.set_title("(가) 구멍 하나가 받아들이는 원뿔", fontsize=9.5)

# (나) 계 해상도 대 거리
Ri = 3.8      # 고유 해상도 (mm)
z = np.linspace(0, 200, 200)
for name, d, L, t, col in (("고해상도형 (LEHR)", 1.11, 24.05, 0.16, C["blue"]),
                           ("범용형 (LEGP)", 1.45, 24.05, 0.20, C["purple"]),
                           ("고해상도형 구멍·격벽 2배", 2.22, 24.05, 0.32, C["red"])):
    Le = L - 2 / 2.7   # 납의 140 keV 감쇠 계수 약 2.7 /mm로 실효 길이 보정
    Rs = np.hypot(d * (Le + z) / Le, Ri)
    g = 0.26 ** 2 * (d / Le) ** 2 * (d / (d + t)) ** 2
    a2.plot(z / 10, Rs, color=col, lw=1.8, label=f"{name}: 효율 {g * 1e4:.1f}×10⁻⁴")
a2.axvspan(10, 15, color=C["light"], zorder=0)
a2.text(12.5, 1.5, "뇌 중심까지\n대략의 거리", ha="center", fontsize=7.6, color=C["gray"])
a2.set_xlim(0, 20)
a2.set_ylim(0, 26)
a2.set_xlabel("선원과 콜리메이터 사이 거리 (cm)")
a2.set_ylabel("계 해상도 FWHM (mm)")
a2.legend(fontsize=7.3, loc="upper left")
a2.set_title("(나) 멀수록 흐리고, 효율과 맞바꾼다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
