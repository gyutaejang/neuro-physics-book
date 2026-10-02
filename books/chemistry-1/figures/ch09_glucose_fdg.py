from figstyle import molecule_grid, save

# α-D-포도당(피라노스)과 FDG. FDG는 2번 탄소의 −OH를 ¹⁸F로 바꾼 분자다.
# 원자 번호(SMILES 순서): 0 C6, 1 C5, 2 C4, 3 C3, 4 C2, 5 C1, 6 고리 O, 7 C1-OH, 8 C2의 치환기
GLC = "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O"
G6P = "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)OP(=O)(O)O"
FDG = "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)[18F])O)O)O"
FDG6P = "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)[18F])O)O)OP(=O)(O)O"

fig, axes = molecule_grid([
    (GLC, "포도당", [8]),
    (G6P, "포도당-6-인산", [11, 12, 13, 14, 15]),
    (FDG, "FDG", [8]),
    (FDG6P, "FDG-6-인산", [8, 11, 12, 13, 14, 15]),
], ncols=4, cell=(1.85, 1.75))
save(fig, __file__)
