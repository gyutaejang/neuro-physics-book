from figstyle import plt, np, save, C

# (가) ¹⁸F 붕괴 도식, (나) 페르미 이론으로 계산한 양전자 에너지 스펙트럼.
alpha, me = 1 / 137.036, 0.511


def spectrum(E0, Z, n=2000):
    T = np.linspace(1e-5, E0, n)
    W = T + me
    p = np.sqrt(W ** 2 - me ** 2)
    eta = Z * alpha * W / p                       # 양전자: 딸핵이 밀어내므로 느린 쪽이 줄어든다
    F = 2 * np.pi * eta / np.expm1(2 * np.pi * eta)
    N = p * W * (E0 - T) ** 2 * F
    return T, N / np.trapezoid(N, T)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1, 1.35]))
# (가) 붕괴 도식: 에너지 준위 (MeV)
a1.plot([0.1, 0.9], [1.656, 1.656], color=C["ink"], lw=2)
a1.plot([0.9, 1.9], [0, 0], color=C["ink"], lw=2)
a1.text(0.5, 1.72, "¹⁸F (Z = 9)", ha="center", fontsize=9)
a1.text(1.4, -0.1, "¹⁸O (Z = 8), 안정", ha="center", va="top", fontsize=9)
# 전자 포획: 곧장 바닥으로
a1.annotate("", xy=(1.05, 0.0), xytext=(0.75, 1.656),
            arrowprops=dict(arrowstyle="-|>", color=C["gray"], lw=1.2))
a1.text(1.0, 1.0, "전자 포획\n3%", fontsize=8, color=C["gray"])
# β⁺: 2mₑc² 만큼 먼저 내려온 뒤
a1.plot([0.3, 0.3], [1.656, 0.634], color=C["red"], lw=1.2, ls=":")
a1.annotate("", xy=(0.95, 0.03), xytext=(0.3, 0.634),
            arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.4))
a1.text(0.34, 1.14, "2mₑc²\n= 1.022", fontsize=7.5, color=C["red"], va="center")
a1.text(0.04, 0.02, "β⁺ 97%\n최대 0.634", fontsize=8, color=C["red"])
a1.set_xlim(0, 2.0)
a1.set_ylim(-0.45, 2.05)
a1.set_xticks([])
a1.spines["bottom"].set_visible(False)
a1.set_ylabel("원자 질량 에너지 차 (MeV)")
a1.set_yticks([0, 0.634, 1.656])
a1.set_title("(가) ¹⁸F의 붕괴 도식", fontsize=9.5)

# (나) 스펙트럼
iso = [("¹⁸F", 0.634, 8, C["red"]), ("¹¹C", 0.960, 5, C["blue"]),
       ("¹⁵O", 1.732, 7, C["green"]), ("⁸²Rb", 3.378, 36, C["purple"])]
for name, E0, Z, col in iso:
    T, N = spectrum(E0, Z)
    mean = np.trapezoid(T * N, T)
    a2.plot(T, N, color=col, lw=1.7, label=f"{name}: 평균 {mean:.2f}, 최대 {E0:.2f} MeV")
    a2.axvline(mean, ymax=0.06, color=col, lw=2)
a2.set_xlim(0, 3.5)
a2.set_ylim(0, None)
a2.set_xlabel("양전자 운동 에너지 (MeV)")
a2.set_ylabel("상대 빈도 (넓이 = 1)")
a2.set_yticks([])
a2.legend(fontsize=7.6, loc="upper right")
a2.set_title("(나) 양전자 에너지는 연속 분포다", fontsize=9.5)
fig.tight_layout()
save(fig, __file__)
