from figstyle import plt, np, save, C

dt = 0.05
t = np.arange(-60, 100, dt)  # ms
rng = np.random.default_rng(7)


def ap_current(t, t0):
    """활동전위의 막 전류: 약 1 ms짜리 두 갈래(안쪽 → 바깥쪽) 파형."""
    s = (t - t0) / 0.25
    return -s * np.exp(-0.5 * s ** 2) / 0.6065


def syn_current(t, t0, tr=1.0, td=10.0):
    s = np.clip(t - t0, 0, None)
    y = (np.exp(-s / td) - np.exp(-s / tr)) * (t >= t0)
    tp = np.log(td / tr) * tr * td / (td - tr)
    return y / (np.exp(-tp / td) - np.exp(-tp / tr))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(width_ratios=[1, 1.25]))

# 왼쪽: 사건 하나
a1.plot(t, ap_current(t, 0), color=C["red"], lw=1.5, label="활동전위 (약 1 ms, 양·음이 상쇄)")
a1.plot(t, syn_current(t, 0), color=C["blue"], lw=1.5, label="시냅스 전류 (수–수십 ms)")
a1.axhline(0, color=C["gray"], lw=0.5)
a1.set_xlim(-5, 40)
a1.set_ylim(-1.3, 1.9)
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("막 전류 (봉우리 = 1)")
a1.legend(fontsize=7.5, loc="upper right")
a1.set_title("사건 하나", fontsize=10)

# 오른쪽: 뉴런 1000개, 시점이 표준편차 10 ms로 흩어진 경우
n = 1000
t0 = rng.normal(0, 10, n)
ap = sum(ap_current(t, x) for x in t0)
sy = sum(syn_current(t, x) for x in t0)
a2.plot(t, sy, color=C["blue"], lw=1.5, label=f"시냅스 전류의 합 (최대 {sy.max():.0f})")
a2.plot(t, ap, color=C["red"], lw=1.0, label=f"활동전위 전류의 합 (최대 {np.abs(ap).max():.0f})")
a2.axhline(0, color=C["gray"], lw=0.5)
a2.set_xlim(-40, 80)
a2.set_xlabel("시간 (ms)")
a2.set_ylabel("합 (사건 하나의 봉우리 = 1)")
a2.legend(fontsize=7.5, loc="upper right")
a2.set_title("1000개, 시점이 ±10 ms로 흩어질 때", fontsize=10)
a2.set_ylim(-80, 560)
fig.tight_layout()
save(fig, __file__)
