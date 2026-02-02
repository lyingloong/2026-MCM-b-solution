"""
Sensitivity Analysis

对公式进行敏感性分析：
    T = max{ SE_ratio * T_S * Amount_S , (1-SE_ratio) * T_R * Amount_R }
    C = SE_ratio * C_S * Amount_S + (1-SE_ratio) * C_R * Amount_R

可分析参数：
    SE_ratio (float): 太空电梯+摆渡火箭系统比例
    T_S (float): 单位运输量的太空电梯+摆渡火箭系统运输时间
    T_R (float): 单位运输量的传统火箭系统运输时间
    C_S (float): 单位运输量的太空电梯+摆渡火箭系统运输成本
    C_R (float): 单位运输量的传统火箭系统运输成本

这里敏感性分析针对 T_S T_R C_S C_R 这四个参数，即分别对这四个参数进行变化，按照 main_model.py 的方法分析运输时间和成本的变化情况。
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *


def calculate_combined_ratio_analysis(SE_ratio, T_S, T_R, C_S, C_R, time_limit):
    """
    计算不同时间限制下的最优SE_ratio（满足时间限制的最小cost）,以及对应的运输时间和成本。
    
    Args:
        SE_ratio (float): 太空电梯+摆渡火箭系统比例
        T_S (float): 单位运输量的太空电梯+摆渡火箭系统运输时间
        T_R (float): 单位运输量的传统火箭系统运输时间
        C_S (float): 单位运输量的太空电梯+摆渡火箭系统运输成本
        C_R (float): 单位运输量的传统火箭系统运输成本
        time_limit (float): 时间限制
    
    Returns:
        dict: 包含分析结果的字典
    """
    # 总材料需求（假设为常量，与问题1和2相同）
    total_material = TOTAL_MATERIAL
    
    # 计算各部分运输量
    amount_S = total_material * SE_ratio
    amount_R = total_material * (1 - SE_ratio)
    
    # 计算运输时间
    time_S = T_S * amount_S if SE_ratio > 0 else 0
    time_R = T_R * amount_R if (1 - SE_ratio) > 0 else 0
    total_time = max(time_S, time_R)
    
    # 计算成本
    cost_S = C_S * amount_S if SE_ratio > 0 else 0
    cost_R = C_R * amount_R if (1 - SE_ratio) > 0 else 0
    total_cost = cost_S + cost_R
    
    # 检查是否满足时间限制
    feasible = total_time <= time_limit
    
    return {
        "SE_ratio": SE_ratio,
        "total_time": total_time,
        "total_cost": total_cost,
        "feasible": feasible
    }


def sensitivity_analysis_parameter(param_name, param_range, problem=2):
    """
    对单个参数进行敏感性分析：
    调用 calculate_combined_ratio_analysis 函数，对参数 param_name 进行变化，分析运输时间和成本的变化情况。
    这个函数会得出在一系列 time_limit 下，不同 SE_ratio 和不同 param_name 取值下的最小成本以及对应的运输时间。
    
    参数说明：
    - T_S: 单位运输量的太空电梯+摆渡火箭系统运输时间
    - T_R: 单位运输量的传统火箭系统运输时间
    - C_S: 单位运输量的太空电梯+摆渡火箭系统运输成本
    - C_R: 单位运输量的传统火箭系统运输成本
    
    Args:
        param_name (str): 参数名称
        param_range (list): 参数取值范围
        problem (int): 问题编号
    
    Returns:
        dict: 包含分析结果的字典
    """
    # 根据问题编号选择参数默认值
    if problem == 1:
        # Problem 1: 100%可靠性
        default_C_S = COST_ELEVATOR_PER_P1
        default_C_R = COST_ROCKET_PER_P1
    else:
        # Problem 2: 当前可靠性
        default_C_S = COST_ELEVATOR_PER
        default_C_R = COST_ROCKET_PER
    
    # 默认运输时间参数（根据年运输能力计算）
    # 太空电梯年运输能力：每个银河港179,000吨，共3个银河港
    total_elevator_capacity = GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY
    # 单位运输量的太空电梯运输时间（假设线性关系）
    default_T_S = 1 / total_elevator_capacity
    
    # 火箭年运输能力：每个发射场每年1000次发射，每次平均125吨，共10个发射场
    total_rocket_capacity = ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG
    # 单位运输量的火箭运输时间（假设线性关系）
    default_T_R = 1 / total_rocket_capacity
    
    # 时间限制范围（与 main_model.py 中的默认值一致）
    time_limits = range(50, 260, 50)
    
    # SE_ratio 范围（从0%到100%，步长1%）
    se_ratios = [i/100 for i in range(0, 101, 1)]
    
    # 存储分析结果
    results = {
        "param_name": param_name,
        "param_range": param_range,
        "time_limits": time_limits,
        "se_ratios": se_ratios,
        "data": {}
    }
    
    # 遍历每个时间限制
    for time_limit in time_limits:
        results["data"][time_limit] = {}
        
        # 遍历每个参数取值
        for param_value in param_range:
            results["data"][time_limit][param_value] = {}
            
            # 遍历每个 SE_ratio
            for se_ratio in se_ratios:
                # 根据参数名称设置当前参数值
                if param_name == "T_S":
                    T_S = param_value
                    T_R = default_T_R
                    C_S = default_C_S
                    C_R = default_C_R
                elif param_name == "T_R":
                    T_S = default_T_S
                    T_R = param_value
                    C_S = default_C_S
                    C_R = default_C_R
                elif param_name == "C_S":
                    T_S = default_T_S
                    T_R = default_T_R
                    C_S = param_value
                    C_R = default_C_R
                elif param_name == "C_R":
                    T_S = default_T_S
                    T_R = default_T_R
                    C_S = default_C_S
                    C_R = param_value
                else:
                    # 未知参数，使用默认值
                    T_S = default_T_S
                    T_R = default_T_R
                    C_S = default_C_S
                    C_R = default_C_R
                
                # 计算分析结果
                analysis_result = calculate_combined_ratio_analysis(se_ratio, T_S, T_R, C_S, C_R, time_limit)
                
                # 存储结果
                results["data"][time_limit][param_value][se_ratio] = analysis_result
    
    return results


def run_sensitivity_analysis(problem=1):
    """
    Run complete sensitivity analysis
    
    Generate a plot for each time_limit, showing the minimum cost variation under different SE_ratio and different param_name values.
    The three axes are:
        x-axis: param_name value
        y-axis: SE_ratio value
        z-axis: cost
    Images are output to results/sensitivity_analysis/

    Args:
        problem (int): problem number
    """
    print(f"=== Running Sensitivity Analysis for Problem {problem} ===")
    
    # Create results directory
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'sensitivity_analysis')
    os.makedirs(results_dir, exist_ok=True)
    
    # Define parameters to analyze and their value ranges
    params_to_analyze = {
        "T_S": np.linspace(0.8, 1.2, 5) * (1 / (GALACTIC_HARBORS * ELEVATOR_ANNUAL_CAPACITY)),  # Space elevator transportation time parameter range
        "T_R": np.linspace(0.8, 1.2, 5) * (1 / (ROCKET_LAUNCH_SITES * ROCKET_LAUNCHES_PER_YEAR_PER_SITE * ROCKET_PAYLOAD_AVG)),  # Rocket transportation time parameter range
        "C_S": np.linspace(0.8, 1.2, 5) * (COST_ELEVATOR_PER_P1 if problem == 1 else COST_ELEVATOR_PER),  # Space elevator cost parameter range
        "C_R": np.linspace(0.8, 1.2, 5) * (COST_ROCKET_PER_P1 if problem == 1 else COST_ROCKET_PER),  # Rocket cost parameter range
    }
    
    # Run sensitivity analysis for each parameter
    for param_name, param_range in params_to_analyze.items():
        print(f"\n=== Analyzing parameter: {param_name} ===")
        
        # Run sensitivity analysis
        analysis_results = sensitivity_analysis_parameter(param_name, param_range, problem)
        
        # Generate a plot for each time limit
        for time_limit in analysis_results["time_limits"]:
            print(f"Generating plot for time_limit: {time_limit} years")
            
            # Prepare data
            param_values = analysis_results["param_range"]
            se_ratios = analysis_results["se_ratios"]
            
            # Create grid (swap x and y axes)
            Y, X = np.meshgrid(param_values, se_ratios)
            Z = np.zeros_like(X)
            
            # Fill data for cost and time
            Z_cost = np.zeros_like(X)
            Z_time = np.zeros_like(X)
            
            for i, param_value in enumerate(param_values):
                for j, se_ratio in enumerate(se_ratios):
                    result = analysis_results["data"][time_limit][param_value][se_ratio]
                    Z_cost[j, i] = result["total_cost"] if result["feasible"] else float('inf')
                    Z_time[j, i] = result["total_time"] if result["feasible"] else float('inf')
            
            # Create and save cost plot
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Add a filled base plane below the surface for better visual depth
            min_z = np.min(Z_cost[Z_cost != float('inf')]) if np.any(Z_cost != float('inf')) else 0
            base_plane = np.full_like(Z_cost, min_z)
            ax.plot_surface(X, Y, base_plane, color='lightgray', alpha=0.3, shade=True)

            # Plot surface
            surf = ax.plot_surface(X, Y, Z_cost, cmap='viridis', edgecolor='none')
            
            # Add color bar
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            
            # Set labels (swap x and y axes)
            ax.set_xlabel('SE_ratio')
            ax.set_ylabel(f'{param_name} Value')
            ax.set_zlabel('Minimum Cost')
            
            # # Invert SE_ratio axis
            # ax.set_xlim(ax.get_xlim()[::-1])
            
            # Adjust layout to fill the figure
            plt.tight_layout()
            
            # Save plot
            plot_filename = os.path.join(results_dir, f'problem_{problem}_time_limit_{time_limit}_{param_name}_cost.png')
            plt.savefig(plot_filename)
            plt.close()
            
            # Create and save time plot
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Add a filled base plane below the surface for better visual depth
            min_z = np.min(Z_time[Z_time != float('inf')]) if np.any(Z_time != float('inf')) else 0
            base_plane = np.full_like(Z_time, min_z)
            ax.plot_surface(X, Y, base_plane, color='lightgray', alpha=0.3, shade=True)

            # Plot surface
            surf = ax.plot_surface(X, Y, Z_time, cmap='plasma', edgecolor='none')
            
            # Add color bar
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            
            # Set labels (swap x and y axes)
            ax.set_xlabel('SE_ratio')
            ax.set_ylabel(f'{param_name} Value')
            ax.set_zlabel('Actual Time (years)')
            
            # Invert SE_ratio axis
            ax.set_xlim(ax.get_xlim()[::-1])
            
            # Adjust layout to fill the figure
            plt.tight_layout()
            
            # Save plot
            plot_filename = os.path.join(results_dir, f'problem_{problem}_time_limit_{time_limit}_{param_name}_time.png')
            plt.savefig(plot_filename)
            plt.close()
            
            # Save cost data to txt file
            data_filename = os.path.join(results_dir, f'problem_{problem}_time_limit_{time_limit}_{param_name}_cost.txt')
            with open(data_filename, 'w') as f:
                f.write(f'Problem: {problem}\n')
                f.write(f'Time Limit: {time_limit} years\n')
                f.write(f'Parameter: {param_name}\n')
                f.write('\n')
                f.write('Data Points:\n')
                f.write('\n')
                f.write('{:<20} {:<20} {:<20}\n'.format('SE_ratio', f'{param_name} Value', 'Minimum Cost'))
                f.write('{:<20} {:<20} {:<20}\n'.format('-' * 20, '-' * 20, '-' * 20))
                
                # Write data points
                for i, param_value in enumerate(param_values):
                    for j, se_ratio in enumerate(se_ratios):
                        cost = Z_cost[j, i]
                        if cost != float('inf'):
                            f.write('{:<20.6f} {:<20.6f} {:<20.2f}\n'.format(se_ratio, param_value, cost))
            
            # Save time data to txt file
            data_filename = os.path.join(results_dir, f'problem_{problem}_time_limit_{time_limit}_{param_name}_time.txt')
            with open(data_filename, 'w') as f:
                f.write(f'Problem: {problem}\n')
                f.write(f'Time Limit: {time_limit} years\n')
                f.write(f'Parameter: {param_name}\n')
                f.write('\n')
                f.write('Data Points:\n')
                f.write('\n')
                f.write('{:<20} {:<20} {:<20}\n'.format('SE_ratio', f'{param_name} Value', 'Actual Time (years)'))
                f.write('{:<20} {:<20} {:<20}\n'.format('-' * 20, '-' * 20, '-' * 20))
                
                # Write data points
                for i, param_value in enumerate(param_values):
                    for j, se_ratio in enumerate(se_ratios):
                        time = Z_time[j, i]
                        if time != float('inf'):
                            f.write('{:<20.6f} {:<20.6f} {:<20.2f}\n'.format(se_ratio, param_value, time))
    
    print(f"\n=== Sensitivity Analysis completed for Problem {problem} ===")
    print(f"Results saved to: {results_dir}")


def main():
    """
    Run sensitivity analysis (Problem 1)
    """
    print("=== Sensitivity Analysis ===")
    run_sensitivity_analysis(1)


if __name__ == "__main__":
    main()
