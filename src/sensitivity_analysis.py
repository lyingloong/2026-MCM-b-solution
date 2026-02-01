"""
gengrated by Doubao AI
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import weibull_min, norm
import warnings
warnings.filterwarnings('ignore')

# ===================== 1. 全局参数设置（贴合你的建模定义）=====================
# 绘图样式设置（论文级美观风格）
plt.rcParams['font.sans-serif'] = ['Times New Roman', 'SimHei']  # 支持英文/中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (10, 6)
sns.set_style('whitegrid')
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']  # 论文级配色

# 太空电梯参数
k = 0.05  # 风速-摆角耦合系数 (rad/(m/s))
phi_crit = 1.0  # 临界摆角 (rad)
v_safe = 20.0   # 安全风速 (m/s)
beta_maint = 0.05  # 维护停机比例
N_SE = 3  # 缆绳数量
Q_e = 50  # 电梯单次载荷 (吨)
rho_e0 = 0.99  # 电梯基础成功率
weibull_shape = 2.0  # 风速威布尔分布形状参数
weibull_scale = 10.0 # 风速威布尔分布尺度参数
MC_n = 10000  # 蒙特卡洛模拟次数（越大越精准）

# 火箭系统参数
# 在轨摆渡火箭(S)
C_veh_S = 20_000_000  # 初始成本 (美元)
N_S = 50  # 设计复用次数
rho_S0 = 0.99  # 基础成功率
A_S = 0.95  # 在轨可用比例
# 地面火箭(g)
C_veh_g = 10_000_000  # 初始成本 (美元)
N_g = 20  # 设计复用次数
rho_g0 = 0.95  # 基础成功率
A_g = 0.90  # 地面可用比例

# 随机扰动参数
epsilon_scale = 0.01  # 扰动项ε的标准差（正态分布）
epsilon_phi_scale = 0.05  # 摆角扰动的标准差（rad）

# ===================== 2. 核心函数定义（贴合建模公式）=====================
def space_elevator_availability(MC_n, k, phi_crit, v_safe, weibull_shape, weibull_scale, epsilon_phi_scale):
    """
    蒙特卡洛模拟计算太空电梯可用度A_SE和有效成功率
    返回：可用度序列、摆角序列、风速序列、有效成功率序列
    """
    # 1. 生成威布尔分布的风速
    v_wind = weibull_min.rvs(c=weibull_shape, scale=weibull_scale, size=MC_n)
    # 2. 生成摆角扰动和成功率扰动（正态分布，均值0）
    epsilon_phi = norm.rvs(loc=0, scale=epsilon_phi_scale, size=MC_n)
    epsilon_rho = norm.rvs(loc=0, scale=epsilon_scale, size=MC_n)
    # 3. 计算摆角（建模公式：phi = k*v_wind + epsilon）
    phi = k * v_wind + epsilon_phi
    # 4. 计算可用度指示函数η(t)（建模公式：phi<=crit 且 v_wind<=safe）
    eta = np.where((phi <= phi_crit) & (v_wind <= v_safe), 1, 0)
    # 5. 计算受扰动的单次成功率（建模公式：rho_e(t) = rho_e0 + epsilon(t)，限制在0-1）
    rho_e = np.clip(rho_e0 + epsilon_rho, 0, 1)
    # 6. 有效成功率（η*rho_e）
    rho_e_eff = eta * rho_e
    # 7. 长期可用率A_SE
    A_SE = np.mean(eta)
    # 8. 平均有效成功率
    rho_e_avg = np.mean(rho_e_eff)
    # 9. 有效运输量（建模公式：Q_SE_eff = N_SE*Q_e*A_SE*rho_e_avg*(1-beta_maint)）
    Q_SE_eff = N_SE * Q_e * A_SE * rho_e_avg * (1 - beta_maint)
    return eta, phi, v_wind, rho_e_eff, A_SE, Q_SE_eff

def rocket_residual_loss(C_veh, N_design, n_failure):
    """
    计算火箭残值损失成本（建模公式：C = C_veh*(N-n+1)/N）
    :param C_veh: 初始制造成本
    :param N_design: 设计复用次数
    :param n_failure: 故障发生在第n次
    :return: 残值损失成本
    """
    n_failure = np.clip(n_failure, 1, N_design)  # 限制n在1~N之间
    C_loss = C_veh * (N_design - n_failure + 1) / N_design
    return C_loss

def sensitivity_analysis(param_name, param_range, base_kwargs):
    """
    敏感性分析：改变单个参数，计算系统关键指标（可用度/运输量/成本）
    :param param_name: 待分析参数名（如v_safe, phi_crit, k）
    :param param_range: 待分析参数的取值范围
    :param base_kwargs: 基础参数字典
    :return: 各参数对应的A_SE和Q_SE_eff
    """
    A_SE_list = []
    Q_SE_eff_list = []
    for param in param_range:
        base_kwargs[param_name] = param
        _, _, _, _, A_SE, Q_SE_eff = space_elevator_availability(
            MC_n=base_kwargs['MC_n'],
            k=base_kwargs['k'],
            phi_crit=base_kwargs['phi_crit'],
            v_safe=base_kwargs['v_safe'],
            weibull_shape=base_kwargs['weibull_shape'],
            weibull_scale=base_kwargs['weibull_scale'],
            epsilon_phi_scale=base_kwargs['epsilon_phi_scale']
        )
        A_SE_list.append(A_SE)
        Q_SE_eff_list.append(Q_SE_eff)
    return np.array(A_SE_list), np.array(Q_SE_eff_list)

# ===================== 3. 数据生成（蒙特卡洛+敏感性分析）=====================
# 3.1 太空电梯蒙特卡洛模拟
eta, phi, v_wind, rho_e_eff, A_SE, Q_SE_eff = space_elevator_availability(
    MC_n=MC_n, k=k, phi_crit=phi_crit, v_safe=v_safe,
    weibull_shape=weibull_shape, weibull_scale=weibull_scale,
    epsilon_phi_scale=epsilon_phi_scale
)
# 3.2 火箭残值损失计算（生成1~N次故障的成本序列）
n_failure_S = np.arange(1, N_S+1)
C_loss_S = rocket_residual_loss(C_veh_S, N_S, n_failure_S)
n_failure_g = np.arange(1, N_g+1)
C_loss_g = rocket_residual_loss(C_veh_g, N_g, n_failure_g)
# 3.3 敏感性分析（以安全风速v_safe、临界摆角phi_crit、耦合系数k为例）
base_kwargs = {
    'MC_n': MC_n, 'k': k, 'phi_crit': phi_crit, 'v_safe': v_safe,
    'weibull_shape': weibull_shape, 'weibull_scale': weibull_scale,
    'epsilon_phi_scale': epsilon_phi_scale
}
# 安全风速敏感性（v_safe: 10~30 m/s）
v_safe_range = np.linspace(10, 30, 20)
A_SE_v, Q_SE_v = sensitivity_analysis('v_safe', v_safe_range, base_kwargs)
# 临界摆角敏感性（phi_crit: 0.5~2.0 rad）
phi_crit_range = np.linspace(0.5, 2.0, 20)
A_SE_phi, Q_SE_phi = sensitivity_analysis('phi_crit', phi_crit_range, base_kwargs)
# 耦合系数敏感性（k: 0.01~0.1 rad/(m/s)）
k_range = np.linspace(0.01, 0.1, 20)
A_SE_k, Q_SE_k = sensitivity_analysis('k', k_range, base_kwargs)

# ===================== 4. 绘制4类核心图表（论文级）=====================
# ---------- 图1：太空电梯风速-摆角分布+可用度阈值（散点图，核心展示环境约束） ----------
fig1, ax1 = plt.subplots(figsize=(8, 6))
# 绘制散点：可用(蓝色)、不可用(红色)
mask_available = (phi <= phi_crit) & (v_wind <= v_safe)
ax1.scatter(v_wind[mask_available], phi[mask_available], c=colors[0], s=1, alpha=0.6, label=f'Available (A_SE={A_SE:.3f})')
ax1.scatter(v_wind[~mask_available], phi[~mask_available], c=colors[3], s=1, alpha=0.3, label='Unavailable')
# 绘制阈值线：安全风速、临界摆角
ax1.axvline(x=v_safe, c=colors[2], lw=2, ls='--', label=f'v_safe={v_safe} m/s')
ax1.axhline(y=phi_crit, c=colors[1], lw=2, ls='--', label=f'phi_crit={phi_crit} rad')
# 标注
ax1.set_xlabel('Wind Speed $v_{wind}$ (m/s)')
ax1.set_ylabel('Sway Angle $\\phi$ (rad)')
ax1.set_title('Space Elevator Wind Speed - Sway Angle Distribution & Availability Threshold')
ax1.legend(loc='upper right')
ax1.set_xlim(0, max(v_wind)*1.1)
ax1.set_ylim(0, max(phi)*1.1)
plt.tight_layout()
plt.savefig('fig1_elevator_availability_threshold.png', bbox_inches='tight')

# ---------- 图2：火箭残值损失成本曲线（折线图，对比在轨/地面火箭） ----------
fig2, ax2 = plt.subplots(figsize=(8, 6))
# 绘制两条曲线
ax2.plot(n_failure_S, C_loss_S/1e6, c=colors[0], lw=2, label=f'Orbital Tug (C_veh=${C_veh_S/1e6:.0f}$M, N={N_S})')
ax2.plot(n_failure_g, C_loss_g/1e6, c=colors[1], lw=2, label=f'Ground Rocket (C_veh=${C_veh_g/1e6:.0f}$M, N={N_g})')
# 标注
ax2.set_xlabel('Failure Occurs at n-th Mission')
ax2.set_ylabel('Residual Value Loss Cost (Million USD)')
ax2.set_title('Rocket Residual Value Loss vs. Failure Mission Number (Linear Depreciation)')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig2_rocket_residual_loss.png', bbox_inches='tight')

# ---------- 图3：太空电梯关键参数敏感性分析（子图，核心展示鲁棒性） ----------
fig3, (ax31, ax32, ax33) = plt.subplots(1, 3, figsize=(15, 5))
# 子图1：安全风速v_safe对可用度A_SE的影响
ax31.plot(v_safe_range, A_SE_v, c=colors[0], lw=2, marker='o', ms=3)
ax31.set_xlabel('Safe Wind Speed $v_{safe}$ (m/s)')
ax31.set_ylabel('Space Elevator Availability $A_{SE}$')
ax31.set_title('Sensitivity to Safe Wind Speed')
ax31.grid(True, alpha=0.3)
# 子图2：临界摆角phi_crit对可用度A_SE的影响
ax32.plot(phi_crit_range, A_SE_phi, c=colors[1], lw=2, marker='o', ms=3)
ax32.set_xlabel('Critical Sway Angle $\\phi_{crit}$ (rad)')
ax32.set_ylabel('Space Elevator Availability $A_{SE}$')
ax32.set_title('Sensitivity to Critical Sway Angle')
ax32.grid(True, alpha=0.3)
# 子图3：耦合系数k对可用度A_SE的影响
ax33.plot(k_range, A_SE_k, c=colors[2], lw=2, marker='o', ms=3)
ax33.set_xlabel('Coupling Coefficient k (rad/(m/s))')
ax33.set_ylabel('Space Elevator Availability $A_{SE}$')
ax33.set_title('Sensitivity to Coupling Coefficient')
ax33.grid(True, alpha=0.3)
# 整体标题
fig3.suptitle('Space Elevator Availability - Key Parameter Sensitivity Analysis', y=1.02)
plt.tight_layout()
plt.savefig('fig3_elevator_sensitivity_analysis.png', bbox_inches='tight')

# ---------- 图4：太空电梯有效运输量vs参数+系统可用度对比（柱状+折线，多指标分析） ----------
fig4, (ax41, ax42) = plt.subplots(2, 1, figsize=(10, 8))
# 子图1：参数对有效运输量的影响
ax41.plot(v_safe_range, Q_SE_v, c=colors[0], lw=2, label='$v_{safe}$ (10~30 m/s)')
ax41.plot(phi_crit_range, Q_SE_phi, c=colors[1], lw=2, label='$\\phi_{crit}$ (0.5~2.0 rad)')
ax41.plot(k_range, Q_SE_k, c=colors[2], lw=2, label='$k$ (0.01~0.1 rad/(m/s))')
ax41.set_xlabel('Parameter Value')
ax41.set_ylabel('Effective Throughput $Q_{SE_{eff}}$ (ton)')
ax41.set_title('Space Elevator Effective Throughput vs. Key Parameters')
ax41.legend()
ax41.grid(True, alpha=0.3)
# 子图2：不同运输系统可用度对比（柱状图：电梯/在轨火箭/地面火箭）
systems = ['Space Elevator', 'Orbital Tug (S)', 'Ground Rocket (g)']
availabilities = [A_SE, A_S, A_g]
ax42.bar(systems, availabilities, color=[colors[0], colors[1], colors[2]], alpha=0.8, width=0.6)
# 标注数值
for i, v in enumerate(availabilities):
    ax42.text(i, v+0.01, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
ax42.set_ylabel('System Availability $A$')
ax42.set_title('Availability Comparison of Different Transportation Systems')
ax42.set_ylim(0, 1.05)
plt.tight_layout()
plt.savefig('fig4_throughput_vs_availability.png', bbox_inches='tight')

# 显示所有图
plt.show()

# ===================== 5. 输出关键模拟结果 =====================
print("="*50)
print("Problem2 Core Simulation Results")
print("="*50)
print(f"Space Elevator Long-term Availability A_SE: {A_SE:.3f}")
print(f"Space Elevator Average Effective Success Rate: {np.mean(rho_e_eff):.3f}")
print(f"Space Elevator Effective Throughput Q_SE_eff: {Q_SE_eff:.2f} ton")
print(f"Orbital Tug Max Residual Loss: {C_loss_S[0]/1e6:.2f} Million USD (1st mission failure)")
print(f"Ground Rocket Max Residual Loss: {C_loss_g[0]/1e6:.2f} Million USD (1st mission failure)")
print("="*50)