"""혼입 요인: 움직임의 거리 의존 인공물과 전역 신호 회귀가 만드는 음의 상관."""
import sys

from scipy import signal

from figstyle import plt, np, save, C

rng = np.random.default_rng(9)
TR = 2.0
T = 300
b, a = signal.butter(2, [0.01, 0.1], btype="band", fs=1 / TR)

# ---------- (가) 움직임: 가까운 영역끼리 같은 인공물을 받는다 ----------
n = 80
pos = rng.standard_normal((n, 3))
pos = pos / np.linalg.norm(pos, axis=1, keepdims=True) * rng.uniform(30, 70, (n, 1))  # mm
D = np.linalg.norm(pos[:, None] - pos[None], axis=2)
iu = np.triu_indices(n, 1)
lab = rng.integers(0, 5, n)


def subject(motion):
    m = rng.standard_normal((T, 5))
    x = 0.6 * m[:, lab] + rng.standard_normal((T, n))
    x = signal.filtfilt(b, a, x, axis=0)
    x /= x.std(0)
    spikes = np.zeros(T, bool)
    if motion:
        spikes[rng.choice(np.arange(5, T - 5), 20, replace=False)] = True
        for t0 in np.where(spikes)[0]:
            # 머리가 움직인 순간: 공간적으로 매끄러운 신호 변화 (길이 척도 약 30 mm)
            cent = rng.standard_normal(3) * 40
            w = np.exp(-np.sum((pos - cent) ** 2, 1) / (2 * 30 ** 2))
            amp = rng.choice([-1, 1]) * rng.uniform(3, 6)
            for k, decay in enumerate([1.0, 0.5, 0.2]):
                x[t0 + k] += amp * decay * w
    return x, spikes


def fc(x, keep=None):
    if keep is not None:
        x = x[keep]
    return np.arctanh(np.clip(np.corrcoef(x.T), -0.999, 0.999))[iu]


low = np.mean([fc(subject(False)[0]) for _ in range(15)], 0)
hi_raw, hi_scr = [], []
for _ in range(15):
    x, sp = subject(True)
    hi_raw.append(fc(x))
    bad = sp | np.roll(sp, 1) | np.roll(sp, 2) | np.roll(sp, -1)  # 스파이크와 앞뒤 볼륨 제거
    hi_scr.append(fc(x, ~bad))
d_raw = np.mean(hi_raw, 0) - low
d_scr = np.mean(hi_scr, 0) - low
dist = D[iu]
bins = np.arange(0, 141, 20)
mid = (bins[:-1] + bins[1:]) / 2


def binned(v):
    return np.array([v[(dist >= lo) & (dist < hi)].mean() for lo, hi in zip(bins[:-1], bins[1:])])


br, bs = binned(d_raw), binned(d_scr)
print("motion dFC raw by dist:", np.round(br, 3), file=sys.stderr)
print("motion dFC scrubbed  :", np.round(bs, 3), file=sys.stderr)

# ---------- (나) 전역 신호 회귀 ----------
nn = 40
grp = np.repeat([0, 1], nn // 2)        # 서로 독립인 두 네트워크
rs = {"참": [], "원자료": [], "GSR 뒤": []}
for _ in range(30):
    netsig = rng.standard_normal((T, 2))
    glob = rng.standard_normal((T, 1))  # 호흡·각성 같은 전역 요동
    clean = 0.8 * netsig[:, grp] + rng.standard_normal((T, nn))
    x = clean + 0.7 * glob
    clean = signal.filtfilt(b, a, clean, axis=0)
    x = signal.filtfilt(b, a, x, axis=0)
    gs = x.mean(1, keepdims=True)
    beta = np.linalg.lstsq(np.c_[np.ones(T), gs], x, rcond=None)[0]
    xg = x - np.c_[np.ones(T), gs] @ beta
    for key, y in [("참", clean), ("원자료", x), ("GSR 뒤", xg)]:
        R = np.corrcoef(y.T)
        rs[key].append(R[np.ix_(grp == 0, grp == 1)].ravel())
for k in rs:
    rs[k] = np.concatenate(rs[k])
    print(f"between-network r [{k}]: mean {rs[k].mean():.2f}", file=sys.stderr)

fig, axes = plt.subplots(1, 2, figsize=(7.3, 2.8), gridspec_kw=dict(wspace=0.32))
ax = axes[0]
ax.scatter(dist, d_raw, s=2, color=C["red"], alpha=0.12, lw=0)
ax.plot(mid, br, "o-", color=C["red"], lw=1.6, ms=4, label="움직임 많은 집단 − 적은 집단")
ax.plot(mid, bs, "s--", color=C["blue"], lw=1.4, ms=3.5, label="스크러빙 뒤")
ax.axhline(0, color=C["gray"], lw=0.6)
ax.set_xlabel("두 영역 사이 거리 (mm)")
ax.set_ylabel("연결 차이 Δz")
ax.set_xlim(0, 140)
ax.set_ylim(-0.1, 0.32)
ax.set_title("(가) 움직임은 가까운 연결을 부풀린다", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper right")

ax = axes[1]
bins_r = np.arange(-0.7, 0.71, 0.04)
for key, col, ls in [("참", C["gray"], "-"), ("원자료", C["red"], "-"), ("GSR 뒤", C["blue"], "-")]:
    h, e = np.histogram(rs[key], bins_r, density=True)
    ax.step(e[:-1], h, where="post", color=col, lw=1.5, label=f"{key} (평균 {rs[key].mean():+.2f})".replace("-", "−"))
ax.axvline(0, color=C["gray"], lw=0.6, ls=":")
ax.set_xlabel("서로 독립인 두 네트워크 사이의 상관 $r$")
ax.set_ylabel("밀도")
ax.set_xlim(-0.7, 0.7)
ax.set_title("(나) 전역 신호 회귀와 음의 상관", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper left")
ax.set_ylim(0, ax.get_ylim()[1] * 1.35)
save(fig, __file__)
