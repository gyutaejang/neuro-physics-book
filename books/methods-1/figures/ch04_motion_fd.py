from figstyle import plt, np, save, C

# 합성 움직임: TR 2 s, 300 볼륨. 느린 표류 + 작은 떨림 + 한 볼륨짜리 순간 움직임 5번.

TR, NV = 2.0, 300
SPIKES = [(61, 1.0), (138, 0.7), (139, -0.6), (212, 0.5), (246, 1.3)]


def motion_params(seed=7):
    """6 파라미터 (볼륨 × 6): x, y, z 평행이동 mm, 피치·롤·요 회전 도."""
    rng = np.random.default_rng(seed)
    t = np.arange(NV) * TR
    p = np.zeros((NV, 6))
    jit = [0.016, 0.016, 0.026, 0.016, 0.011, 0.011]
    for j in range(6):
        p[:, j] = np.cumsum(rng.normal(0, jit[j], NV)) * 0.5 + rng.normal(0, jit[j], NV)
    p[:, 2] += 0.35 * t / t[-1]                                  # 머리가 천천히 가라앉음 (z)
    p[:, 3] += 0.25 * t / t[-1]                                  # 함께 고개가 숙여짐 (피치)
    p[:, 2] += 0.02 * np.sin(2 * np.pi * 0.05 * t)                # 호흡에 묻은 겉보기 움직임(접힘)
    shape = np.array([0.18, -0.1, 0.35, 0.3, 0.12, -0.15])
    for v, a in SPIKES:
        p[v, :] += a * shape * 1.0                               # 한 볼륨만 튀고 돌아옴
    return p


def fd_power(p, r=50.0):
    d = np.diff(p, axis=0)
    d[:, 3:] = np.deg2rad(d[:, 3:]) * r
    return np.concatenate([[0.0], np.abs(d).sum(axis=1)])

p = motion_params()
fd = fd_power(p)
t = np.arange(NV)
print("mean FD", fd.mean().round(3), "n>0.2", (fd > 0.2).sum(), "n>0.5", (fd > 0.5).sum(),
      "max", fd.max().round(2))
print("final z", p[-20:, 2].mean().round(2), "pitch", p[-20:, 3].mean().round(2))

fig, axs = plt.subplots(3, 1, figsize=(7.0, 3.9), sharex=True,
                        gridspec_kw=dict(hspace=0.42, height_ratios=[1, 1, 1.1]))
cols = [C["blue"], C["green"], C["red"]]
for j, (n, c) in enumerate(zip(["x (좌우)", "y (앞뒤)", "z (위아래)"], cols)):
    axs[0].plot(t, p[:, j], color=c, lw=1, label=n)
    axs[1].plot(t, p[:, 3 + j], color=c, lw=1, label=["피치 (x축)", "롤 (y축)", "요 (z축)"][j])
axs[0].set_ylabel("평행이동 (mm)")
axs[1].set_ylabel("회전 (°)")
axs[0].legend(fontsize=7.5, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.08))
axs[1].legend(fontsize=7.5, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.08))
axs[0].set_ylim(-0.3, 0.9)
axs[1].set_ylim(-0.3, 0.9)
axs[0].set_title("(가) 볼륨별 6 파라미터 (첫 볼륨 기준)", fontsize=10, loc="right")

a = axs[2]
a.plot(t, fd, color=C["ink"], lw=0.9)
for thr, c in ((0.2, C["gray"]), (0.5, C["red"])):
    a.axhline(thr, color=c, lw=0.8, ls="--")
    a.text(NV + 2, thr, f"{thr} mm", color=c, fontsize=7.5, va="center")
bad = np.where(fd > 0.5)[0]
a.scatter(bad, fd[bad], s=14, color=C["red"], zorder=3)
a.set_ylabel("FD (mm)")
a.set_xlabel(f"볼륨 번호 (TR {TR:.0f} s, 총 {NV * TR / 60:.0f}분)")
a.set_xlim(0, NV)
a.set_ylim(0, fd.max() * 1.12)
a.set_title("(나) 틀별 변위 FD: 느린 표류는 작고, 순간 움직임은 쌍으로 튄다", fontsize=10, loc="right")
save(fig, __file__)
