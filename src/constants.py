import numpy as np
import math

# 常量定义
TOTAL_MATERIAL = 100_000_000  # 总材料需求（吨）
START_YEAR = 2050  # 开始年份

# 太空电梯系统参数
GALACTIC_HARBORS = 3  # 银河港数量
ELEVATOR_ANNUAL_CAPACITY = 179_000  # 每个银河港年运输能力（吨）
ELEVATOR_COST_PER_TON = 1000  # 每吨运输成本（美元）

# 可靠性设置
# Problem 1: 所有可靠性都是100%
ELEVATOR_RELIABILITY_P1 = 1.0  # 太空电梯可靠性（无故障概率）- Problem 1
TUG_RELIABILITY_P1 = 1.0  # 摆渡火箭可靠性（无故障概率）- Problem 1
ROCKET_RELIABILITY_P1 = 1.0  # 火箭可靠性（无故障概率）- Problem 1

# Problem 2: 使用当前设置的可靠性
ELEVATOR_RELIABILITY_P2 = 0.99  # 太空电梯可靠性（无故障概率）- Problem 2
TUG_RELIABILITY_P2 = 0.99  # 摆渡火箭可靠性（无故障概率）- Problem 2
ROCKET_RELIABILITY_P2 = 0.95  # 火箭可靠性（无故障概率）- Problem 2

# 当前使用的可靠性设置（默认使用 Problem 2）
ELEVATOR_RELIABILITY = ELEVATOR_RELIABILITY_P2
TUG_RELIABILITY = TUG_RELIABILITY_P2
ROCKET_RELIABILITY = ROCKET_RELIABILITY_P2

# 摆渡火箭参数
TUG_DELTA_V = 2800 # m/s
TUG_I_SP = 380 #发动机比冲（秒）
TUG_COST_FUEL_PER = 2 * 1000 # 燃料价格（美元/吨）
TUG_COST_VEHICLE = 20_000_000 # 在轨火箭成本
TUG_N = 50 # 复用次数

# 太空电梯-摆渡火箭单位有效载荷成本
G_0 = 9.81 # 重力加速度
R = math.exp(TUG_DELTA_V / (G_0 * TUG_I_SP)) # 质量比
M_D = 0.2 # 火箭自重和有效载荷比值
M_PROP = (R-1) * (1+M_D) # 燃料质量
M_0 = M_PROP + M_D + 1 # 总质量
# 计算单位有效载荷成本：考虑电梯运输成本、燃料成本、车辆摊销成本，并除以可靠性
# Problem 1 成本计算（100%可靠性）
COST_ELEVATOR_PER_P1 = (ELEVATOR_COST_PER_TON * M_0 + TUG_COST_FUEL_PER * M_PROP + TUG_COST_VEHICLE / TUG_N) / (ELEVATOR_RELIABILITY_P1 * TUG_RELIABILITY_P1)
# Problem 2 成本计算（当前可靠性）
COST_ELEVATOR_PER_P2 = (ELEVATOR_COST_PER_TON * M_0 + TUG_COST_FUEL_PER * M_PROP + TUG_COST_VEHICLE / TUG_N) / (ELEVATOR_RELIABILITY_P2 * TUG_RELIABILITY_P2)
# 当前使用的成本（默认使用 Problem 2）
COST_ELEVATOR_PER = COST_ELEVATOR_PER_P2

# 火箭系统参数
ROCKET_LAUNCH_SITES = 10  # 火箭发射场数量
ROCKET_PAYLOAD_MIN = 100  # 火箭最小有效载荷（吨）
ROCKET_PAYLOAD_MAX = 150  # 火箭最大有效载荷（吨）
ROCKET_PAYLOAD_AVG = (ROCKET_PAYLOAD_MIN + ROCKET_PAYLOAD_MAX) / 2  # 平均有效载荷
ROCKET_COST_PER_LAUNCH = 10_000_000  # 单次发射成本（美元）
ROCKET_THETA = 0.4 # 可回收火箭消耗系数
ROCKET_LAUNCHES_PER_YEAR_PER_SITE = 200  # 每个发射场每年发射次数
ROCKET_N_G = 20 # 复用次数
# 计算单位有效载荷成本：考虑发射成本、消耗系数、复用次数和可靠性
# Problem 1 成本计算（100%可靠性）
COST_ROCKET_PER_P1 = ROCKET_THETA * ROCKET_COST_PER_LAUNCH / (ROCKET_PAYLOAD_AVG * ROCKET_N_G * ROCKET_RELIABILITY_P1)
# Problem 2 成本计算（当前可靠性）
COST_ROCKET_PER_P2 = ROCKET_THETA * ROCKET_COST_PER_LAUNCH / (ROCKET_PAYLOAD_AVG * ROCKET_N_G * ROCKET_RELIABILITY_P2)
# 当前使用的成本（默认使用 Problem 2）
COST_ROCKET_PER = COST_ROCKET_PER_P2

if __name__ == "__main__":
    print(f"COST_ELEVATOR_PER_P1: {COST_ELEVATOR_PER_P1}")
    print(f"COST_ELEVATOR_PER_P2: {COST_ELEVATOR_PER_P2}")
    print(f"COST_ROCKET_PER_P1: {COST_ROCKET_PER_P1}")
    print(f"COST_ROCKET_PER_P2: {COST_ROCKET_PER_P2}")
