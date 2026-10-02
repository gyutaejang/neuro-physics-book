from scipy.ndimage import gaussian_filter1d
from figstyle import plt, np, save, C

# 1차원 피질 팬텀: 뇌척수액 | 회백질 | 백질 | 회백질 | 뇌척수액 ... (주기 15 mm, 백질 7 mm)
# 회백질 농도 4, 백질 1, 뇌척수액 0. FWHM 6 mm로 흐린 뒤 GTM과 Müller-Gärtner로 보정한다.
dx = 0.05
x = np.arange(0, 60, dx)
sig = 6 / 2.355 / dx
blur = lambda v: gaussian_filter1d(v, sig, mode="wrap")


def phantom(gm, period=15.0, wm=7.0):
    csf = period - wm - 2 * gm
    p = np.mod(x, period)
    lab = np.zeros_like(x, dtype=int)
    lab[((p >= csf / 2) & (p < csf / 2 + gm)) | ((p >= csf / 2 + gm + wm) & (p < csf / 2 + 2 * gm + wm))] = 1
    lab[(p >= csf / 2 + gm) & (p < csf / 2 + gm + wm)] = 2
    return lab


def activity(lab, cg):
    return np.choose(lab, [0.0, cg, 1.0])


def gtm(lab, meas):
    R = [lab == k for k in range(3)]
    G = np.array([[blur(R[j].astype(float))[R[i]].mean() for j in range(3)] for i in range(3)])
    return np.linalg.solve(G, np.array([meas[r].mean() for r in R]))


def mg(lab, meas, cw=1.0):
    g, w = blur((lab == 1).astype(float)), blur((lab == 2).astype(float))
    return ((meas - cw * w) / np.maximum(g, 1e-6))[lab == 1].mean()


cases = [("정상\n(3.0 mm)", 3.0, 4.0), ("위축\n(2.2 mm)", 2.2, 4.0), ("저대사 20%\n(3.0 mm)", 3.0, 3.2)]
vals = []
for name, gm, cg in cases:
    lab = phantom(gm)
    m = blur(activity(lab, cg))
    vals.append((m[lab == 1].mean(), gtm(lab, m)[1], mg(lab, m)))
    print(name.replace("\n", " "), np.round(vals[-1], 3))

fig = plt.figure(figsize=(7.4, 3.0))
gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1], wspace=0.3)
a1, a2 = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
xs = x < 30
for gm, col, ls, lab_txt in [(3.0, C["blue"], "-", "정상 (회백질 3.0 mm)"), (2.2, C["red"], "--", "위축 (회백질 2.2 mm)")]:
    lab = phantom(gm)
    a1.plot(x[xs], activity(lab, 4.0)[xs], color=col, lw=0.9, ls=ls, alpha=0.55)
    a1.plot(x[xs], blur(activity(lab, 4.0))[xs], color=col, lw=1.9, ls=ls, label=lab_txt)
a1.text(4.0, 4.15, "참 농도", fontsize=7.8, color=C["gray"], ha="center")
a1.text(7.5, 0.25, "백질", fontsize=7.8, color=C["gray"], ha="center")
a1.text(15.0, 0.25, "고랑", fontsize=7.8, color=C["gray"], ha="center")
a1.text(22.5, 2.65, "PET 측정\n(FWHM 6 mm)", fontsize=7.8, color=C["ink"], ha="center")
a1.set_xlim(0, 30)
a1.set_ylim(0, 4.8)
a1.set_xlabel("피질을 가로지르는 거리 (mm)")
a1.set_ylabel("방사능 농도 (상대 단위)")
a1.legend(fontsize=7.4, loc="upper right", bbox_to_anchor=(1.0, 1.02), ncol=1)
a1.set_title("(가) 같은 농도, 다른 두께", fontsize=9.5)

w = 0.26
labels = ["보정 전 회백질 ROI", "GTM", "Müller-Gärtner"]
cols = [C["gray"], C["blue"], C["purple"]]
for j in range(3):
    xx = np.arange(3) + (j - 1) * w
    hv = [v[j] for v in vals]
    a2.bar(xx, hv, w * 0.92, color=cols[j], label=labels[j])
    for x0, h in zip(xx, hv):
        a2.text(x0, h + 0.06, f"{h:.2f}" if j == 0 else f"{h:.1f}", ha="center", fontsize=6.8)
for i, (_, _, cg) in enumerate(cases):
    a2.plot([i - 0.42, i + 0.42], [cg, cg], color=C["red"], lw=1, ls=":")
a2.set_xticks(range(3))
a2.set_xticklabels([c[0] for c in cases], fontsize=8)
a2.set_ylim(0, 5.6)
a2.set_ylabel("회백질 농도 추정")
a2.legend(fontsize=7, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.03), columnspacing=0.8)
a2.set_title("(나) 부분 용적 보정 (빨간 점선 = 참값)", fontsize=9.5)
save(fig, __file__)
