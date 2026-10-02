from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle

# pCASL: 표지 1.8 s, PLD 1.8 s, 배경 억제(시작 때 포화 + 반전 두 번), 3.6 s에 읽기
tau, pld = 1.8, 1.8
T = tau + pld
tinv = [1.85, 3.18]                 # 반전 펄스 시각 (s): 아래 계산으로 고른 값

fig = plt.figure(figsize=(7.4, 4.4))
gs = fig.add_gridspec(2, 2, height_ratios=[0.75, 1.25], hspace=0.38, wspace=0.3)
at = fig.add_subplot(gs[0, :])

# (가) 시간표
for row, (name, y) in enumerate([("표지", 1.0), ("대조", 0.0)]):
    at.text(-0.1, y + 0.3, name, ha="right", va="center", fontsize=9)
    # RF 펄스열: 약 1 ms 간격의 짧은 펄스 수천 개 (그림에서는 줄여 그림)
    for tp in np.arange(0.02, tau, 0.045):
        at.add_patch(Rectangle((tp, y + 0.05), 0.018, 0.5, color=C["purple"], lw=0))
    sym = "같은 위상 → 흐르는 피가 반전" if name == "표지" else "펄스마다 위상 교대 → 반전 없음"
    at.text(tau / 2, y + 0.72, sym, ha="center", fontsize=8.3, color=C["purple"])
    at.add_patch(Rectangle((-0.06, y + 0.05), 0.04, 0.6, color=C["gray"], lw=0))
    for ti in tinv:
        at.add_patch(Rectangle((ti - 0.02, y + 0.05), 0.04, 0.6, color=C["red"], lw=0))
    at.add_patch(Rectangle((T, y + 0.05), 0.45, 0.5, color=C["blue"], alpha=0.8, lw=0))
at.text(T + 0.225, 1.72, "3D 읽기", ha="center", fontsize=8, color=C["blue"])
at.text(-0.04, -0.25, "포화", ha="center", fontsize=7.5, color=C["gray"])
for ti in tinv:
    at.text(ti, -0.25, "반전", ha="center", fontsize=7.5, color=C["red"])
for x0, x1, lab in [(0, tau, "표지 시간 τ = 1.8 s"), (tau, T, "표지 뒤 지연 PLD = 1.8 s")]:
    at.annotate("", xy=(x0, -0.6), xytext=(x1, -0.6),
                arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.7))
    at.text((x0 + x1) / 2, -0.95, lab, ha="center", fontsize=8)
at.set_xlim(-0.6, 4.3)
at.set_ylim(-1.1, 1.95)
at.axis("off")
at.set_title("(가) 표지 영상과 대조 영상의 시간표", fontsize=9.5, loc="left")

# (나) 배경 억제: 정지 조직의 세로 자화
ab = fig.add_subplot(gs[1, 0])
t = np.linspace(0, T, 2000)
for name, T1, col in [("백질 0.85 s", 0.85, C["green"]), ("회백질 1.35 s", 1.35, C["blue"]),
                      ("뇌척수액 4.0 s", 4.0, C["gray"])]:
    m = np.zeros_like(t)
    mz, last = 0.0, 0.0
    for i, ti in enumerate(t):
        cur = mz
        for tp in tinv:
            if last < tp <= ti:
                cur = 1 - (1 - cur) * np.exp(-(tp - last) / T1)
                cur, last = -cur, tp
                mz = cur
        m[i] = 1 - (1 - mz) * np.exp(-(ti - last) / T1)
    ab.plot(t, m, color=col, lw=1.6, label=name)
    ab.plot(T, m[-1], "o", color=col, ms=3.5)
ab.axhline(0, color=C["gray"], lw=0.6)
ab.axvline(T, color=C["blue"], lw=0.7, ls=":")
ab.set_xlabel("표지 시작 뒤 시간 (s)")
ab.set_ylabel("정지 조직 $M_z/M_0$")
ab.set_ylim(-1.05, 1.05)
ab.legend(fontsize=7.5, loc="lower left", title="조직 T1 (3 T)", title_fontsize=8)
ab.set_title("(나) 배경 억제", fontsize=9.5)
ab.set_xlim(-0.15, 4.4)
ab.text(T + 0.08, 0.35, "읽을 때\n거의 0", ha="left", fontsize=8.3, color=C["blue"])

# (다) 신호 모형: PLD에 따른 차이 신호 (단일 구획, 생리 1권 8장)
ac = fig.add_subplot(gs[1, 1])
alpha, lam, T1b, f = 0.85, 0.9, 1.65, 60 / 6000
w = np.linspace(0, 3.2, 400)
for att, col in [(1.0, C["blue"]), (2.0, C["red"])]:
    dm = np.where(w >= att,
                  2 * alpha * f / lam * T1b * np.exp(-w / T1b) * (1 - np.exp(-tau / T1b)),
                  2 * alpha * f / lam * T1b * np.exp(-att / T1b)
                  * (1 - np.exp(-np.clip(tau + w - att, 0, None) / T1b)))
    ac.plot(w, dm * 100, color=col, lw=1.8, label=f"동맥 통과 시간 {att:.1f} s")
ac.axvline(1.8, color=C["gray"], lw=0.7, ls="--")
ac.text(1.85, 0.05, "PLD 1.8 s", fontsize=8.3, color=C["gray"])
ac.set_xlabel("표지 뒤 지연 PLD (s)")
ac.set_ylabel("표지 − 대조 ($M_0$ 대비 %)")
ac.set_ylim(0, 1.25)
ac.legend(fontsize=7.5, loc="upper right")
ac.set_title("(다) 차이 신호 (CBF 60 mL/100 g/분)", fontsize=9.5)
save(fig, __file__)
