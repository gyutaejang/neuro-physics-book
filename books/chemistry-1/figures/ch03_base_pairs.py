from figstyle import plt, save, molecule_grid

# 왓슨-크릭 짝에서 수소 결합에 쓰이는 원자를 색으로 강조한다 (SMILES 순서의 원자 번호).
items = [
    ("Nc1ncnc2[nH]cnc12", "아데닌 (A)", [0, 2]),            # N6-H 주개, N1 받개
    ("Cc1c[nH]c(=O)[nH]c1=O", "티민 (T)", [6, 8]),          # N3-H 주개, O4 받개
    ("Nc1nc2[nH]cnc2c(=O)[nH]1", "구아닌 (G)", [0, 9, 10]),  # N2-H, N1-H 주개, O6 받개
    ("Nc1cc[nH]c(=O)n1", "사이토신 (C)", [0, 6, 7]),         # N4-H 주개, N3, O2 받개
]
fig, axes = molecule_grid(items, ncols=4, cell=(1.75, 1.75), size=(420, 380))
fig.text(0.27, 0.02, "A–T: 수소 결합 2개", ha="center", fontsize=10)
fig.text(0.76, 0.02, "G–C: 수소 결합 3개", ha="center", fontsize=10)
fig.subplots_adjust(bottom=0.12)
save(fig, __file__)
