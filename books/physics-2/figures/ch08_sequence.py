from figstyle import plt, np, save, C

# 2차원 그래디언트 에코 시퀀스 한 TR의 도식. 시간축은 임의 단위.
fig, ax = plt.subplots(figsize=(6.8, 3.8))
rows = {"RF": 4, "$G_z$ (슬라이스)": 3, "$G_y$ (위상)": 2, "$G_x$ (읽기)": 1, "신호 / ADC": 0}
for name, y in rows.items():
    ax.plot([0, 10], [y, y], color=C["gray"], lw=0.6)
    ax.text(-0.15, y, name, ha="right", va="center", fontsize=9.5)


def trap(t0, rise, flat, amp, y, color, alpha=0.35):
    tt = [t0, t0 + rise, t0 + rise + flat, t0 + 2 * rise + flat]
    aa = [0, amp, amp, 0]
    ax.fill(tt, [y + a for a in aa], color=color, alpha=alpha, lw=0)
    ax.plot(tt, [y + a for a in aa], color=color, lw=1.2)


# RF: sinc 펄스
t = np.linspace(0.4, 1.6, 300)
ax.plot(t, 4 + 0.42 * np.sinc((t - 1.0) * 5) * np.hanning(300), color=C["purple"], lw=1.4)
ax.text(1.35, 4.35, "숙임각 α", ha="left", fontsize=8.5, color=C["purple"])
# Gz: 슬라이스 선택 + 되감기
trap(0.25, 0.15, 1.2, 0.35, 3, C["blue"])
trap(1.75, 0.15, 0.45, -0.39, 3, C["blue"])
ax.text(1.0, 3.42, "슬라이스 선택", ha="center", fontsize=8, color=C["blue"])
# Gy: 위상 부호화 표 (여러 진폭)
for a in np.linspace(-0.38, 0.38, 9):
    tt = [1.75, 1.9, 2.5, 2.65]
    ax.plot(tt, [2, 2 + a, 2 + a, 2], color=C["red"], lw=0.8, alpha=0.8)
ax.text(1.65, 2.0, "TR마다\n한 칸씩", ha="right", va="center", fontsize=8, color=C["red"])
# Gx: 미리 감기(음) + 읽기(양)
trap(1.75, 0.15, 0.45, -0.41, 1, C["blue"])
trap(2.9, 0.15, 1.5, 0.3, 1, C["blue"])
ax.text(2.2, 0.5, "미리 감기", ha="center", va="top", fontsize=8, color=C["blue"])
ax.text(3.95, 1.42, "읽기 경사", ha="left", fontsize=8, color=C["blue"])
# 신호: 에코
te = 3.8
t = np.linspace(3.05, 4.55, 400)
ax.plot(t, 0.38 * np.sinc((t - te) * 4) * np.cos((t - te) * 50), color=C["green"], lw=0.9)
ax.add_patch(plt.Rectangle((3.05, -0.45), 1.5, 0.9, fill=False, ec=C["gray"], ls="--", lw=0.8))
ax.text(3.8, -0.62, "ADC: k-공간 한 줄 표본화", ha="center", va="top", fontsize=8, color=C["gray"])
# TE, TR 표시
ax.annotate("", xy=(te, 4.75), xytext=(1.0, 4.75), arrowprops=dict(arrowstyle="<->", lw=0.9, shrinkA=0, shrinkB=0))
ax.text((1 + te) / 2, 4.8, "TE", ha="center", va="bottom", fontsize=9)
ax.plot([te, te], [-0.45, 4.75], color=C["gray"], ls=":", lw=0.8)
ax.plot([1.0, 1.0], [3.6, 5.2], color=C["gray"], ls=":", lw=0.8)
ax.annotate("", xy=(9.6, 5.2), xytext=(1.0, 5.2), arrowprops=dict(arrowstyle="<->", lw=0.9, shrinkA=0, shrinkB=0))
ax.text(5.3, 5.25, "TR", ha="center", va="bottom", fontsize=9)
ax.plot([9.6, 9.6], [4.5, 5.2], color=C["gray"], ls=":", lw=0.8)
t = np.linspace(9.0, 10.2, 300)
ax.plot(t, 4 + 0.42 * np.sinc((t - 9.6) * 5) * np.hanning(300), color=C["purple"], lw=1.4, alpha=0.6)
ax.text(9.6, 3.6, "다음 펄스", ha="center", va="top", fontsize=8.5, color=C["purple"])
ax.text(7.4, 1.5, "다음 TR에는 $G_y$ 진폭만\n바꾸어 다른 $k_y$ 줄을 얻는다", ha="center", va="center", fontsize=8.5)
ax.set_xlim(-2.2, 10.3)
ax.set_ylim(-1.0, 5.55)
ax.axis("off")
save(fig, __file__)
