from figstyle import plt, np, save, C

T2s = 40e-3      # 회백질 T2* 어림 (3 T, 6장)
df = 50.0        # 기준 주파수와의 차이 (Hz)
fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.1, 0.95])
ax1, ax2, ax3 = [fig.add_subplot(gs[0, i]) for i in range(3)]

# (가) 코일에 걸리는 실제 전압: 128 MHz 진동 (그림에서는 진동 수를 크게 줄였다)
t = np.linspace(0, 0.12, 6000)
env = np.exp(-t / T2s)
ax1.plot(t * 1e3, env * np.cos(2 * np.pi * 250 * t), color=C["gray"], lw=0.6)
ax1.plot(t * 1e3, env, color=C["ink"], lw=1.2, ls="--")
ax1.plot(t * 1e3, -env, color=C["ink"], lw=1.2, ls="--")
ax1.text(45, 0.62, "포락선 $e^{-t/T_2^*}$", fontsize=8.5)
ax1.text(60, -0.85, "실제 진동은 128 MHz\n(1 ms에 약 13만 번)", fontsize=8, color=C["gray"], ha="center")
ax1.set_xlim(0, 120)
ax1.set_ylim(-1.1, 1.1)
ax1.set_yticks([-1, 0, 1])
ax1.set_xlabel("시간 (ms)")
ax1.set_ylabel("신호 (상대)")
ax1.set_title("(가) 코일의 원래 신호", fontsize=10.5)

# (나) 직교 검출 후 복소 신호: 실수부와 허수부
s = np.exp(-t / T2s) * np.exp(2j * np.pi * df * t)
ax2.plot(t * 1e3, s.real, color=C["blue"], lw=1.8, label="실수부")
ax2.plot(t * 1e3, s.imag, color=C["red"], lw=1.6, ls="--", label="허수부")
ax2.plot(t * 1e3, np.abs(s), color=C["ink"], lw=1.2, label="크기 |s|")
ax2.axhline(0, color=C["gray"], lw=0.6)
ax2.set_xlim(0, 120)
ax2.set_ylim(-1.1, 1.35)
ax2.set_yticks([-1, 0, 1])
ax2.set_xlabel("시간 (ms)")
ax2.legend(loc="upper right", fontsize=7.8, ncol=3, handlelength=1.5, columnspacing=0.8)
ax2.set_title(f"(나) 복조 뒤: Δf = {df:.0f} Hz", fontsize=10.5)

# (다) 복소 평면에서 본 같은 신호: 안으로 감기는 나선
ax3.plot(s.real, s.imag, color=C["purple"], lw=1.4)
for tm, off, ha, va in [(0, (0.0, 0.1), "center", "bottom"), (5e-3, (0.1, 0.05), "left", "bottom"),
                        (10e-3, (0.0, -0.12), "center", "top")]:
    v = np.exp(-tm / T2s) * np.exp(2j * np.pi * df * tm)
    ax3.plot([0, v.real], [0, v.imag], color=C["red"], lw=1)
    ax3.plot([v.real], [v.imag], "o", color=C["red"], ms=3.5)
    ax3.text(v.real + off[0], v.imag + off[1], f"{tm * 1e3:.0f} ms", fontsize=7.8, ha=ha, va=va,
             color=C["red"], bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.9), zorder=5)
ax3.axhline(0, color=C["gray"], lw=0.6)
ax3.axvline(0, color=C["gray"], lw=0.6)
ax3.set_xlim(-1.05, 1.25)
ax3.set_ylim(-1.05, 1.15)
ax3.set_aspect("equal")
ax3.set_xlabel("실수부")
ax3.set_ylabel("허수부", labelpad=1)
ax3.set_xticks([-1, 0, 1])
ax3.set_yticks([-1, 0, 1])
ax3.set_title("(다) 복소 평면에서", fontsize=10.5)
fig.tight_layout(w_pad=1.2)
save(fig, __file__)
