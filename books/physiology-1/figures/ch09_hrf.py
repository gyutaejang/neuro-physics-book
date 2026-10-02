import math

from figstyle import plt, np, save, C

# 표준 이중 감마 HRF (SPM 기본형: 정점 감마 a=6, 언더슈트 감마 a=16, 비 1/6).
t = np.linspace(0, 32, 3201)
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
h = g(t, 6) - g(t, 16) / 6
h = h / h.max()
# 초기 감소는 도식으로만 (크기를 과장해 그렸다)
dip = -0.12 * g(t / 0.55, 3) / g(np.array([2.0]), 3)[0]
hd = h + dip * np.exp(-0.0 * t)

fig, ax = plt.subplots(figsize=(6.8, 3.3))
ax.axhline(0, color=C["gray"], lw=0.7)
ax.axvspan(0, 1, color=C["light"], zorder=0)
ax.text(1.3, 1.15, "자극 1 s (회색 띠)", ha="left", va="center", fontsize=7.5, color=C["gray"])
ax.plot(t, h, color=C["blue"], lw=2, label="표준 이중 감마 HRF")
ax.plot(t, hd, color=C["red"], lw=1.2, ls="--", label="초기 감소를 더한 모양 (도식, 과장)")

ip = h.argmax()
ax.annotate("정점: 약 5 s", xy=(t[ip], 1), xytext=(8.0, 0.95), fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6), va="center")
half = t[h >= 0.5]
ax.annotate("", xy=(half.min(), 0.5), xytext=(half.max(), 0.5),
            arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
ax.text(9.3, 0.5, "반치폭 약 5 s", fontsize=8, va="center", color=C["ink"])
im = hd[:400].argmin()
ax.annotate("초기 감소\n(1–2 s, 논쟁)", xy=(t[im], hd[im]), xytext=(2.6, -0.33), fontsize=8,
            color=C["red"], ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
iu = h.argmin()
ax.annotate("후과 언더슈트\n(정점의 약 10%, 수십 초)", xy=(t[iu], h[iu]), xytext=(19.5, -0.32),
            fontsize=8, va="center", arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
zc = t[np.where((h[:-1] > 0) & (h[1:] <= 0))[0][0]]
ax.scatter([zc], [0], s=14, color=C["ink"], zorder=4)
ax.text(zc + 0.4, 0.06, "기저선 통과\n약 12 s", fontsize=7.5)
ax.set_xlim(0, 32)
ax.set_ylim(-0.45, 1.25)
ax.set_xlabel("자극 시작 뒤 시간 (s)")
ax.set_ylabel("BOLD 반응 (정점 = 1)")
ax.legend(fontsize=8, loc="upper right")
fig.tight_layout()
save(fig, __file__)
