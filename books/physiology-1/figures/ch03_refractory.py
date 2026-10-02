from figstyle import plt, np, save, C

# 호지킨-헉슬리 모형(18.5 °C)에서 두 번째 자극의 문턱이 첫 활동전위 뒤 시간에 따라 어떻게 변하는지 계산한다.
PHI = 3 ** ((18.5 - 6.3) / 10)
DT = 0.005
DUR = 0.3   # 자극 길이 (ms)


def rates(V):
    am = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10)); bm = 4 * np.exp(-(V + 65) / 18)
    ah = 0.07 * np.exp(-(V + 65) / 20); bh = 1 / (1 + np.exp(-(V + 35) / 10))
    an = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10)); bn = 0.125 * np.exp(-(V + 65) / 80)
    return am, bm, ah, bh, an, bn


def sim(pulses, tmax):
    """pulses: [(시작, 세기 μA/cm²)]. 세기는 배열이어도 된다(여러 조건을 한꺼번에)."""
    t = np.arange(0, tmax, DT)
    shape = np.broadcast(*[np.asarray(a) for _, a in pulses]).shape
    V = np.full(shape, -65.0)
    am, bm, ah, bh, an, bn = rates(V)
    m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
    out = np.zeros((len(t),) + shape)
    for i, tt in enumerate(t):
        I = sum(np.asarray(a) * (s <= tt < s + DUR) for s, a in pulses)
        am, bm, ah, bh, an, bn = rates(V)
        m = m + DT * PHI * (am * (1 - m) - bm * m)
        h = h + DT * PHI * (ah * (1 - h) - bh * h)
        n = n + DT * PHI * (an * (1 - n) - bn * n)
        V = V + DT * (I - 120 * m ** 3 * h * (V - 50) - 36 * n ** 4 * (V + 77) - 0.3 * (V + 54.387))
        out[i] = V
    return t, out


def fired_after(t, V, s):
    i = np.searchsorted(t, s)
    seg = V[i:]
    return ((seg[:-1] < 0) & (seg[1:] >= 0)).any(axis=0)


def threshold(first, s):
    """첫 자극 뒤 s ms에 준 두 번째 자극의 문턱 세기. 이분법을 여러 후보에 한꺼번에 적용한다."""
    lo, hi = 0.0, 6000.0
    pre = [(1.0, first)] if first else []
    t, V = sim(pre + [(s, np.array(hi))], s + 4)
    if not fired_after(t, V, s):
        return np.nan
    for _ in range(4):   # 한 번에 8등분하는 이분법
        cand = np.linspace(lo, hi, 9)[1:]
        t, V = sim(pre + [(s, cand)], s + 4)
        ok = fired_after(t, V, s)
        k = np.argmax(ok)
        hi, lo = cand[k], (cand[k - 1] if k > 0 else lo)
    return hi


base = threshold(0, 1.0)
isis = np.array([1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 14.0])
ratio = np.array([threshold(3 * base, 1.0 + d) / base for d in isis])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.0), gridspec_kw={"width_ratios": [1, 1.1]})

# (가) 3 ms 뒤 두 번째 자극: 평소 문턱의 1.2배는 실패, 3배는 성공(작은 활동전위)
t, V = sim([(1.0, 3 * base), (4.0, np.array([1.2 * base, 3.0 * base]))], 9)
a1.plot(t, V[:, 1], color=C["blue"], lw=1.6, label="두 번째 자극 = 문턱의 3배")
a1.plot(t, V[:, 0], color=C["gray"], lw=1.4, ls="--", label="두 번째 자극 = 문턱의 1.2배")
a1.set_xlabel("시간 (ms)")
a1.set_ylabel("막전위 (mV)")
a1.set_ylim(-85, 60)
a1.set_yticks([-60, -30, 0, 30])
a1.set_yticklabels(["−60", "−30", "0", "30"])
a1.legend(fontsize=7.5, loc="upper right")
for s in (1.0, 4.0):
    a1.axvspan(s, s + DUR, color=C["gray"], alpha=0.15, lw=0)
a1.set_title("(가) 3 ms 간격의 두 자극", fontsize=10)

# (나) 문턱 곡선
a2.axvspan(0, 1.1, color=C["red"], alpha=0.15, lw=0)
a2.axvspan(1.1, 4.8, color=C["red"], alpha=0.06, lw=0)
a2.semilogy(isis, ratio, "o-", color=C["blue"], ms=3.5, lw=1.5)
a2.axhline(1, color=C["gray"], lw=0.6, ls=":")
a2.text(0.55, 12, "절대 불응기", ha="center", va="center", fontsize=8, color=C["red"], rotation=90)
a2.text(2.9, 40, "상대 불응기", ha="center", fontsize=8, color=C["red"])
a2.set_xlim(0, 14.5)
a2.set_ylim(0.6, 150)
a2.set_yticks([1, 3, 10, 30, 100])
a2.set_yticklabels(["1", "3", "10", "30", "100"])
a2.minorticks_off()
a2.set_xlabel("첫 자극 뒤 시간 (ms)")
a2.set_ylabel("두 번째 자극 문턱 (평소의 배수)")
a2.set_title("(나) 문턱이 회복되는 과정", fontsize=10)
fig.tight_layout()
save(fig, __file__)
print("ratios", dict(zip(isis, np.round(ratio, 2))))
