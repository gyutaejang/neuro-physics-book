from figstyle import plt, np, save, C

gbar = 42.577e6          # Hz/T
B1 = 10e-6               # 10 μT
f1 = gbar * B1           # B₁ 둘레 회전 빠르기 ≈ 426 Hz
t90 = 0.25 / f1          # 90° 펄스 길이 ≈ 0.59 ms

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 3.1))
t = np.linspace(0, 1.3e-3, 400)
ang = 2 * np.pi * f1 * t
ax1.plot(t * 1e3, np.cos(ang), color=C["blue"], lw=2, label="세로 성분 $M_z/M_0$")
ax1.plot(t * 1e3, np.sin(ang), color=C["red"], lw=2, label="가로 성분 $M_{xy}/M_0$")
ax1.axhline(0, color=C["gray"], lw=0.6)
for tt, lab in [(t90, "90°"), (2 * t90, "180°")]:
    ax1.axvline(tt * 1e3, color=C["gray"], lw=0.8, ls="--")
    ax1.text(tt * 1e3 + 0.02, 1.08, f"{lab}\n{tt * 1e3:.2f} ms", fontsize=8.3, va="bottom")
ax1.set_xlim(0, 1.3)
ax1.set_ylim(-1.15, 1.45)
ax1.set_yticks([-1, 0, 1])
ax1.set_xlabel("펄스를 켠 시간 τ (ms)")
ax1.set_ylabel("성분 크기")
ax1.legend(loc="lower left", fontsize=8)
ax1.set_title("(가) $B_1$ = 10 μT: 숙임각 = $\\gamma B_1 \\tau$", fontsize=10.5)


# (나) 공명에서 벗어난 스핀: 회전 좌표계의 유효 자기장 둘레 회전
def rot(v, axis, a):
    axis = axis / np.linalg.norm(axis)
    return v * np.cos(a) + np.cross(axis, v) * np.sin(a) + axis * np.dot(axis, v) * (1 - np.cos(a))


df = np.linspace(-3000, 3000, 601)
mxy, mz = [], []
for d in df:
    beff = np.array([f1, 0.0, d])        # Hz 단위 유효장 (회전 좌표계)
    m = rot(np.array([0.0, 0.0, 1.0]), -beff, 2 * np.pi * np.linalg.norm(beff) * t90)
    mxy.append(np.hypot(m[0], m[1]))
    mz.append(m[2])
ax2.plot(df / 1e3, mxy, color=C["red"], lw=2, label="$M_{xy}/M_0$")
ax2.plot(df / 1e3, mz, color=C["blue"], lw=1.2, ls="--", label="$M_z/M_0$")
ax2.axhline(0, color=C["gray"], lw=0.6)
ax2.annotate("1 ppm (3 T)\n= 128 Hz", xy=(0.128, np.interp(128, df, mxy)), xytext=(-2.9, 0.62),
             fontsize=8.3, arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax2.set_xlim(-3, 3)
ax2.set_ylim(-0.25, 1.15)
ax2.set_xlabel("공명 주파수와의 차이 Δf (kHz)")
ax2.set_ylabel("펄스 직후 성분")
ax2.legend(loc="center right", fontsize=8, bbox_to_anchor=(1.0, 0.5))
ax2.set_title("(나) 같은 90° 펄스, 다른 주파수", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
