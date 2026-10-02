from figstyle import plt, save, molecule_grid

# 생리적 pH(약 7.4)에서 주로 존재하는 이온화 형태로 그린다.
# 주황 강조: 전하를 띤 자리(아미노기 NH3+, 카복실기 COO-), 포도당은 2번 탄소의 OH, FDG는 그 자리의 18F.
items = [
    ("[NH3+]CCc1ccc(O)c(O)c1", "도파민 (+1)", [0]),
    ("[NH3+]CCc1c[nH]c2ccc(O)cc12", "세로토닌 (+1)", [0]),
    ("[NH3+]CCCC(=O)[O-]", "GABA (0, 쯔비터이온)", [0, 5, 6]),
    ("[NH3+][C@@H](CCC(=O)[O-])C(=O)[O-]", "글루탐산 (−1)", [0, 5, 6, 8, 9]),
    ("C([C@@H]1[C@H]([C@@H]([C@H]([C@@H](O1)O)O)O)O)O", "포도당 (β-D-포도당)", [8]),
    ("C([C@@H]1[C@H]([C@@H]([C@H]([C@@H](O1)O)[18F])O)O)O", "FDG (2번 −OH → ¹⁸F)", [8]),
]
fig, axes = molecule_grid(items, ncols=3, cell=(2.45, 2.0))
save(fig, __file__)
