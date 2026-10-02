from figstyle import plt, np, save, C

# 자료형이 값을 바꾸는 두 가지 방식: 정수로 잘림, 범위를 넘어 되감김.
x = np.linspace(0, 60, 400)            # mm, 선 위치

# (가) FA 같은 0–1 실수를 int16에 그대로 넣으면 0과 1만 남는다.
fa = 0.15 + 0.6 * np.exp(-((x - 30) / 9) ** 2)
fa_int = fa.astype(np.int16)                         # 소수점 아래를 버린다
slope = 1.0 / 32767                                  # scl_slope로 눈금을 넣으면
fa_scaled = np.round(fa / slope).astype(np.int16) * slope

# (나) 0–1000 강도를 uint8(0–255)에 넣으면 256마다 되감긴다.
t1 = 120 + 880 * np.clip((x - 8) / 40, 0, 1)
t1_wrap = (np.round(t1).astype(np.int64) % 256).astype(np.uint8)   # 되감김
t1_clip = np.clip(t1, 0, 255)                                       # 잘림(포화)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw=dict(wspace=0.32))
a1.plot(x, fa, color=C["blue"], lw=2.4, label="원래 실수(float32)")
a1.plot(x, fa_scaled, color=C["ink"], lw=0.9, ls="--", label="int16 + 눈금 계수")
a1.plot(x, fa_int, color=C["red"], lw=1.6, label="int16, 눈금 없음")
a1.set_ylim(-0.08, 1.2)
a1.set_xlabel("위치 (mm)")
a1.set_ylabel("FA")
a1.set_title("(가) 실수를 정수로: 잘림", fontsize=10)
a1.legend(fontsize=8, loc="upper left")

a2.plot(x, t1, color=C["blue"], lw=2.4, label="원래 값(int16)")
a2.plot(x, t1_wrap, color=C["red"], lw=1.3, label="uint8로 변환: 되감김")
a2.plot(x, t1_clip, color=C["gray"], lw=1.3, ls="--", label="uint8로 자름: 포화")
a2.axhline(255, color=C["gray"], lw=0.6, ls=":")
a2.text(59, 275, "255", ha="right", fontsize=8, color=C["gray"])
a2.set_ylim(-20, 1150)
a2.set_xlabel("위치 (mm)")
a2.set_ylabel("강도 (임의 단위)")
a2.set_title("(나) 큰 범위를 작은 형식에: 넘침", fontsize=10)
a2.legend(fontsize=8, loc="upper left")
save(fig, __file__)
