import sys

from scipy.signal import butter, sosfiltfilt, hilbert

from figstyle import plt, np, save, C

# 진폭 포락선 상관(AEC)과 직교화(짝별: Hipp 2012, 대칭: Colclough 2015). 두 베타 대역(15–25 Hz) 소스의 위상은 서로 독립이고,
# 포락선만 느린 공통 성분으로 상관(또는 무상관)한다. 관측 신호에는 상대 소스가 λ만큼 섞인다
# (지연 0 누설). 직교화는 한 신호에서 다른 신호와 같은 위상인 성분을 시점마다 지운다.
rng = np.random.default_rng(5)
fs, dur = 200, 300
n = fs * dur
band = butter(4, [15, 25], btype="band", fs=fs, output="sos")
fr = np.fft.rfftfreq(n, 1 / fs)


def lowz(m):
    # 0.2 Hz 아래만 남긴 느린 무작위 요동 (FFT 영역에서 거른다)
    X = np.fft.rfft(rng.normal(size=(m, n)), axis=1) * (fr < 0.2)
    x = np.fft.irfft(X, n, axis=1)
    return x / x.std(axis=1, keepdims=True)


def sources(c):
    g, h = lowz(1)[0], lowz(2)
    amp = np.exp(0.6 * (c * g + np.sqrt(1 - c**2) * h))
    car = sosfiltfilt(band, rng.normal(size=(2, n)), axis=1)
    car /= np.abs(hilbert(car, axis=1)).mean(axis=1, keepdims=True)
    return amp * car


def smooth(e):
    # 포락선을 0.5 Hz 아래로 거른 뒤 상관을 구한다 (실제 분석의 포락선 저역 통과/다운샘플링에 해당)
    return np.fft.irfft(np.fft.rfft(e) * (fr < 0.5), n)


def envcorr(a, b):
    return np.corrcoef(smooth(np.abs(a)), smooth(np.abs(b)))[0, 1]


def symorth(Y):
    # 대칭 직교화 (Colclough 2015): Y에 가장 가까운 서로 직교인 시계열, 크기는 원래대로
    U, _, Vt = np.linalg.svd(Y, full_matrices=False)
    return (U @ Vt) * np.sqrt((Y**2).sum(axis=1, keepdims=True))


def aec(y1, y2, orth):
    z1, z2 = hilbert(y1), hilbert(y2)
    if orth == "none":
        return envcorr(z1, z2)
    if orth == "sym":
        o = symorth(np.vstack([y1, y2]))
        return envcorr(hilbert(o[0]), hilbert(o[1]))
    o21 = np.imag(z2 * np.conj(z1) / np.abs(z1))   # z1에 직교인 z2의 부분 (Hipp 2012 방식)
    o12 = np.imag(z1 * np.conj(z2) / np.abs(z2))
    return 0.5 * (envcorr(z1, o21) + envcorr(z2, o12))


lams = np.linspace(0, 0.6, 7)
out = {}
for c, key in ((0.0, "null"), (0.8, "true")):
    s = sources(c)
    sm = s + 0.05 * rng.normal(size=s.shape)
    rows = []
    for lam in lams:
        y1 = sm[0] + lam * sm[1]
        y2 = sm[1] + lam * sm[0]
        rows.append([aec(y1, y2, m) for m in ("none", "pair", "sym")])
    out[key] = np.array(rows)
    print(key, "실제 포락선 상관", round(envcorr(hilbert(s[0]), hilbert(s[1])), 2), file=sys.stderr)
    for lam, (r, o, q) in zip(lams, out[key]):
        print(f"  λ={lam:.1f} 원래={r:.2f} 짝별 직교화={o:.2f} 대칭 직교화={q:.2f}", file=sys.stderr)

# (가) 예시 구간: 누설이 큰 경우(λ = 0.6, 결합 없음)
s = sources(0.0)
y1, y2 = s[0] + 0.6 * s[1], s[1] + 0.6 * s[0]
t = np.arange(n) / fs
seg = (t >= 0) & (t < 60)
fig = plt.figure(figsize=(7.3, 3.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1], hspace=0.25, wspace=0.3)
for i, (y, col, lab) in enumerate(((y1, C["blue"], "자리 1"), (y2, C["purple"], "자리 2"))):
    a = fig.add_subplot(gs[i, 0])
    a.plot(t[seg], y[seg], color=col, lw=0.3, alpha=0.35)
    a.plot(t[seg], smooth(np.abs(hilbert(y)))[seg], color=col, lw=1.8)
    a.set_yticks([])
    a.set_xlim(0, 60)
    a.spines["left"].set_visible(False)
    a.text(0.5, a.get_ylim()[1] * 0.85, lab, fontsize=8, color=col)
    if i == 0:
        a.set_xticklabels([])
        a.set_title("(가) 결합 없는 두 소스, 누설 λ = 0.6: 포락선이 닮는다", fontsize=9, loc="left")
    else:
        a.set_xlabel("시간 (s)")
b = fig.add_subplot(gs[:, 1])
for key, col, lab in (("true", C["blue"], "결합 있음"), ("null", C["red"], "결합 없음")):
    r = out[key]
    b.plot(lams, r[:, 0], "o-", color=col, ms=3.5, lw=1.4, label=f"{lab}, 원래")
    b.plot(lams, r[:, 1], "s--", color=col, ms=3.5, lw=1.1, mfc="white", label=f"{lab}, 짝별 직교화")
    b.plot(lams, r[:, 2], "^:", color=col, ms=3.5, lw=1.3, label=f"{lab}, 대칭 직교화")
b.axhline(0, color=C["gray"], lw=0.6)
b.set_xlabel("누설 비율 λ")
b.set_ylabel("포락선 상관")
b.set_ylim(-0.15, 1.45)
b.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
b.legend(fontsize=6.8, loc="upper left", handlelength=2.2)
b.set_title("(나) 누설과 직교화", fontsize=9.5)
save(fig, __file__)
