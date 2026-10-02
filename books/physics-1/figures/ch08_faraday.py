from figstyle import plt, np, save, C

# 자석을 코일에 가까이 가져갔다가(0–1 s), 멈추고(1–2 s), 다시 멀리 뺀다(2–3 s).
t = np.linspace(0, 3, 1200)


def smooth(u):
    u = np.clip(u, 0, 1)
    return u * u * (3 - 2 * u)


phi = np.where(t < 1, smooth(t), np.where(t < 2, 1.0, 1 - smooth(t - 2)))
emf = -np.gradient(phi, t)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 3.8), sharex=True,
                               gridspec_kw=dict(hspace=0.15))
ax1.plot(t, phi, color=C["purple"])
ax1.set_ylabel("자기 선속 Φ", fontsize=9.5)
ax1.set_ylim(-0.1, 1.35)
ax1.set_yticks([0, 1])
for x0, lab in ((0.5, "가까워진다"), (1.5, "멈춰 있다"), (2.5, "멀어진다")):
    ax1.text(x0, 1.18, lab, ha="center", fontsize=8.5)
for ax in (ax1, ax2):
    for x0 in (1, 2):
        ax.axvline(x0, color=C["gray"], lw=0.6, ls=":")

ax2.plot(t, emf, color=C["blue"])
ax2.axhline(0, color=C["gray"], lw=0.6)
ax2.set_ylabel("기전력 −dΦ/dt", fontsize=9.5)
ax2.set_ylim(-1.8, 1.8)
ax2.set_yticks([-1.5, 0, 1.5])
ax2.set_xlabel("시간 (s)")
ax2.text(1.5, 0.25, "Φ가 커도 변하지 않으면 0", ha="center", fontsize=8.5, color=C["blue"])
ax2.text(0.5, -0.75, "Φ 증가 → 음(−)", ha="center", fontsize=8.5, color=C["gray"])
ax2.text(2.5, 0.75, "Φ 감소 → 양(+)", ha="center", fontsize=8.5, color=C["gray"])
ax2.set_xlim(0, 3)
save(fig, __file__)
