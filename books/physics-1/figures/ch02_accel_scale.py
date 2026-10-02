from figstyle import log_scale_map, save, C

items = [
    (0.1, "엘리베이터 출발\n~0.1 g"),
    (0.8, "자동차 급제동\n~0.8 g"),
    (1, "지구 중력\n1 g"),
    (4, "롤러코스터\n~3–5 g"),
    (9, "전투기 급선회\n~9 g"),
    (25, "축구 헤딩\n~10–30 g"),
    (100, "뇌진탕을 일으킨 충격\n~60–150 g"),
]
ticks = [(0.01, "0.01 g"), (0.1, "0.1 g"), (1, "1 g"), (10, "10 g"), (100, "100 g"), (1000, "1000 g")]
fig, ax = log_scale_map(items, "가속도 (중력 가속도 g = 9.8 m/s²의 배수, 로그 눈금)", (0.01, 1000),
                        figsize=(7.2, 3.3), color=C["red"], ticks=ticks)
ax.axvspan(60, 150, ymin=0.47, ymax=0.53, color=C["red"], alpha=0.15)
save(fig, __file__)
