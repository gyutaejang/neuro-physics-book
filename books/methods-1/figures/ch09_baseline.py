from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
fs = 250.0
t = np.arange(-0.5, 1.0, 1 / fs)
ms = t * 1000


def g(mu, sd, a):
    return a * np.exp(-0.5 * ((t - mu) / sd) ** 2)


erp = g(0.10, 0.015, 2) + g(0.17, 0.02, -4) + g(0.40, 0.10, 6)
base = (t >= -0.2) & (t < 0)

# (가) 시행마다 다른 직류 치우침과 느린 표류
n_tr = 30
off = rng.normal(0, 15, n_tr)
slope = rng.normal(0, 8, n_tr)            # μV/s
trials = erp + off[:, None] + slope[:, None] * t + rng.normal(0, 4, (n_tr, t.size))
corr = trials - trials[:, base].mean(1, keepdims=True)

# (나) 조건 B에만 자극 앞 예기 음전위(CNV 비슷한 느린 경사)가 있다
cnv = np.where(t < 0, -3.0 * np.clip((t + 0.5) / 0.5, 0, 1), -3.0 * np.exp(-t / 0.15))
A_true = erp
B_true = erp + cnv
A_bc = A_true - A_true[base].mean()
B_bc = B_true - B_true[base].mean()

fig = plt.figure(figsize=(7.3, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.25], wspace=0.35)

a1 = fig.add_subplot(gs[0, 0])
a2 = fig.add_subplot(gs[0, 1], sharey=a1)
for ax, D, title in [(a1, trials, "(가) 보정 전 시행"), (a2, corr, "(나) 기저선 보정 뒤")]:
    ax.axvspan(-200, 0, color=C["light"], zorder=0)
    for y in D:
        ax.plot(ms, y, color=C["gray"], lw=0.3, alpha=0.35)
    ax.plot(ms, D.mean(0), color=C["blue"], lw=1.8, label="평균")
    ax.axvline(0, color=C["gray"], lw=0.5, ls=":")
    ax.set_xlim(-500, 1000)
    ax.set_xlabel("자극 뒤 시간 (ms)")
    ax.set_title(title, fontsize=9.3)
    sd = D[:, (t >= 0.3) & (t <= 0.5)].mean(1).std()
    ax.text(-470, -50, f"시행 간 표준편차\n(300–500 ms) {sd:.0f} μV", fontsize=7.4,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))
a1.set_ylim(-55, 55)
a1.set_ylabel("전위 (μV)")
plt.setp(a2.get_yticklabels(), visible=False)

a3 = fig.add_subplot(gs[0, 2])
a3.axvspan(-200, 0, color=C["light"], zorder=0)
a3.axhline(0, color=C["gray"], lw=0.5)
a3.axvline(0, color=C["gray"], lw=0.5, ls=":")
a3.plot(ms, A_bc, color=C["blue"], lw=1.5, label="A")
a3.plot(ms, B_bc, color=C["red"], lw=1.5, ls="--", label="B (자극 앞 음전위)")
a3.plot(ms, B_true, color=C["red"], lw=0.8, alpha=0.5, label="B 보정 전")
w = (t >= 0.6) & (t <= 0.9)
dfz = (B_bc - A_bc)[w].mean()
a3.text(620, 4.0, f"600–900 ms\n가짜 차이 {dfz:+.1f} μV", fontsize=7.4, color=C["red"])
a3.text(-190, 6.8, "기저선 창", fontsize=7.4, color=C["gray"])
a3.set_xlim(-500, 1000)
a3.set_ylim(-6.5, 8.5)
a3.set_xlabel("자극 뒤 시간 (ms)")
a3.set_ylabel("전위 (μV)")
a3.set_title("(다) 기저선이 조건마다 다를 때", fontsize=9.3)
a3.legend(fontsize=7, loc="lower right", bbox_to_anchor=(1.02, 0.0))

save(fig, __file__)
