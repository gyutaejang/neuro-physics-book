from figstyle import plt, np, save, C

# 몬테카를로: 두 벽 사이(간격 L)에 갇힌 물과 자유로운 물의 확산 신호.
# 펄스 경사 스핀 에코(유효 경사 +G, -G), 신호 = |<exp(i φ)>|.
gam = 2.675e8
rng = np.random.default_rng(7)
dt = 5e-5
N = 4000


def signal(D0, delta, Delta, Gs, L=None):
    T = Delta + delta
    nt = int(round(T / dt))
    t = (np.arange(nt) + 0.5) * dt
    w = np.where(t < delta, 1.0, 0.0) - np.where((t >= Delta) & (t < Delta + delta), 1.0, 0.0)
    x = rng.uniform(0, L, N) if L else np.zeros(N)
    acc = np.zeros(N)                     # ∫ w(t) x(t) dt
    s = np.sqrt(2 * D0 * dt)
    for k in range(nt):
        x = x + rng.normal(0, s, N)
        if L:
            x = np.abs(x)
            x = np.where(x > L, 2 * L - x, x)
        acc += w[k] * x * dt
    return np.array([abs(np.mean(np.exp(1j * gam * G * acc))) for G in Gs])


def bval(G, delta, Delta):
    return gam ** 2 * G ** 2 * delta ** 2 * (Delta - delta / 3) * 1e-6   # s/mm²


delta, Delta = 20e-3, 30e-3
bs = np.linspace(0, 3000, 13)
Gs = np.sqrt(bs * 1e6 / (gam ** 2 * delta ** 2 * (Delta - delta / 3)))
D0 = 2.0e-9                              # 축삭 안 물의 고유 확산계수 (가정)
S10 = signal(D0, delta, Delta, Gs, L=10e-6)
S5 = signal(D0, delta, Delta, Gs, L=5e-6)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1))
bb = np.linspace(0, 3000, 200)
a1.semilogy(bb, np.exp(-bb * 3.0e-3), color=C["blue"], lw=1.8)
a1.semilogy(bb, np.exp(-bb * 0.8e-3), color=C["gray"], lw=1.8)
a1.semilogy(bs, S10, "o-", color=C["red"], ms=3.5, lw=1.4)
a1.semilogy(bs, S5, "s--", color=C["red"], ms=3, lw=1.0, alpha=0.7)
a1.text(1750, 0.0085, "자유 물 (37 °C)\nD = 3.0", color=C["blue"], fontsize=8)
a1.text(1900, 0.062, "장애 확산\nADC = 0.8", color=C["gray"], fontsize=8)
a1.text(1200, 1.18, "벽 사이 5 μm에 갇힌 물", color=C["red"], fontsize=8)
a1.text(1600, 0.43, "벽 사이 10 μm", color=C["red"], fontsize=8)
a1.set_ylim(5e-3, 1.9)
a1.set_xlabel("b (s/mm²)")
a1.set_ylabel("신호 $S/S_0$ (로그 눈금)")
a1.set_title("(가) b에 따른 신호 감쇠", fontsize=9.5)

# (나) 확산 시간에 따른 겉보기 확산계수 (b = 1000에서)
Deltas = np.array([22, 30, 40, 55, 80]) * 1e-3
adc = {}
for L in (15e-6, 10e-6):
    adc[L] = []
    for Dl in Deltas:
        G = np.sqrt(1000e6 / (gam ** 2 * delta ** 2 * (Dl - delta / 3)))
        adc[L].append(-np.log(signal(D0, delta, Dl, [G], L=L)[0]) / 1000 * 1e3)
td = (Deltas - delta / 3) * 1e3
a2.axhline(2.0, color=C["blue"], lw=1.8)
a2.plot(td, adc[15e-6], "o-", color=C["red"], ms=4, lw=1.4)
a2.plot(td, adc[10e-6], "s--", color=C["red"], ms=3, lw=1.0, alpha=0.7)
a2.text(td[-1] + 2, adc[15e-6][-1] + 0.03, "15 μm", color=C["red"], fontsize=8)
a2.text(td[-1] + 2, adc[10e-6][-1] - 0.04, "10 μm", color=C["red"], fontsize=8)
a2.set_xlim(10, 88)
a2.text(td[0], 2.08, "자유 확산: 시간과 무관 (D = 2.0)", color=C["blue"], fontsize=8)
a2.text(td[0], 1.0, "벽 사이에 갇힌 물:\n오래 볼수록 ADC가 작아진다", color=C["red"], fontsize=8)
a2.set_ylim(0, 2.3)
a2.set_xlabel("확산 시간 Δ − δ/3 (ms)")
a2.set_ylabel("겉보기 확산계수 (10⁻³ mm²/s)")
a2.set_title("(나) 확산 시간과 ADC", fontsize=9.5)
fig.tight_layout(w_pad=2.0)
save(fig, __file__)
