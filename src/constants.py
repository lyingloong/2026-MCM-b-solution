import numpy as np
import math

# 常量定义
TOTAL_MATERIAL = 100_000_000  # 总材料需求（吨）
START_YEAR = 2050  # 开始年份

# 太空电梯系统参数
GALACTIC_HARBORS = 3  # 银河港数量
ELEVATOR_ANNUAL_CAPACITY = 179_000  # 每个银河港年运输能力（吨）
ELEVATOR_COST_PER_TON = 1000  # 每吨运输成本（美元）
ELEVATOR_RELIABILITY = 0.99  # 可靠性（无故障概率）

# 摆渡火箭参数
TUG_DELTA_V = 2800 # m/s
TUG_I_SP = 380 #发动机比冲（秒）
TUG_RELIABILITY = 0.99 # 可靠性（无故障概率）
TUG_COST_FUEL_PER = 2 # 燃料价格（美元/千克）
TUG_COST_VEHICLE = 20_000_000 # 在轨火箭成本
TUG_N = 50 # 复用次数

# 太空电梯-摆渡火箭单位有效载荷成本
G_0 = 9.81 # 重力加速度
R = math.exp(TUG_DELTA_V / (G_0 * TUG_I_SP))
M_D = 0.2 # 火箭自重和有效载荷比值
M_PROP = (R-1) * (1+M_D) # 燃料质量
M_0 = M_PROP + M_D + 1 # 总质量
COST_ELEVATOR_PER = (ELEVATOR_COST_PER_TON * M_0 + TUG_COST_FUEL_PER * M_PROP + TUG_COST_VEHICLE / TUG_N) / (ELEVATOR_RELIABILITY*TUG_RELIABILITY)

# 火箭系统参数
ROCKET_LAUNCH_SITES = 10  # 火箭发射场数量
ROCKET_PAYLOAD_MIN = 100  # 火箭最小有效载荷（吨）
ROCKET_PAYLOAD_MAX = 150  # 火箭最大有效载荷（吨）
ROCKET_PAYLOAD_AVG = (ROCKET_PAYLOAD_MIN + ROCKET_PAYLOAD_MAX) / 2  # 平均有效载荷
ROCKET_COST_PER_LAUNCH = 10_000_000  # 单次发射成本（美元）
ROCKET_THETA = 0.4 # 可回收火箭消耗系数
ROCKET_RELIABILITY = 0.95  # 可靠性（无故障概率）
ROCKET_LAUNCHES_PER_YEAR_PER_SITE = 2000  # 每个发射场每年发射次数
ROCKET_N_G = 20 # 复用次数
COST_ROCKET_PER = ROCKET_THETA * ROCKET_COST_PER_LAUNCH / (ROCKET_N_G * ROCKET_RELIABILITY)
