import sys

from scipy.stats import chi2

from figstyle import plt, np, save, C

# 그레인저 인과의 모의실험. X와 Y는 각자 약 32 Hz에서 스펙트럼 봉우리를 갖는 AR(2) 과정이고,
# X가 2 표본(10 ms) 늦게 Y를 민다(결합 세기 c). 표본화 200 Hz, 60 s.
rng = np.random.default_rng(3)
fs, n, p = 200, 12000, 5


def simulate(c, n=n):
    x, y = np.zeros(n), np.zeros(n)
    e = rng.normal(size=(2, n))
    for t in range(2, n):
        x[t] = 0.9 * x[t - 1] - 0.7 * x[t - 2] + e[0, t]
        y[t] = 0.8 * y[t - 1] - 0.6 * y[t - 2] + c * x[t - 2] + e[1, t]
    return x, y


def lagmat(v, p):
    return np.column_stack([v[p - k: len(v) - k] for k in range(1, p + 1)])


def gc(src, dst, p=p):
    # src가 dst의 과거 예측을 얼마나 개선하는가: ln(제한 모형 잔차 분산 / 완전 모형 잔차 분산)
    target = dst[p:]
    own = lagmat(dst, p)
    full = np.column_stack([own, lagmat(src, p)])
    r1 = target - own @ np.linalg.lstsq(own, target, rcond=None)[0]
    r2 = target - full @ np.linalg.lstsq(full, target, rcond=None)[0]
    return np.log(r1.var() / r2.var())


thr = chi2.ppf(0.95, p) / (n - p)
print(f"귀무 95% 문턱 ≈ {thr:.4f}", file=sys.stderr)

cs = np.linspace(0, 0.6, 7)
xy, yx = [], []
for c in cs:
    x, y = simulate(c)
    xy.append(gc(x, y))
    yx.append(gc(y, x))
    print(f"c={c:.1f}: X→Y={xy[-1]:.3f}, Y→X={yx[-1]:.4f}", file=sys.stderr)

# 결합이 전혀 없는 두 소스가 센서에 섞이고 센서마다 다른 잡음이 더해질 때
ms = np.linspace(0, 0.5, 6)
sp_xy, sp_yx = [], []
for m in ms:
    x, y = simulate(0.0)
    x = 3 * x  # X가 Y보다 3배 강한 소스
    s1 = x + m * y + rng.normal(0, 1.0, n)
    s2 = y + m * x + rng.normal(0, 3.0, n)
    sp_xy.append(gc(s1, s2))
    sp_yx.append(gc(s2, s1))
    print(f"혼합 m={m:.1f}: 센서1→2={sp_xy[-1]:.3f}, 2→1={sp_yx[-1]:.3f}", file=sys.stderr)

fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.8), gridspec_kw=dict(width_ratios=[1.15, 1, 1], wspace=0.42))
a = axs[0]
x, y = simulate(0.5, 2000)
t = np.arange(100) / fs * 1000
a.plot(t, x[1000:1100] / x.std() + 4, color=C["blue"], lw=1.0)
a.plot(t, y[1000:1100] / y.std() - 4.5, color=C["purple"], lw=1.0)
a.text(0, 8.6, "X (보내는 쪽)", fontsize=7.8, color=C["blue"])
a.text(0, 0.0, "Y ← Y의 과거 + 0.5·X(t − 10 ms)", fontsize=7.8, color=C["purple"])
a.set_ylim(-9, 10)
a.set_yticks([])
a.spines["left"].set_visible(False)
a.set_xlabel("시간 (ms)")
a.set_title("(가) 결합한 AR 과정", fontsize=9.5)

b = axs[1]
b.plot(cs, xy, "o-", color=C["blue"], ms=3.5, lw=1.4, label="X → Y")
b.plot(cs, yx, "s--", color=C["red"], ms=3.5, lw=1.2, mfc="white", label="Y → X")
b.axhline(thr, color=C["gray"], lw=0.8, ls=":")
b.set_xlabel("실제 결합 세기 c")
b.set_ylabel("그레인저 인과 (ln 비)")
b.legend(fontsize=7.5, loc="upper left")
b.set_title("(나) 방향을 맞게 찾는다", fontsize=9.5)

d = axs[2]
d.plot(ms, sp_xy, "o-", color=C["blue"], ms=3.5, lw=1.4, label="센서 1 → 2")
d.plot(ms, sp_yx, "s--", color=C["red"], ms=3.5, lw=1.2, mfc="white", label="센서 2 → 1")
d.axhline(thr, color=C["gray"], lw=0.8, ls=":")
d.set_xlabel("혼합 비율 m (실제 결합 0)")
d.legend(fontsize=7.5, loc="upper left")
d.set_title("(다) 혼합과 잡음이 만든 가짜", fontsize=9.5)
save(fig, __file__)
