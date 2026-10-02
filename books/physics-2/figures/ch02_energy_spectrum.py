from figstyle import plt, np, save, C

# 511 keV 광자를 섬광 결정으로 잰 에너지 스펙트럼의 몬테카를로 모의.
# 결정 안 콤프턴 산란 뒤 빠져나간 광자는 연속 부분을, 환자 몸 안에서 이미
# 한 번 산란한 광자는 낮은 에너지 쪽 봉우리를 만든다.
rng = np.random.default_rng(3)
me = 511.0


def kn_dsdcos(E, c):                     # 클라인-니시나 dσ/dcosθ (상대값)
    r = 1 / (1 + E / me * (1 - c))
    return r ** 2 * (r + 1 / r - (1 - c ** 2))


def sample_cos(E):
    """광자마다(E는 배열) 클라인-니시나 분포에서 산란각 cosθ를 뽑는다(기각 표본)."""
    c = np.empty(E.size)
    todo = np.arange(E.size)
    while todo.size:
        t = rng.uniform(-1, 1, todo.size)
        ok = rng.uniform(0, 2.0, todo.size) < kn_dsdcos(E[todo], t)
        c[todo[ok]] = t[ok]
        todo = todo[~ok]
    return c


def deposit(E, p_peak=0.6):
    """결정에 남긴 에너지: p_peak 비율은 전부, 나머지는 콤프턴 전자 몫만."""
    full = rng.uniform(size=E.size) < p_peak
    Eg = E / (1 + E / me * (1 - sample_cos(E)))
    return np.where(full, E, E - Eg)


n_true, n_scat = 140000, 60000           # 검출된 광자의 약 30%가 환자 안에서 산란했다고 둔다
c = sample_cos(np.full(4 * n_scat, me))
c = c[c > 0.2][:n_scat]                  # 크게 꺾인 광자는 대개 검출기 고리를 벗어난다고 본다
E_s = me / (2 - c)                       # 환자 안에서 산란한 뒤의 광자 에너지
dep_t = deposit(np.full(n_true, me))
dep_s = deposit(E_s)

hi = 650
bins = np.arange(0, 750, 5)
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2), sharey=True)
for ax, (name, fw, lo) in zip(axes, (("LYSO", 0.11, 425), ("BGO", 0.22, 350))):
    def blur(d):
        sig = fw / 2.355 * np.sqrt(d * me)          # 분해능은 √E에 비례해 넓어진다
        return d + rng.normal(0, 1, d.size) * sig
    bt, bs = blur(dep_t), blur(dep_s)
    ht, _ = np.histogram(bt, bins)
    hs, _ = np.histogram(bs, bins)
    x = bins[:-1] + 2.5
    norm = (ht + hs).max()
    ax.axvspan(lo, hi, color=C["light"], zorder=0)
    ax.plot(x, (ht + hs) / norm, color=C["ink"], lw=1.6, label="측정 스펙트럼")
    ax.plot(x, ht / norm, color=C["blue"], lw=1.1, ls="--", label="산란 없이 온 광자")
    ax.plot(x, hs / norm, color=C["red"], lw=1.1, ls="--", label="환자 안에서 산란한 광자")
    acc_t = np.mean((bt > lo) & (bt < hi))
    acc_s = np.mean((bs > lo) & (bs < hi))
    sf = acc_s * n_scat / (acc_s * n_scat + acc_t * n_true)
    ax.set_title(f"{name}: 511 keV에서 FWHM {fw * 100:.0f}%", fontsize=9.5)
    ax.text((lo + hi) / 2, 1.13, f"창 {lo}–{hi} keV", ha="center", fontsize=8, color=C["blue"])
    ax.text(20, 0.72, f"창 안의 산란 비율\n약 {sf * 100:.0f}%", fontsize=8, color=C["red"], va="top")
    ax.set_xlim(0, 750)
    ax.set_ylim(0, 1.22)
    ax.set_xlabel("결정에 남긴 에너지 (keV)")
    print(name, "window scatter fraction", round(sf, 3))
axes[0].annotate("콤프턴 가장자리\n341 keV", xy=(341, 0.2), xytext=(150, 0.4), fontsize=8,
                 arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
axes[0].set_ylabel("상대 개수")
axes[1].legend(fontsize=7.6, loc="upper left", bbox_to_anchor=(0.0, 1.0))
fig.tight_layout()
save(fig, __file__)
