from figstyle import plt, np, save, C


def j1(x):
    # 1차 베셀 함수 J1(x) = (1/π)∫₀^π cos(τ − x sin τ) dτ 를 수치 적분한다.
    tau = np.linspace(0, np.pi, 801)
    vals = np.cos(tau[None, :] - np.asarray(x)[..., None] * np.sin(tau[None, :]))
    return np.trapezoid(vals, tau, axis=-1) / np.pi

def airy(x):
    v = np.where(np.abs(x) < 1e-9, 1e-9, x)
    return (2 * j1(v) / v) ** 2

# 첫 번째 0점이 x = 1이 되도록 눈금을 맞춘다 (= 레일리 거리 0.61 λ/NA).
k = 3.8317
x = np.linspace(-2.5, 3.5, 800)
fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.6), sharey=True)
for ax, d, title in zip(axes, (2.0, 1.0, 0.6), ("충분히 떨어짐", "레일리 기준 (겨우 구별)", "구별 불가")):
    a = airy(k * x)
    b = airy(k * (x - d))
    ax.plot(x, a, color=C["blue"], lw=0.9, ls="--")
    ax.plot(x, b, color=C["blue"], lw=0.9, ls="--")
    ax.plot(x, a + b, color=C["red"], lw=1.7)
    ax.set_title(title, fontsize=9)
    ax.set_xticks([0, d])
    ax.set_xticklabels(["0", f"{d:g}"], fontsize=8)
    if d < 1:
        ax.get_xticklabels()[0].set_ha("right")
        ax.get_xticklabels()[1].set_ha("left")
    ax.set_xlim(-2, 3)
    ax.set_xlabel("간격 (단위: 0.61 λ/NA)", fontsize=8)
axes[0].set_ylabel("빛의 세기")
axes[0].set_yticks([])
axes[0].text(-1.9, 1.35, "점선: 점 하나의 상\n실선: 두 상의 합", fontsize=7.5, va="top", color=C["ink"])
axes[0].set_ylim(0, 1.6)
fig.tight_layout()
save(fig, __file__)
