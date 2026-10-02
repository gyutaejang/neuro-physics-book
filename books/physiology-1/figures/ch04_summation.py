from figstyle import plt, np, save, C

dt = 0.02
t = np.arange(-5, 170, dt)
Cm, gL, EL = 150.0, 10.0, -70.0  # pF, nS, mV (τ = 15 ms)


def gsyn(t0, gmax, tr=0.3, td=3.0):
    s = np.clip(t - t0, 0, None)
    y = (np.exp(-s / td) - np.exp(-s / tr)) * (t >= t0)
    y0 = np.exp(-np.log(td / tr) * tr / (td - tr)) - np.exp(-np.log(td / tr) * td / (td - tr))
    return gmax * y / y0


def run(ge):
    v = np.full_like(t, EL)
    for k in range(1, len(t)):
        v[k] = v[k - 1] + dt * (-gL * (v[k - 1] - EL) - ge[k] * v[k - 1]) / Cm
    return v


g1 = 0.43  # nS: 하나가 약 0.5 mV EPSP

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[1.2, 1]))

# 왼쪽: 시간 합산 — 같은 시냅스에 10번, 간격 5 ms 대 25 ms
for isi, col in [(20, C["gray"]), (10, C["green"]), (4, C["blue"])]:
    ge = sum(gsyn(k * isi, g1 * 3) for k in range(8))
    v = run(ge)
    a1.plot(t, v, color=col, lw=1.5, label=f"간격 {isi} ms ({1000 // isi} Hz)")
a1.set_xlim(-5, 170)
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("막전위 (mV)")
a1.legend(fontsize=7.8, loc="upper right")
a1.set_title("시간 합산: 입력 8번 (하나에 약 1.5 mV)", fontsize=10)

# 오른쪽: 공간 합산 — N개가 동시에
Ns = np.arange(1, 61)
peaks = []
for n in Ns:
    peaks.append(run(gsyn(0, g1 * n)).max() - EL)
peaks = np.array(peaks)
one = peaks[0]
a2.plot(Ns, one * Ns, color=C["gray"], lw=1.0, ls="--", label=f"선형 합 ({one:.2f} mV × N)")
a2.plot(Ns, peaks, color=C["blue"], lw=1.7, label="전도도 모형")
a2.axhline(15, color=C["red"], lw=0.8, ls=":")
a2.text(59, 14.2, "문턱까지 약 15 mV\n(−70 → −55 mV)", fontsize=7.8, color=C["red"], ha="right", va="top")
nthr = Ns[np.argmax(peaks >= 15)]
a2.scatter([nthr], [15], color=C["red"], s=20, zorder=4)
a2.annotate(f"N ≈ {nthr}", xy=(nthr, 15), xytext=(nthr - 12, 19), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_xlabel("동시에 들어온 입력 수 N")
a2.set_ylabel("EPSP 봉우리 (mV)")
a2.set_ylim(0, 28)
a2.set_xlim(0, 60)
a2.legend(fontsize=7.8, loc="upper left", bbox_to_anchor=(0, 0.93))
a2.set_title("공간 합산", fontsize=10)
fig.tight_layout()
save(fig, __file__)
