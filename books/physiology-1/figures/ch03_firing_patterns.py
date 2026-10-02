from figstyle import plt, np, save, C

# 이지케비치(Izhikevich, 2003) 단순 모형으로 세 가지 발화 패턴을 흉내 낸다.
# 같은 계단 전류를 넣고 a, b, c, d 네 값만 바꾼다.
TYPES = [
    ("규칙 발화 (피질 피라미드 뉴런)", (0.02, 0.2, -65, 8), C["blue"]),
    ("버스트로 시작하는 발화 (5층 피라미드 뉴런 일부)", (0.02, 0.2, -55, 4), C["green"]),
    ("빠른 발화 (PV 억제성 인터뉴런)", (0.1, 0.2, -65, 2), C["red"]),
]
dt, T, t_on, t_off, I0 = 0.05, 300.0, 20.0, 270.0, 10.0
t = np.arange(0, T, dt)

fig, axes = plt.subplots(4, 1, figsize=(6.5, 4.8), sharex=True,
                         gridspec_kw=dict(height_ratios=[1, 1, 1, 0.3], hspace=0.35))
for ax, (name, (a, b, c, d), col) in zip(axes, TYPES):
    v, u = -65.0, b * -65.0
    vs, spikes = np.zeros_like(t), []
    for i, tt in enumerate(t):
        I = I0 if t_on <= tt < t_off else 0.0
        v += dt * (0.04 * v * v + 5 * v + 140 - u + I)
        u += dt * a * (b * v - u)
        if v >= 30:
            vs[i] = 30
            v, u = c, u + d
            spikes.append(tt)
        else:
            vs[i] = v
    sp = np.array(spikes)
    isi = np.diff(sp)
    rate = len(sp) / ((t_off - t_on) / 1000)
    ax.plot(t, vs, color=col, lw=0.9)
    ax.set_ylim(-85, 40)
    ax.set_yticks([-60, 0])
    ax.set_yticklabels(["−60", "0"])
    ax.set_title(f"{name}: 평균 약 {rate:.0f} Hz", fontsize=9, loc="left")
    print(name, "rate", round(rate), "first ISIs", np.round(isi[:4], 1), "last ISI", round(isi[-1], 1))
axes[1].set_ylabel("막전위 (mV)")
axes[3].plot(t, np.where((t >= t_on) & (t < t_off), 1, 0), color=C["gray"], lw=1.2)
axes[3].set_yticks([])
axes[3].spines["left"].set_visible(False)
axes[3].text(t_off + 5, 0.5, "입력 전류", fontsize=8, color=C["gray"], va="center")
axes[3].set_xlabel("시간 (ms)")
axes[3].set_xlim(0, T)
save(fig, __file__)
