from scipy.signal import butter, filtfilt
from figstyle import plt, np, save, C

# 동시 EEG–fMRI의 경사 인공물과 심탄도(BCG) 인공물을 평균 인공물 빼기(AAS)로 지운다 (Allen 1998, 2000의 원리).
rng = np.random.default_rng(3)


def true_eeg(n, fs):
    t = np.arange(n) / fs
    w = filtfilt(*butter(2, [1 / (fs / 2), 40 / (fs / 2)], "band"), rng.standard_normal(n))
    return 20 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)) * np.sin(2 * np.pi * 10 * t) + 6 * w / w.std()


# --- 경사 인공물: 5 kHz 표본화, 슬라이스마다 같은 경사 파형(램프마다 0.05 ms 폭의 펄스)
fs, T = 5000.0, 30.0
n = int(T * fs)
t = np.arange(n) / fs
eeg = true_eeg(n, fs)


def gshape(tau):           # tau: 슬라이스 시작 뒤 시간 (ms) → μV
    out = np.zeros_like(tau)
    for c, s in [(0.6, 1), (2.6, -1), (3.0, -0.6), (5.0, 0.6)]:
        out += s * np.exp(-0.5 * ((tau - c) / 0.06) ** 2)
    for k in range(100):   # EPI 읽기 경사의 램프
        out += 0.8 * (1 if k % 2 == 0 else -1) * np.exp(-0.5 * ((tau - 6 - 0.25 * k) / 0.05) ** 2)
    return 3000 * out


lp = lambda v: filtfilt(*butter(4, 40 / (fs / 2)), v)


def aas(x, starts, L, k=25):
    out = x.copy()
    starts = starts[starts + L <= len(x)]
    E = np.array([x[s:s + L] for s in starts])
    for i, s in enumerate(starts):
        lo = max(0, min(i - k // 2, len(starts) - k))
        out[s:s + L] -= E[lo:lo + k].mean(0)
    return out


res = {}
for Ts, key in [(57.0, "sync"), (57.037, "free")]:        # 슬라이스 간격 (ms): 동기화 / 비동기
    on = np.arange(int(T * 1000 / Ts)) * Ts
    idx = np.searchsorted(on, t * 1000, side="right") - 1
    raw = eeg + gshape(t * 1000 - on[idx])
    clean = lp(aas(raw, np.round(on * fs / 1000).astype(int), int(Ts * fs / 1000)))
    res[key] = (raw, clean)
    print(key, "raw peak", round(np.abs(raw).max()), "resid rms", round((clean - lp(eeg))[10000:-10000].std(), 2))

# --- BCG: 250 Hz로 줄인 뒤, 심전도 R파에 맞춰 평균 박동 모양을 뺀다
fs2, T2 = 250.0, 120.0
n2 = int(T2 * fs2)
t2 = np.arange(n2) / fs2
eeg2 = true_eeg(n2, fs2)
R = np.cumsum(np.clip(rng.normal(60 / 66, 0.05, 400), 0.7, 1.2))
R = R[(R > 0.5) & (R < T2 - 1.5)]


def beat(tau, s):
    tau = tau / s
    return (55 * np.exp(-0.5 * ((tau - 0.20) / 0.035) ** 2) - 40 * np.exp(-0.5 * ((tau - 0.30) / 0.045) ** 2)
            + 18 * np.exp(-0.5 * ((tau - 0.45) / 0.07) ** 2))


bcg = np.zeros(n2)
for r, A, s, j in zip(R, rng.normal(1, 0.12, len(R)), rng.normal(1, 0.04, len(R)), rng.normal(0, 0.004, len(R))):
    m = (t2 >= r) & (t2 < r + 0.8)
    bcg[m] += A * beat(t2[m] - r - j, s)
raw2 = eeg2 + bcg
Ri = np.round(R * fs2).astype(int)
clean2 = aas(raw2, Ri, int(0.75 * fs2), k=21)
mm = slice(int(3 * fs2), int((T2 - 3) * fs2))
print("BCG rms", round(bcg[mm].std(), 1), "peak", round(bcg.max()), "resid rms", round((clean2 - eeg2)[mm].std(), 2),
      "eeg rms", round(eeg2[mm].std(), 1))

fig, axs = plt.subplots(2, 2, figsize=(7.4, 4.0))
w0 = (t >= 10.0) & (t < 10.3)
a = axs[0, 0]
a.plot(t[w0] * 1000 - 10000, res["sync"][0][w0] / 1000, color=C["red"], lw=0.5)
a.set_ylabel("전압 (mV)")
a.set_xlabel("시간 (ms)")
a.set_title("(가) 원 기록: 슬라이스마다 반복되는 경사 인공물", fontsize=9.2)
a.text(150, 3.15, "참 EEG는 ±0.05 mV 안에 묻혀 있다", fontsize=7.6, ha="center", color=C["gray"])
a.set_ylim(-3.2, 3.7)

w1 = (t >= 10.0) & (t < 11.0)
a = axs[0, 1]
a.plot(t[w1] - 10, lp(eeg)[w1], color=C["gray"], lw=2.2, alpha=0.6, label="참 EEG")
a.plot(t[w1] - 10, res["sync"][1][w1], color=C["blue"], lw=1, label="AAS, 시계 동기화")
a.plot(t[w1] - 10, res["free"][1][w1], color=C["red"], lw=0.9, label="AAS, 동기화 없음")
a.set_ylim(-48, 62)
a.set_ylabel("전압 (μV)")
a.set_xlabel("시간 (s)")
a.legend(fontsize=7.2, loc="upper right", ncol=3, columnspacing=0.8, handlelength=1.4)
a.set_title("(나) 평균 인공물을 빼고 40 Hz 저역 통과", fontsize=9.2)

w2 = (t2 >= 20) & (t2 < 24)
a = axs[1, 0]
a.plot(t2[w2] - 20, raw2[w2], color=C["red"], lw=0.9, label="경사 보정 뒤 기록")
a.plot(t2[w2] - 20, eeg2[w2], color=C["gray"], lw=0.8, alpha=0.8, label="참 EEG")
for r in R[(R >= 20) & (R < 24)]:
    a.axvline(r - 20, color=C["purple"], lw=0.7, ls=":")
a.text(0.02, 0.06, "보라 점선: 심전도 R파", transform=a.transAxes, fontsize=7.4, color=C["purple"])
a.set_ylim(-80, 135)
a.set_ylabel("전압 (μV)")
a.set_xlabel("시간 (s)")
a.legend(fontsize=7.2, loc="upper right", ncol=2)
a.set_title("(다) 심탄도 인공물", fontsize=9.2)

a = axs[1, 1]
a.plot(t2[w2] - 20, eeg2[w2], color=C["gray"], lw=2.2, alpha=0.6, label="참 EEG")
a.plot(t2[w2] - 20, clean2[w2], color=C["blue"], lw=0.9, label="BCG 평균 빼기 뒤")
a.set_ylim(-80, 135)
a.set_ylabel("전압 (μV)")
a.set_xlabel("시간 (s)")
a.legend(fontsize=7.2, loc="upper right", ncol=2)
a.set_title("(라) 박동 21개 평균을 빼면", fontsize=9.2)
fig.tight_layout(h_pad=1.2)
save(fig, __file__)
