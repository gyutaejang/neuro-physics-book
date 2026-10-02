from figstyle import plt, np, save, C

# 이동 ↔ 위상 기울기: 3 mm 옮긴 물체는 진폭 스펙트럼이 같고 위상만 직선으로 기운다.
N, dx = 512, 0.5                     # 0.5 mm 간격, 256 mm 구간
x = (np.arange(N) - N // 2) * dx
obj = lambda x0: np.exp(-((x - x0) / 6) ** 2) + 0.6 * np.exp(-((x - x0 - 14) / 3) ** 2)
a, b = obj(0), obj(3.0)
k = np.fft.fftshift(np.fft.fftfreq(N, dx))   # 주기/mm
A = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(a)))
B = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(b)))
dphi = np.angle(B * np.conj(A))

fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), gridspec_kw={"wspace": 0.42})
axes[0].plot(x, a, color=C["blue"], label="원래")
axes[0].plot(x, b, color=C["red"], ls="--", label="3 mm 이동")
axes[0].set_xlim(-25, 35)
axes[0].set_ylim(0, 1.35)
axes[0].set_xlabel("위치 (mm)")
axes[0].legend(fontsize=8, loc="upper left")
axes[0].set_title("(가) 물체", fontsize=10)

axes[1].plot(k, np.abs(A) / np.abs(A).max(), color=C["blue"], lw=2.4)
axes[1].plot(k, np.abs(B) / np.abs(A).max(), color=C["red"], ls="--")
axes[1].set_xlim(-0.12, 0.12)
axes[1].set_ylim(0, 1.15)
axes[1].set_xlabel("공간 주파수 (주기/mm)")
axes[1].set_title("(나) 진폭: 똑같다", fontsize=10)

m = np.abs(k) <= 0.3
axes[2].plot(k[m], np.degrees(dphi[m]), color=C["gray"], lw=1.0, label="접힌 값 (±180°)")
axes[2].plot(k[m], -360 * 3.0 * k[m], color=C["red"], lw=1.6, label="−360° × 3 mm × k")
axes[2].axhline(0, color=C["gray"], lw=0.5)
axes[2].set_xlim(-0.3, 0.3)
axes[2].set_ylim(-420, 420)
axes[2].set_yticks([-360, -180, 0, 180, 360])
axes[2].set_xlabel("공간 주파수 (주기/mm)")
axes[2].set_ylabel("위상 차이 (°)")
axes[2].set_title("(다) 위상: 직선으로 기운다", fontsize=10)
axes[2].legend(fontsize=7, loc="lower left", handlelength=1.2)
axes[2].text(0.02, 330, "기울기 = 이동 거리", fontsize=7.5, color=C["red"])
save(fig, __file__)
