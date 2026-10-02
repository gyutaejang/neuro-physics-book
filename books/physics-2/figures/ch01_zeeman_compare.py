from figstyle import plt, np, save, C

# 전자와 원자핵의 공명 주파수(가)와 체온에서의 정렬 비율(나).
# 정렬 비율(스핀 ½) P = tanh(γħB / 2kT).
hbar, kB, T = 1.054572e-34, 1.380649e-23, 310.0
B = np.logspace(-2, 1.1, 200)
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.3, 3.3), gridspec_kw={"width_ratios": [1.2, 1]})
lines = [("전자", 28025.0, C["red"]), ("¹H", 42.577, C["purple"]), ("³¹P", 17.235, C["green"]),
         ("¹³C", 10.708, C["gray"])]
for name, g, col in lines:
    ax.loglog(B, g * B, color=col, lw=1.8)
    dy = {"³¹P": 1.0, "¹³C": 0.62}.get(name, 1.0)
    ax.text(B[-1] * 1.08, g * B[-1] * dy, name, color=col, fontsize=8.5, va="center")
ax.scatter([0.35], [28025 * 0.35], s=22, color=C["red"], zorder=4)
ax.annotate("EPR 장비\n0.35 T, 9.8 GHz", xy=(0.35, 9809), xytext=(0.013, 2.0e4), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.scatter([3], [127.7], s=22, color=C["purple"], zorder=4)
ax.annotate("MRI 3 T\n128 MHz", xy=(3, 127.7), xytext=(0.6, 1500), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["gray"], lw=0.6))
ax.text(0.034, 30, "약 660배", fontsize=8, color=C["ink"], ha="left", va="center")
ax.annotate("", xy=(0.03, 28025 * 0.03), xytext=(0.03, 42.577 * 0.03),
            arrowprops=dict(arrowstyle="<->", color=C["ink"], lw=0.8))
ax.set_xlim(0.01, 25)
ax.set_ylim(0.05, 1e6)
ax.set_xlabel("자기장 B (T)")
ax.set_ylabel("공명 주파수 (MHz)")
ax.set_title("(가) 공명 주파수는 B에 비례한다", fontsize=10.5)

items = [("전자", 28025.0, C["red"]), ("¹H", 42.577, C["purple"]), ("¹³C", 10.708, C["gray"])]
names, vals, cols = [], [], []
for name, g, col in items:
    P = np.tanh(2 * np.pi * g * 1e6 * hbar * 3 / (2 * kB * T))
    names.append(name); vals.append(P); cols.append(col)
names.append("¹³C 과분극\n(DNP, 예)"); vals.append(0.3); cols.append(C["blue"])
x = np.arange(len(names))
bx.bar(x, vals, color=cols, width=0.6)
bx.set_yscale("log")
bx.set_ylim(1e-6, 1)
labels = ["0.65%", "10 ppm", "2.5 ppm", "약 30%"]
for xi, v, s in zip(x, vals, labels):
    bx.text(xi, v * 1.5, s, ha="center", fontsize=8)
bx.set_xticks(x)
bx.set_xticklabels(names, fontsize=8.5)
bx.set_yticks([1e-6, 1e-4, 1e-2, 1])
bx.set_yticklabels(["10⁻⁶", "10⁻⁴", "10⁻²", "1"])
bx.minorticks_off()
bx.set_ylabel("정렬 비율 (로그)", labelpad=8)
bx.set_title("(나) 3 T, 체온에서의 정렬", fontsize=10.5)
fig.tight_layout()
save(fig, __file__)
