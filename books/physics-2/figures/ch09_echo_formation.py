from figstyle import plt, np, save, C

# 스핀 에코 형성: 여러 등색점(isochromat)의 위상이 흩어졌다가 180° 펄스 뒤 다시 모인다.
# 회백질 T2 = 100 ms에 장 불균일이 큰 자리를 가정: T2' = 25 ms → T2* = 20 ms.
rng = np.random.default_rng(3)
T2, T2p = 100.0, 25.0
n = 4000
# 로렌츠 분포 주파수 오프셋 → 지수적 T2' 감쇠 (반폭 = 1/(2π T2'))
df = np.tan(np.pi * (rng.random(n) - 0.5)) / (2 * np.pi * T2p)  # kHz (1/ms)
tau = 40.0  # 180° 펄스 시각 (ms), 에코는 2τ = 80 ms
t = np.linspace(0, 250, 2501)


def signal(t, refocus=True):
    out = np.zeros_like(t, dtype=complex)
    for i, ti in enumerate(t):
        if refocus and ti > tau:
            ph = 2 * np.pi * df * (ti - 2 * tau)
        else:
            ph = 2 * np.pi * df * ti
        out[i] = np.mean(np.exp(1j * ph)) * np.exp(-ti / T2)
    return np.abs(out)


s_fid = signal(t, refocus=False)
s_se = signal(t, refocus=True)

fig = plt.figure(figsize=(7.0, 3.6))
gsp = fig.add_gridspec(2, 4, height_ratios=[1, 1.55], hspace=0.3, wspace=0.25)
moments = [(0.5, "① 90° 직후"), (tau - 0.1, "② 흩어짐 (τ)"), (tau + 0.1, "③ 180° 뒤 뒤집힘"),
           (2 * tau, "④ 에코 (2τ)")]
sel = rng.choice(n, 9, replace=False)
sel_df = np.sort(np.clip(df[sel], -0.02, 0.02))
cols = plt.cm.coolwarm(np.linspace(0.05, 0.95, len(sel_df)))
for k, (tm, lab) in enumerate(moments):
    ax = fig.add_subplot(gsp[0, k])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=C["gray"], lw=0.6))
    for d, c in zip(sel_df, cols):
        if k == 0:
            ph = 2 * np.pi * d * 0.5
        elif k == 1:
            ph = 2 * np.pi * d * tau
        elif k == 2:
            ph = -2 * np.pi * d * tau
        else:
            ph = 0.0
        ph = ph * 1.5  # 그림에서 퍼짐이 보이도록 과장
        ax.annotate("", xy=(np.cos(ph + np.pi / 2), np.sin(ph + np.pi / 2)), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.0, mutation_scale=7))
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_title(lab, fontsize=8.5)

ax = fig.add_subplot(gsp[1, :])
ax.plot(t, s_fid, color=C["gray"], lw=1.2, label="180° 없음: FID, $e^{-t/T_2^*}$")
ax.plot(t, s_se, color=C["red"], lw=1.6, label="180° 펄스(τ = 40 ms) 뒤 스핀 에코")
ax.plot(t, np.exp(-t / T2), color=C["blue"], ls="--", lw=1.0, label="$e^{-t/T_2}$ 포락선")
ax.axvline(tau, color=C["purple"], lw=0.8, ls=":")
ax.text(tau + 2, 0.92, "180°", color=C["purple"], fontsize=8.5)
ax.annotate(f"에코 높이 = $e^{{-80/100}}$ ≈ {np.exp(-80/100):.2f}", xy=(80, np.exp(-0.8)),
            xytext=(105, 0.55), fontsize=8.5, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.set_xlim(0, 250)
ax.set_ylim(0, 1.05)
ax.set_xlabel("시간 (ms)")
ax.set_ylabel("신호 크기")
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 1.08))
save(fig, __file__)
