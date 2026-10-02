from figstyle import plt, np, save, C

# 수소 1s 전자의 위치를 확률 |ψ|^2 에 따라 무작위로 뽑아 찍고(가),
# 지름 방향 확률 분포 P(r)를 1s, 2s, 2p에 대해 그린다(나). 길이 단위는 보어 반지름 a0.
rng = np.random.default_rng(1)
N = 6000
r = rng.gamma(3, 0.5, N)            # P(r) ∝ r^2 e^{-2r}
cz = rng.uniform(-1, 1, N)
ph = rng.uniform(0, 2 * np.pi, N)
s = np.sqrt(1 - cz ** 2)
x, z = r * s * np.cos(ph), r * cz
sl = np.abs(r * s * np.sin(ph)) < 0.35   # 얇은 단면(|y| < 0.35 a0)만

fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.3, 3.3), gridspec_kw={"width_ratios": [1, 1.35]})
ax.scatter(x[sl], z[sl], s=1.5, color=C["blue"], alpha=0.6, lw=0)
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(th), np.sin(th), color=C["red"], lw=1.2, ls="--")
ax.plot(0, 0, "o", color=C["ink"], ms=3)
ax.text(0.75, -0.95, "보어 궤도\n(r = a₀)", color=C["red"], fontsize=8, ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
ax.set_xlim(-3.2, 3.2)
ax.set_ylim(-3.2, 3.2)
ax.set_aspect("equal")
ax.set_xlabel("x (a₀)")
ax.set_ylabel("z (a₀)")
ax.set_title("(가) 1s 전자를 측정한 위치", fontsize=10.5)

rr = np.linspace(0, 16, 800)
P1 = 4 * rr ** 2 * np.exp(-2 * rr)
P2s = rr ** 2 * (2 - rr) ** 2 * np.exp(-rr) / 8
P2p = rr ** 4 * np.exp(-rr) / 24
bx.plot(rr, P1, color=C["blue"], lw=2, label="1s (n = 1)")
bx.plot(rr, P2s, color=C["green"], lw=1.6, label="2s (n = 2, l = 0)")
bx.plot(rr, P2p, color=C["purple"], lw=1.6, ls="--", label="2p (n = 2, l = 1)")
for n, col in [(1, C["blue"]), (2, C["purple"])]:
    bx.axvline(n ** 2, color=col, lw=0.6, ls=":")
bx.text(1.15, 0.56, "a₀", color=C["blue"], fontsize=8.5)
bx.text(4.15, 0.25, "4a₀", color=C["purple"], fontsize=8.5)
bx.set_xlim(0, 16)
bx.set_ylim(0, 0.62)
bx.set_xlabel("핵에서의 거리 r (a₀ = 0.053 nm)")
bx.set_ylabel("지름 방향 확률 밀도")
bx.legend(fontsize=8, loc="upper right")
bx.set_title("(나) 거리별로 발견될 확률", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
