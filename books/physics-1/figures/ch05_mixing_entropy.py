from figstyle import plt, np, save, C

rng = np.random.default_rng(5)
fig = plt.figure(figsize=(7.4, 2.6))
a1 = fig.add_axes([0.0, 0.08, 0.21, 0.78])
a2 = fig.add_axes([0.29, 0.08, 0.21, 0.78])
a3 = fig.add_axes([0.6, 0.18, 0.38, 0.68])

n = 30
for ax, mixed, title in [(a1, False, "처음: 칸막이 왼쪽"), (a2, True, "나중: 고르게 섞임")]:
    ax.add_patch(plt.Rectangle((0, 0), 2, 1, fill=False, lw=1.2, ec=C["ink"]))
    xs = rng.uniform(0.05, 2 - 0.05 if mixed else 0.95, n)
    ys = rng.uniform(0.05, 0.95, n)
    ax.scatter(xs, ys, s=14, color=C["green"])
    ax.plot([1, 1], [0, 1], color=C["gray"], lw=0.8, ls="--")
    ax.set_xlim(-0.05, 2.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=9.5)
fig.text(0.25, 0.49, "→", fontsize=16, ha="center", va="center")
fig.text(0.25, 0.36, "저절로", fontsize=8.5, ha="center")

N = np.arange(1, 101)
a3.semilogy(N, 0.5 ** N, color=C["red"], lw=1.8)
a3.set_xlabel("분자 수 N")
a3.set_ylabel("모두 왼쪽일 확률", fontsize=9)
a3.set_title("(1/2)ᴺ: 분자가 많을수록 사실상 0", fontsize=10)
for k, lab in [(10, "N = 10: 약 1/1000"), (100, "N = 100: 약 10⁻³⁰")]:
    a3.scatter([k], [0.5 ** k], color=C["red"], s=20, zorder=3)
    a3.annotate(lab, xy=(k, 0.5 ** k), xytext=(k + 12 if k == 10 else k - 52, 0.5 ** k * (1e-3 if k == 10 else 1e2)),
                fontsize=8.5, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
a3.set_xlim(0, 105)
a3.set_yticks([1, 1e-10, 1e-20, 1e-30])
a3.set_yticklabels(["1", "10⁻¹⁰", "10⁻²⁰", "10⁻³⁰"])
save(fig, __file__)
