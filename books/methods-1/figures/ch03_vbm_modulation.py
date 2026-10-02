from scipy import ndimage

from figstyle import plt, np, save, C

# 1차원 VBM: 회백질 띠가 10 mm인 사람 A(위축)와 14 mm인 사람 B를 12 mm 주형에 맞춘다.
dx = 0.05
x = np.arange(-30, 30, dx)
T = 12.0
widths = {"A": 10.0, "B": 14.0}
cols = {"A": C["red"], "B": C["blue"]}


def band(w):
    return ((np.abs(x) <= w / 2)).astype(float)


def smooth(p, fwhm=8.0):
    return ndimage.gaussian_filter1d(p, fwhm / 2.3548 / dx)


res = {}
for k, w in widths.items():
    jac = w / T                                     # 주형 1 mm가 개인 뇌의 몇 mm였는가
    unmod = band(T)                                 # 변형 뒤: 모두 주형 띠와 똑같다
    mod = unmod * jac                               # 변조: 야코비안을 곱해 부피를 보존한다
    res[k] = dict(native=band(w), unmod=unmod, mod=mod, sm=smooth(mod), jac=jac)

if __name__ == "__main__":
    for k, r in res.items():
        print(k, "J=%.3f 원래 부피 %.2f 변조 뒤 적분 %.2f 비변조 적분 %.2f 평활 정점 %.3f" % (
            r["jac"], r["native"].sum() * dx, r["mod"].sum() * dx, r["unmod"].sum() * dx, r["sm"].max()))
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.5), sharey=True, gridspec_kw=dict(wspace=0.12))
    for k, r in res.items():
        off = 0.012 if k == "A" else -0.012
        axs[0].plot(x, r["native"] + off, color=cols[k], lw=1.6, label=f"{k}: {widths[k]:.0f} mm")
        axs[1].plot(x, r["unmod"] + off, color=cols[k], lw=1.6)
        axs[2].plot(x, r["mod"], color=cols[k], lw=1.0, ls=":")
        axs[2].plot(x, r["sm"], color=cols[k], lw=1.7, label=f"{k}: J = {r['jac']:.2f}")
    axs[0].set_title("(가) 개인 공간의 GM", fontsize=9.5)
    axs[1].set_title("(나) 주형 공간, 변조 없음", fontsize=9.5)
    axs[2].set_title("(다) 변조 + 평활화 8 mm", fontsize=9.5)
    axs[0].set_ylabel("GM 값")
    axs[0].legend(fontsize=7.5, loc="upper left")
    axs[2].legend(fontsize=7, loc="upper left", handlelength=1.2)
    axs[1].text(0, 1.12, "A와 B가 똑같다", ha="center", fontsize=8, color=C["ink"])
    for a in axs:
        a.set_xlim(-20, 20)
        a.set_ylim(-0.05, 1.55)
        a.set_xlabel("위치 (mm)")
        a.axvspan(-T / 2, T / 2, color=C["light"], zorder=0, lw=0)
    save(fig, __file__)
