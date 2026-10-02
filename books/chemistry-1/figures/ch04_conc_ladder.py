from figstyle import log_scale_map, save, C

items = [
    (55.5, "순수한 물\n55.5 M"),
    (0.145, "세포 밖 Na⁺\n145 mM"),
    (0.140, "세포 안 K⁺\n140 mM"),
    (0.010, "NAA (MRS)\n약 10 mM"),
    (0.005, "혈당\n약 5 mM"),
    (0.0005, "Gd 조영제\n(분포 후)\n약 0.5 mM"),
    (1e-6, "세포 밖\n글루탐산\n약 μM 이하"),
    (4e-8, "H⁺ (pH 7.4)\n40 nM"),
    (1e-7, "세포 안 Ca²⁺\n100 nM"),
    (1e-8, "세포 밖\n도파민\n수–수십 nM"),
]
ticks = [(1e-9, "1 nM"), (1e-6, "1 μM"), (1e-3, "1 mM"), (1, "1 M"), (100, "100 M")]
fig, ax = log_scale_map(items, "몰 농도 (mol/L), 로그 눈금", (3e-10, 400), figsize=(7.4, 3.0),
                        color=C["green"], ticks=ticks)
ax.set_ylim(-2.0, 1.75)
ax.spines["bottom"].set_position(("data", -2.0))
save(fig, __file__)
