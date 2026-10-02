import math

from figstyle import plt, np, save, C

# 도식: 자극이 이어지는 동안 발화(MUA)는 적응해 줄지만 LFP는 유지된다.
# 두 신호를 각각 HRF와 합성곱하면, 유지되는 BOLD를 더 잘 예측하는 것은 LFP다
# (Logothetis 외 2001의 관찰을 단순화한 그림; 수치는 예시).
dt = 0.05
T = np.arange(-5, 50, dt)
on = (T >= 0) & (T < 24)
tt = np.where(on, T, 0)
mua = np.where(on, 0.15 + 0.85 * np.exp(-tt / 2.5), 0)
lfp = np.where(on, 0.6 + 0.4 * np.exp(-tt / 2.5), 0)
g = lambda t, a: t ** (a - 1) * np.exp(-t) / math.gamma(a)
th = np.arange(0, 32, dt)
h = g(th, 6) - g(th, 16) / 6
conv = lambda s: np.convolve(s, h)[: len(s)] * dt
p_lfp, p_mua = conv(lfp), conv(mua)
sc = 1 / p_lfp.max()
rng = np.random.default_rng(3)
meas = p_lfp * sc + rng.normal(0, 0.04, len(T))
meas = np.convolve(meas, np.ones(20) / 20, mode="same")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1))
for a in (a1, a2):
    a.axvspan(0, 24, color=C["light"], zorder=0)
    a.axhline(0, color=C["gray"], lw=0.5)
    a.set_xlim(-5, 50)
    a.set_xlabel("자극 시작 뒤 시간 (s)")
a1.plot(T, lfp, color=C["blue"], lw=1.8, label="LFP (시냅스 입력)")
a1.plot(T, mua, color=C["red"], lw=1.6, label="MUA (발화 출력)")
a1.set_ylabel("신경 신호 (정점 = 1)")
a1.set_ylim(-0.1, 1.25)
a1.legend(fontsize=7.8, loc="upper right")
a1.set_title("신경 신호: 발화는 적응한다", fontsize=9.5)
a2.plot(T, meas, color=C["ink"], lw=1.0, label="측정한 BOLD (예시)")
a2.plot(T, p_lfp * sc, color=C["blue"], lw=1.8, label="LFP로 예측")
a2.plot(T, p_mua * sc, color=C["red"], lw=1.6, label="MUA로 예측")
a2.set_ylabel("BOLD (정규화)")
a2.set_ylim(-0.3, 1.3)
a2.legend(fontsize=7.8, loc="upper right")
a2.set_title("BOLD는 LFP를 더 잘 따른다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
