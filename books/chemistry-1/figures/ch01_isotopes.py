from figstyle import plt, np, save, C

# (Z, N, 기호, 질량수, 상태, 메모)  상태: s=안정, p=PET 방사성, r=기타 방사성
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
nuc = [
    (1, 0, "H", 1, "s", "99.98%"), (1, 1, "H", 2, "s", "0.016%"), (1, 2, "H", 3, "r", "12년"),
    (2, 1, "He", 3, "s", ""), (2, 2, "He", 4, "s", ""),
    (3, 3, "Li", 6, "s", ""), (3, 4, "Li", 7, "s", ""),
    (4, 5, "Be", 9, "s", ""),
    (5, 5, "B", 10, "s", ""), (5, 6, "B", 11, "s", ""),
    (6, 5, "C", 11, "p", "20분"), (6, 6, "C", 12, "s", "98.9%"), (6, 7, "C", 13, "s", "1.1%"),
    (6, 8, "C", 14, "r", "5730년"),
    (7, 6, "N", 13, "p", "10분"), (7, 7, "N", 14, "s", "99.6%"), (7, 8, "N", 15, "s", "0.4%"),
    (8, 7, "O", 15, "p", "2분"), (8, 8, "O", 16, "s", "99.8%"), (8, 9, "O", 17, "s", ""),
    (8, 10, "O", 18, "s", "0.2%"),
    (9, 9, "F", 18, "p", "110분"), (9, 10, "F", 19, "s", "100%"),
]
fig, ax = plt.subplots(figsize=(6.6, 4.3))
for Z, N, sym, A, st, memo in nuc:
    if st == "s":
        fc, ec, tc = C["light"], C["blue"], C["ink"]
    elif st == "p":
        fc, ec, tc = "#fbe3d6", C["red"], C["red"]
    else:
        fc, ec, tc = "white", C["gray"], C["gray"]
    ax.add_patch(plt.Rectangle((N - 0.46, Z - 0.46), 0.92, 0.92, facecolor=fc, edgecolor=ec, lw=1.1))
    ax.text(N, Z + (0.12 if memo else 0), str(A).translate(SUP) + sym, ha="center", va="center",
            fontsize=9.5, color=tc, weight="bold" if st == "p" else "normal")
    if memo:
        ax.text(N, Z - 0.25, memo, ha="center", va="center", fontsize=6.5, color=tc)
ax.plot([-0.5, 10.5], [-0.5, 10.5], color=C["gray"], lw=0.7, ls=":")
ax.text(10.4, 9.75, "N = Z", fontsize=8, color=C["gray"], ha="right")
names = {1: "수소", 2: "헬륨", 3: "리튬", 4: "베릴륨", 5: "붕소", 6: "탄소", 7: "질소", 8: "산소", 9: "플루오린"}
ax.set_yticks(range(1, 10))
ax.set_yticklabels([f"{names[z]} Z={z}" for z in range(1, 10)], fontsize=8)
ax.set_xticks(range(0, 11))
ax.set_xlim(-0.6, 10.6)
ax.set_ylim(0.4, 9.7)
ax.set_xlabel("중성자 수 N")
ax.set_ylabel("양성자 수 Z (원소를 정한다)")
ax.tick_params(length=0)
for sp in ("left", "bottom"):
    ax.spines[sp].set_visible(False)
h = [plt.Rectangle((0, 0), 1, 1, facecolor=C["light"], edgecolor=C["blue"]),
     plt.Rectangle((0, 0), 1, 1, facecolor="#fbe3d6", edgecolor=C["red"]),
     plt.Rectangle((0, 0), 1, 1, facecolor="white", edgecolor=C["gray"])]
ax.legend(h, ["안정 (% = 자연 존재비)", "PET용 방사성 (반감기)", "기타 방사성 (반감기)"],
          loc="lower right", fontsize=8)
save(fig, __file__)
