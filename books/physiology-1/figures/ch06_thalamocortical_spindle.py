from figstyle import plt, np, save, C
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[1, 1.45]))

# 왼쪽: 시상-피질 고리
a = a1
a.set_xlim(0, 4)
a.set_ylim(0, 4.2)
a.axis("off")


def box(x, y, w, h, text, col):
    a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", facecolor="white",
                               edgecolor=col, lw=1.4))
    a.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5)


box(0.9, 3.2, 2.2, 0.7, "대뇌 피질\n(피라미드 뉴런)", C["green"])
box(0.2, 0.4, 1.6, 0.8, "시상 중계핵\n(흥분성)", C["green"])
box(2.4, 0.4, 1.5, 0.8, "시상 그물핵\n(GABA, 억제성)", C["red"])


def arr(p0, p1, col, style="-|>", rad=0.0):
    a.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=10 if style == "-|>" else 5,
                                color=col, lw=1.3, connectionstyle=f"arc3,rad={rad}"))


arr((0.75, 1.25), (1.2, 3.12), C["blue"])          # 시상 → 피질
arr((1.55, 3.12), (1.25, 1.25), C["blue"])         # 피질 → 시상
arr((2.5, 3.12), (3.1, 1.25), C["blue"])           # 피질 → 그물핵
arr((1.85, 1.0), (2.33, 1.0), C["blue"])           # 중계핵 → 그물핵 (곁가지)
arr((2.33, 0.6), (1.87, 0.6), C["red"], "-[")      # 그물핵 ⊣ 중계핵
a.text(2.1, 0.12, "억제 → 과분극 → T형 Ca²⁺ 통로가\n다시 열릴 준비 → 반동 버스트", ha="center",
       va="top", fontsize=7.5, color=C["red"])
a.set_ylim(-0.6, 4.2)
a.set_title("시상-피질 고리", fontsize=10)

# 오른쪽: N2 수면의 방추파 (모식 신호)
rng = np.random.default_rng(3)
fs = 250
t = np.arange(0, 4, 1 / fs)
f = np.fft.rfftfreq(t.size, 1 / fs)
spec = np.zeros_like(f)
spec[1:] = 1 / f[1:] ** 0.9
spec[f > 40] = 0
bg = np.fft.irfft(spec * np.exp(2j * np.pi * rng.random(f.size)), n=t.size)
bg = bg / bg.std() * 12
env = np.exp(-0.5 * ((t - 2.0) / 0.3) ** 2)
sp = 30 * env * np.sin(2 * np.pi * 13 * t)
a2.plot(t, bg + sp, color=C["blue"], lw=0.8)
a2.plot(t, 30 * env + 45, color=C["gray"], lw=0.6, ls="--")
on = t[env > 0.25]
a2.annotate("", xy=(on[0], -70), xytext=(on[-1], -70),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=0.9))
a2.text(2.0, -78, f"방추파 약 {on[-1] - on[0]:.1f} s, 13 Hz", ha="center", va="top", fontsize=8, color=C["red"])
a2.text(2.0, 80, "점점 커졌다 작아지는 포락선", ha="center", va="bottom", fontsize=7.5, color=C["gray"])
a2.plot([0.1, 0.1], [-60, -10], color=C["ink"], lw=1.2)
a2.text(0.17, -35, "50 μV", fontsize=7.5, va="center")
a2.set_ylim(-100, 100)
a2.set_xlim(0, 4)
a2.set_yticks([])
a2.spines["left"].set_visible(False)
a2.set_xlabel("시간 (s)")
a2.set_title("N2 수면 EEG의 수면방추 (모식도)", fontsize=10)
fig.tight_layout()
save(fig, __file__)
