from figstyle import plt, np, save, C

hbar, k, e = 1.054571817e-34, 1.380649e-23, 1.602176634e-19
g = 2.6752218744e8           # 수소 핵 자기회전비 (rad/s/T)
kT = k * 310.15

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 3.1))
B = np.linspace(0, 7.6, 200)
E = 0.5 * g * hbar * B / e * 1e6   # μeV
ax1.plot(B, -E, color=C["blue"], lw=2)
ax1.plot(B, E, color=C["red"], lw=2)
ax1.plot([0, 7.6], [0, 0], color=C["gray"], lw=0.6, ls=":")
ax1.text(7.55, -E[-1] - 0.12, "B₀와 같은 방향\n(낮은 에너지)", ha="right", va="top", fontsize=8, color=C["blue"])
ax1.text(7.55, E[-1] + 0.12, "B₀와 반대 방향\n(높은 에너지)", ha="right", va="bottom", fontsize=8, color=C["red"])
for b0 in [1.5, 3, 7]:
    d = 0.5 * g * hbar * b0 / e * 1e6
    f = g * b0 / (2 * np.pi) / 1e6
    ax1.annotate("", xy=(b0, d), xytext=(b0, -d),
                 arrowprops=dict(arrowstyle="<->", color=C["purple"], lw=1.2, shrinkA=0, shrinkB=0))
    if b0 < 5:
        ax1.text(b0, -d - 0.1, f"{b0:g} T\n{f:.0f} MHz", ha="center", va="top", fontsize=7.8, color=C["purple"])
    else:
        ax1.text(b0 - 0.12, 0.06, f"{b0:g} T\n{f:.0f} MHz", ha="right", fontsize=7.8, color=C["purple"])
ax1.set_xlim(0, 7.6)
ax1.set_ylim(-1.2, 1.2)
ax1.set_xlabel("주자기장 B₀ (T)")
ax1.set_ylabel("에너지 (μeV)")
ax1.set_title("(가) 제만 분열: ΔE = γħB₀ = hf₀", fontsize=10.5)

# (나) 정렬 여분 (볼츠만)
ex = np.tanh(g * hbar * B / (2 * kT)) * 1e6
ax2.plot(B, ex, color=C["purple"], lw=2)
for b0 in [1.5, 3, 7]:
    v = np.tanh(g * hbar * b0 / (2 * kT)) * 1e6
    ax2.plot([b0], [v], "o", color=C["purple"], ms=5)
    ax2.text(b0 - 0.15, v + 1.0, f"{v:.0f} ppm", ha="right", fontsize=8.5)
ax2.text(0.3, 21, "37 °C에서 kT ≈ 26.7 meV\n= 3 T의 ΔE의 약 5만 배", fontsize=8.3, va="top", color=C["ink"])
ax2.set_xlim(0, 7.6)
ax2.set_ylim(0, 26)
ax2.set_xlabel("주자기장 B₀ (T)")
ax2.set_ylabel("정렬 여분 (ppm)")
ax2.set_title("(나) 100만 개 중 몇 개가 남는가", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
