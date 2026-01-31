import numpy as np
import matplotlib.pyplot as plt
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
COST_ELEVATOR_PER = (ELEVATOR_COST_PER_TON * M_0) / ELEVATOR_RELIABILITY + (TUG_COST_FUEL_PER * M_PROP + TUG_COST_VEHICLE / TUG_N) / TUG_RELIABILITY

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

# 计算每个场景的成本和时间线
def calculate_scenario_1():
    """Scenario 1: Space Elevator Only"""
    total_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
    years_needed = np.ceil(TOTAL_MATERIAL / total_annual_capacity)
    total_cost = TOTAL_MATERIAL * COST_ELEVATOR_PER
    completion_year = START_YEAR + years_needed
    
    return {
        "name": "Space Elevator Only",
        "years_needed": years_needed,
        "completion_year": completion_year,
        "total_cost": total_cost,
        "annual_capacity": total_annual_capacity
    }

def calculate_scenario_2():
    """Scenario 2: Traditional Rockets Only"""
    total_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
    years_needed = np.ceil(TOTAL_MATERIAL / total_annual_capacity)
    total_launches = np.ceil(TOTAL_MATERIAL / ROCKET_PAYLOAD_AVG)
    total_cost = total_launches * ROCKET_THETA * ROCKET_COST_PER_LAUNCH
    completion_year = START_YEAR + years_needed
    
    return {
        "name": "Traditional Rockets Only",
        "years_needed": years_needed,
        "completion_year": completion_year,
        "total_cost": total_cost,
        "annual_capacity": total_annual_capacity
    }

def calculate_scenario_3():
    """Scenario 3: Combined Space Elevator and Traditional Rockets (Finding Optimal Ratio)"""
    best_scenario = None
    min_total_cost = float('inf')
    
    # 遍历不同的太空电梯比例（从0%到100%，步长2%）
    for elevator_ratio in range(0, 101, 2):
        elevator_ratio = elevator_ratio / 100
        rocket_ratio = 1 - elevator_ratio
        
        # 计算各部分运输量
        elevator_material = TOTAL_MATERIAL * elevator_ratio
        rocket_material = TOTAL_MATERIAL * rocket_ratio
        
        # 太空电梯计算
        if elevator_ratio > 0:
            elevator_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
            elevator_years = -(-elevator_material // elevator_annual_capacity)  # 向上取整
            elevator_cost = elevator_material * COST_ELEVATOR_PER
        else:
            elevator_years = 0
            elevator_cost = 0
        
        # 火箭计算
        if rocket_ratio > 0:
            rocket_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
            rocket_years = -(-rocket_material // rocket_annual_capacity)  # 向上取整
            rocket_launches = -(-rocket_material // ROCKET_PAYLOAD_AVG)  # 向上取整
            rocket_cost = rocket_launches * ROCKET_THETA * ROCKET_COST_PER_LAUNCH
        else:
            rocket_years = 0
            rocket_cost = 0
        
        # 总计算
        years_needed = max(elevator_years, rocket_years)
        total_cost = elevator_cost + rocket_cost
        
        # 更新最优解
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            best_scenario = {
                "name": "Combined System",
                "years_needed": years_needed,
                "completion_year": START_YEAR + years_needed,
                "total_cost": total_cost,
                "elevator_material": elevator_material,
                "rocket_material": rocket_material,
                "elevator_ratio": elevator_ratio,
                "rocket_ratio": rocket_ratio
            }
    
    return best_scenario

# 计算系统故障的影响
def calculate_reliability_impact():
    """Analyze the impact of system failures on each scenario"""
    scenarios = [calculate_scenario_1(), calculate_scenario_2(), calculate_scenario_3()]
    impacted_scenarios = []
    
    for scenario in scenarios:
        if scenario["name"] == "Space Elevator Only":
            # 考虑太空电梯可靠性
            effective_capacity = scenario["annual_capacity"] * ELEVATOR_RELIABILITY
            years_needed = np.ceil(TOTAL_MATERIAL / effective_capacity)
            total_cost = TOTAL_MATERIAL * COST_ELEVATOR_PER  # 考虑重试成本
        elif scenario["name"] == "Traditional Rockets Only":
            # 考虑火箭可靠性
            effective_capacity = scenario["annual_capacity"] * ROCKET_RELIABILITY
            years_needed = np.ceil(TOTAL_MATERIAL / effective_capacity)
            total_launches = np.ceil(TOTAL_MATERIAL / ROCKET_PAYLOAD_AVG / ROCKET_RELIABILITY)
            total_cost = total_launches * ROCKET_THETA * ROCKET_COST_PER_LAUNCH
        else:  # 组合场景
            # 获取最优比例
            elevator_ratio = scenario.get("elevator_ratio", 0.7)
            rocket_ratio = scenario.get("rocket_ratio", 0.3)
            
            # 太空电梯部分
            elevator_material = TOTAL_MATERIAL * elevator_ratio
            elevator_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
            effective_elevator_capacity = elevator_annual_capacity * ELEVATOR_RELIABILITY
            elevator_years = np.ceil(elevator_material / effective_elevator_capacity)
            elevator_cost = elevator_material * COST_ELEVATOR_PER
            
            # 火箭部分
            rocket_material = TOTAL_MATERIAL * rocket_ratio
            rocket_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
            effective_rocket_capacity = rocket_annual_capacity * ROCKET_RELIABILITY
            rocket_years = np.ceil(rocket_material / effective_rocket_capacity)
            rocket_launches = np.ceil(rocket_material / ROCKET_PAYLOAD_AVG / ROCKET_RELIABILITY)
            rocket_cost = rocket_launches * ROCKET_THETA * ROCKET_COST_PER_LAUNCH
            
            years_needed = max(elevator_years, rocket_years)
            total_cost = elevator_cost + rocket_cost
        
        impacted_scenarios.append({
            "name": scenario["name"],
            "years_needed": years_needed,
            "completion_year": START_YEAR + years_needed,
            "total_cost": total_cost,
            "impact": "System Failure Impact"
        })
    
    return impacted_scenarios

# 保存结果到文件
def save_results_to_file():
    """保存计算结果到文件，供画图工具使用"""
    import os
    
    # 计算三个场景
    scenario1 = calculate_scenario_1()
    scenario2 = calculate_scenario_2()
    scenario3 = calculate_scenario_3()
    
    # 计算系统故障影响
    impacted_scenarios = calculate_reliability_impact()
    
    # 获取结果目录的绝对路径
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # 保存场景分析结果
    scenario_file = os.path.join(results_dir, 'scenario_analysis.txt')
    with open(scenario_file, 'w') as f:
        f.write("=== 场景分析 ===\n")
        for scenario in [scenario1, scenario2, scenario3]:
            f.write(f"场景: {scenario['name']}\n")
            f.write(f"所需时间: {scenario['years_needed']} 年\n")
            f.write(f"完成年份: {scenario['completion_year']}\n")
            f.write(f"总成本: {scenario['total_cost']}\n")
            if 'elevator_ratio' in scenario:
                f.write(f"太空电梯比例: {scenario['elevator_ratio']*100}%\n")
                f.write(f"传统火箭比例: {scenario['rocket_ratio']*100}%\n")
            f.write("\n")
    
    # 保存系统故障影响结果
    reliability_file = os.path.join(results_dir, 'reliability_impact.txt')
    with open(reliability_file, 'w') as f:
        f.write("=== 系统故障影响分析 ===\n")
        for scenario in impacted_scenarios:
            f.write(f"场景: {scenario['name']}\n")
            f.write(f"所需时间: {scenario['years_needed']} 年\n")
            f.write(f"完成年份: {scenario['completion_year']}\n")
            f.write(f"总成本: {scenario['total_cost']}\n")
            f.write("\n")
    
    # 保存组合场景的比例分析
    ratio_file = os.path.join(results_dir, 'ratio_analysis.txt')
    with open(ratio_file, 'w') as f:
        f.write("=== 组合场景比例分析 ===\n")
        # 遍历不同的太空电梯比例（从0%到100%，步长2%）
        for elevator_ratio in range(0, 101, 2):
            elevator_ratio = elevator_ratio / 100
            rocket_ratio = 1 - elevator_ratio
            
            # 计算各部分运输量
            elevator_material = TOTAL_MATERIAL * elevator_ratio
            rocket_material = TOTAL_MATERIAL * rocket_ratio
            
            # 太空电梯计算
            if elevator_ratio > 0:
                elevator_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
                elevator_years = -(-elevator_material // elevator_annual_capacity)  # 向上取整
                elevator_cost = elevator_material * COST_ELEVATOR_PER
            else:
                elevator_years = 0
                elevator_cost = 0
            
            # 火箭计算
            if rocket_ratio > 0:
                rocket_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
                rocket_years = -(-rocket_material // rocket_annual_capacity)  # 向上取整
                rocket_launches = -(-rocket_material // ROCKET_PAYLOAD_AVG)  # 向上取整
                rocket_cost = rocket_launches * ROCKET_THETA * ROCKET_COST_PER_LAUNCH
            else:
                rocket_years = 0
                rocket_cost = 0
            
            # 总计算
            years_needed = max(elevator_years, rocket_years)
            total_cost = elevator_cost + rocket_cost
            
            f.write(f"太空电梯比例: {elevator_ratio*100}%\n")
            f.write(f"传统火箭比例: {rocket_ratio*100}%\n")
            f.write(f"所需时间: {years_needed} 年\n")
            f.write(f"总成本: {total_cost}\n")
            f.write("\n")

# 主函数
def main():
    """运行所有计算并输出结果"""
    # 计算三个场景
    scenario1 = calculate_scenario_1()
    scenario2 = calculate_scenario_2()
    scenario3 = calculate_scenario_3()
    
    print("=== 场景分析 ===")
    for scenario in [scenario1, scenario2, scenario3]:
        print(f"场景: {scenario['name']}")
        print(f"所需时间: {scenario['years_needed']} 年")
        print(f"完成年份: {scenario['completion_year']}")
        print(f"总成本: ${scenario['total_cost']:,.2f}")
        if 'elevator_ratio' in scenario:
            print(f"太空电梯比例: {scenario['elevator_ratio']*100}%")
            print(f"传统火箭比例: {scenario['rocket_ratio']*100}%")
        print()
    
    # 计算系统故障影响
    print("=== 系统故障影响分析 ===")
    impacted_scenarios = calculate_reliability_impact()
    for scenario in impacted_scenarios:
        print(f"场景: {scenario['name']}")
        print(f"所需时间: {scenario['years_needed']} 年")
        print(f"完成年份: {scenario['completion_year']}")
        print(f"总成本: ${scenario['total_cost']:,.2f}")
        print()
    
    # 保存结果到文件
    save_results_to_file()
    print("结果已保存到 results/ 目录")

if __name__ == "__main__":
    main()
