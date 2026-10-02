import math

from figstyle import plt, np, save, C

# 풍선 모형(Buxton 1998; 점탄성 확장)으로 그린 20 s 자극의 혈류역학 반응 도식.
dt = 0.01
T = np.arange(-5, 60, dt)
stim = ((T >= 0) & (T < 20)).astype(float)
# 혈류와 산소 소비의 입력: 상자 함수를 짧은 감마 커널로 부드럽게 (지연 약 1–2 s)
tk = np.arange(0, 12, dt)
k = tk ** 2 * np.exp(-tk / 0.9)
k /= k.sum()
sm = np.convolve(stim, k)[: len(T)]
f = 1 + 0.5 * sm          # CBF +50%
m = 1 + 0.2 * sm          # CMRO2 +20%

tau0, alpha = 2.0, 0.3   # 정맥 통과 시간 (s), 정상 상태 지수 (정맥 쪽)
tv_in, tv_out = 2.0, 18.0  # 부풀 때와 줄어들 때의 점탄성 시간 상수 (s)
v, q = np.ones_like(T), np.ones_like(T)
for i in range(1, len(T)):
    vi, qi, fi = v[i - 1], q[i - 1], f[i - 1]
    tv = tv_in if fi >= vi ** (1 / alpha) else tv_out
    fout = (vi ** (1 / alpha) + tv / tau0 * fi) / (1 + tv / tau0)
    v[i] = vi + dt * (fi - fout) / tau0
    q[i] = qi + dt * (m[i - 1] - fout * qi / vi) / tau0
M, beta = 0.08, 1.3
bold = M * (1 - v ** (1 - beta) * q ** beta) * 100

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3))
for a in (a1, a2):
    a.axvspan(0, 20, color=C["light"], zorder=0)
    a.axhline(0, color=C["gray"], lw=0.6)
    a.set_xlim(-5, 60)
    a.set_xlabel("자극 시작 뒤 시간 (s)")
a1.plot(T, (f - 1) * 100, color=C["red"], lw=1.8, label="CBF (혈류)")
a1.plot(T, (v - 1) * 100, color=C["purple"], lw=1.8, label="정맥 CBV (혈액량)")
a1.plot(T, (m - 1) * 100, color=C["green"], lw=1.8, label="CMRO$_2$ (산소 소비)")
a1.plot(T, (q - 1) * 100, color=C["blue"], lw=1.4, ls="--", label="탈산소Hb 총량")
a1.set_ylabel("기저선 대비 변화 (%)")
a1.set_ylim(-25, 60)
a1.legend(fontsize=7.6, loc="upper right")
a1.text(10, -21, "자극 20 s", ha="center", fontsize=8, color=C["gray"])
a1.set_title("혈류, 혈액량, 산소 소비", fontsize=9.5)

a2.plot(T, bold, color=C["blue"], lw=2)
iu = np.argmin(bold[T > 20]) + np.argmax(T > 20)
a2.annotate("언더슈트: 혈류는 돌아왔지만\n혈액량이 늦게 줄어든다", xy=(T[iu], bold[iu]),
            xytext=(27, 0.9), fontsize=8, va="center",
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_ylabel("BOLD 신호 변화 (%)")
a2.set_ylim(-0.4, 1.6)
a2.set_title("BOLD (3 T 어림)", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
