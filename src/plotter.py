"""
plotter for main_model
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D
import os

# 使用相对导入
from .constants import *

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

# 绘制3D可靠性影响分析图
def plot_reliability_3d_analysis():
    """Plot 3D analysis of reliability impact on cost and time
    
    目的：使用3D图表结合显示Problem 1和Problem 2的成本和时间差异
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent_p1 = [ratios_p1[i] * 100 for i in step_indices]
    ratio_percent_p2 = [ratios_p2[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置整体字体
    plt.rcParams.update({'font.size': 12})
    
    # 柱形尺寸
    bar_width = 3.0
    bar_depth = 3.0
    
    # 绘制Problem 1的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p1, years_p1_sampled, costs_billion_p1)):
        ax.bar3d(ratio, year, 0, bar_width, 2, cost, alpha=0.6, 
                 color='#1f77b4', edgecolor='black', linewidth=0.5)
    
    # 绘制Problem 2的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p2, years_p2_sampled, costs_billion_p2)):
        ax.bar3d(ratio + bar_width, year, 0, bar_width, 2, cost, alpha=0.6, 
                 color='#2ca02c', edgecolor='black', linewidth=0.5)
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time Required (Years)', fontsize=12, fontweight='bold')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=12, fontweight='bold')
    
    # 设置标题
    ax.set_title('3D Reliability Impact Analysis: Cost & Time vs Ratio (Bar Chart)', 
                fontsize=16, fontweight='bold')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor='#1f77b4', alpha=0.6, edgecolor='black', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor='#2ca02c', alpha=0.6, edgecolor='black', label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    # 添加说明文字
    fig.text(0.5, 0.02, 'Note: 3D bar chart with 10% step shows minimal differences between Problem 1 and Problem 2', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 调整视角以获得最佳观察角度
    ax.view_init(elev=25, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_analysis.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f'Reliability 3D analysis chart saved to {output_file}')


def plot_reliability_3d_style1():
    """Style 1: Modern color scheme 3D bar chart
    
    目的：使用现代配色方案和更好的视觉效果创建3D柱形图
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent_p1 = [ratios_p1[i] * 100 for i in step_indices]
    ratio_percent_p2 = [ratios_p2[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置现代风格
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 12, })
    
    # 柱形尺寸
    bar_width = 3.0
    bar_depth = 3.0
    
    # 现代配色方案
    colors_p1 = '#4361ee'  # 现代蓝色
    colors_p2 = '#3a0ca3'  # 现代紫色
    
    # 绘制Problem 1的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p1, years_p1_sampled, costs_billion_p1)):
        ax.bar3d(ratio, year, 0, bar_width, 2, cost, alpha=0.8, 
                 color=colors_p1, edgecolor='#2b2d42', linewidth=0.8, 
                 shade=True)
    
    # 绘制Problem 2的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p2, years_p2_sampled, costs_billion_p2)):
        ax.bar3d(ratio + bar_width + 1, year, 0, bar_width, 2, cost, alpha=0.8, 
                 color=colors_p2, edgecolor='#2b2d42', linewidth=0.8, 
                 shade=True)
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold', color='#2b2d42')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold', color='#2b2d42')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=14, fontweight='bold', color='#2b2d42')
    
    # 设置标题
    ax.set_title('Style 1: Modern 3D Reliability Impact Analysis', 
                fontsize=18, fontweight='bold', color='#2b2d42')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=colors_p1, alpha=0.8, edgecolor='#2b2d42', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor=colors_p2, alpha=0.8, edgecolor='#2b2d42', label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12, frameon=True, framealpha=0.9)
    
    # 添加说明文字
    fig.text(0.5, 0.02, 'Modern 3D visualization with enhanced color scheme and styling', 
             ha='center', fontsize=12, style='italic', color='#666666')
    
    # 调整视角以获得最佳观察角度
    ax.view_init(elev=30, azim=60)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_style1.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'Style 1 chart saved to {output_file}')


def plot_reliability_3d_style2():
    """Style 2: Different perspective and layout 3D bar chart
    
    目的：使用不同视角和布局创建3D柱形图
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent_p1 = [ratios_p1[i] * 100 for i in step_indices]
    ratio_percent_p2 = [ratios_p2[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建3D图表
    fig = plt.figure(figsize=(20, 14))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({'font.size': 12})
    
    # 柱形尺寸
    bar_width = 4.0
    bar_depth = 4.0
    
    # 明亮的配色方案
    colors_p1 = '#4cc9f0'  # 亮蓝色
    colors_p2 = '#4895ef'  # 深蓝色
    
    # 绘制Problem 1的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p1, years_p1_sampled, costs_billion_p1)):
        ax.bar3d(ratio, year, 0, bar_width, 3, cost, alpha=0.7, 
                 color=colors_p1, edgecolor='white', linewidth=1.0, 
                 shade=True)
    
    # 绘制Problem 2的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p2, years_p2_sampled, costs_billion_p2)):
        ax.bar3d(ratio + bar_width + 1, year, 0, bar_width, 3, cost, alpha=0.7, 
                 color=colors_p2, edgecolor='white', linewidth=1.0, 
                 shade=True)
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold', color='white')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=14, fontweight='bold', color='white')
    
    # 设置标题
    ax.set_title('Style 2: Alternative Perspective 3D Analysis', 
                fontsize=18, fontweight='bold', color='white')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=colors_p1, alpha=0.7, edgecolor='white', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor=colors_p2, alpha=0.7, edgecolor='white', label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12, frameon=True, framealpha=0.9)
    
    # 添加说明文字
    fig.text(0.5, 0.02, 'Alternative perspective with enhanced depth and spacing', 
             ha='center', fontsize=12, style='italic', color='white')
    
    # 调整视角以获得最佳观察角度
    ax.view_init(elev=45, azim=30)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_style2.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'Style 2 chart saved to {output_file}')


def plot_reliability_3d_style3():
    """Style 3: Different bar style and arrangement 3D chart
    
    目的：使用不同柱形样式和排列方式创建3D图表
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent_p1 = [ratios_p1[i] * 100 for i in step_indices]
    ratio_percent_p2 = [ratios_p2[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-bright')
    plt.rcParams.update({'font.size': 12})
    
    # 柱形尺寸
    bar_width = 3.5
    bar_depth = 3.5
    
    # 渐变配色方案
    colors_p1 = '#f72585'  # 粉红色
    colors_p2 = '#7209b7'  # 紫色
    
    # 绘制Problem 1的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p1, years_p1_sampled, costs_billion_p1)):
        ax.bar3d(ratio, year, 0, bar_width, 2.5, cost, alpha=0.9, 
                 color=colors_p1, edgecolor='#2b2d42', linewidth=0.5, 
                 shade=False)
    
    # 绘制Problem 2的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p2, years_p2_sampled, costs_billion_p2)):
        ax.bar3d(ratio, year + 3, 0, bar_width, 2.5, cost, alpha=0.9, 
                 color=colors_p2, edgecolor='#2b2d42', linewidth=0.5, 
                 shade=False)
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=14, fontweight='bold')
    
    # 设置标题
    ax.set_title('Style 3: Stacked Arrangement 3D Analysis', 
                fontsize=18, fontweight='bold')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=colors_p1, alpha=0.9, edgecolor='#2b2d42', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor=colors_p2, alpha=0.9, edgecolor='#2b2d42', label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
    
    # 添加说明文字
    fig.text(0.5, 0.02, 'Stacked arrangement with vibrant colors and simplified styling', 
             ha='center', fontsize=12, style='italic', color='#666666')
    
    # 调整视角以获得最佳观察角度
    ax.view_init(elev=35, azim=75)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_style3.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'Style 3 chart saved to {output_file}')


def plot_reliability_3d_style4():
    """Style 4: 3D chart with more interactive elements and annotations
    
    目的：添加更多交互元素和标注创建3D图表
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent_p1 = [ratios_p1[i] * 100 for i in step_indices]
    ratio_percent_p2 = [ratios_p2[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建3D图表
    fig = plt.figure(figsize=(20, 14))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-pastel')
    plt.rcParams.update({'font.size': 12})
    
    # 柱形尺寸
    bar_width = 3.0
    bar_depth = 3.0
    
    # 柔和的配色方案
    colors_p1 = '#90e0ef'  # 浅蓝色
    colors_p2 = '#00b4d8'  # 深蓝色
    
    # 绘制Problem 1的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p1, years_p1_sampled, costs_billion_p1)):
        ax.bar3d(ratio, year, 0, bar_width, 2, cost, alpha=0.8, 
                 color=colors_p1, edgecolor='#03045e', linewidth=0.8)
    
    # 绘制Problem 2的3D柱形图
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p2, years_p2_sampled, costs_billion_p2)):
        ax.bar3d(ratio + bar_width + 1, year, 0, bar_width, 2, cost, alpha=0.8, 
                 color=colors_p2, edgecolor='#03045e', linewidth=0.8)
    
    # 添加数据标注
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent_p1, years_p1_sampled, costs_billion_p1)):
        if i % 2 == 0:  # 每两个点标注一个
            ax.text(ratio + bar_width/2, year + 1, cost + 5, 
                    f'{cost:.1f}B', 
                    fontsize=10, ha='center', va='bottom', color='#03045e')
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold', color='#03045e')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold', color='#03045e')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=14, fontweight='bold', color='#03045e')
    
    # 设置标题
    ax.set_title('Style 4: Enhanced 3D Analysis with Annotations', 
                fontsize=18, fontweight='bold', color='#03045e')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor=colors_p1, alpha=0.8, edgecolor='#03045e', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor=colors_p2, alpha=0.8, edgecolor='#03045e', label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12, frameon=True, framealpha=0.9)
    
    # 添加说明文字
    fig.text(0.5, 0.02, 'Enhanced visualization with data annotations and detailed styling', 
             ha='center', fontsize=12, style='italic', color='#666666')
    
    # 调整视角以获得最佳观察角度
    ax.view_init(elev=20, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_style4.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'Style 4 chart saved to {output_file}')


def plot_reliability_3d_scatter_diff():
    """3D Scatter Plot showing differences between Problem 1 and Problem 2
    
    目的：使用3D散点图显示两个问题的差值分析
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 计算差值
    cost_diff = [costs_billion_p2[i] - costs_billion_p1[i] for i in range(len(costs_billion_p1))]
    year_diff = [years_p2_sampled[i] - years_p1_sampled[i] for i in range(len(years_p1_sampled))]
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 12})
    
    # 绘制3D散点图
    scatter = ax.scatter(ratio_percent, year_diff, cost_diff, 
                        c=cost_diff, cmap='RdYlBu_r', s=200, 
                        alpha=0.7, edgecolors='black', linewidth=1.5)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20)
    cbar.set_label('Cost Difference (Billion USD)', fontsize=12, fontweight='bold')
    
    # 添加参考平面（零平面）
    xx, yy = np.meshgrid(np.linspace(0, 100, 10), np.linspace(-5, 5, 10))
    zz = np.zeros_like(xx)
    ax.plot_surface(xx, yy, zz, alpha=0.2, color='gray')
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Time Difference (Years)', fontsize=14, fontweight='bold')
    ax.set_zlabel('Cost Difference (Billion USD)', fontsize=14, fontweight='bold')
    
    # 设置标题
    ax.set_title('3D Scatter Plot: Reliability Impact Analysis (Differences)', 
                fontsize=18, fontweight='bold')
    
    # 添加说明文字
    fig.text(0.5, 0.02, '3D scatter plot showing cost and time differences between Problem 1 and Problem 2', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 调整视角
    ax.view_init(elev=25, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_scatter_diff.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'3D scatter difference chart saved to {output_file}')


def plot_reliability_3d_surface():
    """3D Surface Plot showing cost variations
    
    目的：使用3D表面图显示成本变化趋势
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建网格数据
    X, Y = np.meshgrid(ratio_percent, years_p1_sampled)
    Z1 = np.array([costs_billion_p1] * len(years_p1_sampled))
    Z2 = np.array([costs_billion_p2] * len(years_p2_sampled))
    
    # 创建3D图表
    fig = plt.figure(figsize=(20, 14))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({'font.size': 12})
    
    # 改进的颜色映射
    cmap_p1 = 'viridis'  # 更现代的颜色映射
    cmap_p2 = 'plasma'    # 更现代的颜色映射
    
    # 绘制Problem 1的表面（改进版）
    surf1 = ax.plot_surface(X, Y, Z1, 
                          alpha=0.8,           # 提高透明度
                          cmap=cmap_p1,        # 改进的颜色映射
                          edgecolor='white',   # 添加边缘
                          linewidth=0.5,       # 边缘线宽
                          antialiased=True,    # 抗锯齿
                          shade=True)          # 添加阴影
    
    # 绘制Problem 2的表面（稍微偏移，改进版）
    Y_shifted = Y + 2  # 增加偏移量，提高可读性
    surf2 = ax.plot_surface(X, Y_shifted, Z2, 
                          alpha=0.8,           # 提高透明度
                          cmap=cmap_p2,        # 改进的颜色映射
                          edgecolor='white',   # 添加边缘
                          linewidth=0.5,       # 边缘线宽
                          antialiased=True,    # 抗锯齿
                          shade=True)          # 添加阴影
    
    # 优化颜色条位置和样式
    cbar1 = plt.colorbar(surf1, ax=ax, shrink=0.5, aspect=25, pad=0.015)
    cbar1.set_label('Problem 1 Cost (Billion USD)', fontsize=11, fontweight='bold', color='black')
    cbar1.ax.tick_params(color='black', labelcolor='black', labelsize=10)
    cbar1.outline.set_edgecolor('black')
    
    cbar2 = plt.colorbar(surf2, ax=ax, shrink=0.5, aspect=25, pad=0.015)
    cbar2.set_label('Problem 2 Cost (Billion USD)', fontsize=11, fontweight='bold', color='black')
    cbar2.ax.tick_params(color='black', labelcolor='black', labelsize=10)
    cbar2.outline.set_edgecolor('black')
    
    # 添加参考平面（零平面）
    xx, yy = np.meshgrid(np.linspace(0, 100, 20), np.linspace(0, max(years_p1_sampled) + 5, 20))
    zz = np.zeros_like(xx)
    ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray', edgecolor='none')
    
    # 优化数据点标注：更稀疏、更美观的排布
    annotation_count = 0
    max_annotations = 6  # 限制总标注数量
    annotation_step = max(1, len(ratio_percent) // max_annotations)
    key_ratios = [0, 50, 100]  # 0%, 50%, 100%比例点
    for ratio in key_ratios:
        if ratio in ratio_percent:
            idx = ratio_percent.index(ratio)
            cost = costs_billion_p1[idx]
            year = years_p1_sampled[idx]
            ax.text(ratio, year, cost + 12, 
                    f'{ratio}%: {cost:.1f}B', 
                    fontsize=9, 
                    ha='center', 
                    va='bottom', 
                    color='yellow', 
                    fontweight='bold',
                    bbox=dict(facecolor='black', 
                             alpha=0.9, 
                             edgecolor='yellow', 
                             boxstyle='round,pad=0.4'),
                    zorder=10)  # 设置高zorder确保在最上层
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', 
                 fontsize=16, fontweight='bold', color='black', 
                 labelpad=20)  # 增加标签间距
    ax.set_ylabel('Time Required (Years)', 
                 fontsize=16, fontweight='bold', color='black', 
                 labelpad=20)  # 增加标签间距
    ax.set_zlabel('Total Cost (Billion USD)', 
                 fontsize=16, fontweight='bold', color='black', 
                 labelpad=20)  # 增加标签间距
    
    # 设置坐标轴刻度
    ax.tick_params(axis='x', colors='black', labelsize=12)
    ax.tick_params(axis='y', colors='black', labelsize=12)
    ax.tick_params(axis='z', colors='black', labelsize=12)
    
    # 优化刻度显示
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], color='black')
    
    # 优化图例位置和样式
    legend_elements = [
        mpatches.Patch(facecolor='#1f77b4', alpha=0.8, edgecolor='black', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor='#ff7f0e', alpha=0.8, edgecolor='black', label='Problem 2 (Current Reliability)')
    ]
    
    # 将图例移到右下角，避免遮挡数据
    ax.legend(handles=legend_elements, 
              loc='upper left', 
              fontsize=12, 
              frameon=True, 
              framealpha=0.9, 
              facecolor='white', 
              edgecolor='black',
              labelcolor='black',
              borderpad=1,
              labelspacing=0.8)
    
    # 视角
    ax.view_init(elev=32, azim=66)
    
    # 设置图表背景为白色
    ax.set_facecolor('white')  # 白色背景
    fig.patch.set_facecolor('white')  # 白色画布背景
    
    # 添加网格线，提高可读性
    ax.xaxis._axinfo['grid'].update(color='gray', linestyle='--', alpha=0.3)
    ax.yaxis._axinfo['grid'].update(color='gray', linestyle='--', alpha=0.3)
    ax.zaxis._axinfo['grid'].update(color='gray', linestyle='--', alpha=0.3)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_surface.png')
    plt.savefig(output_file, dpi=250, bbox_inches='tight')
    print(f'Enhanced 3D surface chart saved to {output_file}')


def plot_reliability_3d_wireframe():
    """3D Wireframe Plot showing cost structure
    
    目的：使用3D线框图显示成本结构
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建网格数据
    X, Y = np.meshgrid(ratio_percent, years_p1_sampled)
    Z1 = np.array([costs_billion_p1] * len(years_p1_sampled))
    Z2 = np.array([costs_billion_p2] * len(years_p2_sampled))
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 12})
    
    # 绘制Problem 1的线框
    wire1 = ax.plot_wireframe(X, Y, Z1, color='blue', alpha=0.6, 
                             linewidth=1.5, rstride=1, cstride=1)
    
    # 绘制Problem 2的线框（稍微偏移）
    Y_shifted = Y + 1
    wire2 = ax.plot_wireframe(X, Y_shifted, Z2, color='red', alpha=0.6, 
                             linewidth=1.5, rstride=1, cstride=1)
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=14, fontweight='bold')
    
    # 设置标题
    ax.set_title('3D Wireframe Plot: Cost Structure Analysis', 
                fontsize=18, fontweight='bold')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor='blue', alpha=0.6, label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor='red', alpha=0.6, label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    # 添加说明文字
    fig.text(0.5, 0.02, '3D wireframe visualization showing underlying structure of cost variations', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 调整视角
    ax.view_init(elev=35, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_wireframe.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'3D wireframe chart saved to {output_file}')


def plot_reliability_3d_relative_bars():
    """3D Bar Chart showing relative differences
    
    目的：使用3D柱形图显示相对差异
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 计算相对差异（百分比）
    cost_rel_diff = [((costs_billion_p2[i] - costs_billion_p1[i]) / costs_billion_p1[i]) * 100 
                    for i in range(len(costs_billion_p1))]
    year_rel_diff = [((years_p2_sampled[i] - years_p1_sampled[i]) / years_p1_sampled[i]) * 100 
                    for i in range(len(years_p1_sampled))]
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-bright')
    plt.rcParams.update({'font.size': 12})
    
    # 柱形尺寸
    bar_width = 3.0
    bar_depth = 3.0
    
    # 绘制成本相对差异的柱形图
    for i, (ratio, diff) in enumerate(zip(ratio_percent, cost_rel_diff)):
        color = 'red' if diff > 0 else 'green'
        ax.bar3d(ratio, 0, 0, bar_width, 1, abs(diff), alpha=0.8, 
                 color=color, edgecolor='black', linewidth=0.8)
    
    # 绘制时间相对差异的柱形图（偏移）
    for i, (ratio, diff) in enumerate(zip(ratio_percent, year_rel_diff)):
        color = 'red' if diff > 0 else 'green'
        ax.bar3d(ratio, 2, 0, bar_width, 1, abs(diff), alpha=0.8, 
                 color=color, edgecolor='black', linewidth=0.8)
    
    # 添加零平面
    xx, yy = np.meshgrid(np.linspace(0, 100, 10), np.linspace(0, 3, 10))
    zz = np.zeros_like(xx)
    ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Metric Type', fontsize=14, fontweight='bold')
    ax.set_zlabel('Relative Difference (%)', fontsize=14, fontweight='bold')
    
    # 设置Y轴刻度
    ax.set_yticks([0.5, 2.5])
    ax.set_yticklabels(['Cost', 'Time'])
    
    # 设置标题
    ax.set_title('3D Bar Chart: Relative Differences (Problem 2 vs Problem 1)', 
                fontsize=18, fontweight='bold')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor='red', alpha=0.8, edgecolor='black', label='Increase'),
        mpatches.Patch(facecolor='green', alpha=0.8, edgecolor='black', label='Decrease')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    # 添加说明文字
    fig.text(0.5, 0.02, '3D bar chart showing relative percentage differences in cost and time', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 调整视角
    ax.view_init(elev=25, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_relative_bars.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'3D relative bars chart saved to {output_file}')


def plot_reliability_3d_contour():
    """3D Contour Plot showing cost variations
    
    目的：使用3D等高线图显示成本变化
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    
    # 创建网格数据
    X, Y = np.meshgrid(ratio_percent, years_p1_sampled)
    Z = np.array([costs_billion_p1] * len(years_p1_sampled))
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 12})
    
    # 绘制3D等高线图
    contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
    
    # 添加颜色条
    cbar = plt.colorbar(contour, ax=ax, shrink=0.5, aspect=20)
    cbar.set_label('Cost (Billion USD)', fontsize=12, fontweight='bold')
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold')
    ax.set_zlabel('Total Cost (Billion USD)', fontsize=14, fontweight='bold')
    
    # 设置标题
    ax.set_title('3D Contour Plot: Cost Variations (Problem 1)', 
                fontsize=18, fontweight='bold')
    
    # 添加说明文字
    fig.text(0.5, 0.02, '3D contour visualization showing cost variations across different ratios and time periods', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 调整视角
    ax.view_init(elev=45, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_contour.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'3D contour chart saved to {output_file}')


def plot_reliability_3d_waterfall():
    """3D Waterfall Plot showing cost breakdown
    
    目的：使用3D瀑布图显示成本分解
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    years_p2_sampled = [years_p2[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    costs_billion_p2 = [costs_p2[i] / 1e9 for i in step_indices]
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 12})
    
    # 柱形尺寸
    bar_width = 3.0
    bar_depth = 3.0
    
    # 绘制瀑布图
    current_height = 0
    for i, (ratio, cost1, cost2) in enumerate(zip(ratio_percent, costs_billion_p1, costs_billion_p2)):
        # Problem 1的柱形
        ax.bar3d(ratio, 0, 0, bar_width, 1, cost1, alpha=0.8, 
                 color='#4361ee', edgecolor='black', linewidth=0.8)
        
        # Problem 2的柱形（堆叠）
        ax.bar3d(ratio, 1, 0, bar_width, 1, cost2, alpha=0.8, 
                 color='#3a0ca3', edgecolor='black', linewidth=0.8)
        
        # 连接线
        ax.plot([ratio, ratio], [0, 1], [cost1, cost2], 
                color='gray', linestyle='--', linewidth=1.5, alpha=0.6)
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Problem Type', fontsize=14, fontweight='bold')
    ax.set_zlabel('Cost (Billion USD)', fontsize=14, fontweight='bold')
    
    # 设置Y轴刻度
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(['Problem 1', 'Problem 2'])
    
    # 设置标题
    ax.set_title('3D Waterfall Plot: Cost Comparison Between Problems', 
                fontsize=18, fontweight='bold')
    
    # 添加图例
    legend_elements = [
        mpatches.Patch(facecolor='#4361ee', alpha=0.8, edgecolor='black', label='Problem 1 (100% Reliability)'),
        mpatches.Patch(facecolor='#3a0ca3', alpha=0.8, edgecolor='black', label='Problem 2 (Current Reliability)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    # 添加说明文字
    fig.text(0.5, 0.02, '3D waterfall visualization showing cost progression from Problem 1 to Problem 2', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 调整视角
    ax.view_init(elev=25, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_waterfall.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'3D waterfall chart saved to {output_file}')


def plot_reliability_3d_heatmap():
    """3D Heatmap showing cost intensity
    
    目的：使用3D热力图显示成本强度
    """
    # 读取两份数据
    ratios_p1, years_p1, costs_p1 = read_ratio_analysis(1)
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    
    # 提高步长：从1%提高到10%
    step_indices = list(range(0, len(ratios_p1), 10))
    
    # 转换为百分比和十亿美元
    ratio_percent = [ratios_p1[i] * 100 for i in step_indices]
    years_p1_sampled = [years_p1[i] for i in step_indices]
    costs_billion_p1 = [costs_p1[i] / 1e9 for i in step_indices]
    
    # 创建网格数据
    X, Y = np.meshgrid(ratio_percent, years_p1_sampled)
    Z = np.array([costs_billion_p1] * len(years_p1_sampled))
    
    # 创建3D图表
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置风格
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({'font.size': 12})
    
    # 绘制3D热力图（使用柱形图模拟）
    bar_width = 3.0
    bar_depth = 3.0
    
    # 归一化成本值用于颜色映射
    norm = plt.Normalize(vmin=min(costs_billion_p1), vmax=max(costs_billion_p1))
    cmap = plt.cm.RdYlBu_r
    
    for i, (ratio, year, cost) in enumerate(zip(ratio_percent, years_p1_sampled, costs_billion_p1)):
        color = cmap(norm(cost))
        ax.bar3d(ratio, year, 0, bar_width, 1, cost, alpha=0.9, 
                 color=color, edgecolor='black', linewidth=0.5)
    
    # 添加颜色条
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.5, aspect=20)
    cbar.set_label('Cost (Billion USD)', fontsize=12, fontweight='bold')
    
    # 设置坐标轴标签
    ax.set_xlabel('Space Elevator Ratio (%)', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Time Required (Years)', fontsize=14, fontweight='bold', color='white')
    ax.set_zlabel('Cost (Billion USD)', fontsize=14, fontweight='bold', color='white')
    
    # 设置标题
    ax.set_title('3D Heatmap: Cost Intensity Analysis (Problem 1)', 
                fontsize=18, fontweight='bold', color='white')
    
    # 添加说明文字
    fig.text(0.5, 0.02, '3D heatmap visualization showing cost intensity across different ratios and time periods', 
             ha='center', fontsize=11, style='italic', color='white')
    
    # 调整视角
    ax.view_init(elev=45, azim=45)
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'reliability_3d_heatmap.png')
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'3D heatmap chart saved to {output_file}')

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
    
    # 运行 Problem 3（额外材料需求）的绘图
    print("\n=== Problem 3: 额外材料需求 ===")
    plot_scenario_comparison_p3()
    plot_ratio_analysis_p3()
    plot_time_limit_analysis_p3()
    
    # 绘制Problem 2 vs Problem 3对比图
    print("\n=== Problem 2 vs Problem 3 Comparison ===")
    plot_problem_2_vs_3_comparison()
    plot_ratio_comparison_p2_p3()
    
    # 绘制可靠性对比图
    print("\n=== Reliability Comparison ===")
    plot_reliability_comparison()
    plot_reliability_difference_analysis()
    plot_reliability_statistics()
    plot_reliability_3d_analysis()
    
    # 绘制不同风格的3D图表
    print("\n=== Different 3D Styles ===")
    plot_reliability_3d_style1()
    plot_reliability_3d_style2()
    plot_reliability_3d_style3()
    plot_reliability_3d_style4()
    
    # 绘制更多样化的3D图表
    print("\n=== More 3D Visualizations ===")
    plot_reliability_3d_scatter_diff()
    plot_reliability_3d_surface()
    plot_reliability_3d_wireframe()
    plot_reliability_3d_relative_bars()
    plot_reliability_3d_contour()
    plot_reliability_3d_waterfall()
    plot_reliability_3d_heatmap()

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

# 绘制Problem 3的场景对比图
def plot_scenario_comparison_p3():
    """Plot cost and time comparison for all scenarios in Problem 3
    
    Problem 3: 额外材料需求（121,765吨）
    """
    scenarios = read_scenario_analysis(3)
    
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
    ax1.set_title('Total Cost Comparison (Problem 3)', fontsize=14, fontweight='bold')
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
    ax2.set_title('Time Required Comparison (Problem 3)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Time Required (Years)' if not MONTH_MODE else 'Time Required (Months)', fontsize=12)
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
    fig.suptitle(f'Scenario Comparison Analysis (Problem 3: Extra Material {EXTRA_MATERIAL_P3} tons)', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    results_dir = get_results_dir(3)
    output_file = os.path.join(results_dir, 'scenario_comparison.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=150)
    print(f'Scenario comparison chart (Problem 3) saved to {output_file}')

# 绘制Problem 3的比例分析图
def plot_ratio_analysis_p3():
    """Plot cost and time variation with different ratios in combined scenario for Problem 3
    
    Problem 3: 额外材料需求（121,765吨）
    """
    ratios, years, costs = read_ratio_analysis(3)
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
    ax2.set_ylabel('Time Required (Years)' if not MONTH_MODE else 'Time Required (Months)', color=color_time, fontsize=12)
    ax2.plot(ratio_percent, years, 's-', color=color_time, label='Time Required', linewidth=2, markersize=6)
    ax2.tick_params(axis='y', labelcolor=color_time, labelsize=11)
    # 标题和图例
    fig1.suptitle(f'Cost & Time vs Space Elevator Ratio (Line Chart) - Problem 3 (Extra Material: {EXTRA_MATERIAL_P3} tons)', 
                  fontsize=14, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=11)
    # 保存折线图
    results_dir = get_results_dir(3)
    line_file = os.path.join(results_dir, 'ratio_analysis_line.png')
    plt.tight_layout()
    plt.savefig(line_file, bbox_inches='tight', dpi=150)
    print(f'Ratio analysis line chart (Problem 3) saved to {line_file}')
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
    bars2 = ax_twin.bar(x2, target_years, width=bar_width, label='Time Required (Years)' if not MONTH_MODE else 'Time Required (Months)',
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
    ax_twin.set_ylabel('Time Required (Years)' if not MONTH_MODE else 'Time Required (Months)', fontsize=12, fontweight='bold', color=color_time_bar)
    ax_twin.tick_params(axis='y', labelcolor=color_time_bar, labelsize=11)
    # 标题
    fig2.suptitle(f'Cost & Time vs Space Elevator Ratio (Bar Chart, 10% Step) - Problem 3 (Extra Material: {EXTRA_MATERIAL_P3} tons)',
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
    print(f'Ratio analysis bar chart (10% step, Problem 3) saved to {bar_file}')
    plt.close(fig2)

# 绘制Problem 3与Problem 2的对比图
def plot_problem_2_vs_3_comparison():
    """Plot comparison between Problem 2 and Problem 3
    
    目的：显示额外材料需求对方案的影响
    """
    # 读取两份数据
    scenarios_p2 = read_scenario_analysis(2)
    scenarios_p3 = read_scenario_analysis(3)
    
    # 提取数据
    names_p2 = [s['name'] for s in scenarios_p2]
    costs_p2 = [s['cost'] / 1e9 for s in scenarios_p2]
    years_p2 = [s['years'] for s in scenarios_p2]
    
    names_p3 = [s['name'] for s in scenarios_p3]
    costs_p3 = [s['cost'] / 1e9 for s in scenarios_p3]
    years_p3 = [s['years'] for s in scenarios_p3]
    
    # 计算差异
    cost_diff = [costs_p3[i] - costs_p2[i] for i in range(len(costs_p2))]
    year_diff = [years_p3[i] - years_p2[i] for i in range(len(years_p2))]
    cost_pct_diff = [(costs_p3[i] - costs_p2[i]) / costs_p2[i] * 100 for i in range(len(costs_p2))]
    
    # 创建对比图表
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))
    
    # 设置整体字体
    plt.rcParams.update({'font.size': 12})
    
    # 1. 成本对比图
    x = np.arange(len(names_p2))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, costs_p2, width, label='Problem 2 (100M tons)', 
                    color='#1f77b4', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x + width/2, costs_p3, width, label=f'Problem 3 ({TOTAL_MATERIAL_P3/1e6:.3f}M tons)', 
                    color='#2ca02c', alpha=0.8, edgecolor='black')
    
    ax1.set_title('Cost Comparison: Problem 2 vs Problem 3', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Total Cost (Billion USD)', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(names_p2, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    
    # 2. 时间对比图
    bars3 = ax2.bar(x - width/2, years_p2, width, label='Problem 2 (100M tons)', 
                    color='#1f77b4', alpha=0.8, edgecolor='black')
    bars4 = ax2.bar(x + width/2, years_p3, width, label=f'Problem 3 ({TOTAL_MATERIAL_P3/1e6:.3f}M tons)', 
                    color='#2ca02c', alpha=0.8, edgecolor='black')
    
    ax2.set_title('Time Comparison: Problem 2 vs Problem 3', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Time Required (Years)', fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names_p2, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    # 3. 成本差异图
    bars5 = ax3.bar(x, cost_diff, color='#ff7f0e', alpha=0.8, edgecolor='black')
    ax3.set_title('Cost Difference (Problem 3 - Problem 2)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Cost Difference (Billion USD)', fontsize=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(names_p2, rotation=45, ha='right')
    ax3.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax3.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bar, val in zip(bars5, cost_diff):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01 if height > 0 else height - 0.01,
                f'{val:.3f}', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)
    
    # 4. 成本相对差异图
    bars6 = ax4.bar(x, cost_pct_diff, color='#d62728', alpha=0.8, edgecolor='black')
    ax4.set_title('Cost Percentage Difference (Problem 3 - Problem 2)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Percentage Difference (%)', fontsize=12)
    ax4.set_xticks(x)
    ax4.set_xticklabels(names_p2, rotation=45, ha='right')
    ax4.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax4.grid(axis='y', alpha=0.3)
    
    # 添加数据标签
    for bar, val in zip(bars6, cost_pct_diff):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.001 if height > 0 else height - 0.001,
                f'{val:.3f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)
    
    # 调整布局
    plt.tight_layout()
    
    # 添加整体标题和说明
    fig.suptitle('Problem 2 vs Problem 3: Impact of Extra Material Demand', 
                 fontsize=16, fontweight='bold', y=1.02)
    fig.text(0.5, 0.02, f'Problem 2: {TOTAL_MATERIAL/1e6}M tons | Problem 3: {TOTAL_MATERIAL_P3/1e6:.3f}M tons (Extra: {EXTRA_MATERIAL_P3} tons)', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'problem_2_vs_3_comparison.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f'Problem 2 vs Problem 3 comparison chart saved to {output_file}')

# 绘制Problem 3与Problem 2的比例分析对比图
def plot_ratio_comparison_p2_p3():
    """Plot ratio analysis comparison between Problem 2 and Problem 3
    
    目的：显示额外材料需求对比例分析的影响
    """
    # 读取两份数据
    ratios_p2, years_p2, costs_p2 = read_ratio_analysis(2)
    ratios_p3, years_p3, costs_p3 = read_ratio_analysis(3)
    
    # 转换为百分比和十亿美元
    ratio_percent_p2 = [r * 100 for r in ratios_p2]
    ratio_percent_p3 = [r * 100 for r in ratios_p3]
    costs_billion_p2 = [c / 1e9 for c in costs_p2]
    costs_billion_p3 = [c / 1e9 for c in costs_p3]
    
    # 计算差异
    cost_diff = [costs_billion_p3[i] - costs_billion_p2[i] for i in range(len(costs_billion_p2))]
    cost_pct_diff = [(costs_billion_p3[i] - costs_billion_p2[i]) / costs_billion_p2[i] * 100 for i in range(len(costs_billion_p2))]
    
    # 创建对比图表 - 改进版
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
    
    # 设置整体字体
    plt.rcParams.update({'font.size': 12})
    
    # 1. 成本对比图（改进版）
    ax1.plot(ratio_percent_p2, costs_billion_p2, 'o-', color='#1f77b4', alpha=0.8, 
             label=f'Problem 2 ({TOTAL_MATERIAL/1e6}M tons)', linewidth=3, markersize=8)
    ax1.plot(ratio_percent_p3, costs_billion_p3, 's-', color='#2ca02c', alpha=0.8, 
             label=f'Problem 3 ({TOTAL_MATERIAL_P3/1e6:.3f}M tons)', linewidth=3, markersize=8)
    # 添加填充区域，突出差异
    ax1.fill_between(ratio_percent_p2, costs_billion_p2, costs_billion_p3, 
                     where=[costs_billion_p3[i] > costs_billion_p2[i] for i in range(len(costs_billion_p2))],
                     color='#2ca02c', alpha=0.2, label='Cost Increase')
    ax1.set_title('Cost Comparison: Problem 2 vs Problem 3', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax1.set_ylabel('Total Cost (Billion USD)', fontsize=12)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # 2. 时间对比图
    ax2.plot(ratio_percent_p2, years_p2, 'o-', color='#1f77b4', alpha=0.8, 
             label=f'Problem 2 ({TOTAL_MATERIAL/1e6}M tons)', linewidth=3, markersize=8)
    ax2.plot(ratio_percent_p3, years_p3, 's-', color='#2ca02c', alpha=0.8, 
             label=f'Problem 3 ({TOTAL_MATERIAL_P3/1e6:.3f}M tons)', linewidth=3, markersize=8)
    ax2.set_title('Time Comparison: Problem 2 vs Problem 3', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax2.set_ylabel('Time Required (Years)', fontsize=12)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # 3. 成本差异图（新增）
    ax3.plot(ratio_percent_p2, cost_diff, '^-', color='#ff7f0e', alpha=0.8, 
             label='Cost Difference (Problem 3 - Problem 2)', linewidth=3, markersize=8)
    ax3.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.6)
    ax3.set_title('Cost Difference: Problem 3 - Problem 2', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax3.set_ylabel('Cost Difference (Billion USD)', fontsize=12)
    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.3)
    
    # 4. 成本相对差异图（新增）
    ax4.plot(ratio_percent_p2, cost_pct_diff, 'v-', color='#d62728', alpha=0.8, 
             label='Cost Percentage Difference', linewidth=3, markersize=8)
    ax4.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.6)
    ax4.set_title('Cost Percentage Difference: Problem 3 vs Problem 2', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax4.set_ylabel('Percentage Difference (%)', fontsize=12)
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)
    
    # 调整布局
    plt.tight_layout()
    
    # 添加整体标题和说明
    fig.suptitle('Enhanced Ratio Analysis: Problem 2 vs Problem 3', 
                 fontsize=16, fontweight='bold', y=1.02)
    fig.text(0.5, 0.02, f'Problem 2: {TOTAL_MATERIAL/1e6}M tons | Problem 3: {TOTAL_MATERIAL_P3/1e6:.3f}M tons (Extra: {EXTRA_MATERIAL_P3} tons)', 
             ha='center', fontsize=11, style='italic', color='#666666')
    
    # 保存图表
    results_dir = get_results_dir()
    output_file = os.path.join(results_dir, 'ratio_comparison_p2_p3.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f'Enhanced ratio comparison (Problem 2 vs Problem 3) chart saved to {output_file}')

    # 额外生成一个专注于差异的图表
    fig2, (ax_diff, ax_pct) = plt.subplots(2, 1, figsize=(16, 10))
    
    # 1. 成本差异详细图
    ax_diff.plot(ratio_percent_p2, cost_diff, 'o-', color='#ff7f0e', 
                 linewidth=3, markersize=8)
    ax_diff.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    ax_diff.set_title('Detailed Cost Difference: Problem 3 - Problem 2', fontsize=14, fontweight='bold')
    ax_diff.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax_diff.set_ylabel('Cost Difference (Billion USD)', fontsize=12)
    ax_diff.grid(True, alpha=0.3)
    
    # 添加数据标签
    key_ratios = [0, 25, 50, 75, 100]
    for ratio in key_ratios:
        if ratio in ratio_percent_p2:
            idx = ratio_percent_p2.index(ratio)
            diff = cost_diff[idx]
            ax_diff.text(ratio, diff + 0.001 if diff > 0 else diff - 0.001,
                        f'{diff:.3f}', ha='center', va='bottom' if diff > 0 else 'top',
                        fontsize=10, fontweight='bold', color='#ff7f0e')
    
    # 2. 成本相对差异详细图
    ax_pct.plot(ratio_percent_p2, cost_pct_diff, 's-', color='#d62728', 
                linewidth=3, markersize=8)
    ax_pct.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    ax_pct.set_title('Detailed Cost Percentage Difference: Problem 3 vs Problem 2', fontsize=14, fontweight='bold')
    ax_pct.set_xlabel('Space Elevator Ratio (%)', fontsize=12)
    ax_pct.set_ylabel('Percentage Difference (%)', fontsize=12)
    ax_pct.grid(True, alpha=0.3)
    
    # 添加数据标签
    for ratio in key_ratios:
        if ratio in ratio_percent_p2:
            idx = ratio_percent_p2.index(ratio)
            pct_diff = cost_pct_diff[idx]
            ax_pct.text(ratio, pct_diff + 0.001 if pct_diff > 0 else pct_diff - 0.001,
                       f'{pct_diff:.3f}%', ha='center', va='bottom' if pct_diff > 0 else 'top',
                       fontsize=10, fontweight='bold', color='#d62728')
    
    plt.tight_layout()
    fig2.suptitle('Focused Difference Analysis: Problem 2 vs Problem 3', 
                  fontsize=16, fontweight='bold', y=1.02)
    fig2.text(0.5, 0.02, f'Problem 2: {TOTAL_MATERIAL/1e6}M tons | Problem 3: {TOTAL_MATERIAL_P3/1e6:.3f}M tons (Extra: {EXTRA_MATERIAL_P3} tons)', 
              ha='center', fontsize=11, style='italic', color='#666666')
    
    # 保存专注差异的图表
    output_file2 = os.path.join(results_dir, 'ratio_comparison_p2_p3_difference_focus.png')
    plt.savefig(output_file2, dpi=150, bbox_inches='tight')
    print(f'Focused difference analysis chart saved to {output_file2}')

# 绘制Problem 3的时间限制分析图
def plot_time_limit_analysis_p3():
    """Plot optimal solutions under different time limits for Problem 3
    
    Problem 3: 额外材料需求（121,765吨）
    """
    time_limits, actual_years, costs, elevator_ratios, rocket_ratios = read_time_limit_analysis(3)
    
    # Convert cost to billions of dollars
    costs_billion = [c / 1e9 for c in costs]
    # Convert ratios to percentage
    elevator_ratios_percent = [r * 100 for r in elevator_ratios]
    rocket_ratios_percent = [r * 100 for r in rocket_ratios]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot cost variation with time limit
    ax1.plot(time_limits, costs_billion, marker='o', color='blue')
    ax1.set_title('Cost Variation with Time Limit (Problem 3)')
    ax1.set_xlabel('Time Limit (Years)' if not MONTH_MODE else 'Time Limit (Months)')
    ax1.set_ylabel('Total Cost (Billion USD)')
    ax1.grid(True)
    
    # Plot actual time vs time limit
    ax2.plot(time_limits, actual_years, marker='o', color='green')
    ax2.plot(time_limits, time_limits, linestyle='--', color='red', label='Time Limit')
    ax2.set_title('Actual Time vs Time Limit (Problem 3)')
    ax2.set_xlabel('Time Limit (Years)' if not MONTH_MODE else 'Time Limit (Months)')
    ax2.set_ylabel('Actual Time (Years)')
    ax2.legend()
    ax2.grid(True)
    
    # Plot ratio variation with time limit
    ax3.plot(time_limits, elevator_ratios_percent, marker='o', color='blue', label='Space Elevator')
    ax3.plot(time_limits, rocket_ratios_percent, marker='o', color='orange', label='Traditional Rockets')
    ax3.set_title('Ratio Variation with Time Limit (Problem 3)')
    ax3.set_xlabel('Time Limit (Years)' if not MONTH_MODE else 'Time Limit (Months)')
    ax3.set_ylabel('Ratio (%)')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    results_dir = get_results_dir(3)
    output_file = os.path.join(results_dir, 'time_limit_analysis.png')
    plt.savefig(output_file)
    print(f'Time limit analysis chart (Problem 3) saved to {output_file}')

if __name__ == "__main__":
    main()
