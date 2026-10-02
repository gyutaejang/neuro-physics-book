from figstyle import plt, np, save, C

# 많은 등색 스핀 묶음의 합으로 만든 FID와 스핀 에코.
# T2 = 95 ms(회백질 3 T)에 자기장이 고르지 않은 복셀을 가정해 T2' = 30 ms를 둔다. 주파수 분포는 로런츠형.
T2, T2p = 95.0, 30.0
T2s = 1 / (1 / T2 + 1 / T2p)
tau = 40.0                                   # 180° 펄스 시각 (ms), 에코는 2τ = 80 ms
N = 20001
q = (np.arange(N) + 0.5) / N
dw = np.tan(np.pi * (q - 0.5)) / T2p         # rad/ms, 반폭 1/T2'
dw = dw[np.abs(dw) < 60 / T2p]               # 극단의 꼬리는 잘라 계산을 안정시킨다

t = np.linspace(0, 160, 1601)
phase = np.where(t[:, None] < tau, dw * t[:, None], dw * (t[:, None] - 2 * tau))
S = np.abs(np.exp(1j * phase).mean(axis=1)) * np.exp(-t / T2)
print("에코 높이", S[np.argmin(abs(t - 80))], "기대", np.exp(-80 / T2))

fig, ax = plt.subplots(figsize=(6.6, 2.9))
ax.plot(t, np.exp(-t / T2), color=C["gray"], ls="--", lw=1)
ax.plot(t, np.exp(-t / T2s), color=C["blue"], ls=":", lw=1.2)
ax.plot(t, S, color=C["purple"], lw=1.8)
for x0, lab in ((0, "90°"), (tau, "180°")):
    ax.annotate(lab, (x0, 1.0), xytext=(x0, 1.13), ha="center", fontsize=9, color=C["red"],
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1))
ax.axvline(2 * tau, color=C["gray"], lw=0.6, ls=":")
ax.text(2 * tau + 2, 1.12, "TE = 2τ", ha="left", fontsize=8.5)
ax.text(118, 0.37, "$e^{-t/T_2}$ (T2 = 95 ms)", fontsize=8.5, color=C["gray"])
ax.text(14, 0.05, f"$e^{{-t/T_2^*}}$\n(T2* = {T2s:.0f} ms)", fontsize=8.5, color=C["blue"])
ax.text(20, 0.6, "FID", fontsize=9, color=C["purple"])
ax.text(84, 0.47, "에코", fontsize=9, color=C["purple"])
ax.set_xlim(-4, 160)
ax.set_ylim(0, 1.25)
ax.set_xlabel("시간 (ms)")
ax.set_ylabel("신호 크기 (상대값)")
save(fig, __file__)
