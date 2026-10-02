from figstyle import plt, np, save, C

f = np.linspace(1, 45, 400)
rng = np.random.default_rng(1)
power = 40 / f ** 1.2 + 3.0 * np.exp(-0.5 * ((f - 10) / 1.3) ** 2) + 0.15 * np.exp(-0.5 * ((f - 20) / 2) ** 2)
power *= np.exp(rng.normal(0, 0.05, f.size))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
a1.plot(f, power, color=C["blue"])
a1.set_title("선형 눈금")
a1.set_xlabel("주파수 (Hz)")
a1.set_ylabel("파워 (μV²/Hz)")
a1.annotate("알파 봉우리", xy=(10, 7.4), xytext=(22, 15), fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a1.annotate("20 Hz 성분은\n바닥에 묻힌다", xy=(20, 1.2), xytext=(25, 7), fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.semilogy(f, power, color=C["blue"])
a2.set_title("세로축 로그 눈금")
a2.set_xlabel("주파수 (Hz)")
a2.annotate("베타 성분이 보인다", xy=(20, 1.5), xytext=(24, 6), fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
fig.tight_layout()
save(fig, __file__)
