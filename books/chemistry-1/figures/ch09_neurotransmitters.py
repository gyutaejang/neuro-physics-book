from figstyle import molecule_grid, save

# 주요 신경전달물질. 위: 아미노산 계열, 가운데: 모노아민, 아래: 그 밖의 것.
fig, axes = molecule_grid([
    ("C(CC(=O)O)[C@@H](C(=O)O)N", "글루탐산 (흥분)"),
    ("NCCCC(=O)O", "GABA (억제)"),
    ("NCC(=O)O", "글라이신 (억제)"),
    ("NCCc1ccc(O)c(O)c1", "도파민"),
    ("C1=CC(=C(C=C1[C@H](CN)O)O)O", "노르에피네프린"),
    ("NCCc1c[nH]c2ccc(O)cc12", "세로토닌 (5-HT)"),
    ("CC(=O)OCC[N+](C)(C)C", "아세틸콜린"),
    ("NCCc1c[nH]cn1", "히스타민"),
    ("[N]=O", "일산화질소 (NO)"),
], ncols=3, cell=(2.2, 1.55))
save(fig, __file__)
