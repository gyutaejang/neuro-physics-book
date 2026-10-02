from figstyle import plt, np, save, C

f = np.logspace(-3, 4, 600)
fh, fl = 0.1, 100.0
hp = (f / fh) / np.sqrt(1 + (f / fh) ** 2)
lp = 1 / np.sqrt(1 + (f / fl) ** 2)
db = lambda x: 20 * np.log10(x)

fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.semilogx(f, db(lp), color=C["blue"], ls="--", lw=1, label="저역 통과 (차단 100 Hz)")
ax.semilogx(f, db(hp), color=C["red"], ls="--", lw=1, label="고역 통과 (차단 0.1 Hz)")
ax.semilogx(f, db(hp * lp), color=C["ink"], lw=1.8, label="둘을 이은 대역 통과")
ax.axhline(-3, color=C["gray"], lw=0.6, ls=":")
ax.text(1.2e-3, -2.2, "−3 dB", fontsize=8, color=C["gray"])
for fc in (fh, fl):
    ax.axvline(fc, color=C["gray"], lw=0.6, ls=":")
ax.axvspan(1, 40, color=C["green"], alpha=0.1)
ax.text(6.3, -26, "주요 EEG 리듬\n(약 1–40 Hz)", ha="center", fontsize=8, color=C["green"])
ax.annotate("느린 성분 깎임", xy=(0.012, -18), xytext=(0.03, -32), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.annotate("빠른 잡음 깎임", xy=(1000, -20), xytext=(250, -34), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.set_xlim(1e-3, 1e4)
ax.set_ylim(-42, 5)
ax.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4])
ax.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100", "1000", "10⁴"])
ax.set_xlabel("주파수 (Hz, 로그 눈금)")
ax.set_ylabel("진폭 이득 (dB)")
ax.legend(fontsize=7.5, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=1)
save(fig, __file__)
