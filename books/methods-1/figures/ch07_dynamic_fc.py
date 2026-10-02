"""미끄럼 창 동적 연결성: 참 상관이 일정해도 창 상관은 크게 출렁인다."""
import sys

from scipy import signal

from figstyle import plt, np, save, C

rng = np.random.default_rng(21)
TR = 2.0
T = 300  # 10분
b, a = signal.butter(2, [0.01, 0.1], btype="band", fs=1 / TR)
rho = 0.3


def pair(T):
    """참 상관이 rho로 일정한 두 시계열(같은 대역 통과)."""
    z = rng.standard_normal((T + 200, 2))
    x = z[:, 0]
    y = rho * z[:, 0] + np.sqrt(1 - rho ** 2) * z[:, 1]
    xy = signal.filtfilt(b, a, np.c_[x, y], axis=0)[100:-100]
    return xy


def sliding(xy, w):
    out = []
    for s in range(0, len(xy) - w + 1):
        seg = xy[s:s + w]
        out.append(np.corrcoef(seg.T)[0, 1])
    return np.array(out)


xy = pair(T)
t = np.arange(T) * TR

fig, axes = plt.subplots(1, 2, figsize=(7.3, 2.8), gridspec_kw=dict(width_ratios=[1.6, 1], wspace=0.3))
ax = axes[0]
for w_s, col in [(30, C["gray"]), (60, C["blue"]), (120, C["red"])]:
    w = int(w_s / TR)
    r = sliding(xy, w)
    tc = t[: len(r)] + w_s / 2
    ax.plot(tc / 60, r, color=col, lw=1.3 if w_s != 30 else 1.0, label=f"창 {w_s} s")
    print(f"window {w_s}s: range {r.min():.2f}..{r.max():.2f}, sd {r.std():.2f}", file=sys.stderr)
ax.axhline(rho, color=C["ink"], lw=1, ls="--")
ax.text(9.9, -0.95, "점선: 참 상관 0.3 (내내 일정)", fontsize=8, va="bottom", ha="right")
ax.axhline(0, color=C["gray"], lw=0.5)
ax.set_xlim(0, 10)
ax.set_ylim(-1.05, 1.15)
ax.set_xlabel("창 가운데 시각 (분)")
ax.set_ylabel("창 안의 상관 $r$")
ax.set_title("(가) 잡음만으로 생기는 “상태 변화”", fontsize=9.5)
ax.legend(fontsize=7.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.0), handlelength=2.2)
for ln_ in ax.get_legend().get_lines():
    ln_.set_linewidth(2.0)

ax = axes[1]
wins = np.array([20, 30, 45, 60, 90, 120, 180, 240])
sd_f, sd_w = [], []
for w_s in wins:
    w = int(w_s / TR)
    vals_f, vals_w = [], []
    for _ in range(300):
        xy = pair(w)
        vals_f.append(np.corrcoef(xy.T)[0, 1])
        z = rng.standard_normal((w, 2))
        vals_w.append(np.corrcoef(z[:, 0], rho * z[:, 0] + np.sqrt(1 - rho ** 2) * z[:, 1])[0, 1])
    sd_f.append(np.std(vals_f))
    sd_w.append(np.std(vals_w))
sd_f, sd_w = np.array(sd_f), np.array(sd_w)
for w_s, s1, s2 in zip(wins, sd_f, sd_w):
    print(f"  w={w_s}s sd_filtered={s1:.3f} sd_white={s2:.3f}", file=sys.stderr)
ax.plot(wins, sd_f, "o-", color=C["blue"], ms=3.5, lw=1.5, label="대역 통과 (0.01–0.1 Hz)")
ax.plot(wins, sd_w, "s--", color=C["gray"], ms=3, lw=1.2, label="백색 잡음 (같은 표본 수)")
ax.axvline(100, color=C["red"], lw=0.8, ls=":")
ax.text(106, 0.02, "1/$f_{\\min}$ = 100 s", color=C["red"], fontsize=7.5)
ax.set_xlabel("창 길이 (s)")
ax.set_ylabel("창 상관의 표준편차")
ax.set_ylim(0, 0.55)
ax.set_xlim(0, 250)
ax.set_title("(나) 창이 짧을수록 출렁임이 크다", fontsize=9.5)
ax.legend(fontsize=7.2, loc="upper right", bbox_to_anchor=(1.02, 1.02))
save(fig, __file__)
