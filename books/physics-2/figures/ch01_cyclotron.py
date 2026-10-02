from figstyle import plt, np, save, C
from matplotlib.patches import Wedge

# 사이클로트론. 균일한 자기장(종이로 들어감) 속 두 D자 전극 사이 틈에서
# 양성자가 반 바퀴마다 가속된다. 반지름은 r = mv/(eB) 이고 에너지 E ∝ v^2 이므로
# k번째 반원의 반지름은 sqrt(k)에 비례한다. 돌림 주기는 반지름과 무관하다.
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.3, 3.4), gridspec_kw={"width_ratios": [1.15, 1]})
R = 1.0
gap = 0.06
ax.add_patch(Wedge((-gap, 0), R, 90, 270, color=C["light"], ec=C["gray"]))
ax.add_patch(Wedge((gap, 0), R, -90, 90, color=C["light"], ec=C["gray"]))
for xx in np.linspace(-0.85, 0.85, 6):
    for yy in np.linspace(-0.85, 0.85, 6):
        if xx ** 2 + yy ** 2 < 0.8:
            ax.plot(xx, yy, "x", ms=4, color=C["purple"], mew=0.8, alpha=0.6)
# 궤적: 반원을 이어 붙인다. 자기장이 종이로 들어가므로 양성자는 시계 반대 방향으로 돈다.
# 오른쪽 반원은 아래→위, 왼쪽 반원은 위→아래. k번째 반지름은 sqrt(k)에 비례한다.
K = 20
r0 = 0.88 / np.sqrt(K)
xs, ys = [], []
c = 0.0
ystart = -r0
for k in range(1, K + 1):
    rk = r0 * np.sqrt(k)
    if k % 2:      # 오른쪽: 시작점이 바닥
        c = ystart + rk
        th = np.linspace(-np.pi / 2, np.pi / 2, 80)
        x, y = gap + rk * np.cos(th), c + rk * np.sin(th)
    else:          # 왼쪽: 시작점이 꼭대기
        c = ystart - rk
        th = np.linspace(np.pi / 2, 3 * np.pi / 2, 80)
        x, y = -gap + rk * np.cos(th), c + rk * np.sin(th)
    xs.extend(x)
    ys.extend(y)
    ystart = y[-1]
xs, ys = np.array(xs), np.array(ys)
ax.plot(xs, ys, color=C["red"], lw=1.0)
yo = ys[-1]
ax.plot([xs[-1], 1.25], [yo, yo], color=C["red"], lw=1.0)
ax.annotate("", xy=(1.34, yo), xytext=(1.2, yo), arrowprops=dict(arrowstyle="-|>", color=C["red"]))
ax.text(1.38, yo, "표적으로\n(약 10–20 MeV)", fontsize=8, va="center")
ax.plot(0, 0, "o", color=C["red"], ms=4)
ax.text(-0.55, 1.08, "D 전극", fontsize=8, ha="center")
ax.text(0.55, 1.08, "D 전극", fontsize=8, ha="center")
ax.text(0, -1.17, "틈의 교류 전압이 반 바퀴마다 밀어 준다", fontsize=8, ha="center", color=C["blue"])
ax.text(1.05, 0.85, "× 자기장 B\n(종이로 들어감)", fontsize=8, color=C["purple"], ha="left")
ax.set_xlim(-1.15, 1.9)
ax.set_ylim(-1.3, 1.2)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("(가) 위에서 본 사이클로트론", fontsize=10.5)

# (나) 반지름과 주기
mp, e = 1.67262e-27, 1.602177e-19
B = 1.9
E = np.linspace(0.1, 18, 200)
v = np.sqrt(2 * E * 1e6 * e / mp)
r = mp * v / (e * B)
bx.plot(E, r * 100, color=C["red"], lw=1.8)
bx.set_xlabel("양성자 운동 에너지 (MeV)")
bx.set_ylabel("궤도 반지름 (cm)", color=C["red"])
bx.set_ylim(0, 35)
cx2 = bx.twinx()
cx2.spines["right"].set_visible(True)
cx2.axhline(e * B / (2 * np.pi * mp) / 1e6, color=C["purple"], lw=1.8, ls="--")
cx2.set_ylim(0, 35)
cx2.set_ylabel("돌림 주파수 (MHz)", color=C["purple"])
cx2.text(9, 30.3, "주파수 29 MHz로 일정", color=C["purple"], fontsize=8.5, ha="center")
bx.text(12, 18, "반지름 ∝ √E", color=C["red"], fontsize=8.5)
bx.set_title("(나) B = 1.9 T일 때", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
