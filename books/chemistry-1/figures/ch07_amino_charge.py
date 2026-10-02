from figstyle import molecule_grid, save

items = [
    ("[NH3+]CC(=O)O", "글라이신, pH 1 (알짜 +1)"),
    ("[NH3+]CC(=O)[O-]", "글라이신, pH 7.4 (알짜 0)"),
    ("NCC(=O)[O-]", "글라이신, pH 12 (알짜 −1)"),
    ("[NH3+]CCCC(=O)[O-]", "GABA, pH 7.4 (알짜 0)"),
    ("[NH3+][C@@H](CCC(=O)[O-])C(=O)[O-]", "L-글루탐산, pH 7.4 (알짜 −1)"),
    ("[NH3+][C@@H](Cc1ccc(O)c(O)c1)C(=O)[O-]", "L-DOPA, pH 7.4 (알짜 0)"),
]
fig, axes = molecule_grid(items, ncols=3, cell=(2.4, 1.9))
save(fig, __file__)
