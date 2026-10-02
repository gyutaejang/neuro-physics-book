from figstyle import molecule_grid, save

# L-아미노산 세 개와 다이펩타이드. 펩타이드 결합(C(=O)–N)을 강조한다.
# 글라이실알라닌 원자 번호: 0 N, 1 Cα, 2 C, 3 O, 4 N, 5 Cα, 6 CH3, 7 C, 8 O, 9 O
fig, axes = molecule_grid([
    ("C[C@@H](C(=O)O)N", "L-알라닌", [1]),
    ("C1=CC(=CC=C1C[C@@H](C(=O)O)N)O", "L-티로신", [7]),
    ("C1=CC=C2C(=C1)C(=CN2)C[C@@H](C(=O)O)N", "L-트립토판", [10]),
    ("NCC(=O)N[C@@H](C)C(=O)O", "글라이실알라닌 (펩타이드 결합)", [2, 3, 4]),
], ncols=4, cell=(1.85, 1.75))
save(fig, __file__)
