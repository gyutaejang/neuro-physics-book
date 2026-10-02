from figstyle import plt, np, save, C

syms = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr "
        "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu "
        "Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn").split()


def pos(Z):
    """원자번호 → (주기, 족). 란타넘족(57–71)은 아래 따로 뺀 줄(주기 8.4)에 둔다."""
    if Z == 1:
        return 1, 1
    if Z == 2:
        return 1, 18
    starts = [(3, 2), (11, 3), (19, 4), (37, 5), (55, 6)]
    for z0, p in reversed(starts):
        if Z >= z0:
            k = Z - z0
            break
    if p in (2, 3):
        return p, (k + 1 if k < 2 else k + 11)
    if p in (4, 5):
        return p, k + 1
    # 6주기
    if k < 2:
        return 6, k + 1
    if 2 <= k <= 16:  # La–Lu
        return 7.4, k + 1  # 3족부터 시작
    return 6, k - 13


body = {"H", "C", "N", "O", "P", "S"}
ions = {"Na", "K", "Ca", "Mg", "Cl"}
metals = {"Fe", "Cu", "Zn", "Mn", "Gd"}
other = {"F": "PET ¹⁸F", "I": "CT 조영제", "Li": "기분 안정제"}
nonmetal = {"H", "He", "C", "N", "O", "F", "Ne", "P", "S", "Cl", "Ar", "Se", "Br", "Kr", "I", "Xe", "Rn"}

fig, ax = plt.subplots(figsize=(7.4, 4.6))
s = 1.0
for Z, sym in enumerate(syms, start=1):
    p, g = pos(Z)
    x, y = g, -p
    if sym in body:
        fc, ec, tc = C["blue"], C["blue"], "white"
    elif sym in ions:
        fc, ec, tc = C["green"], C["green"], "white"
    elif sym in metals:
        fc, ec, tc = C["purple"], C["purple"], "white"
    elif sym in other:
        fc, ec, tc = "white", C["red"], C["red"]
    else:
        fc, ec, tc = ("#f3f3f3" if sym in nonmetal else "white"), "#bbbbbb", "#888888"
    ax.add_patch(plt.Rectangle((x - 0.46, y - 0.46), 0.92, 0.92, facecolor=fc, edgecolor=ec, lw=0.9))
    ax.text(x, y + 0.2, str(Z), ha="center", va="center", fontsize=5, color=tc)
    ax.text(x, y - 0.1, sym, ha="center", va="center", fontsize=8,
            color=tc, weight="bold" if tc == "white" else "normal")
# 란타넘족 자리 표시
ax.add_patch(plt.Rectangle((3 - 0.46, -6 - 0.46), 0.92, 0.92, facecolor="white", edgecolor="#bbbbbb", lw=0.9, ls="--"))
ax.text(3, -6, "57–71", ha="center", va="center", fontsize=5.5, color="#888888")
ax.text(2.4, -7.4, "란타넘족", ha="right", va="center", fontsize=7.5, color=C["gray"])
for g in range(1, 19):
    ax.text(g, -0.38 if g in (1, 18) else (-1.38 if g in (2, 13, 14, 15, 16, 17) else -3.38), str(g),
            ha="center", va="bottom", fontsize=6.5, color=C["gray"])
for p in range(1, 7):
    ax.text(0.3, -p, str(p), ha="right", va="center", fontsize=7, color=C["gray"])
ax.text(0.3, -0.45, "주기", ha="right", va="bottom", fontsize=7, color=C["gray"])
ax.text(9.5, -0.2, "족 (세로줄)", ha="center", va="bottom", fontsize=7.5, color=C["gray"])
# 금속-비금속 경계 (계단선)
stair = [(12.5, -1.5), (12.5, -2.5), (13.5, -2.5), (13.5, -3.5), (14.5, -3.5), (14.5, -4.5),
         (15.5, -4.5), (15.5, -5.5), (16.5, -5.5), (16.5, -6.5)]
xs, ys = zip(*stair)
ax.plot(xs, ys, color=C["ink"], lw=1.4)
ax.text(5.0, -2.6, "← 금속", ha="center", fontsize=8.5, color=C["ink"])
ax.text(15.6, -0.95, "비금속 →", ha="center", fontsize=8.5, color=C["ink"])
# 범례
leg = [(C["blue"], "몸의 뼈대 원소 C H O N P S"), (C["green"], "뇌의 주요 이온 Na K Ca Mg Cl"),
       (C["purple"], "미량 금속과 조영제 Fe Cu Zn Mn Gd"), ("white", "영상·치료에 쓰는 원소 F I Li")]
for i, (col, lab) in enumerate(leg):
    yy = -8.55 - 0.75 * (i // 2)
    xx = 1.0 + (i % 2) * 8.5
    ax.add_patch(plt.Rectangle((xx, yy - 0.22), 0.45, 0.45, facecolor=col,
                               edgecolor=C["red"] if col == "white" else col, lw=0.9))
    ax.text(xx + 0.65, yy, lab, va="center", fontsize=8)
ax.set_xlim(-0.2, 18.6)
ax.set_ylim(-9.7, 0.3)
ax.set_aspect("equal")
ax.axis("off")
save(fig, __file__)
