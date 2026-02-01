"""
plotter for main_model
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import os

# 获取结果目录的绝对路径
def get_results_dir(problem=None):
    """获取结果目录的绝对路径
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。如果为None，返回根results目录
        
    Returns:
        str: 结果目录的绝对路径
    """
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    if problem is not None:
        return os.path.join(base_dir, f'problem_{problem}')
    return base_dir

# 读取场景分析结果
def read_scenario_analysis(problem=2):
    """读取场景分析结果
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。默认为2
        
    Returns:
        list: 场景分析结果列表
    """
    scenarios = []
    results_dir = get_results_dir(problem)
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



# 读取比例分析结果
def read_ratio_analysis(problem=2):
    """读取组合场景比例分析结果
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。默认为2
        
    Returns:
        tuple: 包含比例、时间和成本的元组
    """
    ratios = []
    years = []
    costs = []
    results_dir = get_results_dir(problem)
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

# 读取不同时间限制下的最优方案结果
def read_time_limit_analysis(problem=2):
    """读取不同时间限制下的最优方案结果
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。默认为2
        
    Returns:
        tuple: 包含时间限制、实际时间、成本、太空电梯比例和传统火箭比例的元组
    """
    time_limits = []
    actual_years = []
    costs = []
    elevator_ratios = []
    rocket_ratios = []
    
    results_dir = get_results_dir(problem)
    time_limit_file = os.path.join(results_dir, 'time_limit_analysis.txt')
    
    with open(time_limit_file, 'r') as f:
        lines = f.readlines()
        current_scenario = {}
        for line in lines:
            line = line.strip()
            if line.startswith('时间限制:'):
                if current_scenario:
                    time_limits.append(current_scenario['time_limit'])
                    actual_years.append(current_scenario['actual_years'])
                    costs.append(current_scenario['cost'])
                    elevator_ratios.append(current_scenario['elevator_ratio'])
                    rocket_ratios.append(current_scenario['rocket_ratio'])
                    current_scenario = {}
                current_scenario['time_limit'] = float(line.split('时间限制: ')[1].split(' 年')[0])
            elif line.startswith('实际所需时间:'):
                current_scenario['actual_years'] = float(line.split('实际所需时间: ')[1].split(' 年')[0])
            elif line.startswith('太空电梯比例:'):
                current_scenario['elevator_ratio'] = float(line.split('太空电梯比例: ')[1].split('%')[0]) / 100
            elif line.startswith('传统火箭比例:'):
                current_scenario['rocket_ratio'] = float(line.split('传统火箭比例: ')[1].split('%')[0]) / 100
            elif line.startswith('总成本:'):
                current_scenario['cost'] = float(line.split('总成本: ')[1])
        if current_scenario:
            time_limits.append(current_scenario['time_limit'])
            actual_years.append(current_scenario['actual_years'])
            costs.append(current_scenario['cost'])
            elevator_ratios.append(current_scenario['elevator_ratio'])
            rocket_ratios.append(current_scenario['rocket_ratio'])
    
    return time_limits, actual_years, costs, elevator_ratios, rocket_ratios

# 绘制场景对比图
def plot_scenario_comparison(problem=2):
    """Plot cost and time comparison for all scenarios
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。默认为2
    """
    scenarios = read_scenario_analysis(problem)
    
    names = [scenario['name'] for scenario in scenarios]
    costs = [scenario['cost'] / 1e9 for scenario in scenarios]  # Convert to billions of dollars
    years = [scenario['years'] for scenario in scenarios]
    
    # 使用更美观的颜色方案
    colors = ['#1f77b4', '#2ca02c', '#9467bd']  # 蓝色、绿色、紫色
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # 设置整体字体大小
    plt.rcParams.update({'font.size': 12})
    
    # Cost comparison
    bars1 = ax1.bar(names, costs, color=colors, edgecolor='black', alpha=0.8)
    ax1.set_title('Total Cost Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Total Cost (Billion USD)', fontsize=12)
    ax1.tick_params(axis='x', rotation=45, labelsize=11)
    ax1.tick_params(axis='y', labelsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # 添加成本数据标签
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10)
    
    # Time comparison
    bars2 = ax2.bar(names, years, color=colors, edgecolor='black', alpha=0.8)
    ax2.set_title('Time Required Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Time Required (Years)', fontsize=12)
    ax2.tick_params(axis='x', rotation=45, labelsize=11)
    ax2.tick_params(axis='y', labelsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    # 添加时间数据标签
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}', ha='center', va='bottom', fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 添加整体标题
    fig.suptitle(f'Scenario Comparison Analysis (Problem {problem})', fontsize=16, fontweight='bold', y=1.02)
    
    results_dir = get_results_dir(problem)
    output_file = os.path.join(results_dir, 'scenario_comparison.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=150)
    print(f'Scenario comparison chart saved to {output_file}')



# 绘制组合场景比例分析图
def plot_ratio_analysis(problem=2):
    """Plot cost and time variation with different ratios in combined scenario
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。默认为2
    """
    ratios, years, costs = read_ratio_analysis(problem)
    # 原始数据转换：比例转百分比，成本转十亿美元
    ratio_percent = [r * 100 for r in ratios]
    costs_billion = [c / 1e9 for c in costs]
    
    # ===================== 1. 绘制原有双轴折线图（保留原逻辑）=====================
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    # 成本曲线（左轴）
    color_cost = '#1f77b4'
    ax1.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax1.set_ylabel('Total Cost (Billion USD)', color=color_cost, fontsize=12)
    ax1.plot(ratio_percent, costs_billion, 'o-', color=color_cost, label='Total Cost', linewidth=2, markersize=6)
    ax1.tick_params(axis='y', labelcolor=color_cost, labelsize=11)
    ax1.grid(True, alpha=0.3)
    # 时间曲线（右轴）
    color_time = '#2ca02c'
    ax2 = ax1.twinx()
    ax2.set_ylabel('Time Required (Years)', color=color_time, fontsize=12)
    ax2.plot(ratio_percent, years, 's-', color=color_time, label='Time Required', linewidth=2, markersize=6)
    ax2.tick_params(axis='y', labelcolor=color_time, labelsize=11)
    # 标题和图例
    fig1.suptitle(f'Cost & Time vs Space Elevator Ratio (Line Chart) - Problem {problem}', fontsize=14, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=11)
    # 保存折线图
    results_dir = get_results_dir(problem)
    line_file = os.path.join(results_dir, 'ratio_analysis_line.png')
    plt.tight_layout()
    plt.savefig(line_file, bbox_inches='tight', dpi=150)
    print(f'Ratio analysis line chart saved to {line_file}')
    plt.close(fig1)

    # ===================== 2. 绘制10%步长双组柱形图（核心新增）=====================
    # 2.1 生成10%步长的目标比例（0,10,20,...,100）
    target_ratios = np.arange(0, 101, 10)  # 严格10%步长
    # 2.2 插值匹配原始数据到目标比例（保证每个步长有对应成本/时间）
    f_cost = interp1d(ratio_percent, costs_billion, kind='linear', fill_value='extrapolate')
    f_time = interp1d(ratio_percent, years, kind='linear', fill_value='extrapolate')
    target_costs = f_cost(target_ratios)  # 目标比例对应的成本
    target_years = f_time(target_ratios)  # 目标比例对应的时间

    # 2.3 绘制双组柱形图
    fig2, ax = plt.subplots(figsize=(14, 7))
    # 柱形参数：宽度、偏移量（避免重叠）
    bar_width = 3.5  # 柱形宽度，适配10%步长
    x1 = target_ratios - bar_width/2  # 成本柱形x坐标
    x2 = target_ratios + bar_width/2  # 时间柱形x坐标
    # 定义配色（论文级，与折线图统一）
    color_cost_bar = '#1f77b4'
    color_time_bar = '#2ca02c'

    # 绘制成本柱形
    bars1 = ax.bar(x1, target_costs, width=bar_width, label='Total Cost (Billion USD)',
                   color=color_cost_bar, edgecolor='black', alpha=0.8)
    # 绘制时间柱形（次坐标轴，因为成本和时间量纲不同）
    ax_twin = ax.twinx()
    bars2 = ax_twin.bar(x2, target_years, width=bar_width, label='Time Required (Years)',
                        color=color_time_bar, edgecolor='black', alpha=0.8)

    # 2.4 图表样式设置
    # 主坐标轴（成本）
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Cost (Billion USD)', fontsize=12, fontweight='bold', color=color_cost_bar)
    ax.tick_params(axis='x', labelsize=11)
    ax.tick_params(axis='y', labelcolor=color_cost_bar, labelsize=11)
    ax.set_xticks(target_ratios)  # x轴刻度严格匹配10%步长
    ax.grid(axis='y', alpha=0.3)
    # 次坐标轴（时间）
    ax_twin.set_ylabel('Time Required (Years)', fontsize=12, fontweight='bold', color=color_time_bar)
    ax_twin.tick_params(axis='y', labelcolor=color_time_bar, labelsize=11)
    # 标题
    fig2.suptitle(f'Cost & Time vs Space Elevator Ratio (Bar Chart, 10% Step) - Problem {problem}',
                  fontsize=14, fontweight='bold', y=1.02)
    # 合并图例
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=11, ncol=2)

    # 2.5 添加数据标签（柱形顶部显示数值，更直观）
    # 成本标签
    for bar, val in zip(bars1, target_costs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(target_costs)*0.01,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    # 时间标签
    for bar, val in zip(bars2, target_years):
        height = bar.get_height()
        ax_twin.text(bar.get_x() + bar.get_width()/2., height + max(target_years)*0.02,
                     f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 2.6 保存柱形图
    bar_file = os.path.join(results_dir, 'ratio_analysis_bar_10step.png')
    plt.tight_layout()
    plt.savefig(bar_file, bbox_inches='tight', dpi=150)
    print(f'Ratio analysis bar chart (10% step) saved to {bar_file}')
    plt.close(fig2)
    # ratios, years, costs = read_ratio_analysis(problem)
    
    # # Convert to percentage
    # ratio_percent = [r * 100 for r in ratios]
    # # Convert cost to billions of dollars
    # costs_billion = [c / 1e9 for c in costs]
    
    # fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # # Cost variation with ratio (left y-axis)
    # color = 'tab:blue'
    # ax1.set_xlabel('Space Elevator Ratio (%)')
    # ax1.set_ylabel('Total Cost (Billion USD)', color=color)
    # ax1.plot(ratio_percent, costs_billion, 'o-', color=color, label='Total Cost')
    # ax1.tick_params(axis='y', labelcolor=color)
    # ax1.grid(True, alpha=0.3)
    
    # # Time variation with ratio (right y-axis)
    # ax2 = ax1.twinx()
    # color = 'tab:green'
    # ax2.set_ylabel('Time Required (Years)', color=color)
    # ax2.plot(ratio_percent, years, 's-', color=color, label='Time Required')
    # ax2.tick_params(axis='y', labelcolor=color)
    
    # # Title and legend
    # plt.title('Cost and Time Variation with Space Elevator Ratio')
    
    # # Combine legends
    # lines1, labels1 = ax1.get_legend_handles_labels()
    # lines2, labels2 = ax2.get_legend_handles_labels()
    # ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center')
    
    # plt.tight_layout()
    # results_dir = get_results_dir(problem)
    # output_file = os.path.join(results_dir, 'ratio_analysis.png')
    # plt.savefig(output_file)
    # print(f'Ratio analysis chart saved to {output_file}')

# 绘制Problem 1和Problem 2的对比图
def plot_reliability_comparison():
    """Plot comparison between Problem 1 (100% reliability) and Problem 2 (current reliability)
    
    目的：显示两份数据的区别，说明不可靠扰动对方案影响不大
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 转换为百分比和十亿美元
    ratio_percent_p1 = [r * 100 for r in ratios_p1]
    ratio_percent_p2 = [r * 100 for r in ratios_p2]
    costs_billion_p1 = [c / 1e9 for c in costs_p1]
    costs_billion_p2 = [c / 1e9 for c in costs_p2]
    
    # 计算差异
    cost_diff = [abs(costs_billion_p1[i] - costs_billion_p2[i]) for i in range(len(costs_billion_p1))]
    year_diff = [abs(years_p1[i] - years_p2[i]) for i in range(len(years_p1))]
    
    # 创建对比图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 10))
    
    # 设置整体字体
    plt.rcParams.update({'font.size': 12})
    
    # 成本对比图
    ax1.plot(ratio_percent_p1, costs_billion_p1, 'o-', color='#1f77b4', alpha=0.7, label='Problem 1 (100% Reliability)')
    ax1.plot(ratio_percent_p2, costs_billion_p2, 'o-', color='#2ca02c', alpha=0.7, label='Problem 2 (Current Reliability)')
    ax1.set_title('Cost Comparison: Problem 1 vs Problem 2', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax1.set_ylabel('Total Cost (Billion USD)', fontsize=12)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # 时间对比图
    ax2.plot(ratio_percent_p1, years_p1, 's-', color='#1f77b4', alpha=0.7, label='Problem 1 (100% Reliability)')
    ax2.plot(ratio_percent_p2, years_p2, 's-', color='#2ca02c', alpha=0.7, label='Problem 2 (Current Reliability)')
    ax2.set_title('Time Comparison: Problem 1 vs Problem 2', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax2.set_ylabel('Time Required (Years)', fontsize=12)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # 添加整体标题和说明
    fig.suptitle('Reliability Impact Analysis: 100% vs Current Reliability', fontsize=16, fontweight='bold', y=1.02)
    fig.text(0.5, 0.02, 'Note: Small differences indicate minimal impact of reliability variations', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    plt.tight_layout()
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_comparison.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f'Reliability comparison chart saved to {output_file}')

# 绘制差异分析图
def plot_reliability_difference_analysis():
    """Plot absolute and relative differences between Problem 1 and Problem 2
    
    目的：显示两份数据的差异，说明不可靠扰动对方案影响不大
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 转换为百分比和十亿美元
    ratio_percent = [r * 100 for r in ratios_p1]
    costs_billion_p1 = [c / 1e9 for c in costs_p1]
    costs_billion_p2 = [c / 1e9 for c in costs_p2]
    
    # 计算绝对差异
    cost_diff = [abs(costs_billion_p1[i] - costs_billion_p2[i]) for i in range(len(costs_billion_p1))]
    year_diff = [abs(years_p1[i] - years_p2[i]) for i in range(len(years_p1))]
    
    # 计算相对差异（百分比）
    cost_pct_diff = [((costs_billion_p2[i] - costs_billion_p1[i]) / costs_billion_p1[i]) * 100 for i in range(len(costs_billion_p1))]
    
    # 创建差异分析图表
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(18, 14))
    
    # 设置整体字体
    plt.rcParams.update({'font.size': 12})
    
    # 成本绝对差异图
    ax1.plot(ratio_percent, cost_diff, 'o-', color='#ff7f0e', linewidth=2, markersize=6)
    ax1.set_title('Absolute Cost Difference Between Problem 1 and Problem 2', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax1.set_ylabel('Cost Difference (Billion USD)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 时间绝对差异图
    ax2.plot(ratio_percent, year_diff, 's-', color='#d62728', linewidth=2, markersize=6)
    ax2.set_title('Absolute Time Difference Between Problem 1 and Problem 2', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax2.set_ylabel('Time Difference (Years)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 成本相对差异图（百分比）
    ax3.plot(ratio_percent, cost_pct_diff, '^-', color='#9467bd', linewidth=2, markersize=6)
    ax3.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax3.set_title('Relative Cost Difference (Percentage Change)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax3.set_ylabel('Cost Difference (%)', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # 添加整体标题和说明
    fig.suptitle('Reliability Impact Analysis: Difference Between 100% and Current Reliability', 
                  fontsize=16, fontweight='bold', y=1.02)
    fig.text(0.5, 0.02, 'Note: Minimal differences indicate that reliability variations have negligible impact on the solution', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    plt.tight_layout()
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_difference_analysis.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f'Reliability difference analysis chart saved to {output_file}')

# 绘制统计摘要图
def plot_reliability_statistics():
    """Plot statistical summary comparing Problem 1 and Problem 2
    
    目的：显示统计信息，说明不可靠扰动对方案影响不大
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 转换为十亿美元
    costs_billion_p1 = [c / 1e9 for c in costs_p1]
    costs_billion_p2 = [c / 1e9 for c in costs_p2]
    
    # 计算差异
    cost_diff = [abs(costs_billion_p1[i] - costs_billion_p2[i]) for i in range(len(costs_billion_p1))]
    year_diff = [abs(years_p1[i] - years_p2[i]) for i in range(len(years_p1))]
    
    # 计算统计信息
    stats = {
        'Cost': {
            'Max Difference': max(cost_diff),
            'Min Difference': min(cost_diff),
            'Mean Difference': np.mean(cost_diff),
            'Std Difference': np.std(cost_diff),
            'Max Percentage': max(cost_diff) / np.mean(costs_billion_p1) * 100
        },
        'Time': {
            'Max Difference': max(year_diff),
            'Min Difference': min(year_diff),
            'Mean Difference': np.mean(year_diff),
            'Std Difference': np.std(year_diff),
            'Max Percentage': max(year_diff) / np.mean(years_p1) * 100
        }
    }
    
    # 创建统计摘要图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # 设置整体字体
    plt.rcParams.update({'font.size': 12})
    
    # 成本统计图
    categories = ['Max Diff', 'Min Diff', 'Mean Diff', 'Std Dev', 'Max %']
    cost_values = [stats['Cost']['Max Difference'], stats['Cost']['Min Difference'], 
                   stats['Cost']['Mean Difference'], stats['Cost']['Std Difference'], 
                   stats['Cost']['Max Percentage']]
    colors_cost = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    bars1 = ax1.bar(categories, cost_values, color=colors_cost, alpha=0.8, edgecolor='black')
    ax1.set_title('Cost Statistics: Problem 1 vs Problem 2', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Value', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bar, val in zip(bars1, cost_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(cost_values)*0.02,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 时间统计图
    time_values = [stats['Time']['Max Difference'], stats['Time']['Min Difference'], 
                  stats['Time']['Mean Difference'], stats['Time']['Std Difference'], 
                  stats['Time']['Max Percentage']]
    colors_time = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    bars2 = ax2.bar(categories, time_values, color=colors_time, alpha=0.8, edgecolor='black')
    ax2.set_title('Time Statistics: Problem 1 vs Problem 2', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Value', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bar, val in zip(bars2, time_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(time_values)*0.02,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 添加整体标题和说明
    fig.suptitle('Reliability Impact Analysis: Statistical Summary', 
                  fontsize=16, fontweight='bold', y=1.02)
    fig.text(0.5, 0.02, 'Note: Small statistical differences confirm minimal impact of reliability variations', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    plt.tight_layout()
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_statistics.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f'Reliability statistics chart saved to {output_file}')

# Main function
def main():
    """Run all plotting functions for both problems"""
    # 运行 Problem 1（100%可靠性）的绘图
    print("=== Problem 1: 100%可靠性 ===")
    plot_scenario_comparison(1)
    plot_ratio_analysis(1)
    plot_time_limit_analysis(1)
    
    # 运行 Problem 2（当前可靠性）的绘图
    print("\n=== Problem 2: 当前可靠性 ===")
    plot_scenario_comparison(2)
    plot_ratio_analysis(2)
    plot_time_limit_analysis(2)
    
    # 绘制可靠性对比图
    print("\n=== Reliability Comparison ===")
    plot_reliability_comparison()
    plot_reliability_difference_analysis()
    plot_reliability_statistics()

# 绘制不同时间限制下的最优方案分析图
def plot_time_limit_analysis(problem=2):
    """Plot optimal solutions under different time limits
    
    Args:
        problem (int, optional): 问题编号，1表示Problem 1，2表示Problem 2。默认为2
    """
    time_limits, actual_years, costs, elevator_ratios, rocket_ratios = read_time_limit_analysis(problem)
    
    # Convert cost to billions of dollars
    costs_billion = [c / 1e9 for c in costs]
    # Convert ratios to percentage
    elevator_ratios_percent = [r * 100 for r in elevator_ratios]
    rocket_ratios_percent = [r * 100 for r in rocket_ratios]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot cost variation with time limit
    ax1.plot(time_limits, costs_billion, marker='o', color='blue')
    ax1.set_title('Cost Variation with Time Limit')
    ax1.set_xlabel('Time Limit (Years)')
    ax1.set_ylabel('Total Cost (Billion USD)')
    ax1.grid(True)
    
    # Plot actual time vs time limit
    ax2.plot(time_limits, actual_years, marker='o', color='green')
    ax2.plot(time_limits, time_limits, linestyle='--', color='red', label='Time Limit')
    ax2.set_title('Actual Time vs Time Limit')
    ax2.set_xlabel('Time Limit (Years)')
    ax2.set_ylabel('Actual Time (Years)')
    ax2.legend()
    ax2.grid(True)
    
    # Plot ratio variation with time limit
    ax3.plot(time_limits, elevator_ratios_percent, marker='o', color='blue', label='Space Elevator')
    ax3.plot(time_limits, rocket_ratios_percent, marker='o', color='orange', label='Traditional Rockets')
    ax3.set_title('Ratio Variation with Time Limit')
    ax3.set_xlabel('Time Limit (Years)')
    ax3.set_ylabel('Ratio (%)')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    results_dir = get_results_dir(problem)
    output_file = os.path.join(results_dir, 'time_limit_analysis.png')
    plt.savefig(output_file)
    print(f'Time limit analysis chart saved to {output_file}')

if __name__ == "__main__":
    main()
