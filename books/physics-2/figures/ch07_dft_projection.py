from figstyle import plt, np, save, C

# 푸리에 변환의 직관: 신호를 주파수 f로 도는 화살표에 실어 감고, 그 무게중심을 본다.
T, fs = 2.0, 400
t = np.arange(0, T, 1 / fs)
x = np.cos(2 * np.pi * 3 * t) + 0.5 * np.cos(2 * np.pi * 5 * t)

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.75),
                         gridspec_kw={"width_ratios": [1, 1, 1.45], "wspace": 0.35})
for ax, f, title in ((axes[0], 2.5, "(가) f = 2.5 Hz로 감기"), (axes[1], 3.0, "(나) f = 3 Hz로 감기")):
    w = x * np.exp(-1j * 2 * np.pi * f * t)
    ax.plot(w.real, w.imag, color=C["blue"], lw=0.6, alpha=0.85)
    m = w.mean()
    ax.plot([m.real], [m.imag], "o", color=C["red"], ms=6, zorder=5)
    ax.axhline(0, color=C["gray"], lw=0.5)
    ax.axvline(0, color=C["gray"], lw=0.5)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.85, 1.6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=9.5)
    ax.text(0, -1.83, f"무게중심 크기 {abs(m):.2f}", ha="center", va="bottom", fontsize=8,
            color=C["red"], bbox=dict(fc="white", ec="none", pad=1))

fr = np.linspace(0, 7, 1401)
amp = np.array([abs(np.mean(x * np.exp(-1j * 2 * np.pi * ff * t))) for ff in fr])
ax = axes[2]
ax.plot(fr, amp, color=C["blue"])
for ff, lab, xt, yt in ((2.5, "가", 1.3, 0.22), (3.0, "나", 2.0, 0.53)):
    i = np.argmin(abs(fr - ff))
    ax.plot([ff], [amp[i]], "o", color=C["red"], ms=4, zorder=5)
    ax.annotate(lab, xy=(ff, amp[i]), xytext=(xt, yt), fontsize=8, color=C["red"], ha="center",
                arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.6))
ax.set_xlabel("감는 주파수 f (Hz)")
ax.set_ylabel("무게중심 크기")
ax.set_ylim(0, 0.62)
ax.set_xlim(0, 7)
ax.set_title("(다) f를 훑으면 스펙트럼", fontsize=9.5)
ax.text(5.2, 0.33, "5 Hz 성분\n(진폭 0.5)", fontsize=8, ha="center")
ax.text(3.9, 0.53, "3 Hz 성분 (진폭 1)", fontsize=8, ha="left")
save(fig, __file__)
