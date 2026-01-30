import matplotlib.pyplot as plt
import numpy as np

import os

# 获取结果目录的绝对路径
def get_results_dir():
    """获取结果目录的绝对路径"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')

# 读取场景分析结果
def read_scenario_analysis():
    """读取场景分析结果"""
    scenarios = []
    results_dir = get_results_dir()
    scenario_file = os.path.join(results_dir, 'scenario_analysis.txt')
    
    with open(scenario_file, 'r') as f:
        lines = f.readlines()
        current_scenario = {}
        for line in lines:
            line = line.strip()
            if line.startswith('场景:'):
                if current_scenario:
                    scenarios.append(current_scenario)
                    current_scenario = {}
                current_scenario['name'] = line.split('场景: ')[1]
            elif line.startswith('所需时间:'):
                current_scenario['years'] = float(line.split('所需时间: ')[1].split(' 年')[0])
            elif line.startswith('完成年份:'):
                current_scenario['completion_year'] = int(float(line.split('完成年份: ')[1]))
            elif line.startswith('总成本:'):
                current_scenario['cost'] = float(line.split('总成本: ')[1])
            elif line.startswith('太空电梯比例:'):
                current_scenario['elevator_ratio'] = float(line.split('太空电梯比例: ')[1].split('%')[0]) / 100
            elif line.startswith('传统火箭比例:'):
                current_scenario['rocket_ratio'] = float(line.split('传统火箭比例: ')[1].split('%')[0]) / 100
        if current_scenario:
            scenarios.append(current_scenario)
    return scenarios

# 读取系统故障影响结果
def read_reliability_impact():
    """读取系统故障影响结果"""
    scenarios = []
    results_dir = get_results_dir()
    reliability_file = os.path.join(results_dir, 'reliability_impact.txt')
    
    with open(reliability_file, 'r') as f:
        lines = f.readlines()
        current_scenario = {}
        for line in lines:
            line = line.strip()
            if line.startswith('场景:'):
                if current_scenario:
                    scenarios.append(current_scenario)
                    current_scenario = {}
                current_scenario['name'] = line.split('场景: ')[1]
            elif line.startswith('所需时间:'):
                current_scenario['years'] = float(line.split('所需时间: ')[1].split(' 年')[0])
            elif line.startswith('完成年份:'):
                current_scenario['completion_year'] = int(float(line.split('完成年份: ')[1]))
            elif line.startswith('总成本:'):
                current_scenario['cost'] = float(line.split('总成本: ')[1])
        if current_scenario:
            scenarios.append(current_scenario)
    return scenarios

# 读取比例分析结果
def read_ratio_analysis():
    """读取组合场景比例分析结果"""
    ratios = []
    years = []
    costs = []
    results_dir = get_results_dir()
    ratio_file = os.path.join(results_dir, 'ratio_analysis.txt')
    
    with open(ratio_file, 'r') as f:
        lines = f.readlines()
        current_ratio = {}
        for line in lines:
            line = line.strip()
            if line.startswith('太空电梯比例:'):
                if current_ratio:
                    ratios.append(current_ratio['elevator_ratio'])
                    years.append(current_ratio['years'])
                    costs.append(current_ratio['cost'])
                    current_ratio = {}
                current_ratio['elevator_ratio'] = float(line.split('太空电梯比例: ')[1].split('%')[0]) / 100
            elif line.startswith('传统火箭比例:'):
                current_ratio['rocket_ratio'] = float(line.split('传统火箭比例: ')[1].split('%')[0]) / 100
            elif line.startswith('所需时间:'):
                current_ratio['years'] = float(line.split('所需时间: ')[1].split(' 年')[0])
            elif line.startswith('总成本:'):
                current_ratio['cost'] = float(line.split('总成本: ')[1])
        if current_ratio:
            ratios.append(current_ratio['elevator_ratio'])
            years.append(current_ratio['years'])
            costs.append(current_ratio['cost'])
    return ratios, years, costs

# 绘制场景对比图
def plot_scenario_comparison():
    """Plot cost and time comparison for all scenarios"""
    scenarios = read_scenario_analysis()
    
    names = [scenario['name'] for scenario in scenarios]
    costs = [scenario['cost'] / 1e9 for scenario in scenarios]  # Convert to billions of dollars
    years = [scenario['years'] for scenario in scenarios]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Cost comparison
    ax1.bar(names, costs, color=['blue', 'green', 'purple'])
    ax1.set_title('Total Cost Comparison')
    ax1.set_ylabel('Total Cost (Billion USD)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Time comparison
    ax2.bar(names, years, color=['blue', 'green', 'purple'])
    ax2.set_title('Time Required Comparison')
    ax2.set_ylabel('Time Required (Years)')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'scenario_comparison.png')
    plt.savefig(output_file)
    print(f'Scenario comparison chart saved to {output_file}')

# 绘制系统故障影响对比图
def plot_reliability_impact():
    """Plot impact of system failures on each scenario"""
    normal_scenarios = read_scenario_analysis()
    impacted_scenarios = read_reliability_impact()
    
    # Create mapping for easy comparison
    normal_map = {scenario['name']: scenario for scenario in normal_scenarios}
    impacted_map = {scenario['name']: scenario for scenario in impacted_scenarios}
    
    names = list(normal_map.keys())
    normal_costs = [normal_map[name]['cost'] / 1e9 for name in names]  # Convert to billions of dollars
    impacted_costs = [impacted_map[name]['cost'] / 1e9 for name in names]
    normal_years = [normal_map[name]['years'] for name in names]
    impacted_years = [impacted_map[name]['years'] for name in names]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Cost comparison
    x = np.arange(len(names))
    width = 0.35
    
    ax1.bar(x - width/2, normal_costs, width, label='Normal Condition', color='blue')
    ax1.bar(x + width/2, impacted_costs, width, label='System Failure', color='red')
    ax1.set_title('Impact of System Failures on Cost')
    ax1.set_ylabel('Total Cost (Billion USD)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45)
    ax1.legend()
    
    # Time comparison
    ax2.bar(x - width/2, normal_years, width, label='Normal Condition', color='blue')
    ax2.bar(x + width/2, impacted_years, width, label='System Failure', color='red')
    ax2.set_title('Impact of System Failures on Time')
    ax2.set_ylabel('Time Required (Years)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=45)
    ax2.legend()
    
    plt.tight_layout()
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_impact.png')
    plt.savefig(output_file)
    print(f'System failure impact chart saved to {output_file}')

# 绘制组合场景比例分析图
def plot_ratio_analysis():
    """Plot cost and time variation with different ratios in combined scenario"""
    ratios, years, costs = read_ratio_analysis()
    
    # Convert to percentage
    ratio_percent = [r * 100 for r in ratios]
    # Convert cost to billions of dollars
    costs_billion = [c / 1e9 for c in costs]
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Cost variation with ratio (left y-axis)
    color = 'tab:blue'
    ax1.set_xlabel('Space Elevator Ratio (%)')
    ax1.set_ylabel('Total Cost (Billion USD)', color=color)
    ax1.plot(ratio_percent, costs_billion, 'o-', color=color, label='Total Cost')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Time variation with ratio (right y-axis)
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Time Required (Years)', color=color)
    ax2.plot(ratio_percent, years, 's-', color=color, label='Time Required')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Title and legend
    plt.title('Cost and Time Variation with Space Elevator Ratio')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center')
    
    plt.tight_layout()
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'ratio_analysis.png')
    plt.savefig(output_file)
    print(f'Ratio analysis chart saved to {output_file}')

# Main function
def main():
    """Run all plotting functions"""
    plot_scenario_comparison()
    plot_reliability_impact()
    plot_ratio_analysis()

if __name__ == "__main__":
    main()
