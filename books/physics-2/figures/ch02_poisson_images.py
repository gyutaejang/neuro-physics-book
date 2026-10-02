from figstyle import plt, np, save, C

# 뇌 단면을 흉내 낸 FDG 섭취 지도(회백질 : 백질 : 뇌척수액 ≈ 4 : 1 : 0.1)에
# 화소당 기대 개수를 정하고 포아송 잡음을 넣는다.
n = 128
y, x = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
r = np.sqrt((x / 0.78) ** 2 + (y / 0.95) ** 2)
th = np.arctan2(y, x)
edge = 0.93 + 0.01 * np.sin(5 * th)
brain = r < edge
wm = r < edge - 0.14 - 0.06 * np.sin(17 * th + 0.6) * (1 + 0.4 * np.sin(5 * th))
vent = (((x + 0.12) / 0.07) ** 2 + (y / 0.3) ** 2 < 1) | (((x - 0.12) / 0.07) ** 2 + (y / 0.3) ** 2 < 1)
deep = (((np.abs(x) - 0.33) / 0.12) ** 2 + ((y + 0.05) / 0.2) ** 2) < 1
act = np.zeros((n, n))
act[brain] = 4.0
act[wm] = 1.0
act[deep] = 3.5
act[vent] = 0.1
act /= 4.0                          # 회백질 = 1

rng = np.random.default_rng(7)
levels = (5, 50, 500)
fig, axes = plt.subplots(1, 4, figsize=(7.4, 2.3))
axes[0].imshow(act, cmap="gray", vmin=0, vmax=1.25)
axes[0].set_title("참 섭취 지도", fontsize=9)
for ax, m in zip(axes[1:], levels):
    img = rng.poisson(act * m) / m
    ax.imshow(img, cmap="gray", vmin=0, vmax=1.25)
    ax.set_title(f"회백질 화소당 {m}개", fontsize=9)
    ax.text(0.5, -0.06, f"상대 잡음 약 {100 / np.sqrt(m):.0f}%", transform=ax.transAxes,
            ha="center", va="top", fontsize=8.5, color=C["red"])
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
fig.tight_layout(w_pad=0.6)
save(fig, __file__)
