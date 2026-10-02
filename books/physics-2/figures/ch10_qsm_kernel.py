from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.2))

# (가) 자화율이 큰 작은 구(반지름 a) 둘레의 장 이동, B0 대비 (단위: Δχ)
x = np.linspace(-4, 4, 401)
X, Z = np.meshgrid(x, x)
R = np.sqrt(X ** 2 + Z ** 2) + 1e-9
cos2 = (Z / R) ** 2
dB = np.where(R > 1, (3 * cos2 - 1) / (3 * R ** 3), 0.0)   # 구 안은 균일 (로런츠 보정 뒤 0)
im = a1.imshow(dB, extent=(-4, 4, -4, 4), origin="lower", cmap="RdBu_r", vmin=-0.25, vmax=0.25)
a1.add_patch(plt.Circle((0, 0), 1, facecolor="white", edgecolor=C["ink"], lw=0.8))
a1.text(0, 0, "Δχ > 0", ha="center", va="center", fontsize=8)
a1.annotate("", xy=(-3.3, 3.6), xytext=(-3.3, 2.0),
            arrowprops=dict(arrowstyle="->", color=C["purple"], lw=1.4))
a1.text(-3.0, 2.8, "$B_0$", color=C["purple"], fontsize=10)
a1.set_xticks([]); a1.set_yticks([])
for s in a1.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=a1, shrink=0.8, pad=0.03)
cb.set_label("장 이동 ΔB/(Δχ·$B_0$)", fontsize=8)
cb.ax.tick_params(labelsize=7.5)
a1.set_title("(가) 공간: 쌍극자 무늬", fontsize=9.5)

# (나) k-공간 핵: D(k) = 1/3 − kz²/k²
k = np.linspace(-1, 1, 401)
KX, KZ = np.meshgrid(k, k)
K2 = KX ** 2 + KZ ** 2 + 1e-12
Dk = 1 / 3 - KZ ** 2 / K2
im2 = a2.imshow(Dk, extent=(-1, 1, -1, 1), origin="lower", cmap="RdBu_r", vmin=-0.67, vmax=0.67)
th = np.degrees(np.arccos(1 / np.sqrt(3)))
for sgn in (1, -1):
    xx = np.array([-1, 1])
    a2.plot(xx, sgn * xx / np.tan(np.radians(th)), color=C["ink"], lw=1.0, ls="--")
a2.set_xlim(-1, 1); a2.set_ylim(-1, 1)
a2.text(0.0, 0.7, f"D = 0인 원뿔\n(kz 축과 {th:.1f}°)", fontsize=8, ha="center",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.5))
a2.set_xlabel("$k_x$")
a2.set_ylabel("$k_z$ ($B_0$ 방향)")
a2.set_xticks([]); a2.set_yticks([])
cb2 = fig.colorbar(im2, ax=a2, shrink=0.8, pad=0.03)
cb2.set_label("D(k)", fontsize=8)
cb2.ax.tick_params(labelsize=7.5)
a2.set_title("(나) k-공간: 나눗셈이 막히는 곳", fontsize=9.5)
fig.tight_layout(w_pad=1.5)
save(fig, __file__)
