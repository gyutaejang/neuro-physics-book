from figstyle import plt, np, save, C
from matplotlib.patches import Rectangle

# 장난감 순문제: 반무한 균질 도체(전도율 0.33 S/m, 두개골 없음)의 표면에 센서 32개(0.75 cm 간격),
# 그 아래 x = −10…10 cm, 깊이 2…6 cm에 0.5 cm 간격으로 수직(지름 방향) 쌍극자 자리 369개.
# 표면이 절연 경계이므로 무한 매질 전위의 2배가 된다.
xs = (np.arange(32) - 15.5) * 0.75
xg = np.arange(-10, 10.01, 0.5)
dg = np.arange(2.0, 6.01, 0.5)
X, D = np.meshgrid(xg, dg)
sx, sd = X.ravel(), D.ravel()


def lead(xsens, sx, sd, sig=0.33):
    dx = (xsens[:, None] - sx[None, :]) * 1e-2
    d = sd[None, :] * 1e-2
    return 2 * 1e-9 * d / (4 * np.pi * sig * (dx**2 + d**2) ** 1.5) * 1e6   # μV / (nA·m)


L = lead(xs, sx, sd)
pick = [(-4.0, 2.0, C["red"]), (4.0, 5.0, C["purple"])]
cols = [int(np.where(np.isclose(sx, x) & np.isclose(sd, d))[0][0]) for x, d, _ in pick]

fig = plt.figure(figsize=(7.3, 3.4))
gs = fig.add_gridspec(2, 2, width_ratios=[1.05, 1], height_ratios=[1, 1.05], hspace=0.12, wspace=0.28)
a1 = fig.add_subplot(gs[0, 0])
a2 = fig.add_subplot(gs[1, 0], sharex=a1)
a3 = fig.add_subplot(gs[:, 1])

for (x, d, c), k in zip(pick, cols):
    a1.plot(xs, L[:, k], "o-", ms=2.5, lw=1.2, color=c)
    print("깊이", d, "cm 최대", L[:, k].max(), "μV/(nA·m)")
a1.text(-4, 1.28, "얕은 자리(깊이 2 cm)", color=C["red"], fontsize=8, ha="center")
a1.text(4.6, 0.3, "깊은 자리(5 cm)", color=C["purple"], fontsize=8, ha="center")
a1.set_ylabel("센서 값\n(μV, 1 nA·m당)", fontsize=8.5)
a1.set_ylim(0, 1.5)
a1.set_title("(가) 자리 하나가 센서에 남기는 무늬 = L의 한 열", fontsize=9.5)
plt.setp(a1.get_xticklabels(), visible=False)

a2.plot(sx, -sd, ".", ms=1.6, color=C["gray"])
a2.plot(xs, np.zeros_like(xs), "v", ms=4, color=C["blue"])
for (x, d, c) in pick:
    a2.annotate("", xy=(x, -d + 0.55), xytext=(x, -d - 0.55),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6))
a2.axhline(0, color=C["ink"], lw=0.8)
a2.text(11.9, 0.35, "센서 32개", color=C["blue"], fontsize=8, ha="right", va="bottom")
a2.text(-10.5, -6.6, "소스 자리 369개 (0.5 cm 간격)", color=C["gray"], fontsize=8, ha="left", va="top")
a2.set_ylim(-8.0, 1.2)
a2.set_xlim(-12, 12)
a2.set_yticks([0, -2, -4, -6])
a2.set_yticklabels(["0", "2", "4", "6"])
a2.set_ylabel("깊이 (cm)", fontsize=8.5)
a2.set_xlabel("가로 위치 x (cm)")

im = a3.imshow(L, aspect="auto", cmap="Blues", vmin=0, vmax=0.6, interpolation="nearest",
               extent=[-0.5, L.shape[1] - 0.5, 31.5, -0.5])
for b in range(1, len(dg)):
    a3.axvline(b * len(xg) - 0.5, color="white", lw=0.6)
for (x, d, c), k in zip(pick, cols):
    a3.add_patch(Rectangle((k - 2, -0.5), 4, 32, fill=False, ec=c, lw=1.4))
a3.set_xticks([(i + 0.5) * len(xg) for i in range(0, len(dg), 2)])
a3.set_xticklabels([f"{d:g}" for d in dg[::2]])
a3.set_xlabel("열 = 소스 자리 (깊이별 묶음, cm)")
a3.set_ylabel("행 = 센서 번호")
a3.set_yticks([0, 15, 31])
a3.set_yticklabels(["1", "16", "32"])
a3.set_title("(나) 리드필드 행렬 L (32 × 369)", fontsize=9.5)
cb = fig.colorbar(im, ax=a3, shrink=0.8, pad=0.02, extend="max")
cb.ax.tick_params(labelsize=7.5)
cb.ax.set_title("μV", fontsize=8)
save(fig, __file__)
