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


# 카펫 그림: 회백질 420, 백질 150, 뇌척수액 80 복셀의 합성 시계열 (% 신호 단위).
p = motion_params()
fd = fd_power(p)
rng = np.random.default_rng(11)
nG, nW, nF = 420, 150, 80
t = np.arange(NV) * TR


def lowfreq(n, fl=0.01, fh=0.1):
    f = np.fft.rfftfreq(NV, TR)
    X = (rng.normal(size=(n, f.size)) + 1j * rng.normal(size=(n, f.size)))
    X[:, (f < fl) | (f > fh)] = 0
    x = np.fft.irfft(X, NV, axis=1)
    return x / x.std(axis=1, keepdims=True)


net = lowfreq(4)                                             # 네트워크 시계열 4개
G = (rng.dirichlet(np.ones(4) * 0.3, nG) @ net) * 0.6 + rng.normal(0, 0.55, (nG, NV))
W = rng.normal(0, 0.35, (nW, NV))
F = rng.normal(0, 0.9, (nF, NV)) + 0.5 * np.sin(2 * np.pi * 0.2 * t + rng.uniform(0, 6, (nF, 1)))
# 깊은 숨 (180번째 볼륨 근처): CO2 변화로 회백질 전체가 천천히 내려갔다 올라옴
breath = -1.2 * np.exp(-0.5 * ((t - 180 * TR - 12) / 8) ** 2)
G += breath * rng.uniform(0.6, 1.2, (nG, 1))
W += 0.3 * breath
# 순간 움직임: 그 볼륨에서 모든 조직이 튀고, 경계 복셀일수록 크다
spk = np.zeros(NV)
for v, a in SPIKES:
    spk[v] += abs(a)
edge = lambda n: rng.choice([-1, 1], (n, 1)) * rng.gamma(1.2, 1.0, (n, 1))
G += 2.2 * edge(nG) * spk
W += 1.4 * edge(nW) * spk
F += 3.0 * edge(nF) * spk
Y = np.vstack([G, W, F])                                     # % 신호
dv = np.concatenate([[0], np.sqrt(np.mean(np.diff(Y, axis=1) ** 2, axis=0))])
print("DVARS median", np.median(dv).round(2), "at spikes", dv[[v for v, _ in SPIKES]].round(2))
print("corr FD-DVARS", np.corrcoef(fd, dv)[0, 1].round(2))
Z = (Y - Y.mean(1, keepdims=True)) / Y.std(1, keepdims=True)

fig, axs = plt.subplots(3, 1, figsize=(7.0, 3.6), sharex=True,
                        gridspec_kw=dict(hspace=0.22, height_ratios=[0.75, 0.75, 2.6]))
x = np.arange(NV)
axs[0].plot(x, fd, color=C["ink"], lw=0.9)
axs[0].axhline(0.5, color=C["red"], ls="--", lw=0.8)
axs[0].set_ylabel("FD\n(mm)", fontsize=8.5)
axs[0].set_ylim(0, 1.7)
axs[1].plot(x, dv, color=C["blue"], lw=0.9)
axs[1].set_ylabel("DVARS\n(%)", fontsize=8.5)
axs[1].set_ylim(0, dv.max() * 1.1)
a = axs[2]
a.imshow(Z, aspect="auto", cmap="gray", vmin=-2.2, vmax=2.2, interpolation="nearest",
         extent=(-0.5, NV - 0.5, Z.shape[0], 0))
for y0, y1, lab, c in ((0, nG, "회백질", C["green"]), (nG, nG + nW, "백질", C["gray"]),
                       (nG + nW, nG + nW + nF, "뇌척수액", C["blue"])):
    a.add_patch(plt.Rectangle((-9, y0), 7, y1 - y0, color=c, clip_on=False))
    a.text(-12, (y0 + y1) / 2, lab, ha="right", va="center", fontsize=8.5)
    a.axhline(y1, color="white", lw=0.8)
a.set_yticks([])
a.set_xlim(-0.5, NV - 0.5)
a.set_xlabel("볼륨 번호")
axs[1].text(66, 3.6, "← 순간 움직임 (세로 띠)", fontsize=7.5,
            color=C["red"], va="center")
axs[1].text(186, 2.6, "깊은 숨 ↓", fontsize=7.5,
            color=C["ink"], ha="center", va="center")
for s in ("left",):
    a.spines[s].set_visible(False)
save(fig, __file__)
