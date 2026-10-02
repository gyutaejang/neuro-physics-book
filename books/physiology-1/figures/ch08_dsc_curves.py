from figstyle import plt, np, save, C

dt = 0.1
t = np.arange(0, 60, dt)          # s


def gamma(t, t0, a=3.0, b=1.5):
    x = np.clip(t - t0, 0, None)
    return x ** a * np.exp(-x / b)


aif = gamma(t, 8)
aif = aif / (aif.sum() * dt)       # 넓이 1


def tissue(cbf, mtt, delay):
    """C(t) = CBF · (AIF ⊗ R)(t − delay), R(t) = exp(−t/MTT). cbf는 mL/100 g/분."""
    f = cbf / 100 / 60             # 1/s (mL/g/s, 밀도 1 가정)
    R = np.exp(-t / mtt)
    c = np.convolve(aif, f * R)[:len(t)] * dt
    shift = int(round(delay / dt))
    return np.concatenate([np.zeros(shift), c[:len(t) - shift]]), f * np.where(t >= delay, np.exp(-(t - delay) / mtt), 0)


cn, rn = tissue(60, 4.0, 0.0)
ci, ri = tissue(20, 12.0, 7.0)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
a1.plot(t, aif / aif.max(), color=C["red"], lw=1.4, label="동맥 입력 함수 (AIF, 정규화)")
s = 1 / cn.max()
a1.plot(t, cn * s, color=C["blue"], lw=1.8, label="정상 조직")
a1.plot(t, ci * s, color=C["purple"], lw=1.8, label="관류 저하 조직")
a1.set_xlabel("조영제 도착 뒤 시간 (s)")
a1.set_ylabel("농도 (상대, ΔR2*에 비례)")
a1.set_title("첫 통과 농도 곡선", fontsize=10)
a1.set_xlim(0, 50)
a1.set_ylim(0, 1.15)
a1.legend(fontsize=7.3, loc="upper right")

a2.fill_between(t, 0, rn * 6000, color=C["blue"], alpha=0.12)
a2.fill_between(t, 0, ri * 6000, color=C["purple"], alpha=0.12)
a2.plot(t, rn * 6000, color=C["blue"], lw=1.8)
a2.plot(t, ri * 6000, color=C["purple"], lw=1.8)
a2.text(4.5, 50, "정상: CBF 60, CBV 4\nMTT 4 s, Tmax 0 s", fontsize=7.6, color=C["blue"])
a2.text(13, 23, "저하: CBF 20, CBV 4\nMTT 12 s, Tmax 7 s", fontsize=7.6, color=C["purple"])
a2.annotate("", xy=(7, 2), xytext=(0, 2), arrowprops=dict(arrowstyle="<->", color=C["gray"], lw=0.8))
a2.text(3.5, 3.5, "Tmax", fontsize=7.5, color=C["gray"], ha="center")
a2.set_xlabel("시간 (s)")
a2.set_ylabel("CBF × R(t)  (mL/100 g/분)")
a2.set_title("디컨볼루션으로 얻는 잔류 함수", fontsize=10)
a2.set_xlim(0, 40)
a2.set_ylim(0, 66)
a2.text(39, 62, "높이 = CBF, 넓이 = CBV", fontsize=7.6, color=C["ink"], ha="right", va="top")
fig.tight_layout()
save(fig, __file__)
