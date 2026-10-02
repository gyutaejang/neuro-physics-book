from figstyle import plt, np, save, C

# 수동 케이블 모형: 지름 1 μm, 길이 1 mm 수상돌기 + 세포체(나머지 세포를 뭉뚱그린 구획)
Rm, Ri, Cm = 20e3, 100.0, 1e-6       # Ω·cm², Ω·cm, F/cm²  (τ = 20 ms, λ ≈ 0.7 mm)
d, L, dx = 1e-4, 0.1, 10e-4           # cm
n = int(round(L / dx))
area = np.pi * d * dx
c = Cm * area
gm = area / Rm
ga = 1.0 / (Ri * dx / (np.pi * d ** 2 / 4))
Cs, gs = 100e-12, 5e-9                # 세포체 구획: 100 pF, 5 nS (τ = 20 ms)
N = n + 1                             # 0번이 세포체
Cv = np.r_[Cs, np.full(n, c)]
G = np.zeros((N, N))
G[np.arange(N), np.arange(N)] = np.r_[gs, np.full(n, gm)]
for i in range(N - 1):
    G[i, i] += ga; G[i + 1, i + 1] += ga
    G[i, i + 1] -= ga; G[i + 1, i] -= ga

dt = 0.025e-3
t = np.arange(0, 60e-3, dt)
Esyn = 70e-3                          # 휴지 기준 +70 mV (AMPA 역전 전위 0 mV)
tr, td, gmax = 0.3e-3, 3e-3, 0.5e-9
tp = np.log(td / tr) * tr * td / (td - tr)
gnorm = np.exp(-tp / td) - np.exp(-tp / tr)
gt = gmax * (np.exp(-t / td) - np.exp(-t / tr)) / gnorm


def run(site):
    v = np.zeros(N)
    vs, vl = [], []
    A0 = np.diag(Cv / dt) + G
    for k in range(len(t)):
        A = A0.copy()
        A[site, site] += gt[k]
        b = Cv / dt * v
        b[site] += gt[k] * Esyn
        v = np.linalg.solve(A, b)
        vs.append(v[0]); vl.append(v[site])
    return np.array(vl) * 1e3, np.array(vs) * 1e3


fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0))
sites = [(5, C["blue"], "50 μm"), (30, C["green"], "300 μm"), (70, C["purple"], "700 μm")]
for idx, col, lab in sites:
    vl, vs = run(idx)
    a1.plot(t * 1e3, vl, color=col, lw=1.5, label=f"{lab}: {vl.max():.1f} mV")
    tpk = t[np.argmax(vs)] * 1e3
    a2.plot(t * 1e3, vs, color=col, lw=1.5, label=f"{lab}: {vs.max():.2f} mV, 봉우리 {tpk:.1f} ms")
a1.set_title("시냅스 자리의 막전위", fontsize=10)
a2.set_title("세포체의 막전위", fontsize=10)
for a in (a1, a2):
    a.set_xlabel("시간 (ms)")
    a.set_xlim(0, 40)
a1.set_ylabel("휴지 전위에서의 변화 (mV)")
a1.legend(fontsize=7.8, title="세포체에서의 거리", title_fontsize=7.8)
a2.legend(fontsize=7.6, loc="upper right")
a2.set_ylim(0, None)
fig.tight_layout()
save(fig, __file__)
