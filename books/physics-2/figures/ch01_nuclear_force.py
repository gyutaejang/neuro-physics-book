from figstyle import plt, np, save, C

# 두 양성자 사이의 위치에너지: 쿨롱 반발 1.44 MeV·fm / r 와
# 핵력(도식). 핵력은 유카와 꼴 -V0 e^{-r/a}/(r/a), 도달 거리 a = 1.4 fm에
# 0.5 fm 안쪽의 반발 중심을 더한 그림용 모형이다.
r = np.linspace(0.3, 6, 600)
a = 1.41
UC = 1.44 / r
UN = -60 * np.exp(-r / a) / (r / a) + 5000 * np.exp(-r / 0.2) / (r / 0.2)
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.3, 3.2))
ax.axhline(0, color=C["gray"], lw=0.7)
ax.plot(r, UC, color=C["blue"], lw=1.8, label="전기 반발 (쿨롱)")
ax.plot(r, UN, color=C["red"], lw=1.8, ls="--", label="핵력 (도식)")
ax.plot(r, UC + UN, color=C["ink"], lw=1.4, label="합")
ax.set_xlim(0.3, 4)
ax.set_ylim(-50, 40)
ax.set_xlabel("두 양성자 중심 사이 거리 (fm)")
ax.set_ylabel("위치에너지 (MeV)")
ax.legend(fontsize=8, loc="lower right")
ax.text(0.62, 28, "너무 가까우면\n밀어낸다", fontsize=8, color=C["gray"], ha="left")
ax.set_title("(가) 1–2 fm에서는 핵력이 이긴다", fontsize=10.5)

rr = np.linspace(0.5, 20, 600)
bx.semilogy(rr, 1.44 / rr, color=C["blue"], lw=1.8, label="쿨롱: 1/r로 천천히 줄어든다")
bx.semilogy(rr, 60 * np.exp(-rr / a) / (rr / a), color=C["red"], lw=1.8, ls="--",
            label="핵력: 지수적으로 사라진다")
bx.axvspan(0, 2 * 1.2 * 12 ** (1 / 3), color=C["light"], zorder=0)
bx.text(3.3, 1.3e-5, "¹²C 핵 지름\n(약 5.5 fm)", fontsize=8, color=C["gray"], ha="center")
bx.set_xlim(0.5, 20)
bx.set_ylim(1e-6, 300)
bx.set_xlabel("거리 (fm)")
bx.set_ylabel("크기 (MeV, 로그)")
bx.legend(fontsize=8, loc="upper right")
bx.set_title("(나) 멀어지면 전기 반발만 남는다", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
