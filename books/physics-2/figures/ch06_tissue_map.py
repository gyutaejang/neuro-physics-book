from figstyle import plt, np, save, C

# (가) 3 T 조직별 T1–T2 지도, (나) 장 세기에 따른 T1 (대략값, 측정법에 따라 10–30% 다르다).
tis = [("백질", 0.85, 75, C["blue"]), ("회백질", 1.35, 95, C["green"]),
       ("뇌척수액", 4.0, 2000, C["purple"]), ("동맥혈", 1.65, 150, C["red"]),
       ("정맥혈", 1.65, 55, C["red"]), ("지방", 0.38, 70, C["gray"])]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.3, 3.1), gridspec_kw=dict(wspace=0.38, width_ratios=[1.15, 1]))
for name, t1, t2, col in tis:
    mk = "s" if name == "정맥혈" else "o"
    a1.plot(t1, t2, mk, ms=7, color=col, mfc=col if name != "정맥혈" else "white", mew=1.4)
    dx, dy, ha = {"백질": (1.1, 0.78, "left"), "회백질": (1.08, 0.8, "left"), "뇌척수액": (0.93, 1.0, "right"),
                  "동맥혈": (1.08, 1.0, "left"), "정맥혈": (1.08, 0.95, "left"), "지방": (1.1, 1.0, "left")}[name]
    a1.text(t1 * dx, t2 * dy, name, fontsize=8.5, color=col, ha=ha, va="center")
a1.set_xscale("log"); a1.set_yscale("log")
a1.set_xlim(0.25, 6); a1.set_ylim(30, 4000)
a1.set_xticks([0.3, 0.5, 1, 2, 4]); a1.set_xticklabels(["0.3", "0.5", "1", "2", "4"])
a1.set_yticks([30, 100, 300, 1000, 3000]); a1.set_yticklabels(["30", "100", "300", "1000", "3000"])
a1.minorticks_off()
a1.set_xlabel("T1 (s)")
a1.set_ylabel("T2 (ms)")
a1.set_title("(가) 3 T의 T1과 T2", fontsize=10)

B = np.array([1.5, 3, 7])
for name, vals, col in (("회백질", [1.05, 1.35, 1.95], C["green"]), ("백질", [0.65, 0.85, 1.15], C["blue"]),
                        ("혈액", [1.35, 1.65, 2.2], C["red"]), ("뇌척수액", [4.2, 4.0, 4.1], C["purple"])):
    a2.plot(B, vals, "o-", color=col, ms=4.5, label=name)
a2.set_xticks(B); a2.set_xticklabels(["1.5", "3", "7"])
a2.set_xlim(1, 7.5)
a2.set_ylim(0, 4.8)
a2.set_xlabel("주자기장 $B_0$ (T)")
a2.set_ylabel("T1 (s)")
a2.set_title("(나) 장 세기와 T1", fontsize=10)
a2.legend(fontsize=8, loc="center right", bbox_to_anchor=(1.0, 0.62))
save(fig, __file__)
