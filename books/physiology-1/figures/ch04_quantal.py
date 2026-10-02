from figstyle import plt, np, save, C
from math import factorial

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.0), gridspec_kw=dict(width_ratios=[1.3, 1]))

# 왼쪽: 낮은 Ca²⁺에서 유발 반응 진폭 분포 (푸아송, m = 1.4, q = 0.4 mV)
m, q, sq, sn = 1.4, 0.4, 0.07, 0.035
x = np.linspace(-0.2, 2.4, 800)
tot = np.zeros_like(x)
for k in range(0, 7):
    pk = np.exp(-m) * m ** k / factorial(k)
    s = np.sqrt(sn ** 2 + k * sq ** 2)
    g = pk * np.exp(-0.5 * ((x - k * q) / s) ** 2) / (s * np.sqrt(2 * np.pi))
    tot += g
a1.fill_between(x, tot, color=C["blue"], alpha=0.25, lw=0)
a1.plot(x, tot, color=C["blue"], lw=1.4)
for k, lab in [(0, "실패\n(0개)"), (1, "1개"), (2, "2개"), (3, "3개")]:
    a1.axvline(k * q, color=C["gray"], lw=0.6, ls=":")
    pk = np.exp(-m) * m ** k / factorial(k)
    a1.text(k * q, tot.max() * 1.08, lab, ha="center", va="bottom", fontsize=8)
a1.set_xlabel("유발 EPP 진폭 (mV)")
a1.set_ylabel("빈도 (상대값)")
a1.set_yticks([])
a1.set_ylim(0, tot.max() * 1.45)
a1.set_xlim(-0.2, 2.0)
a1.text(1.95, tot.max() * 0.55, "봉우리 간격 q ≈ 0.4 mV\n= 자발 미니 EPP 하나의 크기\n\n실패 비율 $e^{-m}$ ≈ 25 %\n→ 평균 양자 수 m ≈ 1.4",
        ha="right", va="center", fontsize=8)
a1.set_title("양자 방출: 진폭이 계단처럼 나뉜다", fontsize=10)

# 오른쪽: 세포 밖 Ca²⁺와 방출량 (4제곱 협동성)
ca = np.logspace(np.log10(0.1), np.log10(10), 300)
K = 5.0
rel = ca ** 4 / (ca ** 4 + K ** 4)
rel = rel / (2 ** 4 / (2 ** 4 + K ** 4))  # 2 mM에서 1
a2.loglog(ca, rel, color=C["green"], lw=1.7)
ref = (ca / 2) ** 4
a2.loglog(ca[ca < 1.6], ref[ca < 1.6], color=C["gray"], lw=0.8, ls="--")
for c0, lab, dy in [(2, "2 mM", 1.4), (1, "1 mM", 1.4)]:
    r0 = c0 ** 4 / (c0 ** 4 + K ** 4) / (2 ** 4 / (2 ** 4 + K ** 4))
    a2.scatter([c0], [r0], color=C["red"], s=20, zorder=4)
    a2.annotate(f"{lab}: {r0:.2f}" if c0 == 1 else f"{lab}: 1", xy=(c0, r0), xytext=(c0 * 0.22, r0 * 2.2),
                fontsize=8, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.5))
a2.text(1.6, 2e-3, "낮은 농도에서\n기울기 ≈ 4\n(Ca²⁺ 2배 →\n방출 약 16배)", fontsize=8, color=C["gray"], va="center")
a2.set_xlabel("세포 밖 Ca²⁺ (mM)")
a2.set_ylabel("방출량 (2 mM = 1)")
a2.set_ylim(1e-4, 30)
a2.set_title("Ca²⁺ 협동성", fontsize=10)
fig.tight_layout()
save(fig, __file__)
