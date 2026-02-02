import numpy as np
import matplotlib.pyplot as plt
from src.constants import *

# 计算每个场景的成本和时间线
def calculate_scenario_1(problem=2):
    """Scenario 1: Space Elevator Only
    
    计算仅使用太空电梯系统时的运输时间和成本
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性），3表示Problem 3（额外材料需求）
        
    Returns:
        dict: 包含场景名称、所需时间、完成年份、总成本和年运输能力的字典
    """
    # 根据问题编号选择可靠性设置
    if problem == 1:
        # Problem 1: 使用100%可靠性
        elevator_reliability = ELEVATOR_RELIABILITY_P1
        tug_reliability = TUG_RELIABILITY_P1
        cost_elevator_per = COST_ELEVATOR_PER_P1
    elif problem == 3:
        # Problem 3: 使用当前可靠性（与Problem 2相同）
        elevator_reliability = ELEVATOR_RELIABILITY_P2
        tug_reliability = TUG_RELIABILITY_P2
        cost_elevator_per = COST_ELEVATOR_PER_P2
    else:  # problem == 2
        # Problem 2: 使用当前可靠性
        elevator_reliability = ELEVATOR_RELIABILITY_P2
        tug_reliability = TUG_RELIABILITY_P2
        cost_elevator_per = COST_ELEVATOR_PER_P2
    
    # 根据问题编号选择总材料需求
    if problem == 3:
        total_material = TOTAL_MATERIAL_P3
    else:
        total_material = TOTAL_MATERIAL
    
    # 计算太空电梯系统的理论年运输能力
    # 理论年运输能力 = 银河港数量 * 每个银河港年运输能力
    theoretical_annual_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
    
    # 计算有效年运输能力：考虑可靠性因素
    # 有效年运输能力 = 理论年运输能力 * 太空电梯可靠性 * 摆渡火箭可靠性
    effective_annual_capacity = theoretical_annual_capacity * elevator_reliability * tug_reliability
    
    # 计算所需时间：总材料需求除以有效年运输能力，向上取整
    years_needed = np.ceil(total_material / effective_annual_capacity)
    # 计算总成本：总材料需求乘以单位有效载荷成本
    total_cost = total_material * cost_elevator_per
    # 计算完成年份
    completion_year = START_YEAR + years_needed
    
    return {
        "name": "Space Elevator Only",
        "years_needed": years_needed,
        "completion_year": completion_year,
        "total_cost": total_cost,
        "annual_capacity": effective_annual_capacity
    }

def calculate_scenario_2(problem=2):
    """Scenario 2: Traditional Rockets Only
    
    计算仅使用传统火箭系统时的运输时间和成本
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性），3表示Problem 3（额外材料需求）
        
    Returns:
        dict: 包含场景名称、所需时间、完成年份、总成本和年运输能力的字典
    """
    # 根据问题编号选择可靠性设置
    if problem == 1:
        # Problem 1: 使用100%可靠性
        rocket_reliability = ROCKET_RELIABILITY_P1
        cost_rocket_per = COST_ROCKET_PER_P1
    elif problem == 3:
        # Problem 3: 使用当前可靠性（与Problem 2相同）
        rocket_reliability = ROCKET_RELIABILITY_P2
        cost_rocket_per = COST_ROCKET_PER_P2
    else:  # problem == 2
        # Problem 2: 使用当前可靠性
        rocket_reliability = ROCKET_RELIABILITY_P2
        cost_rocket_per = COST_ROCKET_PER_P2
    
    # 根据问题编号选择总材料需求
    if problem == 3:
        total_material = TOTAL_MATERIAL_P3
    else:
        total_material = TOTAL_MATERIAL
    
    # 计算火箭系统的理论年运输能力
    # 理论年运输能力 = 发射场数量 * 每个发射场年发射次数 * 平均有效载荷
    theoretical_annual_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
    
    # 计算有效年运输能力：考虑可靠性因素
    # 有效年运输能力 = 理论年运输能力 * 火箭可靠性
    effective_annual_capacity = theoretical_annual_capacity * rocket_reliability
    
    # 计算所需时间：总材料需求除以有效年运输能力，向上取整
    years_needed = np.ceil(total_material / effective_annual_capacity)
    # 计算总成本：总材料需求乘以单位有效载荷成本
    total_cost = total_material * cost_rocket_per
    # 计算完成年份
    completion_year = START_YEAR + years_needed
    
    return {
        "name": "Traditional Rockets Only",
        "years_needed": years_needed,
        "completion_year": completion_year,
        "total_cost": total_cost,
        "annual_capacity": effective_annual_capacity
    }

def calculate_scenario_3(problem=2, time_limit=None):
    """Scenario 3: Combined Space Elevator and Traditional Rockets (Finding Optimal Ratio)
    
    计算太空电梯和传统火箭组合使用时的最优比例
    - 如果提供了time_limit，则寻找能在该时间内完成且成本最小的组合
    - 如果未提供time_limit，则寻找总成本最小的组合
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性），3表示Problem 3（额外材料需求）
        time_limit (int, optional): 时间限制（年）。如果为None，则寻找总成本最小的组合
        
    Returns:
        dict: 包含场景名称、所需时间、完成年份、总成本、各部分运输量和比例的字典
    """
    best_scenario = None
    min_total_cost = float('inf')
    
    # 根据问题编号选择总材料需求
    if problem == 3:
        total_material = TOTAL_MATERIAL_P3
    else:
        total_material = TOTAL_MATERIAL
    
    # 使用通用函数获取所有比例的分析结果
    ratio_scenarios = calculate_combined_ratio_analysis(problem)
    
    # 遍历所有比例方案，寻找最优解
    for scenario in ratio_scenarios:
        elevator_ratio = scenario['elevator_ratio']
        rocket_ratio = scenario['rocket_ratio']
        years_needed = scenario['years_needed']
        total_cost = scenario['total_cost']
        
        # 计算各部分运输量
        elevator_material = total_material * elevator_ratio
        rocket_material = total_material * rocket_ratio
        
        # 更新最优解
        if time_limit is None:
            # 无时间限制，寻找总成本最小的方案
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
        else:
            # 有时间限制，寻找能在时间限制内完成且成本最小的方案
            if years_needed <= time_limit and total_cost < min_total_cost:
                min_total_cost = total_cost
                best_scenario = {
                    "name": "Combined System",
                    "years_needed": years_needed,
                    "completion_year": START_YEAR + years_needed,
                    "total_cost": total_cost,
                    "elevator_material": elevator_material,
                    "rocket_material": rocket_material,
                    "elevator_ratio": elevator_ratio,
                    "rocket_ratio": rocket_ratio,
                    "time_limit": time_limit
                }
    
    return best_scenario

# 计算不同比例下的组合方案
def calculate_combined_ratio_analysis(problem=2):
    """计算不同太空电梯比例下的组合方案分析
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性），3表示Problem 3（额外材料需求）
        
    Returns:
        list: 包含不同比例下组合方案分析结果的列表
    """
    scenarios = []
    
    # 根据问题编号选择可靠性设置
    if problem == 1:
        elevator_reliability = ELEVATOR_RELIABILITY_P1
        tug_reliability = TUG_RELIABILITY_P1
        rocket_reliability = ROCKET_RELIABILITY_P1
    else:  # problem == 2 or problem == 3
        elevator_reliability = ELEVATOR_RELIABILITY_P2
        tug_reliability = TUG_RELIABILITY_P2
        rocket_reliability = ROCKET_RELIABILITY_P2
    
    # 根据问题编号选择总材料需求
    if problem == 3:
        total_material = TOTAL_MATERIAL_P3
    else:
        total_material = TOTAL_MATERIAL
    
    # 遍历不同的太空电梯比例（从0%到100%，步长1%）
    for elevator_ratio in range(0, 101, 1):
        elevator_ratio = elevator_ratio / 100
        rocket_ratio = 1 - elevator_ratio
        
        # 计算各部分运输量
        elevator_material = total_material * elevator_ratio
        rocket_material = total_material * rocket_ratio
        
        # 太空电梯计算
        if elevator_ratio > 0:
            # 太空电梯系统理论年运输能力
            theoretical_elevator_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
            # 太空电梯系统有效年运输能力：考虑可靠性因素
            effective_elevator_capacity = theoretical_elevator_capacity * elevator_reliability * tug_reliability
            # 计算太空电梯部分所需时间，向上取整
            elevator_years = np.ceil(elevator_material / effective_elevator_capacity)
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
            # 火箭系统理论年运输能力
            theoretical_rocket_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
            # 火箭系统有效年运输能力：考虑可靠性因素
            effective_rocket_capacity = theoretical_rocket_capacity * rocket_reliability
            # 计算火箭部分所需时间，向上取整
            rocket_years = np.ceil(rocket_material / effective_rocket_capacity)
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
        
        scenarios.append({
            "elevator_ratio": elevator_ratio,
            "rocket_ratio": rocket_ratio,
            "elevator_years": elevator_years,
            "rocket_years": rocket_years,
            "years_needed": years_needed,
            "elevator_cost": elevator_cost,
            "rocket_cost": rocket_cost,
            "total_cost": total_cost
        })
    
    return scenarios

# 计算不同时间限制下的最优组合方案
def calculate_combined_scenarios_by_time_limit(problem=2, time_limits=None):
    """计算不同时间限制下的最优组合方案
    
    Args:
        problem (int): 问题编号，1表示Problem 1（100%可靠性），2表示Problem 2（当前可靠性）
        time_limits (list, optional): 时间限制列表。如果为None，默认使用 range(150, 410, 10)
        
    Returns:
        list: 包含不同时间限制下最优方案的列表
    """
    if time_limits is None:
        # 默认时间限制列表
        time_limits = range(10, 410, 10)
    
    scenarios = []
    for time_limit in time_limits:
        scenario = calculate_scenario_3(problem, time_limit)
        if scenario:
            scenarios.append(scenario)
    
    return scenarios



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
    

    
    # 保存组合场景的比例分析
    ratio_file = os.path.join(problem_dir, 'ratio_analysis.txt')
    with open(ratio_file, 'w') as f:
        f.write(f"=== 组合场景比例分析 (Problem {problem}) ===\n")
        
        # 使用通用函数计算比例分析
        ratio_scenarios = calculate_combined_ratio_analysis(problem)
        
        for scenario in ratio_scenarios:
            f.write(f"太空电梯比例: {scenario['elevator_ratio']*100}%\n")
            f.write(f"传统火箭比例: {scenario['rocket_ratio']*100}%\n")
            f.write(f"所需时间: {scenario['years_needed']} 年\n")
            f.write(f"总成本: {scenario['total_cost']}\n")
            f.write("\n")
    
    # 保存不同时间限制下的最优组合方案
    time_limit_file = os.path.join(problem_dir, 'time_limit_analysis.txt')
    with open(time_limit_file, 'w') as f:
        f.write(f"=== 不同时间限制下的最优组合方案分析 (Problem {problem}) ===\n")
        
        # 计算不同时间限制下的最优方案
        time_limit_scenarios = calculate_combined_scenarios_by_time_limit(problem)
        
        for scenario in time_limit_scenarios:
            f.write(f"时间限制: {scenario.get('time_limit', 'N/A')} 年\n")
            f.write(f"实际所需时间: {scenario['years_needed']} 年\n")
            f.write(f"太空电梯比例: {scenario['elevator_ratio']*100}%\n")
            f.write(f"传统火箭比例: {scenario['rocket_ratio']*100}%\n")
            f.write(f"总成本: {scenario['total_cost']}\n")
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
    

    
    # 保存 Problem 2 结果到文件
    save_results_to_file(2)
    print("Problem 2 结果已保存到 results/problem_2/ 目录")
    
    # 运行 Problem 3（额外材料需求）
    print("\n=== Problem 3: 额外材料需求 ===")
    print(f"额外材料需求: {EXTRA_MATERIAL_P3} 吨")
    print(f"总材料需求: {TOTAL_MATERIAL_P3} 吨")
    scenario1_p3 = calculate_scenario_1(3)
    scenario2_p3 = calculate_scenario_2(3)
    scenario3_p3 = calculate_scenario_3(3)
    
    print("\n=== 场景分析 ===")
    for scenario in [scenario1_p3, scenario2_p3, scenario3_p3]:
        print(f"场景: {scenario['name']}")
        print(f"所需时间: {scenario['years_needed']} 年")
        print(f"完成年份: {scenario['completion_year']}")
        print(f"总成本: ${scenario['total_cost']:,.2f}")
        if 'elevator_ratio' in scenario:
            print(f"太空电梯比例: {scenario['elevator_ratio']*100}%")
            print(f"传统火箭比例: {scenario['rocket_ratio']*100}%")
        print()
    
    # 保存 Problem 3 结果到文件
    save_results_to_file(3)
    print("Problem 3 结果已保存到 results/problem_3/ 目录")

if __name__ == "__main__":
    main()
