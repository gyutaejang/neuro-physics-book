from figstyle import plt, np, save, C

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1.25, 1]})
D = 1.0  # μm²/ms 단위로 생각한다
x = np.linspace(-12, 12, 500)
for t, col in [(1, C["blue"]), (4, C["purple"]), (16, C["gray"])]:
    c = np.exp(-x ** 2 / (4 * D * t)) / np.sqrt(4 * np.pi * D * t)
    a1.plot(x, c, color=col, lw=1.6, label=f"t = {t}")
    w = np.sqrt(2 * D * t)
    a1.annotate("", xy=(w, c.max() * np.exp(-0.5)), xytext=(0, c.max() * np.exp(-0.5)),
                arrowprops=dict(arrowstyle="->", color=col, lw=0.9))
a1.set_xlabel("위치 x")
a1.set_ylabel("농도")
a1.set_yticks([])
a1.set_title("한곳에 풀어 놓은 분자의 퍼짐")
a1.legend(fontsize=8.5, title="시간", title_fontsize=8.5)
a1.text(4.5, 0.2, "시간 4배 →\n폭 2배", fontsize=8.5)

# 오른쪽: 농도 기울기와 흐름 (픽의 법칙)
xs = np.linspace(0, 10, 200)
cs = 1 - 0.08 * xs
a2.plot(xs, cs, color=C["blue"], lw=1.8)
a2.fill_between(xs, 0, cs, color=C["light"])
for x0 in (2, 5, 8):
    a2.annotate("", xy=(x0 + 1.4, 0.12), xytext=(x0, 0.12),
                arrowprops=dict(arrowstyle="->", color=C["red"], lw=1.6))
a2.text(5, 0.22, "흐름 J (진한 곳 → 묽은 곳)", ha="center", fontsize=8.5, color=C["red"])
a2.annotate("기울기 dc/dx < 0", xy=(6, 1 - 0.48), xytext=(5.0, 0.85), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
a2.set_xlabel("위치 x")
a2.set_ylabel("농도 c")
a2.set_yticks([])
a2.set_ylim(0, 1.05)
a2.set_title("픽의 법칙: J = −D dc/dx")
fig.tight_layout()
save(fig, __file__)
