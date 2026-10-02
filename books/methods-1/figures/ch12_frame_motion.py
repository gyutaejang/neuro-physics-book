from scipy.ndimage import gaussian_filter, shift as nshift
from figstyle import plt, np, save, C

# 동적 PET 중 머리 움직임이 선조체 TAC와 BP_ND를 어떻게 바꾸는지 보는 합성 시뮬레이션.
# 입력 함수와 속도 상수는 물리 2권 3장 그림과 같다 (BP_ND = 3인 라클로프라이드 비슷한 추적자).
dt = 0.01
t = np.arange(0, 90 + dt, dt)
A1, A2, A3, l1, l2, l3 = 851.1, 21.88, 20.81, 4.134, 0.1191, 0.01043
Cp = np.maximum((A1 * t - A2 - A3) * np.exp(-l1 * t) + A2 * np.exp(-l2 * t) + A3 * np.exp(-l3 * t), 0)


def tcm(K1, k2, k3, k4):
    a, b = np.zeros_like(t), np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (K1 * Cp[i - 1] - (k2 + k3) * a[i - 1] + k4 * b[i - 1])
        b[i] = b[i - 1] + dt * (k3 * a[i - 1] - k4 * b[i - 1])
    return a + b


CT, CR = tcm(0.1, 0.4, 0.24, 0.08), tcm(0.1, 0.4, 0.0, 0.0)
dur = np.array([0.5] * 6 + [1] * 3 + [3] * 3 + [5] * 15)
ends = np.cumsum(dur)
starts, mid = ends - dur, ends - dur / 2


def frame(c):
    return np.array([c[(t >= s) & (t < e)].mean() for s, e in zip(starts, ends)])


# 2차원 팬텀: 폭 10 mm, 길이 20 mm 타원(조가비핵 비슷한 크기), FWHM 5 mm로 흐린다.
px = 0.5
xg = np.arange(-20, 20, px)
X, Y = np.meshgrid(xg, xg)
roi = ((X / 5) ** 2 + (Y / 10) ** 2) <= 1
blurred = gaussian_filter(roi.astype(float), 5 / 2.355 / px)
ds = np.linspace(0, 8, 81)
rec = np.array([nshift(blurred, (0, d / px), order=1)[roi].mean() for d in ds])
fr = lambda d: np.interp(np.abs(d), ds, rec)

pos = np.where(t < 47.5, 0, np.where(t < 70, 3, 3 + 3 * (t - 70) / 20))   # 머리 위치 (mm)
pos_hat = frame(pos)                                                       # 프레임 정합이 찾는 위치
no_motion = frame(CR + (CT - CR) * fr(0))
moved = frame(CR + (CT - CR) * fr(pos))
fixed = np.array([np.mean(CR[m] + (CT[m] - CR[m]) * fr(pos[m] - pos_hat[k]))
                  for k, m in enumerate((t >= s) & (t < e) for s, e in zip(starts, ends))])

fig = plt.figure(figsize=(7.4, 2.9))
gs = fig.add_gridspec(1, 3, width_ratios=[0.8, 1, 1.25], wspace=0.42)
a0, a1, a2 = (fig.add_subplot(gs[0, i]) for i in range(3))

img = nshift(blurred, (0, 4 / px), order=1)
a0.imshow(img, extent=[-20, 20, -20, 20], origin="lower", cmap="Blues", vmin=0, vmax=1)
a0.contour(X, Y, roi.astype(float), levels=[0.5], colors=[C["red"]], linewidths=1.2)
a0.set_xticks([-10, 0, 10])
a0.set_yticks([-10, 0, 10])
a0.set_xlabel("x (mm)")
a0.text(0, -17.5, "빨강: MRI로 그린 ROI", ha="center", fontsize=7.5, color=C["red"])
a0.set_title("(가) 4 mm 움직인 프레임", fontsize=9.5)

a1.plot(t, pos, color=C["gray"], lw=1.2, label="실제 머리 위치")
a1.step(np.r_[starts, ends[-1]], np.r_[pos_hat, pos_hat[-1]], where="post", color=C["blue"], lw=1.5,
        label="프레임별 정합 추정")
a1.set_xlim(0, 90)
a1.set_ylim(-0.5, 7)
a1.set_xlabel("주사 뒤 시간 (분)")
a1.set_ylabel("x 방향 이동 (mm)")
a1.legend(fontsize=7.4, loc="upper left")
a1.set_title("(나) 머리 움직임", fontsize=9.5)

a2.plot(mid, no_motion, "o-", color=C["blue"], ms=3, lw=1.3, label="움직임 없음")
a2.plot(mid, moved, "s-", color=C["red"], ms=3, lw=1.3, label="움직임, 보정 안 함")
a2.plot(mid, fixed, "^", color=C["purple"], ms=4, mfc="none", label="프레임 정합 후")
a2.plot(mid, frame(CR), "-", color=C["green"], lw=1.3, label="참조 영역 (소뇌)")
a2.axvspan(45, 50, color=C["light"], zorder=0)
a2.set_xlim(0, 90)
a2.set_ylim(0, 26)
a2.set_xlabel("주사 뒤 시간 (분)")
a2.set_ylabel("ROI 평균 (상대 단위)")
a2.legend(fontsize=7.2, loc="upper right")
a2.set_title("(다) 선조체 TAC", fontsize=9.5)
save(fig, __file__)
