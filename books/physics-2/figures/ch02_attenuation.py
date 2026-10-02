from figstyle import plt, np, save, C

# 물의 질량 감쇠 계수: 콤프턴은 클라인-니시나 식으로 계산하고,
# 광전 효과와 쌍생성은 NIST XCOM 값에 맞춘 근사식을 쓴다(간섭성 산란은 뺐다).
re_ = 2.8179403e-13                     # 고전 전자 반지름 (cm)
Ne = 6.02214e23 * 10 / 18.015           # 물 1 g의 전자 수


def compton(E):                          # E: keV → cm²/g
    k = E / 511.0
    a = (1 + k) / k ** 2 * (2 * (1 + k) / (1 + 2 * k) - np.log(1 + 2 * k) / k)
    b = np.log(1 + 2 * k) / (2 * k) - (1 + 3 * k) / (1 + 2 * k) ** 2
    return 2 * np.pi * re_ ** 2 * (a + b) * Ne


def photo(E):
    return 0.152 * (30 / E) ** 3.2


def pair(E):
    Em = np.array([1022, 1500, 2000, 3000, 5000, 10000])
    v = np.array([1e-7, 1e-4, 4.9e-4, 1.4e-3, 2.6e-3, 5.2e-3])
    out = np.zeros_like(E)
    m = E > 1022
    out[m] = np.exp(np.interp(np.log(E[m]), np.log(Em), np.log(v)))
    return out


E = np.logspace(1, 4, 400)
tot = compton(E) + photo(E) + pair(E)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1.25, 1]))
a1.loglog(E, photo(E), color=C["red"], lw=1.4, ls="--", label="광전 효과")
a1.loglog(E, compton(E), color=C["blue"], lw=1.4, ls="--", label="콤프턴 산란")
m = E > 1100
a1.loglog(E[m], pair(E)[m], color=C["purple"], lw=1.4, ls="--", label="쌍생성")
a1.loglog(E, tot, color=C["ink"], lw=2, label="합")
for e0, lab, up in ((70, "CT\n~70 keV", False), (140, "SPECT\n140 keV", True), (511, "PET\n511 keV", True)):
    mu = compton(np.array([e0]))[0] + photo(np.array([e0]))[0]
    a1.scatter([e0], [mu], color=C["red"], s=20, zorder=4)
    a1.text(e0, mu * (1.5 if up else 0.62), lab, ha="center", va="bottom" if up else "top", fontsize=7.8)
a1.set_xlim(10, 1e4)
a1.set_ylim(1e-3, 10)
a1.set_xticks([10, 100, 1000, 10000])
a1.set_xticklabels(["10 keV", "100 keV", "1 MeV", "10 MeV"])
a1.set_xlabel("광자 에너지")
a1.set_ylabel("물의 질량 감쇠 계수 (cm²/g)")
a1.legend(fontsize=7.6, loc="upper right")
a1.set_title("(가) 에너지에 따라 주인공이 바뀐다", fontsize=9.5)

# (나) 지름 18 cm 물 속 한 점에서 나온 광자가 빠져나갈 확률
L = 18.0
x = np.linspace(0, L, 200)
mu511 = compton(np.array([511.0]))[0]
mu140 = compton(np.array([140.0]))[0] + photo(np.array([140.0]))[0]
a2.plot(x, np.exp(-mu140 * x), color=C["green"], lw=1.7, label="SPECT: 140 keV 광자 하나\n(깊이 = 검출기까지 거리)")
a2.plot(x, np.exp(-mu511 * x), color=C["blue"], lw=1.3, ls="--", label="511 keV 광자 하나")
a2.plot(x, np.exp(-mu511 * L) * np.ones_like(x), color=C["red"], lw=2,
        label="PET: 511 keV 광자 둘 다")
a2.text(9, np.exp(-mu511 * L) - 0.03, f"어디서 나와도 {np.exp(-mu511 * L) * 100:.0f}%", ha="center",
        va="top", fontsize=8, color=C["red"])
a2.set_xlim(0, L)
a2.set_ylim(0, 1.02)
a2.set_xlabel("광원의 깊이 (cm)")
a2.set_ylabel("빠져나갈 확률")
a2.legend(fontsize=7.4, loc="upper right")
a2.set_title("(나) 지름 18 cm 물 머리 모형", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
