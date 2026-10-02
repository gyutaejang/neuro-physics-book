from figstyle import molecule_grid, save

# SMILES는 PubChem 이성질체 SMILES와 대조했다 (D-만니톨 CID 6251, β-D-포도당 CID 64689, 요소 CID 1176).
items = [
    ("C([C@H]([C@H]([C@@H]([C@@H](CO)O)O)O)O)O", "만니톨 (182 g/mol)\n막을 거의 못 지난다"),
    ("C([C@@H]1[C@H]([C@@H]([C@H]([C@@H](O1)O)O)O)O)O", "포도당 (180 g/mol)\n운반체(GLUT)로 지난다"),
    ("NC(N)=O", "요소 (60 g/mol)\n세포막을 비교적 잘 지난다"),
    ("[Na+].[Cl-]", "염화 나트륨 (58 g/mol)\n물에서 이온 2개"),
]
fig, axes = molecule_grid(items, ncols=4, cell=(1.85, 1.95), size=(420, 340))
save(fig, __file__)
