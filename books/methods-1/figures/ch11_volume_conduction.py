import sys

from scipy.signal import butter, sosfiltfilt

from figstyle import plt, np, save, C

# 체적 전도의 모의실험. 알파 대역(8–12 Hz) 소스를 두 센서에 섞거나(지연 0),
# 한 소스가 15 ms 늦게 다른 자리를 움직이게(실제 지연 결합) 만든 뒤,
# 10 Hz에서 결맞음 크기 |Coh|, 허수 결맞음 |ImCoh|, wPLI를 비교한다.
rng = np.random.default_rng(11)
fs, T, ne = 200, 2.0, 200
n = int(fs * T)
sos = butter(4, [8, 12], btype="band", fs=fs, output="sos")
f = np.fft.rfftfreq(n, 1 / fs)
k10 = np.argmin(abs(f - 10))
win = np.hanning(n)
lag = int(0.015 * fs)  # 15 ms = 3 표본


def alpha(m):
    return sosfiltfilt(sos, rng.normal(size=(m, n + 40)), axis=1)[:, 20:-20] / 0.25


def noise(m):
    return rng.normal(0, 3.0, size=(m, n))


def scenario(kind):
    s = alpha(ne)
    s_lag = np.roll(s, lag, axis=1)
    c = alpha(ne)          # 두 센서에 동시에 섞이는 큰 공통 소스
    x1, x2 = noise(ne), noise(ne)
    if kind == "mix":
        x1 = x1 + 1.0 * s
        x2 = x2 + 0.7 * s
    elif kind == "lag":
        x1 = x1 + 1.0 * s
        x2 = x2 + 0.7 * s_lag
    elif kind == "lagmix":
        x1 = x1 + 1.0 * s + 1.0 * c
        x2 = x2 + 0.7 * s_lag + 0.8 * c
    X1 = np.fft.rfft(x1 * win, axis=1)[:, k10]
    X2 = np.fft.rfft(x2 * win, axis=1)[:, k10]
    S12 = X1 * np.conj(X2)
    coh = S12.mean() / np.sqrt((abs(X1) ** 2).mean() * (abs(X2) ** 2).mean())
    wpli = abs(S12.imag.mean()) / abs(S12.imag).mean()
    z = S12 / np.sqrt((abs(X1) ** 2).mean() * (abs(X2) ** 2).mean())  # 시행별 교차 스펙트럼(평균 파워로 나눔)
    return abs(coh), abs(coh.imag), wpli, np.angle(coh), z


kinds = [("none", "결합 없음"), ("mix", "혼합만\n(지연 0)"), ("lag", "지연 결합\n(15 ms)"),
         ("lagmix", "지연 결합\n+ 강한 혼합")]
res = {k: scenario(k) for k, _ in kinds}
for k, lab in kinds:
    a, b, w, ph, _ = res[k]
    print(f"{k:7s} |Coh|={a:.2f} |ImCoh|={b:.2f} wPLI={w:.2f} 위상={np.degrees(ph):.0f}°", file=sys.stderr)
print("15 ms @10 Hz 위상 =", 360 * 10 * 0.015, "도", file=sys.stderr)

fig = plt.figure(figsize=(7.3, 3.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.45], wspace=0.28)
a = fig.add_subplot(gs[0])
bins = np.linspace(-180, 180, 25)
for k, col, lab in (("mix", C["red"], "혼합만"), ("lag", C["blue"], "지연 결합")):
    ang = np.degrees(np.angle(res[k][4]))
    a.hist(ang, bins=bins, color=col, alpha=0.55, label=lab)
a.axvline(0, color=C["red"], lw=1, ls="--")
a.axvline(54, color=C["blue"], lw=1, ls="--")
a.text(58, a.get_ylim()[1] * 0.93, "54° = 15 ms", color=C["blue"], fontsize=7.5)
a.set_xticks([-180, -90, 0, 90, 180])
a.set_xlim(-180, 180)
a.set_xlabel("시행별 위상차 (°)")
a.set_ylabel("시행 수")
a.legend(fontsize=7.5, loc="upper left", handlelength=1)
a.set_title("(가) 10 Hz 위상차의 분포", fontsize=9.5)

b = fig.add_subplot(gs[1])
xs = np.arange(len(kinds))
wd = 0.26
cols = [C["gray"], C["red"], C["blue"]]
names = ["|Coh|", "|ImCoh|", "wPLI"]
for j in range(3):
    vals = [res[k][j] for k, _ in kinds]
    b.bar(xs + (j - 1) * wd, vals, wd, color=cols[j], label=names[j])
    for x, v in zip(xs, vals):
        b.text(x + (j - 1) * wd, v + 0.015, f"{v:.2f}", ha="center", va="bottom", fontsize=6.3)
b.set_xticks(xs)
b.set_xticklabels([lab for _, lab in kinds], fontsize=8)
b.set_ylim(0, 1.12)
b.set_ylabel("10 Hz 값")
b.legend(fontsize=7.5, loc="upper left", ncol=3, columnspacing=0.8)
b.set_title("(나) 지연 0 성분을 버리는 지표", fontsize=9.5)
save(fig, __file__)
