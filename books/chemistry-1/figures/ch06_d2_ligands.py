from figstyle import molecule_grid, save

items = [
    ("NCCc1ccc(O)c(O)c1", "도파민 (내인성 작용제)"),
    ("CCN1CCC[C@H]1CNC(=O)c1c(OC)c(Cl)cc(Cl)c1O", "라클로프라이드 (PET 추적자)"),
    ("OC1(CCN(CCCC(=O)c2ccc(F)cc2)CC1)c1ccc(Cl)cc1", "할로페리돌 (항정신병 약물)"),
]
fig, axes = molecule_grid(items, ncols=3, cell=(2.45, 2.1))
save(fig, __file__)
