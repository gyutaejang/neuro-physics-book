from figstyle import plt, np, save, C
from ch08_det_tracking import (build_field, track, seeds_A, draw_field, CEN, RAD, VOX, NX, NY)

# 확률적 추적: 매 걸음 섬유 방향을 불확실성(표준편차)만큼 흔들어 5000개를 뿌린다.
rng = np.random.default_rng(5)
field = build_field()
nstream = 5000
seeds = seeds_A(41)


def run(disp):
    dens = np.zeros((NX, NY))
    reach = []
    for k in range(nstream):
        p0, d0 = seeds[rng.integers(len(seeds))]
        p0 = p0 + rng.uniform(-0.3, 0.3, 2)
        s = track(p0, d0, field, "peak", rng=rng, disp=disp, max_len=120)
        ij = np.unique((s // VOX).astype(int), axis=0)
        ok = (ij[:, 0] >= 0) & (ij[:, 0] < NX) & (ij[:, 1] >= 0) & (ij[:, 1] < NY)
        dens[ij[ok, 0], ij[ok, 1]] += 1
        # 활을 따라 간 거리(출발 각도 158°에서 시계 방향으로)
        ang = np.degrees(np.arctan2(s[:, 1] - CEN[1], s[:, 0] - CEN[0]))
        onarc = np.abs(np.hypot(s[:, 0] - CEN[0], s[:, 1] - CEN[1]) - RAD) < 3.0
        prog = (158 - ang[onarc]).max() if onarc.any() else 0
        reach.append(np.radians(max(prog, 0)) * RAD)
    return dens / nstream, np.array(reach)


dens_a, reach_a = run(8.0)
dens_b, reach_b = run(12.0)
L = np.radians(158 - 25) * RAD  # 시야 가장자리에 닿기 전까지
s_axis = np.linspace(0, L, 200)
for name, r in (("8도", reach_a), ("12도", reach_b)):
    print(name, "끝까지(%)", np.mean(r > L - 2) * 100, "절반(%)", np.mean(r > L / 2) * 100)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.2), gridspec_kw=dict(width_ratios=[1.25, 1]))
draw_field(a1, field)
show = np.ma.masked_less(dens_b, 1e-4)
show = np.ma.masked_where(show.mask, np.log10(np.clip(dens_b, 1e-4, None)))
im = a1.imshow(show.T, origin="lower", extent=[0, NX * VOX, 0, NY * VOX], cmap="Blues",
               vmin=-4, vmax=0, alpha=0.95)
cb = fig.colorbar(im, ax=a1, fraction=0.035, pad=0.03)
cb.set_ticks([-4, -3, -2, -1, 0])
cb.set_ticklabels(["0.01%", "0.1%", "1%", "10%", "100%"])
cb.ax.tick_params(labelsize=7.5)
cb.set_label("지나간 스트림라인 비율", fontsize=8)
a1.plot(*np.array([p for p, _ in seeds]).T, color=C["red"], lw=2.2)
a1.text(5, 10.5, "씨앗", fontsize=8, color=C["red"])
a1.set_title("(가) 방문 밀도 (방향 불확실성 12°)", fontsize=9.5)
a1.set_xlabel("x (mm)")
a1.set_ylabel("y (mm)")

for r, col, lab in ((reach_a, C["blue"], "불확실성 8°"), (reach_b, C["red"], "불확실성 12°")):
    frac = [(r >= s).mean() * 100 for s in s_axis]
    a2.plot(s_axis, frac, color=col, lw=1.7, label=lab)
a2.axvline(np.radians(158 - 90) * RAD, color=C["gray"], lw=0.7, ls=":")
a2.text(np.radians(158 - 90) * RAD + 1, 3, "교차", fontsize=8, color=C["gray"], va="bottom")
a2.set_xlabel("씨앗에서 다발을 따라 간 거리 (mm)")
a2.set_ylabel("그 거리까지 간 비율 (%)")
a2.set_title("(나) 멀수록 덜 도달한다", fontsize=9.5)
a2.set_ylim(0, 102)
a2.set_xlim(0, L)
a2.legend(fontsize=8, loc="lower left")
fig.tight_layout()
save(fig, __file__)
