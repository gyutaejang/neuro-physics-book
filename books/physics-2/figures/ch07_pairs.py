from figstyle import plt, np, save, C

# 세 가지 중요한 푸리에 짝을 numpy FFT로 직접 계산한다.
N, dt = 2 ** 14, 0.01            # 시간 축: 0.01 s 간격 (가로축은 임의 단위로 읽어도 된다)
t = (np.arange(N) - N // 2) * dt
f = np.fft.fftshift(np.fft.fftfreq(N, dt))


def ft(x):
    X = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(x))) * dt
    return X


fig, axes = plt.subplots(3, 2, figsize=(6.6, 5.2), gridspec_kw={"hspace": 0.75, "wspace": 0.28})
narrow, wide = C["red"], C["blue"]

# 1. 사각 ↔ sinc
for T, col, lab in ((1.0, narrow, "폭 1 s"), (2.0, wide, "폭 2 s")):
    x = (np.abs(t) <= T / 2).astype(float)
    X = ft(x).real
    axes[0, 0].plot(t, x, color=col, label=lab)
    axes[0, 1].plot(f, X, color=col)
axes[0, 0].set_xlim(-2, 2)
axes[0, 0].set_ylim(-0.1, 1.45)
axes[0, 0].legend(fontsize=8, loc="upper right", ncol=2, handlelength=1.2)
axes[0, 0].set_title("(가) 사각 펄스", fontsize=10)
axes[0, 1].set_xlim(-3, 3)
axes[0, 1].axhline(0, color=C["gray"], lw=0.5)
axes[0, 1].set_title("sinc: 첫 영점이 ±1/폭", fontsize=10)
axes[0, 1].annotate("±1 Hz", xy=(1, 0), xytext=(1.5, 0.9), fontsize=8, color=narrow,
                    arrowprops=dict(arrowstyle="-", color=narrow, lw=0.6))
axes[0, 1].annotate("±0.5 Hz", xy=(0.5, 0), xytext=(1.1, 1.6), fontsize=8, color=wide,
                    arrowprops=dict(arrowstyle="-", color=wide, lw=0.6))
axes[0, 1].set_ylim(-0.6, 2.2)

# 2. 가우스 ↔ 가우스
for s, col, lab in ((0.2, narrow, "σ = 0.2 s"), (0.5, wide, "σ = 0.5 s")):
    x = np.exp(-t ** 2 / (2 * s ** 2))
    X = ft(x).real
    axes[1, 0].plot(t, x, color=col, label=lab)
    axes[1, 1].plot(f, X / X.max(), color=col)
axes[1, 0].set_xlim(-2, 2)
axes[1, 0].set_ylim(-0.05, 1.45)
axes[1, 0].legend(fontsize=8, loc="upper right", ncol=2, handlelength=1.2)
axes[1, 0].set_title("(나) 가우스", fontsize=10)
axes[1, 1].set_xlim(-3, 3)
axes[1, 1].set_ylim(-0.05, 1.3)
axes[1, 1].set_title("가우스: 폭이 역수로 바뀐다 (최댓값 = 1)", fontsize=10)

# 3. 지수 감쇠(FID) ↔ 로렌츠 선
for T2, col, lab in ((0.3, narrow, "$T_2^*$ = 0.3 s"), (1.0, wide, "$T_2^*$ = 1 s")):
    x = np.where(t >= 0, np.exp(-np.abs(t) / T2), 0.0)
    X = ft(x).real                       # 흡수 모양(실수부)이 로렌츠 선이다
    axes[2, 0].plot(t, x, color=col, label=lab)
    axes[2, 1].plot(f, X / X.max(), color=col)
axes[2, 0].set_xlim(-0.5, 3.5)
axes[2, 0].set_ylim(-0.05, 1.45)
axes[2, 0].legend(fontsize=8, loc="upper right", ncol=2, handlelength=1.2)
axes[2, 0].set_title("(다) 지수 감쇠 (FID의 포락선)", fontsize=10)
axes[2, 0].set_xlabel("시간 (s)")
axes[2, 1].set_xlim(-3, 3)
axes[2, 1].set_ylim(-0.05, 1.3)
axes[2, 1].set_title("로렌츠 선: 반치폭 = 1/(π$T_2^*$)", fontsize=10)
axes[2, 1].set_xlabel("주파수 (Hz)")
axes[2, 1].annotate("반치폭 약 1.06 Hz", xy=(0.53, 0.5), xytext=(1.0, 0.75), fontsize=8,
                    color=narrow, arrowprops=dict(arrowstyle="-", color=narrow, lw=0.6))
for a in axes.flat:
    a.tick_params(labelsize=8.5)
fig.text(0.075, 0.955, "시간 영역", fontsize=9.5, color=C["gray"])
fig.text(0.53, 0.955, "주파수 영역 (스펙트럼)", fontsize=9.5, color=C["gray"])
save(fig, __file__)
