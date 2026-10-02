from figstyle import plt, save, molecule_image, C

# 카테콜아민 합성(위)과 도파민 분해(아래). 새로 붙거나 바뀐 원자를 강조한다.
TYR = "N[C@@H](Cc1ccc(O)cc1)C(=O)O"
DOPA = "N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O"     # 9: 새 −OH
DA = "NCCc1ccc(O)c(O)c1"
NE = "NC[C@H](O)c1ccc(O)c(O)c1"            # 3: β-OH
DOPAC = "OC(=O)Cc1ccc(O)c(O)c1"            # 0–2: 카복실기
HVA = "COc1cc(CC(=O)O)ccc1O"               # 0–1: 메톡시기

fig = plt.figure(figsize=(7.3, 4.3))
W, H = 0.2, 0.33
top, bot = 0.58, 0.08
xs = [0.02, 0.27, 0.52, 0.77]
mols = [(TYR, "L-티로신", None, xs[0], top), (DOPA, "L-DOPA", [9], xs[1], top),
        (DA, "도파민", None, xs[2], top), (NE, "노르에피네프린", [3], xs[3], top),
        (DOPAC, "DOPAC", [0, 1, 2], xs[2], bot), (HVA, "호모바닐산 (HVA)", [0, 1], xs[1], bot)]
for smi, name, hl, x, y in mols:
    ax = fig.add_axes([x, y, W, H])
    ax.imshow(molecule_image(smi, (440, 330), hl))
    ax.axis("off")
    ax.set_title(name, fontsize=9.5, pad=2)


def arrow(p0, p1, txt, col, tx=0.0, ty=0.035, ha="center"):
    fig.patches.append(plt.matplotlib.patches.FancyArrowPatch(
        p0, p1, transform=fig.transFigure, arrowstyle="-|>", mutation_scale=12, color=col, lw=1.4))
    fig.text((p0[0] + p1[0]) / 2 + tx, (p0[1] + p1[1]) / 2 + ty, txt, ha=ha, va="bottom",
             fontsize=7.8, color=col)

ym = top + H * 0.45
arrow((xs[0] + W - 0.005, ym), (xs[1] + 0.01, ym), "TH", C["blue"])
arrow((xs[1] + W - 0.005, ym), (xs[2] + 0.01, ym), "AADC", C["blue"])
arrow((xs[2] + W - 0.005, ym), (xs[3] + 0.01, ym), "DBH", C["blue"])
# 분해
xd = xs[2] + W / 2
arrow((xd, top - 0.02), (xd, bot + H + 0.035), "MAO", C["red"], tx=0.012, ty=-0.02, ha="left")
yb = bot + H * 0.45
arrow((xs[2] + 0.01, yb), (xs[1] + W - 0.005, yb), "COMT", C["red"])
fig.text(xs[3] - 0.03, bot + 0.17,
         "합성 (파랑)\nTH: 티로신 수산화효소 (속도 제한)\nAADC: 방향족 아미노산 탈카복실효소\nDBH: 도파민 β-수산화효소\n\n분해 (빨강)\nMAO: 모노아민 산화효소\nCOMT: 카테콜-O-메틸전달효소",
         fontsize=7.8, va="center", color=C["ink"], linespacing=1.35)
fig.text(xs[0] + 0.01, bot + 0.16, "뇌척수액의 HVA는\n도파민 회전율의 지표",
         fontsize=8, va="center", color=C["gray"])
save(fig, __file__)
