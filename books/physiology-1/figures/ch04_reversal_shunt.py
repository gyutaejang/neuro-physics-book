from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw=dict(width_ratios=[1, 1.1]))

# 왼쪽: 시냅스 전류의 I–V (전도도 1 nS)
V = np.linspace(-100, 40, 200)
for E, col, lab in [(0, C["blue"], "AMPA, nACh: E ≈ 0 mV"),
                    (-70, C["green"], "GABA-A: E ≈ −70 mV"),
                    (-90, C["purple"], "GIRK K⁺: E ≈ −90 mV")]:
    a1.plot(V, 1.0 * (V - E), color=col, lw=1.6, label=lab)
    a1.scatter([E], [0], color=col, s=18, zorder=4)
a1.axhline(0, color=C["gray"], lw=0.6)
a1.axvline(-70, color=C["gray"], lw=0.6, ls=":")
a1.text(-68, 128, "휴지 −70 mV", fontsize=7.5, color=C["gray"], va="top", ha="left")
a1.annotate("", xy=(-70, -68), xytext=(-70, -2),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.1, mutation_scale=9))
a1.text(-66, -28, "구동력", fontsize=7.5, color=C["red"], va="center", ha="left")
a1.text(-98, 70, "바깥 전류 (+)", fontsize=7.5, color=C["gray"], va="top")
a1.text(-98, -128, "안쪽 전류 (−)", fontsize=7.5, color=C["gray"], va="bottom")
a1.legend(fontsize=7.3, loc="lower right", handlelength=1.4)
a1.set_xlabel("막전위 V (mV)")
a1.set_ylabel("전류 (pA, g = 1 nS)")
a1.set_xlim(-100, 40)
a1.set_ylim(-135, 135)
a1.set_title("I = g (V − E): 역전 전위에서 0", fontsize=10)

# 오른쪽: 단일 구획 모형의 EPSP와 분로 억제
dt = 0.02
t = np.arange(-5, 60, dt)
Cm, gL, EL = 150.0, 10.0, -70.0  # pF, nS, mV  (τ = 15 ms)


def gsyn(t, t0, gmax, tr, td):
    s = np.clip(t - t0, 0, None)
    y = (np.exp(-s / td) - np.exp(-s / tr)) * (t >= t0)
    return gmax * y / y.max()


ge = gsyn(t, 0, 3.0, 0.3, 3.0)
gi = gsyn(t, -1, 30.0, 0.5, 20.0)


def run(ge, gi, Ei):
    v = np.full_like(t, EL)
    for k in range(1, len(t)):
        dv = (-gL * (v[k - 1] - EL) - ge[k] * (v[k - 1] - 0.0) - gi[k] * (v[k - 1] - Ei)) / Cm
        v[k] = v[k - 1] + dt * dv
    return v


z = np.zeros_like(t)
cases = [(run(ge, z, -70), C["blue"], "EPSP만"),
         (run(ge, gi, -70), C["green"], "EPSP + 분로 억제 (E = −70 mV)"),
         (run(z, gi, -70), C["gray"], "억제만 (E = −70 mV): 변화 없음"),
         (run(ge, gi, -80), C["purple"], "EPSP + 과분극 억제 (E = −80 mV)")]
for v, col, lab in cases:
    a2.plot(t, v, color=col, lw=1.6, label=f"{lab}  ({v.max() - EL:+.1f} mV)" if v.max() - EL > 0.05
            else f"{lab}")
a2.set_xlabel("시간 (ms)")
a2.set_ylabel("막전위 (mV)")
a2.set_xlim(-5, 60)
a2.set_ylim(-76.5, -63.5)
a2.legend(fontsize=7.3, loc="upper right", handlelength=1.4)
a2.set_title("전압이 그대로여도 억제는 일어난다", fontsize=10)
fig.tight_layout()
save(fig, __file__)
