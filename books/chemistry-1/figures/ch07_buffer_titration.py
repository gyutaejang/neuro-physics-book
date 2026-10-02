from figstyle import plt, np, save, C

KW = 1e-14


def solve_ph(net_base_M, ct_M=0.0, pka=6.8):
    """전하 균형 [H⁺] + (강염기 − 강산) = [A⁻] + [OH⁻]를 이분법으로 푼다 (log[H⁺] 기준)."""
    ka = 10 ** -pka

    def f(lh):
        h = 10 ** lh
        return h + net_base_M - ct_M * ka / (ka + h) - KW / h

    lo, hi = -14.0, 0.5  # f(lo) < 0, f(hi) > 0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return -0.5 * (lo + hi)


# 완충액: 인산 20 mM, HA 10 mM + A⁻ 10 mM (pH = pKa = 6.8)에서 출발한다.
# 짝염기 10 mM은 강염기 10 mM을 넣은 것과 같으므로 net_base = 10 mM + 넣은 양.
added = np.linspace(-15, 15, 401)  # mM, 음수는 강산
buf = [solve_ph((10 + x) * 1e-3, 20e-3) for x in added]
# 물은 pH 7에서 출발 (37 °C의 Kw 차이는 무시한다)
wat = [solve_ph(x * 1e-3) for x in added]

fig, ax = plt.subplots(figsize=(6.4, 3.3))
ax.axhspan(5.8, 7.8, color=C["blue"], alpha=0.08, lw=0)
ax.text(-14.6, 7.95, "완충 범위 pKa ± 1", fontsize=8.5, color=C["blue"], va="bottom")
ax.plot(added, wat, color=C["gray"], lw=1.6, label="순수한 물")
ax.plot(added, buf, color=C["blue"], lw=2, label="인산 완충액 20 mM (pKa 6.8)")
ax.axvline(0, color=C["gray"], lw=0.6, ls=":")
pb, pw = solve_ph(8e-3, 20e-3), solve_ph(-2e-3)
ax.scatter([-2, -2], [pb, pw], color=C["red"], s=20, zorder=5)
ax.annotate(f"강산 2 mM → 완충액 pH {pb:.2f}", xy=(-2, pb), xytext=(-14.6, 10.2),
            fontsize=8, color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.7))
ax.annotate(f"강산 2 mM → 물 pH {pw:.1f}", xy=(-2, pw), xytext=(1.5, 3.2),
            fontsize=8, color=C["red"], arrowprops=dict(arrowstyle="->", color=C["red"], lw=0.7))
ax.set_xlabel("넣은 강산(−) 또는 강염기(+)의 농도 (mM)")
ax.set_ylabel("pH")
ax.set_xlim(-15, 15)
ax.set_ylim(1, 13)
ax.set_xticks([-15, -10, -5, 0, 5, 10, 15])
ax.set_xticklabels(["−15", "−10", "−5", "0", "5", "10", "15"])
ax.legend(fontsize=8, loc="lower right")
save(fig, __file__)
