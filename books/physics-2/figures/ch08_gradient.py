from figstyle import plt, np, save, C

# 3 T에 x 방향 경사 10 mT/m를 걸 때 위치에 따른 라머 주파수, 그리고 경사를 잠깐 켠 뒤 생긴 위상 무늬.
gbar = 42.58e6      # Hz/T
G = 10e-3           # T/m
x = np.linspace(-0.12, 0.12, 200)
df = gbar * G * x   # Hz

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1, 1.25], wspace=0.3))
a1.plot(x * 100, df / 1e3, color=C["purple"], lw=2)
a1.axhline(0, color=C["gray"], lw=0.6); a1.axvline(0, color=C["gray"], lw=0.6)
for xx in (-0.1, 0.05):
    f = gbar * G * xx / 1e3
    a1.plot([xx * 100, xx * 100], [0, f], color=C["gray"], ls=":", lw=0.8)
    a1.plot([0, xx * 100], [f, f], color=C["gray"], ls=":", lw=0.8)
    a1.plot(xx * 100, f, "o", color=C["red"], ms=4)
a1.text(-9.2, -44, "−42.6 kHz", fontsize=8.5, ha="left", va="top", color=C["red"])
a1.text(5.6, 21.3, "+21.3 kHz", fontsize=8.5, va="bottom", ha="left", color=C["red"])
a1.set_xlabel("위치 x (cm)")
a1.set_ylabel("중심 주파수와의 차이 Δf (kHz)", fontsize=9.5)
a1.set_ylim(-58, 58)
a1.text(-11.5, 45, "기울기\n425.8 Hz/mm", fontsize=8.5, color=C["purple"])
a1.set_title("(가) 경사 10 mT/m: 위치 → 주파수", fontsize=10)

# (나) k = γ̄ G t = 50 /m가 되도록 경사를 잠깐 켠 뒤의 위상
k = 50.0
t = k / (gbar * G)
xs = np.linspace(-2, 2, 13) / 100
ph = 2 * np.pi * k * xs
from matplotlib.patches import Circle
a2.scatter(xs * 100, np.full_like(xs, 1.05), s=190, facecolors="none", edgecolors=C["gray"], lw=0.6)
a2.quiver(xs * 100, np.full_like(xs, 1.05), np.sin(ph), np.cos(ph), angles="uv", scale_units="inches",
          scale=1 / 0.075, pivot="tail", color=C["purple"], width=0.006, headwidth=4, headlength=4, headaxislength=3.5)
xf = np.linspace(-0.02, 0.02, 400)
a2.plot(xf * 100, 0.25 * np.cos(2 * np.pi * k * xf) + 0.4, color=C["blue"], lw=1.4)
a2.text(2.25, 0.4, "실수부\n(cos)", fontsize=8, color=C["blue"], va="center")
a2.text(2.25, 1.05, "스핀\n위상", fontsize=8, color=C["purple"], va="center")
a2.annotate("", xy=(1.0, -0.05), xytext=(-1.0, -0.05), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=0.9, shrinkA=0, shrinkB=0))
a2.text(0, -0.12, "한 바퀴 = 1/k = 2 cm", fontsize=8.5, color=C["red"], ha="center", va="top")
a2.set_xlim(-2.3, 2.9); a2.set_ylim(-0.4, 1.4)
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xlabel("위치 x (cm)")
a2.set_title(f"(나) 경사를 {t * 1e3:.2f} ms 켠 뒤: 위상 무늬", fontsize=10)
save(fig, __file__)
