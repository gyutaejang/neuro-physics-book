from figstyle import plt, np, save, C

icp = np.linspace(0, 50, 200)
MAP = 90
cpp = MAP - icp
fig, ax = plt.subplots(figsize=(6.2, 2.7))
ax.axvspan(5, 15, color=C["green"], alpha=0.12)
ax.axvspan(22, 50, color=C["red"], alpha=0.08)
ax.plot(icp, cpp, color=C["blue"], lw=2)
ax.axhline(60, color=C["red"], ls="--", lw=0.9)
ax.text(49, 62, "CPP 60 mmHg 아래: 허혈 위험", ha="right", fontsize=8.5, color=C["red"])
ax.text(10, 22, "정상 ICP\n5–15 mmHg", ha="center", fontsize=8.5, color=C["green"])
ax.text(36, 22, "ICP > 20–22 mmHg\n치료 시작 기준", ha="center", fontsize=8.5, color=C["red"])
ax.scatter([10, 30], [80, 60], color=C["blue"], zorder=3, s=18)
ax.annotate("ICP 10 → CPP 80", xy=(10, 80), xytext=(15, 88), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.annotate("ICP 30 → CPP 60", xy=(30, 60), xytext=(33, 74), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=C["gray"]))
ax.set_xlim(0, 50)
ax.set_ylim(10, 95)
ax.set_xlabel("두개내압 ICP (mmHg)")
ax.set_ylabel("뇌관류압 CPP (mmHg)")
ax.set_title("평균 동맥압 90 mmHg일 때 CPP = MAP − ICP", fontsize=10)
save(fig, __file__)
