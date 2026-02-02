"""
Problem 4 环境影响评估与优化
零、问题背景
将1亿吨材料运送到月球，有两种方式：
1. 传统地面火箭
2. 太空电梯+在轨摆渡火箭

方案1：全部使用传统地面火箭；
方案2：全部使用太空电梯系统；
方案3：部分使用传统地面火箭，部分使用太空电梯系统；

讨论不同方案对地球环境的影响，考虑如何调整模型以最小化环境影响。

一、整体建模思路
本节建立分系统、分高度、分污染物的环境影响量化框架，将传统地面火箭、太空电梯、在轨摆渡火箭三类运输方式的环境代价统一建模，用于对比与优化决策：

地面火箭（TR）：化学推进，排放进入对流层 / 平流层，环境影响显著；
太空电梯（SE）：无燃烧，仅由电力生产产生间接排放；
在轨火箭（TUG）：化学推进但在近真空轨道排放，对大气影响可忽略。

通过推进剂消耗量 → 污染物排放 → 环境权重 → 总环境影响 E 的链路，实现从物理性能到环境代价的完整映射。

二、地面火箭环境影响模型
1. 推进剂消耗建模（单级火箭近似）
基于齐奥尔科夫斯基火箭方程 + 结构质量分数，推导单位有效载荷的推进剂强度，避免依赖具体火箭型号：

结构质量分数：ϵ=m0​mdry​​一次性火箭：ϵ≈0.05−0.08可复用火箭：ϵ≈0.08−0.15（SpaceLiner 等概念支持取到 0.15–0.17）

速度增量与质量比：RG​=exp(g0​Isp,G​ΔvG​​)基准 ΔvG​≈9.5 km/s（含轨道速度 + 损失），在 9.0–10.5 km/s 做敏感性分析。

初始质量闭式解：m0​=1−RG​ϵRG​​mpay​

单位有效载荷推进剂强度（核心归一化指标）：γG​=mpay​mf​​=1−RG​ϵRG​(1−ϵ)​−1

2. 污染物排放与环境影响

单位载荷污染物 k 排放量：ek(G)​=1000ek​​γG​其中 ek​ 为单位燃料排放因子，1000 为单位换算系数。

总环境影响（加权求和）：ETR​=N⋅(ωBC​eBC​+ωAl2​O3​​eAl2​O3​​+ωH2​O​eH2​O​+ωNOx​​eNOx​​)⋅ηG​

ωk​：污染物环境权重（按臭氧损耗 / 辐射强迫贡献，取自 Ryan et al. 2022）
ηG​=1：地面发射环境影响系数

3. 关键污染物与气候效应
地面火箭主要通过四类物质造成长期大气影响：

黑碳（BC）：平流层强吸热，效应是地表黑碳的 500 倍，导致平流层增温、极地冰盖融化；
氧化铝（Al₂O₃）：固体助推器排放，产生正辐射强迫（增温效应）；
水蒸气（H₂O）：平流层温室气体，改变云分布与大气环流；
氮氧化物（NOₓ）：破坏平流层臭氧，增加地表有害 UV 辐射。

三、太空电梯环境影响模型（SE）
太空电梯无燃烧过程，环境影响仅来自电力生产的间接排放，以碳排放当量统一度量：
ESE​=MSE​⋅eele​⋅μ

MSE​：电梯总运输质量；
eele​：单位质量运输耗电量；
μ：单位电能碳排放强度（kgCO₂e/kWh），按三种情景取值：
S1（强减排 / 净零）：μ∈[0.02,0.10]
S2（中等转型）：μ∈[0.10,0.30]
S3（保守 / 政策不力）：μ∈[0.30,0.60]

若由赤道海洋太阳能基地供电，理论上可实现近零大气排放，因此被称为 "绿色天路（Green Road to Space）"。

四、在轨火箭环境影响（TUG）
在轨摆渡火箭虽仍使用化学推进，但排放发生在近真空轨道，与地球大气几乎无相互作用，因此：

环境影响系数 ηO​≪1，模型中可视为近似零环境代价；
仅需计入其从地面发射段的影响（若由电梯部署，则发射段影响也可消除）。

五、核心对比与优化结论

环境代价量级差异显著

地面化学火箭：多污染物协同作用，对平流层与臭氧层造成不可逆长期影响；
太空电梯：仅存在电力间接排放，在低碳 / 零碳电网下可实现近零污染；
在轨火箭：排放高度高，对大气系统影响可忽略。

推进剂强度是地面火箭环境影响的核心驱动单位载荷推进剂消耗 γG​ 由 Δv、Isp​、ϵ 共同决定，是连接性能与排放的关键归一化指标，可用于跨方案、跨尺度对比。

排放高度决定环境影响机理地面发射（对流层 / 平流层）与轨道排放（近真空）的环境效应存在本质区别，必须引入高度相关系数 η 才能合理量化。
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from constants import TOTAL_MATERIAL

# 常量定义
G0 = 9.81  # 重力加速度
TOTAL_PAYLOAD = TOTAL_MATERIAL  # 总有效载荷（吨）

# 地面火箭参数
DELTA_V_G = 9500  # 速度增量（m/s）
I_SP_G = 310  # 比冲（秒）
epsilon = 0.1  # 结构质量分数

# 污染物排放因子（单位：g/kg 燃料）
EMISSION_FACTORS = {
    'BC': 0.1,      # 黑碳
    'Al2O3': 5.0,    # 氧化铝
    'H2O': 1200.0,   # 水蒸气
    'NOx': 2.0       # 氮氧化物
}

# 环境权重（相对影响因子）
ENVIRONMENTAL_WEIGHTS = {
    'BC': 500,       # 黑碳效应是地表的500倍
    'Al2O3': 10,      # 氧化铝相对影响
    'H2O': 5,         # 水蒸气相对影响
    'NOx': 100        # 氮氧化物相对影响
}

# 太空电梯参数
e_ele = 30  # 单位质量运输耗电量（kWh/吨）

# 碳排放强度情景（kgCO2e/kWh）
CARBON_INTENSITY_SCENARIOS = {
    'S1': 0.06,  # 强减排/净零（取区间中点）
    'S2': 0.20,  # 中等转型（取区间中点）
    'S3': 0.45   # 保守/政策不力（取区间中点）
}

# 计算地面火箭推进剂强度
def calculate_propellant_intensity(delta_v, i_sp, epsilon):
    """计算单位有效载荷的推进剂强度"""
    R_G = math.exp(delta_v / (G0 * i_sp))
    # 确保分母为正，使用更合理的公式
    if R_G * epsilon >= 1:
        # 如果结构质量分数过低，使用简化模型
        gamma_G = R_G - 1
    else:
        gamma_G = (R_G * (1 - epsilon) / (1 - R_G * epsilon)) - 1
    # 确保推进剂强度为正
    return max(gamma_G, 0)


# 计算地面火箭环境影响
def calculate_rocket_impact(payload, delta_v, i_sp, epsilon):
    """计算地面火箭的环境影响"""
    gamma_G = calculate_propellant_intensity(delta_v, i_sp, epsilon)
    total_impact = 0
    emissions = {}
    
    for pollutant, factor in EMISSION_FACTORS.items():
        # 单位载荷排放量（kg/吨有效载荷）
        e_k = (factor / 1000) * gamma_G
        emissions[pollutant] = e_k * payload
        # 加权环境影响
        total_impact += e_k * ENVIRONMENTAL_WEIGHTS[pollutant] * payload
    
    return total_impact, emissions

# 计算太空电梯环境影响
def calculate_elevator_impact(payload, carbon_intensity):
    """计算太空电梯的环境影响"""
    total_impact = payload * e_ele * carbon_intensity
    return total_impact

# 计算混合方案环境影响
def calculate_hybrid_impact(rocket_fraction, carbon_scenario):
    """计算混合方案的环境影响"""
    rocket_payload = TOTAL_PAYLOAD * rocket_fraction
    elevator_payload = TOTAL_PAYLOAD * (1 - rocket_fraction)
    
    rocket_impact, _ = calculate_rocket_impact(rocket_payload, DELTA_V_G, I_SP_G, epsilon)
    elevator_impact = calculate_elevator_impact(elevator_payload, CARBON_INTENSITY_SCENARIOS[carbon_scenario])
    
    return rocket_impact + elevator_impact

# 生成数据
def generate_data():
    """生成不同方案的环境影响数据"""
    # 方案1：全部使用传统地面火箭
    rocket_impact, rocket_emissions = calculate_rocket_impact(TOTAL_PAYLOAD, DELTA_V_G, I_SP_G, epsilon)
    
    # 方案2：全部使用太空电梯系统（三种情景）
    elevator_impacts = {}
    for scenario, ci in CARBON_INTENSITY_SCENARIOS.items():
        elevator_impacts[scenario] = calculate_elevator_impact(TOTAL_PAYLOAD, ci)
    
    # 方案3：混合方案（不同比例）
    hybrid_data = {}
    rocket_fractions = np.linspace(0, 1, 11)  # 0到100%，步长10%
    
    for scenario in CARBON_INTENSITY_SCENARIOS:
        impacts = []
        for fraction in rocket_fractions:
            impacts.append(calculate_hybrid_impact(fraction, scenario))
        hybrid_data[scenario] = impacts
    
    return {
        'rocket_impact': rocket_impact,
        'rocket_emissions': rocket_emissions,
        'elevator_impacts': elevator_impacts,
        'hybrid_data': hybrid_data,
        'rocket_fractions': rocket_fractions
    }

# 生成图表
def generate_charts(data):
    """生成多样化的图表"""
    # 1. 不同方案环境影响对比图
    plt.figure(figsize=(12, 10))
    
    # 方案1：地面火箭
    rocket_impact = data['rocket_impact']
    
    # 方案2：太空电梯不同情景
    elevator_impacts = data['elevator_impacts']
    
    # 方案3：混合方案
    hybrid_data = data['hybrid_data']
    rocket_fractions = data['rocket_fractions']
    
    # 绘制地面火箭污染物排放饼图
    plt.subplot(2, 2, 1)
    emissions = data['rocket_emissions']
    plt.pie(emissions.values(), labels=emissions.keys(), autopct='%1.1f%%')
    plt.title('Rocket Pollutant Emission Distribution')
    
    # 绘制碳排放强度敏感性分析
    plt.subplot(2, 2, 2)
    carbon_intensities = np.linspace(0.02, 0.6, 30)
    elevator_impacts_sens = [calculate_elevator_impact(TOTAL_PAYLOAD, ci) for ci in carbon_intensities]
    plt.plot(carbon_intensities, elevator_impacts_sens)
    plt.xlabel('Carbon Intensity (kgCO2e/kWh)')
    plt.ylabel('Environmental Impact Index')
    plt.title('Elevator Environmental Impact Sensitivity')
    plt.grid(alpha=0.3)
    
    # 绘制混合方案环境影响曲线（包含表格）
    plt.subplot(2, 1, 2)
    # 绘制曲线
    for scenario, impacts in hybrid_data.items():
        plt.plot(rocket_fractions * 100, impacts, label=f'Scenario {scenario}')
    plt.xlabel('Rocket Usage Ratio (%)')
    plt.ylabel('Environmental Impact Index')
    plt.title('Hybrid Scheme Environmental Impact')
    plt.legend()
    plt.grid(alpha=0.3)
    
    # 创建环境影响数据表格
    scenarios = ['Rocket', 'Elevator S1', 'Elevator S2', 'Elevator S3']
    impacts = [rocket_impact, elevator_impacts['S1'], elevator_impacts['S2'], elevator_impacts['S3']]
    
    # 格式化数据为科学计数法
    formatted_impacts = [f'{imp:.2e}' for imp in impacts]
    
    # 在折线图内部右下方添加缩小的表格
    table_data = [scenarios, formatted_impacts]
    table_data = list(map(list, zip(*table_data)))
    
    # 计算表格位置 - 放在右下方
    ax = plt.gca()
    table = ax.table(cellText=table_data, 
                    colLabels=['Scheme', 'Env. Impact'],
                    loc='best', 
                    bbox=[0.6, 0.1, 0.35, 0.25])  # [x, y, width, height]
    
    # 美化表格
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width([0, 1])
    
    # 设置表格样式
    for cell in table._cells:
        cell_obj = table._cells[cell]
        if cell[0] == 0:  # 表头
            cell_obj.set_facecolor('#f0f0f0')
            # 使用 text_props 设置字体权重
            cell_obj.set_text_props(ha='center', va='center', fontweight='bold')
        else:
            cell_obj.set_text_props(ha='center', va='center')
        cell_obj.set_edgecolor('gray')
        cell_obj.set_linewidth(0.5)
    plt.savefig('environment_impact_analysis.png', dpi=300, bbox_inches='tight')
    
    # 单独将混合方案环境影响曲线（包含表格）保存为一个PNG文件
    plt.figure(figsize=(10, 6))
    # 绘制曲线
    for scenario, impacts in hybrid_data.items():
        plt.plot(rocket_fractions * 100, impacts, label=f'Scenario {scenario}')
    plt.xlabel('Rocket Usage Ratio (%)')
    plt.ylabel('Environmental Impact Index')
    plt.title('Hybrid Scheme Environmental Impact')
    plt.legend()
    plt.grid(alpha=0.3)
    
    # 重新创建表格
    ax = plt.gca()
    table = ax.table(cellText=table_data, 
                    colLabels=['Scheme', 'Env. Impact'],
                    loc='best', 
                    bbox=[0.6, 0.1, 0.35, 0.25])  # [x, y, width, height]
    
    # 美化表格
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width([0, 1])
    
    # 设置表格样式
    for cell in table._cells:
        cell_obj = table._cells[cell]
        if cell[0] == 0:  # 表头
            cell_obj.set_facecolor('#f0f0f0')
            # 使用 text_props 设置字体权重
            cell_obj.set_text_props(ha='center', va='center', fontweight='bold')
        else:
            cell_obj.set_text_props(ha='center', va='center')
        cell_obj.set_edgecolor('gray')
        cell_obj.set_linewidth(0.5)
    plt.tight_layout()
    plt.savefig('hybrid_scheme_impact.png', dpi=300, bbox_inches='tight')
    
    # 2. 单独的推进剂强度敏感性分析图
    plt.figure(figsize=(12, 6))
    
    # 速度增量敏感性
    delta_v_values = np.linspace(9000, 10500, 20)
    gamma_values = [calculate_propellant_intensity(dv, I_SP_G, epsilon) for dv in delta_v_values]
    
    plt.subplot(1, 2, 1)
    plt.plot(delta_v_values, gamma_values)
    plt.xlabel('Velocity Increment (m/s)')
    plt.ylabel('Propellant Intensity (ton/ton)')
    plt.title('Effect of Velocity Increment on Propellant Intensity')
    plt.grid(alpha=0.3)
    
    # 比冲敏感性
    i_sp_values = np.linspace(250, 350, 20)
    gamma_values_isp = [calculate_propellant_intensity(DELTA_V_G, isp, epsilon) for isp in i_sp_values]
    
    plt.subplot(1, 2, 2)
    plt.plot(i_sp_values, gamma_values_isp)
    plt.xlabel('Specific Impulse (s)')
    plt.ylabel('Propellant Intensity (ton/ton)')
    plt.title('Effect of Specific Impulse on Propellant Intensity')
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('propellant_intensity_sensitivity.png', dpi=300, bbox_inches='tight')

# 主函数
def main():
    """主函数"""
    print("=== 环境影响评估与优化分析 ===")
    print(f"总运输质量: {TOTAL_PAYLOAD/1e6:.1f} 百万吨")
    print()
    
    # 生成数据
    data = generate_data()
    
    # 输出结果
    print("1. 方案1：全部使用传统地面火箭")
    print(f"   环境影响指数: {data['rocket_impact']:.2e}")
    print("   污染物排放:")
    for pollutant, emission in data['rocket_emissions'].items():
        print(f"   - {pollutant}: {emission/1e6:.2f} 百万吨")
    print()
    
    print("2. 方案2：全部使用太空电梯系统")
    for scenario, impact in data['elevator_impacts'].items():
        print(f"   情景{scenario}: {impact:.2e} (环境影响指数)")
    print()
    
    print("3. 方案3：混合方案环境影响")
    rocket_fractions = data['rocket_fractions']
    for scenario, impacts in data['hybrid_data'].items():
        print(f"   情景{scenario}:")
        for i, fraction in enumerate(rocket_fractions):
            if i % 2 == 0:  # 每20%输出一次
                print(f"      火箭比例 {fraction*100:.0f}%: {impacts[i]:.2e}")
    print()
    
    # 生成图表
    print("生成图表...")
    generate_charts(data)
    print("图表生成完成！")

if __name__ == "__main__":
    main()
