from figstyle import plt, np, save, C

g, m = 9.8, 1.0
xs = np.linspace(0, 10, 400)
def h(x):
    return 1.0 * np.exp(-(x / 2.4) ** 2) + 0.5 * np.exp(-((x - 7.2) / 1.2) ** 2)


H = h(xs)
valley = (xs > 2) & (xs < 6)
xB = float(xs[valley][np.argmin(H[valley])])
H = H - H[valley].min()
H = H * 1.25 / H[0]  # A(왼쪽 끝)의 높이를 1.25 m로 맞춘다
x_pts = {"A": 0.0, "B": xB, "C": 7.2}
h_pts = {k: float(np.interp(v, xs, H)) for k, v in x_pts.items()}
E = h_pts["A"]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [1.6, 1]})
a1.fill_between(xs, -0.1, H, color=C["light"])
a1.plot(xs, H, color=C["ink"], lw=1.2)
a1.axhline(E, color=C["gray"], ls="--", lw=0.8)
a1.text(9.9, E + 0.04, "전체 에너지 수준", ha="right", va="bottom", fontsize=8, color=C["gray"])
for k, x in x_pts.items():
    y = h_pts[k]
    a1.scatter([x], [y + 0.07], s=70, color=C["blue"], zorder=3)
    a1.text(x, y + 0.2, k, ha="center", va="bottom", fontsize=10, weight="bold")
a1.set_xlim(-0.4, 10)
a1.set_ylim(-0.1, 1.6)
a1.set_xticks([])
a1.set_ylabel("높이 h (m)")
a1.set_title("마찰 없는 언덕 위의 공")

labels = list(x_pts)
pe = np.array([m * g * h_pts[k] for k in labels])
ke = m * g * E - pe
a2.bar(labels, pe, color=C["blue"], alpha=0.8, label="위치에너지 mgh")
a2.bar(labels, ke, bottom=pe, color=C["red"], alpha=0.8, label="운동에너지 ½mv²")
a2.axhline(m * g * E, color=C["gray"], ls="--", lw=0.8)
a2.set_ylim(0, m * g * E * 1.45)
a2.set_ylabel("에너지 (J, 질량 1 kg)")
a2.set_title("두 에너지의 합은 같다")
a2.legend(loc="upper center", fontsize=8, ncol=1)
fig.tight_layout()
print({k: round(v, 2) for k, v in h_pts.items()})
save(fig, __file__)
