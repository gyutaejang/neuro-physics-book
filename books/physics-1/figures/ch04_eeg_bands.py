from figstyle import plt, np, save, C

rng = np.random.default_rng(3)
t = np.linspace(0, 1.0, 2000)
bands = [
    ("델타 δ", "0.5–4 Hz", 2.5, 1.0, "깊은 수면"),
    ("세타 θ", "4–8 Hz", 6, 0.7, "졸림, 기억 과제(해마)"),
    ("알파 α", "8–13 Hz", 10, 0.75, "눈 감은 휴식(후두엽)"),
    ("베타 β", "13–30 Hz", 20, 0.4, "운동 준비, 각성"),
    ("감마 γ", "30–100 Hz", 40, 0.25, "국소 회로 처리"),
]
fig, ax = plt.subplots(figsize=(6.8, 3.6))
for i, (name, rng_txt, f, a, note) in enumerate(bands):
    y0 = -i * 1.9
    sig = a * np.sin(2 * np.pi * f * t + i) * (1 + 0.15 * np.sin(2 * np.pi * 1.3 * t + i))
    ax.plot(t, sig + y0, color=C["blue"], lw=1)
    ax.text(-0.03, y0 + 0.15, name, ha="right", va="center", fontsize=9.5, weight="bold")
    ax.text(-0.03, y0 - 0.5, rng_txt, ha="right", va="center", fontsize=8.5, color=C["gray"])
    ax.text(1.02, y0, note, ha="left", va="center", fontsize=8.5, color="#444")
ax.plot([0, 0.1], [-8.9, -8.9], color=C["ink"], lw=2)
ax.text(0.05, -9.15, "100 ms", ha="center", va="top", fontsize=8)
ax.set_xlim(-0.3, 1.45)
ax.set_ylim(-9.8, 1.3)
ax.axis("off")
save(fig, __file__)
