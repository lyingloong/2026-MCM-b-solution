import numpy as np
import matplotlib.pyplot as plt
from src.constants import *

# 计算每个场景的成本和时间线
def calculate_scenario_1(problem=2):
    """Scenario 1: Space Elevator Only
    
    计算仅使用太空电梯系统时的运输时间和成本
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性）
        
    Returns:
        dict: 包含场景名称、所需时间、完成年份、总成本和年运输能力的字典
    """
    # 根据问题编号选择成本设置
    if problem == 1:
        # Problem 1: 使用100%可靠性计算的成本
        cost_elevator_per = COST_ELEVATOR_PER_P1
    else:  # problem == 2
        # Problem 2: 使用当前可靠性计算的成本
        cost_elevator_per = COST_ELEVATOR_PER_P2
    
    # 计算太空电梯系统的总年运输能力
    # 总年运输能力 = 银河港数量 * 每个银河港年运输能力
    total_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
    # 计算所需时间：总材料需求除以总年运输能力，向上取整
    years_needed = np.ceil(TOTAL_MATERIAL / total_annual_capacity)
    # 计算总成本：总材料需求乘以单位有效载荷成本
    total_cost = TOTAL_MATERIAL * cost_elevator_per
    # 计算完成年份
    completion_year = START_YEAR + years_needed
    
    return {
        "name": "Space Elevator Only",
        "years_needed": years_needed,
        "completion_year": completion_year,
        "total_cost": total_cost,
        "annual_capacity": total_annual_capacity
    }

def calculate_scenario_2(problem=2):
    """Scenario 2: Traditional Rockets Only
    
    计算仅使用传统火箭系统时的运输时间和成本
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性）
        
    Returns:
        dict: 包含场景名称、所需时间、完成年份、总成本和年运输能力的字典
    """
    # 根据问题编号选择成本设置
    if problem == 1:
        # Problem 1: 使用100%可靠性计算的成本
        cost_rocket_per = COST_ROCKET_PER_P1
    else:  # problem == 2
        # Problem 2: 使用当前可靠性计算的成本
        cost_rocket_per = COST_ROCKET_PER_P2
    
    # 计算火箭系统的总年运输能力
    # 总年运输能力 = 发射场数量 * 每个发射场年发射次数 * 平均有效载荷
    total_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
    # 计算所需时间：总材料需求除以总年运输能力，向上取整
    years_needed = np.ceil(TOTAL_MATERIAL / total_annual_capacity)
    # 计算总成本：总材料需求乘以单位有效载荷成本
    total_cost = TOTAL_MATERIAL * cost_rocket_per
    # 计算完成年份
    completion_year = START_YEAR + years_needed
    
    return {
        "name": "Traditional Rockets Only",
        "years_needed": years_needed,
        "completion_year": completion_year,
        "total_cost": total_cost,
        "annual_capacity": total_annual_capacity
    }

def calculate_scenario_3(problem=2):
    """Scenario 3: Combined Space Elevator and Traditional Rockets (Finding Optimal Ratio)
    
    计算太空电梯和传统火箭组合使用时的最优比例，以最小化总成本
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性）
        
    Returns:
        dict: 包含场景名称、所需时间、完成年份、总成本、各部分运输量和比例的字典
    """
    best_scenario = None
    min_total_cost = float('inf')
    
    # 根据问题编号选择成本设置
    if problem == 1:
        cost_elevator_per = COST_ELEVATOR_PER_P1
        cost_rocket_per = COST_ROCKET_PER_P1
    else:  # problem == 2
        cost_elevator_per = COST_ELEVATOR_PER_P2
        cost_rocket_per = COST_ROCKET_PER_P2
    
    # 遍历不同的太空电梯比例（从0%到100%，步长2%）
    for elevator_ratio in range(0, 101, 2):
        elevator_ratio = elevator_ratio / 100
        rocket_ratio = 1 - elevator_ratio
        
        # 计算各部分运输量
        elevator_material = TOTAL_MATERIAL * elevator_ratio
        rocket_material = TOTAL_MATERIAL * rocket_ratio
        
        # 太空电梯计算
        if elevator_ratio > 0:
            # 太空电梯系统年运输能力
            elevator_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
            # 计算太空电梯部分所需时间，向上取整
            elevator_years = np.ceil(elevator_material / elevator_annual_capacity)
            # 计算太空电梯部分成本
            elevator_cost = elevator_material * cost_elevator_per
        else:
            elevator_years = 0
            elevator_cost = 0
        
        # 火箭计算
        if rocket_ratio > 0:
            # 火箭系统年运输能力
            rocket_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
            # 计算火箭部分所需时间，向上取整
            rocket_years = np.ceil(rocket_material / rocket_annual_capacity)
            # 计算火箭部分成本
            rocket_cost = rocket_material * cost_rocket_per
        else:
            rocket_years = 0
            rocket_cost = 0
        
        # 总计算：总时间由运输能力较慢的部分决定
        years_needed = max(elevator_years, rocket_years)
        # 计算总成本：两部分成本之和
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
def calculate_reliability_impact(problem=2):
    """Analyze the impact of system failures on each scenario
    
    分析系统故障对每个场景的影响，考虑可靠性因素
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性）
        
    Returns:
        list: 包含各场景故障影响分析结果的列表
    """
    scenarios = [calculate_scenario_1(problem), calculate_scenario_2(problem), calculate_scenario_3(problem)]
    impacted_scenarios = []
    
    # 根据问题编号选择可靠性和成本设置
    if problem == 1:
        elevator_reliability = ELEVATOR_RELIABILITY_P1
        rocket_reliability = ROCKET_RELIABILITY_P1
        cost_elevator_per = COST_ELEVATOR_PER_P1
        cost_rocket_per = COST_ROCKET_PER_P1
    else:  # problem == 2
        elevator_reliability = ELEVATOR_RELIABILITY_P2
        rocket_reliability = ROCKET_RELIABILITY_P2
        cost_elevator_per = COST_ELEVATOR_PER_P2
        cost_rocket_per = COST_ROCKET_PER_P2
    
    for scenario in scenarios:
        if scenario["name"] == "Space Elevator Only":
            # 考虑太空电梯可靠性
            # 有效运输能力 = 原始运输能力 * 可靠性
            effective_capacity = scenario["annual_capacity"] * elevator_reliability
            # 计算考虑可靠性后的所需时间
            years_needed = np.ceil(TOTAL_MATERIAL / effective_capacity)
            # 计算总成本：使用预计算的成本
            total_cost = TOTAL_MATERIAL * cost_elevator_per
        elif scenario["name"] == "Traditional Rockets Only":
            # 考虑火箭可靠性
            # 有效运输能力 = 原始运输能力 * 可靠性
            effective_capacity = scenario["annual_capacity"] * rocket_reliability
            # 计算考虑可靠性后的所需时间
            years_needed = np.ceil(TOTAL_MATERIAL / effective_capacity)
            # 计算总成本：使用预计算的成本
            total_cost = TOTAL_MATERIAL * cost_rocket_per
        else:  # 组合场景
            # 获取最优比例
            elevator_ratio = scenario.get("elevator_ratio", 0.7)
            rocket_ratio = scenario.get("rocket_ratio", 0.3)
            
            # 太空电梯部分
            elevator_material = TOTAL_MATERIAL * elevator_ratio
            elevator_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
            # 考虑太空电梯可靠性后的有效运输能力
            effective_elevator_capacity = elevator_annual_capacity * elevator_reliability
            # 计算太空电梯部分考虑可靠性后的所需时间
            elevator_years = np.ceil(elevator_material / effective_elevator_capacity)
            # 计算太空电梯部分成本：使用预计算的成本
            elevator_cost = elevator_material * cost_elevator_per
            
            # 火箭部分
            rocket_material = TOTAL_MATERIAL * rocket_ratio
            rocket_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
            # 考虑火箭可靠性后的有效运输能力
            effective_rocket_capacity = rocket_annual_capacity * rocket_reliability
            # 计算火箭部分考虑可靠性后的所需时间
            rocket_years = np.ceil(rocket_material / effective_rocket_capacity)
            # 计算火箭部分成本：使用预计算的成本
            rocket_cost = rocket_material * cost_rocket_per
            
            # 总计算：总时间由运输能力较慢的部分决定
            years_needed = max(elevator_years, rocket_years)
            # 计算总成本：两部分成本之和
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
def save_results_to_file(problem=2):
    """保存计算结果到文件，供画图工具使用
    
    将场景分析、系统故障影响分析和组合场景比例分析的结果保存到文件
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性）
    """
    import os
    
    # 计算三个场景
    scenario1 = calculate_scenario_1(problem)
    scenario2 = calculate_scenario_2(problem)
    scenario3 = calculate_scenario_3(problem)
    
    # 计算系统故障影响
    impacted_scenarios = calculate_reliability_impact(problem)
    
    # 获取结果目录的绝对路径
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # 根据问题编号创建子目录
    problem_dir = os.path.join(results_dir, f'problem_{problem}')
    os.makedirs(problem_dir, exist_ok=True)
    
    # 保存场景分析结果
    scenario_file = os.path.join(problem_dir, 'scenario_analysis.txt')
    with open(scenario_file, 'w') as f:
        f.write(f"=== 场景分析 (Problem {problem}) ===\n")
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
    reliability_file = os.path.join(problem_dir, 'reliability_impact.txt')
    with open(reliability_file, 'w') as f:
        f.write(f"=== 系统故障影响分析 (Problem {problem}) ===\n")
        for scenario in impacted_scenarios:
            f.write(f"场景: {scenario['name']}\n")
            f.write(f"所需时间: {scenario['years_needed']} 年\n")
            f.write(f"完成年份: {scenario['completion_year']}\n")
            f.write(f"总成本: {scenario['total_cost']}\n")
            f.write("\n")
    
    # 保存组合场景的比例分析
    ratio_file = os.path.join(problem_dir, 'ratio_analysis.txt')
    with open(ratio_file, 'w') as f:
        f.write(f"=== 组合场景比例分析 (Problem {problem}) ===\n")
        # 根据问题编号选择可靠性设置
        if problem == 1:
            elevator_reliability = ELEVATOR_RELIABILITY_P1
            tug_reliability = TUG_RELIABILITY_P1
            rocket_reliability = ROCKET_RELIABILITY_P1
        else:  # problem == 2
            elevator_reliability = ELEVATOR_RELIABILITY_P2
            tug_reliability = TUG_RELIABILITY_P2
            rocket_reliability = ROCKET_RELIABILITY_P2
        
        # 遍历不同的太空电梯比例（从0%到100%，步长2%）
        for elevator_ratio in range(0, 101, 2):
            elevator_ratio = elevator_ratio / 100
            rocket_ratio = 1 - elevator_ratio
            
            # 计算各部分运输量
            elevator_material = TOTAL_MATERIAL * elevator_ratio
            rocket_material = TOTAL_MATERIAL * rocket_ratio
            
            # 太空电梯计算
            if elevator_ratio > 0:
                # 太空电梯系统年运输能力
                elevator_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
                # 计算太空电梯部分所需时间，向上取整
                elevator_years = np.ceil(elevator_material / elevator_annual_capacity)
                # 根据问题编号计算太空电梯部分成本
                if problem == 1:
                    # Problem 1: 100%可靠性
                    cost_elevator_per = (ELEVATOR_COST_PER_TON * M_0 + TUG_COST_FUEL_PER * M_PROP + TUG_COST_VEHICLE / TUG_N) / (elevator_reliability * tug_reliability)
                else:
                    # Problem 2: 使用默认计算的成本
                    cost_elevator_per = COST_ELEVATOR_PER
                elevator_cost = elevator_material * cost_elevator_per
            else:
                elevator_years = 0
                elevator_cost = 0
            
            # 火箭计算
            if rocket_ratio > 0:
                # 火箭系统年运输能力
                rocket_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
                # 计算火箭部分所需时间，向上取整
                rocket_years = np.ceil(rocket_material / rocket_annual_capacity)
                # 计算火箭部分发射次数
                rocket_launches = np.ceil(rocket_material / ROCKET_PAYLOAD_AVG)
                # 根据问题编号计算火箭部分成本
                if problem == 1:
                    # Problem 1: 100%可靠性
                    cost_rocket_per = ROCKET_THETA * ROCKET_COST_PER_LAUNCH / (ROCKET_PAYLOAD_AVG * ROCKET_N_G * rocket_reliability)
                else:
                    # Problem 2: 使用默认计算的成本
                    cost_rocket_per = COST_ROCKET_PER
                rocket_cost = rocket_material * cost_rocket_per
            else:
                rocket_years = 0
                rocket_cost = 0
            
            # 总计算：总时间由运输能力较慢的部分决定
            years_needed = max(elevator_years, rocket_years)
            # 计算总成本：两部分成本之和
            total_cost = elevator_cost + rocket_cost
            
            f.write(f"太空电梯比例: {elevator_ratio*100}%\n")
            f.write(f"传统火箭比例: {rocket_ratio*100}%\n")
            f.write(f"所需时间: {years_needed} 年\n")
            f.write(f"总成本: {total_cost}\n")
            f.write("\n")

# 主函数
def main():
    """运行所有计算并输出结果
    
    计算三个场景的运输方案，分析系统故障影响，并保存结果到文件
    同时运行 Problem 1（100%可靠性）和 Problem 2（当前可靠性）的计算
    """
    # 运行 Problem 1（100%可靠性）
    print("=== Problem 1: 100%可靠性 ===")
    scenario1_p1 = calculate_scenario_1(1)
    scenario2_p1 = calculate_scenario_2(1)
    scenario3_p1 = calculate_scenario_3(1)
    
    print("\n=== 场景分析 ===")
    for scenario in [scenario1_p1, scenario2_p1, scenario3_p1]:
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
    impacted_scenarios_p1 = calculate_reliability_impact(1)
    for scenario in impacted_scenarios_p1:
        print(f"场景: {scenario['name']}")
        print(f"所需时间: {scenario['years_needed']} 年")
        print(f"完成年份: {scenario['completion_year']}")
        print(f"总成本: ${scenario['total_cost']:,.2f}")
        print()
    
    # 保存 Problem 1 结果到文件
    save_results_to_file(1)
    print("Problem 1 结果已保存到 results/problem_1/ 目录")
    
    # 运行 Problem 2（当前可靠性）
    print("\n=== Problem 2: 当前可靠性 ===")
    scenario1_p2 = calculate_scenario_1(2)
    scenario2_p2 = calculate_scenario_2(2)
    scenario3_p2 = calculate_scenario_3(2)
    
    print("\n=== 场景分析 ===")
    for scenario in [scenario1_p2, scenario2_p2, scenario3_p2]:
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
    impacted_scenarios_p2 = calculate_reliability_impact(2)
    for scenario in impacted_scenarios_p2:
        print(f"场景: {scenario['name']}")
        print(f"所需时间: {scenario['years_needed']} 年")
        print(f"完成年份: {scenario['completion_year']}")
        print(f"总成本: ${scenario['total_cost']:,.2f}")
        print()
    
    # 保存 Problem 2 结果到文件
    save_results_to_file(2)
    print("Problem 2 结果已保存到 results/problem_2/ 目录")

if __name__ == "__main__":
    main()
