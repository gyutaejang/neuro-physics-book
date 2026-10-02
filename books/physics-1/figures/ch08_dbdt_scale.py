from figstyle import log_scale_map, save, C

# 자기장의 변화율 dB/dt 크기 지도 (모두 어림값, 최대값 기준)
items = [
    (4e-3, "가전제품 곁 60 Hz\n(~10 μT) ~0.004 T/s"),
    (1, "7 T 자석 입구로\n머리 이동 ~1 T/s"),
    (50, "MRI 경사 코일 전환\n(몸 가장자리) 수십 T/s"),
    (8e3, "MRI RF 자기장\n(128 MHz) ~10⁴ T/s"),
    (3e4, "TMS 펄스\n(피질) ~10⁴ T/s"),
]
ticks = [(1e-3, "10⁻³"), (1e-2, "10⁻²"), (1e-1, "10⁻¹"), (1, "1"), (10, "10"), (1e2, "10²"),
         (1e3, "10³"), (1e4, "10⁴"), (1e5, "10⁵")]
fig, ax = log_scale_map(items, "자기장 변화율 dB/dt (T/s, 로그 눈금)", (5e-4, 3e5), figsize=(7.2, 3.2),
                        color=C["purple"], ticks=ticks)
# 세로 연결선을 조금 짧게 해 두 줄 이름과 닿지 않게 한다.
for ln in ax.lines:
    xd, yd = ln.get_xdata(), ln.get_ydata()
    if len(xd) == 2 and xd[0] == xd[1]:
        ln.set_ydata([0, yd[1] * 0.75])
save(fig, __file__)
