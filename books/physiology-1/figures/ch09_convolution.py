import math

from figstyle import plt, np, save, C

dt = 0.05
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6
h = h / h.max()


def conv(s):
    return np.convolve(s, h)[: len(s)]


fig = plt.figure(figsize=(7.2, 4.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.1], hspace=0.6, wspace=0.28)

# (가) 사건 세 개: 반응이 겹쳐 더해진다
a1 = fig.add_subplot(gs[0, 0])
T = np.arange(0, 40, dt)
ons = [2, 6, 10]
tot = np.zeros_like(T)
for k, o in enumerate(ons):
    s = np.zeros_like(T)
    s[int(round(o / dt))] = 1
    y = conv(s)
    tot += y
    a1.plot(T, y, color=C["gray"], lw=0.8, ls="--")
    a1.annotate("", xy=(o, 0), xytext=(o, -0.5),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1, mutation_scale=8))
a1.plot(T, tot, color=C["blue"], lw=1.8)
a1.axhline(0, color=C["gray"], lw=0.5)
a1.set_xlim(0, 40)
a1.set_ylim(-0.6, 2.0)
a1.set_title("(가) 4 s 간격 사건 세 개", fontsize=9.5)
a1.set_xlabel("시간 (s)")
a1.set_ylabel("예측 반응")
a1.text(21, 1.45, "합 (파랑)", color=C["blue"], fontsize=8)
a1.text(21, 1.15, "사건마다의 HRF (회색)", color=C["gray"], fontsize=8)

# (나) 사건 간격과 합의 정점
a2 = fig.add_subplot(gs[0, 1])
gaps = np.arange(1, 16.01, 0.25)
peaks = []
for gp in gaps:
    s = np.zeros_like(T)
    s[int(round(2 / dt))] = 1
    s[int(round((2 + gp) / dt))] = 1
    peaks.append(conv(s).max())
a2.plot(gaps, peaks, color=C["blue"], lw=1.8)
for gp in (2, 4, 8):
    i = np.argmin(abs(gaps - gp))
    a2.scatter([gp], [peaks[i]], color=C["red"], s=18, zorder=3)
    a2.text(gp + 0.5, peaks[i] + 0.06, f"{gp} s: {peaks[i]:.1f}", fontsize=8)
a2.axhline(1, color=C["gray"], lw=0.6, ls=":")
a2.set_xlabel("두 사건 사이 간격 (s)")
a2.set_ylabel("합의 정점 (사건 하나 = 1)")
a2.set_title("(나) 사건 두 개의 겹침", fontsize=9.5)
a2.set_ylim(0.8, 2.1)
a2.set_xlim(0, 16)

# (다) 블록 설계: 20 s 켜짐 / 20 s 꺼짐
a3 = fig.add_subplot(gs[1, :])
T = np.arange(0, 160, dt)
box = ((T % 40) < 20) & (T < 140)
s = box.astype(float) * dt
y = conv(s)
y = y / y.max()
a3.fill_between(T, 0, box * 1.0, color=C["light"], step="pre", label="자극 (상자 함수)")
a3.plot(T, y, color=C["blue"], lw=1.8, label="상자 함수 ⊛ HRF = 예측 BOLD")
a3.axhline(0, color=C["gray"], lw=0.5)
i5 = np.argmax(y > 0.5)
a3.annotate("", xy=(T[i5], 0.5), xytext=(0, 0.5),
            arrowprops=dict(arrowstyle="<->", color=C["red"], lw=0.8, shrinkA=0, shrinkB=0))
a3.text(7, 0.32, f"절반까지\n약 {T[i5]:.0f} s", fontsize=8, color=C["red"], va="top")
ib = np.argmin(y[int(140 / dt):]) + int(140 / dt)
a3.annotate("언더슈트", xy=(T[ib], y[ib]), xytext=(T[ib] + 4, -0.3), fontsize=8, va="center",
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a3.set_xlim(0, 160)
a3.set_ylim(-0.4, 1.3)
a3.set_xlabel("시간 (s)")
a3.set_ylabel("정규화한 크기")
a3.set_title("(다) 20 s 켜짐 / 20 s 꺼짐 블록 설계", fontsize=9.5)
a3.legend(fontsize=8, loc="upper right", ncol=2)
save(fig, __file__)
