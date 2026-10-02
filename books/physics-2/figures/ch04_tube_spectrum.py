from figstyle import plt, np, C, save

# X선관 스펙트럼: 크라머스 제동 복사 + 텅스텐 K 특성선 + 알루미늄 여과.
# 알루미늄 질량 감쇠 계수(NIST XCOM 근삿값, cm²/g)
E_T = np.array([10, 15, 20, 30, 40, 50, 60, 80, 100, 150.])
AL = np.array([26.23, 7.955, 3.441, 1.128, 0.5685, 0.3681, 0.2778, 0.2018, 0.1704, 0.1378])


def mu_al(E):
    return np.exp(np.interp(np.log(E), np.log(E_T), np.log(AL))) * 2.699  # 1/cm


dE = 0.25
LINES = [(58.0, 0.6), (59.3, 1.0), (67.2, 0.35)]  # Kα2, Kα1, Kβ (keV, 상대 세기)


def spectrum(kvp, al_mm=7.0, lines=True):
    E = np.arange(10, kvp + dE / 2, dE)
    N = (kvp - E) / E                          # 광자 수 / keV (크라머스)
    if lines and kvp > 69.5:                   # 텅스텐 K 껍질 결합 에너지 69.5 keV
        for e0, w in LINES:
            N = N + 0.35 * w * (kvp - 69.5) / 50 * np.exp(-0.5 * ((E - e0) / 0.35) ** 2)
    filt = np.exp(-mu_al(E) * al_mm / 10)
    return E, N, N * filt


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
ax = axes[0]
E, N0, N1 = spectrum(120)
s = 1 / N1.max()
ax.plot(E, N0 * s, color=C["gray"], lw=1.2, ls="--", label="여과 전")
ax.fill_between(E, N1 * s, color=C["light"])
ax.plot(E, N1 * s, color=C["blue"], lw=1.6, label="알루미늄 7 mm 여과 뒤")
ax.set_ylim(0, 1.25)
ax.set_xlim(0, 125)
iα = np.argmin(abs(E - 59.3)); iβ = np.argmin(abs(E - 67.2))
ax.annotate("Kα", xy=(59.3, N1[iα] * s), xytext=(40, 1.0), fontsize=9, color=C["red"],
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.7))
ax.annotate("Kβ", xy=(67.4, N1[iβ] * s), xytext=(80, 0.78), fontsize=9, color=C["red"],
            arrowprops=dict(arrowstyle="-", color=C["red"], lw=0.7))
ax.annotate("최대 120 keV\n(= 관전압)", xy=(120, 0), xytext=(103, 0.4), fontsize=8.5,
            ha="center", arrowprops=dict(arrowstyle="->", color=C["ink"], lw=0.7))
ax.set_xlabel("광자 에너지 (keV)")
ax.set_ylabel("광자 수 (상대값)")
ax.set_title("(가) 120 kVp 스펙트럼", fontsize=10.5)
ax.legend(loc="upper right", fontsize=8.5, bbox_to_anchor=(1.10, 1.02), handlelength=1.6)

ax = axes[1]
shades = [0.35, 0.55, 0.78, 1.0]
ref = spectrum(140)[2].max()
for kvp, a in zip([80, 100, 120, 140], shades):
    E, _, N1 = spectrum(kvp)
    m = (E * N1).sum() / N1.sum()
    ax.plot(E, N1 / ref, color=C["blue"], alpha=a, lw=1.5)
    ax.text(kvp + 1, 0.04, f"{kvp}", fontsize=8.5, color=C["blue"], ha="left")
    print(kvp, "kVp 평균 에너지", round(m, 1), "keV")
    yk = np.interp(m, E, N1 / ref)
    ax.plot([m], [yk], "o", ms=4, color=C["red"])
ax.text(40, 1.08, "● 평균 에너지: 47, 53, 59, 64 keV", fontsize=8.5, color=C["red"])
ax.set_xlim(0, 150)
ax.set_ylim(0, 1.18)
ax.set_xlabel("광자 에너지 (keV)")
ax.set_title("(나) 관전압을 올리면 (같은 mAs)", fontsize=10.5)
ax.set_yticks([0, 0.5, 1.0])
fig.tight_layout()
save(fig, __file__)
