from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
N, jitter = 1000, 5.0                      # 뉴런 수, 시작 시각의 흩어짐(표준편차, ms)
t = np.arange(-40, 80, 0.02)


def spike(tt):          # 세포 밖에서 본 활동전위: 약 1 ms의 양상(두 갈래) 파형
    s = 0.25
    return -tt / s * np.exp(-0.5 * (tt / s) ** 2) / np.exp(-0.5)


def syn(tt):            # 시냅스 후 전위: 알파 함수, 시간 상수 10 ms
    tau = 10.0
    x = np.clip(tt, 0, None) / tau
    return x * np.exp(1 - x)


t0 = rng.normal(0, jitter, N)
sum_sp = sum(spike(t - s) for s in t0) / N
sum_sy = sum(syn(t - s) for s in t0) / N
r_sp, r_sy = np.abs(sum_sp).max(), sum_sy.max()
print("summed / perfect  spike", round(r_sp, 3), "synaptic", round(r_sy, 3))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.0), gridspec_kw={"width_ratios": [1.15, 1]})
a1.plot(t, syn(t), color=C["blue"], lw=0.9, ls=":")
a1.plot(t, spike(t), color=C["red"], lw=0.9, ls=":")
a1.plot(t, sum_sy, color=C["blue"], lw=2, label=f"시냅스 전위 1000개 합: {r_sy * 100:.0f}% 남음")
a1.plot(t, sum_sp, color=C["red"], lw=2, label=f"활동전위 1000개 합: {r_sp * 100:.0f}% 남음")
a1.axhline(0, color=C["gray"], lw=0.5)
a1.set_xlim(-25, 60)
a1.set_ylim(-1.15, 1.6)
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("크기 (하나의 최댓값 = 1)")
a1.legend(fontsize=7.5, loc="upper right")
a1.text(14, -0.95, "점선: 뉴런 하나\n시작 시각 표준편차 5 ms", fontsize=7.5, color=C["gray"])
a1.set_title("(가) 시간: 짧은 신호는 합쳐지지 않는다", fontsize=10)

r = np.logspace(-1, np.log10(30), 100)    # mm
a2.loglog(r, (0.1 / r) ** 2, color=C["blue"], lw=2, label="쌍극자 (시냅스 전류): 1/r²")
a2.loglog(r, (0.1 / r) ** 3, color=C["red"], lw=2, label="사극자 (활동전위): 1/r³")
a2.axvspan(10, 30, color=C["gray"], alpha=0.15, lw=0)
a2.text(17, 3e-1, "두피까지\n거리", ha="center", va="top", fontsize=7.5, color=C["gray"])
a2.set_xlabel("발생원에서의 거리 r (mm)")
a2.set_ylabel("전위 (0.1 mm에서 = 1)")
a2.set_xticks([0.1, 1, 10])
a2.set_xticklabels(["0.1", "1", "10"])
a2.set_yticks([1, 1e-2, 1e-4, 1e-6, 1e-8])
a2.set_yticklabels(["1", "10⁻²", "10⁻⁴", "10⁻⁶", "10⁻⁸"])
a2.minorticks_off()
a2.set_ylim(1e-8, 2)
a2.legend(fontsize=7.5, loc="lower left")
a2.set_title("(나) 공간: 사극자는 더 빨리 줄어든다", fontsize=10)
fig.tight_layout()
save(fig, __file__)
