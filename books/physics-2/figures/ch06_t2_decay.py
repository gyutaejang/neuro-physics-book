from figstyle import plt, np, save, C

# 3 T 가로 자화 감쇠. 양성자 밀도는 같다고 두고 T2 효과만 본다.
T2 = [("백질", 75, C["blue"]), ("회백질", 95, C["green"]), ("뇌척수액", 2000, C["purple"])]
te = np.linspace(0, 300, 601)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(wspace=0.32))
for name, T, col in T2:
    lab = f"{name} (T2 {T:g} ms)" if T < 1000 else f"{name} (T2 약 2 s)"
    a1.plot(te, np.exp(-te / T), color=col, label=lab)
a1.axvline(90, color=C["red"], lw=0.8, ls="--")
a1.text(95, 0.04, "TE 90 ms", fontsize=8, color=C["red"])
a1.set_ylim(0, 1.05)
a1.set_xlim(0, 300)
a1.set_xlabel("에코 시간 TE (ms)")
a1.set_ylabel("$M_{xy} / M_0$")
a1.set_title("(가) 가로 자화의 감쇠", fontsize=10)
a1.legend(fontsize=8, loc="center right", bbox_to_anchor=(1.0, 0.62))

d = np.exp(-te / 95) - np.exp(-te / 75)
k = d.argmax()
a2.plot(te, d * 100, color=C["red"])
a2.plot(te[k], d[k] * 100, "o", ms=4.5, color=C["red"])
a2.annotate(f"최대: TE ≈ {te[k]:.0f} ms", (te[k], d[k] * 100), xytext=(te[k] + 25, d[k] * 100 + 0.4),
            fontsize=8.5, color=C["red"])
a2.set_xlim(0, 300)
a2.set_ylim(0, 10)
a2.set_xlabel("에코 시간 TE (ms)")
a2.set_ylabel("회백질 − 백질 (%)")
a2.set_title("(나) 두 조직의 신호 차이", fontsize=10)
save(fig, __file__)
