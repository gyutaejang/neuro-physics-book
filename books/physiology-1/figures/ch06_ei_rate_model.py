from figstyle import plt, np, save, C


def S(x, a, th):
    return 1 / (1 + np.exp(-a * (x - th))) - 1 / (1 + np.exp(a * th))


def run(tauI, tauE=1.0, P=1.5, T=500.0, dt=0.02):
    """윌슨-코완 형태의 흥분(E)-억제(I) 집단 발화율 모형. 시간 단위는 ms."""
    n = int(T / dt)
    E = np.zeros(n)
    I = np.zeros(n)
    E[0] = 0.05
    for k in range(n - 1):
        E[k + 1] = E[k] + dt / tauE * (-E[k] + S(16 * E[k] - 12 * I[k] + P, 1.3, 4))
        I[k + 1] = I[k] + dt / tauI * (-I[k] + S(15 * E[k] - 3 * I[k], 2, 3.7))
    t = np.arange(n) * dt
    return t, E, I


def freq(t, E):
    m = t > 200
    x = E[m] - E[m].mean()
    zc = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    return 1000 / (np.mean(np.diff(zc)) * (t[1] - t[0]))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1.35, 1]))

t, E, I = run(4.0)
m = (t >= 300) & (t <= 400)
a1.plot(t[m] - 300, E[m], color=C["blue"], lw=1.5, label="흥분 집단 E")
a1.plot(t[m] - 300, I[m], color=C["red"], lw=1.5, label="억제 집단 I")
f4 = freq(t, E)
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("발화율 (최대값에 대한 비)")
a1.set_title(f"억제 시간 상수 4 ms: 약 {f4:.0f} Hz 진동", fontsize=10)
a1.set_ylim(-0.05, 1.42)
a1.set_yticks([0, 0.5, 1])
a1.legend(fontsize=8, loc="upper right", ncol=2, bbox_to_anchor=(1.0, 1.04))
# 흥분이 먼저 오르고 억제가 몇 ms 뒤따르는 것을 표시 (두 번째 주기, 절반 높이를 지나는 시점)
tt = t[m] - 300
up = lambda y: tt[np.where((y[:-1] < 0.5) & (y[1:] >= 0.5))[0]]
e0 = up(E[m])[1]
i0 = up(I[m])[up(I[m]) > e0][0]
a1.annotate("", xy=(i0, 1.06), xytext=(e0, 1.06),
            arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=0.9))
for x in (e0, i0):
    a1.plot([x, x], [0.5, 1.06], color=C["gray"], lw=0.6, ls=":")
a1.text((e0 + i0) / 2, 1.13, f"억제가 약 {i0 - e0:.0f} ms 뒤따른다", ha="center", va="bottom", fontsize=7.5, color=C["gray"])

taus = np.array([2, 2.5, 3, 4, 5, 6, 8, 10, 12])
fs = np.array([freq(*run(ti)[:2]) for ti in taus])
a2.axhspan(30, 100, color=C["light"], lw=0)
a2.text(11.8, 62, "감마 대역", ha="right", fontsize=8, color=C["blue"])
a2.axhspan(13, 30, color="#f3efe6", lw=0)
a2.text(1.4, 15, "베타 대역", ha="left", fontsize=8, color=C["gray"])
a2.plot(taus, fs, "o-", color=C["blue"], lw=1.4, ms=4)
a2.set_xlabel("억제의 실효 시간 상수 (ms)")
a2.set_ylabel("진동 주파수 (Hz)")
a2.set_title("억제가 길수록 리듬이 느려진다", fontsize=10)
a2.set_ylim(0, 75)
a2.set_xlim(1, 13)
fig.tight_layout()
save(fig, __file__)
