from figstyle import plt, np, save, C

# SRTM(기저 함수법)과 참조 로건 도표를 잡음 수준을 바꿔 가며 합성 TAC에 적합한다.
dt = 0.01
t = np.arange(0, 90 + dt, dt)
A1, A2, A3, l1, l2, l3 = 851.1, 21.88, 20.81, 4.134, 0.1191, 0.01043
Cp = np.maximum((A1 * t - A2 - A3) * np.exp(-l1 * t) + A2 * np.exp(-l2 * t) + A3 * np.exp(-l3 * t), 0)


def tcm(K1, k2, k3, k4):
    a, b = np.zeros_like(t), np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (K1 * Cp[i - 1] - (k2 + k3) * a[i - 1] + k4 * b[i - 1])
        b[i] = b[i - 1] + dt * (k3 * a[i - 1] - k4 * b[i - 1])
    return a + b


CT, CR = tcm(0.1, 0.4, 0.24, 0.08), tcm(0.1, 0.4, 0.0, 0.0)
dur = np.array([0.5] * 6 + [1] * 3 + [3] * 3 + [5] * 15)
ends = np.cumsum(dur)
starts, mid = ends - dur, ends - dur / 2
frame = lambda c: np.array([c[(t >= s) & (t < e)].mean() for s, e in zip(starts, ends)])
ct, cr = frame(CT), frame(CR)

# 기저 함수: C_R ⊗ exp(-θt), θ = k2a 후보
thetas = np.geomspace(0.01, 1.0, 120)
basis = np.array([frame(np.convolve(CR, np.exp(-th * t) * dt)[: len(t)]) for th in thetas])
lam = np.log(2) / 20.4                                 # ¹¹C 붕괴 상수 (1/분)
var0 = ct * np.exp(lam * mid) / dur                    # 프레임 분산 ∝ 계수 / 길이
W = 1 / var0


def srtm(Y):
    """Y: (n, 프레임). 가중 최소제곱으로 θ마다 선형 적합하고 잔차가 가장 작은 θ를 고른다."""
    sw = np.sqrt(W)
    best, bp, fit = np.full(len(Y), np.inf), np.zeros(len(Y)), np.zeros_like(Y)
    for th, B in zip(thetas, basis):
        X = np.c_[cr, B]
        beta = np.linalg.lstsq(X * sw[:, None], (Y * sw).T, rcond=None)[0]
        rss = (((Y * sw).T - (X * sw[:, None]) @ beta) ** 2).sum(0)
        m = rss < best
        best[m] = rss[m]
        bp[m] = ((beta[1] + beta[0] * th) / th - 1)[m]
        fit[m] = (X @ beta).T[m]
    return bp, fit


def logan(Y, tstar=30, k2p=0.4):
    ict, icr = np.cumsum(Y * dur, 1), np.cumsum(cr * dur)
    x, y = ((icr + cr / k2p) / Y)[:, mid > tstar], (ict / Y)[:, mid > tstar]
    xm, ym = x.mean(1, keepdims=True), y.mean(1, keepdims=True)
    return ((x - xm) * (y - ym)).sum(1) / ((x - xm) ** 2).sum(1) - 1


rng = np.random.default_rng(1)
sd_unit = np.sqrt(var0) / (np.sqrt(var0[-1]) / ct[-1])   # 마지막 프레임 변동계수가 1이 되는 눈금

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(width_ratios=[1.1, 1]))
y1 = np.maximum(ct + rng.standard_normal(len(ct)) * 0.05 * sd_unit, 0.05)
bp1, fit1 = srtm(y1[None])
a1.errorbar(mid, y1, yerr=0.05 * sd_unit, fmt="o", color=C["blue"], ms=3, lw=0.8, capsize=0,
            label="목표 영역 (ROI 평균, 잡음 5%)")
a1.plot(mid, fit1[0], color=C["red"], lw=1.4, label=f"SRTM 적합, $BP_{{ND}}$ = {bp1[0]:.2f}")
a1.plot(mid, cr, "o-", color=C["green"], ms=2.5, lw=1.1, label="참조 영역 $C_R$")
a1.set_xlim(0, 90)
a1.set_ylim(0, 22)
a1.set_xlabel("주사 뒤 시간 (분)")
a1.set_ylabel("방사능 농도 (상대 단위)")
a1.legend(fontsize=7.4, loc="upper right")
a1.set_title("(가) SRTM 적합 (참값 $BP_{ND}$ = 3)", fontsize=9.5)

levels = np.array([0.02, 0.05, 0.1, 0.2, 0.3, 0.4])
res = {"srtm": [], "logan": []}
for s in levels:
    Y = np.maximum(ct + rng.standard_normal((400, len(ct))) * s * sd_unit, 0.05)
    res["srtm"].append(srtm(Y)[0])
    res["logan"].append(logan(Y))
for k, col, lab, off in [("srtm", C["blue"], "SRTM (기저 함수법)", -0.4), ("logan", C["red"], "참조 로건 도표", 0.4)]:
    m = np.array([v.mean() for v in res[k]])
    sd = np.array([v.std() for v in res[k]])
    xx = levels * 100 + off
    a2.fill_between(xx, m - sd, m + sd, color=col, alpha=0.15, lw=0)
    a2.plot(xx, m, "o-", color=col, ms=3.5, lw=1.4, label=lab)
    print(k, np.round(m, 3), np.round(sd, 3))
a2.axhline(3, color=C["gray"], ls="--", lw=0.8, label="참값 3")
a2.axvspan(15, 42, color=C["light"], alpha=0.6, zorder=0)
a2.text(28.5, 2.3, "복셀 수준 잡음", fontsize=7.6, color=C["gray"], ha="center")
a2.set_xlim(0, 42)
a2.set_ylim(2.2, 3.5)
a2.set_xlabel("마지막 프레임의 잡음 (변동계수, %)")
a2.set_ylabel("추정한 $BP_{ND}$ (평균 ± 표준편차)")
a2.legend(fontsize=7.4, loc="upper left")
a2.set_title("(나) 잡음이 키우는 치우침", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
