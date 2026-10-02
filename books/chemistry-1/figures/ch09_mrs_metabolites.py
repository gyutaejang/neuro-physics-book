from figstyle import molecule_grid, save

# ¹H-MRS의 주요 대사물. 강조한 탄소에 붙은 수소들이 대표 봉우리를 만든다.
fig, axes = molecule_grid([
    ("CC(=O)N[C@@H](CC(=O)O)C(=O)O", "NAA: CH$_3$ → 2.01 ppm", [0]),
    ("CN(CC(=O)O)C(=N)N", "크레아틴: CH$_3$ 3.03, CH$_2$ 3.9", [0, 2]),
    ("C[N+](C)(C)CCO", "콜린: N(CH$_3$)$_3$ → 3.2 ppm", [0, 2, 3]),
    ("O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O", "미오이노시톨: 3.56 ppm", None),
    ("C(CC(=O)O)[C@@H](C(=O)O)N", "글루탐산: 2.0–2.4, 3.75", None),
    ("C[C@@H](C(=O)O)O", "젖산: CH$_3$ → 1.33 ppm", [0]),
], ncols=3, cell=(2.35, 1.6))
save(fig, __file__)
