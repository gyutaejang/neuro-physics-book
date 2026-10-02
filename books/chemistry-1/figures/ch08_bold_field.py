from matplotlib.colors import LinearSegmentedColormap

from figstyle import plt, np, save, C

# 탈산소헤모글로빈이 만드는 자화율 차이와 정맥 주변의 자기장 왜곡.
# 혈액-조직 자화율 차이: Δχ = Hct × Δχ_do × (1 − Y), Δχ_do ≈ 3.4 ppm (SI), Hct = 0.4.
hct, dchi_do = 0.4, 3.4
f0 = 127.7e6  # 3 T 수소 공명 주파수 (Hz)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1, 1.15]))

# 왼쪽: B0에 수직인 무한 원기둥(정맥) 단면 주변의 주파수 이동
dchi = hct * dchi_do * (1 - 0.6) * 1e-6
x = np.linspace(-4, 4, 401)
X, Y = np.meshgrid(x, x)
r2 = X ** 2 + Y ** 2
cos2phi = (Y ** 2 - X ** 2) / np.where(r2 == 0, 1, r2)  # B0는 세로(y) 방향
df = np.where(r2 > 1, dchi / 2 / np.where(r2 == 0, 1, r2) * cos2phi, -dchi / 6) * f0
cmap = LinearSegmentedColormap.from_list("bw", [C["blue"], "white", C["red"]])
im = a1.imshow(df, extent=(-4, 4, -4, 4), origin="lower", cmap=cmap, vmin=-35, vmax=35)
a1.add_patch(plt.Circle((0, 0), 1, fill=False, edgecolor=C["ink"], lw=1))
a1.annotate("", xy=(-3.3, 3.6), xytext=(-3.3, 1.9),
            arrowprops=dict(arrowstyle="-|>", color=C["purple"], lw=1.8, mutation_scale=12))
a1.text(-2.95, 2.75, r"$B_0$", color=C["purple"], fontsize=10, va="center")
a1.text(0, 0, "정맥", ha="center", va="center", fontsize=8.5)
a1.set_xticks([])
a1.set_yticks([])
for s in a1.spines.values():
    s.set_visible(True)
a1.set_title("정맥 주변의 자기장 왜곡 (3 T)", fontsize=9.5)
cb = fig.colorbar(im, ax=a1, fraction=0.046, pad=0.03)
cb.set_label("공명 주파수 이동 (Hz)", fontsize=8.5)
cb.set_ticks([-30, -15, 0, 15, 30])
cb.set_ticklabels(["−30", "−15", "0", "15", "30"])
cb.ax.tick_params(labelsize=8)
a1.set_xlabel("가로·세로: 혈관 반지름의 ±4배", fontsize=8.5)

# 오른쪽: 산소 포화도와 혈액의 자화율 차이
Ysat = np.linspace(0, 100, 200)
a2.plot(Ysat, hct * dchi_do * (1 - Ysat / 100), color=C["purple"], lw=2)
pts = [(98, "동맥 (약 98%)", (-70, 18)), (60, "쉬는 정맥 (약 60%)", (6, 12)), (70, "활성 시 정맥 (약 70%)", (8, 10))]
for yv, lab, off in pts:
    v = hct * dchi_do * (1 - yv / 100)
    a2.scatter([yv], [v], color=C["red"] if "활성" in lab else C["ink"], s=24, zorder=3)
    a2.annotate(lab, xy=(yv, v), xytext=off, textcoords="offset points", fontsize=8.3,
                arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a2.set_xlabel("혈액 산소 포화도 Y (%)")
a2.set_ylabel("혈액 − 조직 자화율 차이 (ppm)")
a2.set_xlim(0, 102)
a2.set_ylim(0, 1.45)
a2.text(3, 0.06, r"Hct 0.4, $\Delta\chi = $ Hct $\times$ 3.4 ppm $\times$ (1 − Y)", fontsize=8,
        color=C["gray"], va="bottom")
fig.tight_layout()
save(fig, __file__)
