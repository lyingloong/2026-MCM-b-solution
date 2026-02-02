# 敏感性分析图表说明文档
# Sensitivity Analysis Figures Documentation

## 目录 / Table of Contents
1. 图 1：太空电梯风速 - 摆角分布 + 可用度阈值（散点图）
   Figure 1: Space Elevator Wind Speed - Swing Angle Distribution + Availability Threshold (Scatter Plot)
2. 图 2：火箭残值损失成本曲线（折线图）
   Figure 2: Rocket Residual Value Loss Cost Curve (Line Plot)
3. 图 3：太空电梯关键参数敏感性分析（三子图）
   Figure 3: Space Elevator Key Parameters Sensitivity Analysis (Three Subplots)
4. 图 4：有效运输量 vs 参数 + 系统可用度对比（组合图）
   Figure 4: Effective Transport Capacity vs Parameters + System Availability Comparison (Combined Plot)

## 1. 图 1：太空电梯风速 - 摆角分布 + 可用度阈值（散点图）
### Figure 1: Space Elevator Wind Speed - Swing Angle Distribution + Availability Threshold (Scatter Plot)

**核心作用 / Core Function:**
可视化建模中「太空电梯可用度的双重约束（ϕ≤ϕcrit​ 且 vwind​≤vsafe​）」，蓝色点为可用状态，红色为不可用，虚线为阈值线，直接展示威布尔分布风速和线性摆角的随机特性，蒙特卡洛模拟得到的长期可用率ASE​标注在图例中，是环境约束模块的核心可视化。

Visualizes the dual constraints of space elevator availability (ϕ≤ϕcrit​ and vwind​≤vsafe​) in the model. Blue points represent available states, red points represent unavailable states, and dashed lines represent threshold lines. It directly demonstrates the random characteristics of Weibull distribution wind speed and linear swing angle, with the long-term availability rate ASE​ obtained from Monte Carlo simulation labeled in the legend. This is the core visualization of the environmental constraint module.

**论文标注 / Paper Annotation:**
可在图中标注蒙特卡洛模拟次数，说明ASE​的统计意义。

The number of Monte Carlo simulations can be annotated in the figure to explain the statistical significance of ASE​.

**可写结论示例 / Example Conclusion:**
由图可见，大部分工况落在可用域内，长期可用度 ASE​≈0.95，说明电梯在设计风速与摆角约束下具备较高可用性。高风速与大摆角共同构成主要不可用来源。

As shown in the figure, most operating conditions fall within the available domain, with a long-term availability rate of ASE​≈0.95, indicating that the elevator has high availability under the designed wind speed and swing angle constraints. High wind speeds and large swing angles together constitute the main sources of unavailability.

## 2. 图 2：火箭残值损失成本曲线（折线图）
### Figure 2: Rocket Residual Value Loss Cost Curve (Line Plot)

**核心作用 / Core Function:**
可视化建模中「线性折旧的残值损失公式」，对比在轨摆渡火箭和地面火箭的损失成本随故障次数的变化 —— 故障发生得越早，残值损失越大（第 1 次故障损失 100% 成本，第 N 次故障损失 1/N 成本），完美匹配建模中的CS​和Cg​公式，是火箭残值损失模块的核心可视化。

Visualizes the "linear depreciation residual value loss formula" in the model, comparing the loss costs of on-orbit ferry rockets and ground rockets as they change with the number of failures. The earlier a failure occurs, the greater the residual value loss (100% cost loss for the first failure, 1/N cost loss for the Nth failure). This perfectly matches the CS​ and Cg​ formulas in the model and is the core visualization of the rocket residual value loss module.

**论文标注 / Paper Annotation:**
可标注 "线性折旧假设"，说明成本计算的前提。

The "linear depreciation assumption" can be annotated to explain the premise of cost calculation.

**论文可写 / Paper Content:**
残值损失随故障任务次数线性递减，早期故障带来的经济冲击远大于后期故障，因此提升前若干次任务的可靠性对控制总成本至关重要。

Residual value loss decreases linearly with the number of failed missions. Early failures bring much greater economic impact than later failures, so improving the reliability of the first few missions is crucial for controlling total costs.

## 3. 图 3：太空电梯关键参数敏感性分析（三子图）
### Figure 3: Space Elevator Key Parameters Sensitivity Analysis (Three Subplots)

**核心作用 / Core Function:**
分析安全风速、临界摆角、耦合系数对太空电梯可用度ASE​的影响，是鲁棒性分析的核心—— 比如安全风速越大、临界摆角越大，可用度越高；耦合系数越大（风速对摆角影响越显著），可用度越低，直观展示系统对环境参数的敏感程度。

Analyzes the impact of safe wind speed, critical swing angle, and coupling coefficient on space elevator availability ASE​, which is the core of robustness analysis. For example, higher safe wind speed and larger critical swing angle lead to higher availability; larger coupling coefficient (more significant impact of wind speed on swing angle) leads to lower availability. It intuitively demonstrates the system's sensitivity to environmental parameters.

**论文扩展 / Paper Extension:**
可增加「扰动项标准差ϵ、维护停机比例βmaint​」的敏感性分析，丰富鲁棒性结论。

Sensitivity analysis of "disturbance term standard deviation ϵ and maintenance downtime ratio βmaint​" can be added to enrich robustness conclusions.

**示例写法 / Example Writing:**
敏感性分析表明，太空电梯可用度对安全风速与临界摆角呈正向单调响应，对耦合系数呈负向单调响应。其中，低风速区间内 ASE​ 对 vsafe​ 变化尤为敏感，表明工程上应优先保证足够的风速安全裕度。

Sensitivity analysis shows that space elevator availability has a positive monotonic response to safe wind speed and critical swing angle, and a negative monotonic response to coupling coefficient. Among them, ASE​ is particularly sensitive to changes in vsafe​ in the low wind speed range, indicating that sufficient wind speed safety margin should be prioritized in engineering.

## 4. 图 4：有效运输量 vs 参数 + 系统可用度对比（组合图）
### Figure 4: Effective Transport Capacity vs Parameters + System Availability Comparison (Combined Plot)

**核心作用 / Core Function:**
上子图：展示参数变化对太空电梯 ** 有效运输量QSEeff​​** 的影响（贴合建模公式），直接关联 "可用度 - 成功率 - 运输量" 的逻辑链；
下子图：对比太空电梯、在轨火箭、地面火箭的可用度，突出不同运输系统的鲁棒性差异，为后续 "组合系统优化" 提供数据支撑；
核心价值：将 "可用度" 这一中间指标转化为系统实际运输能力，贴合工程实际。

Upper subplot: Shows the impact of parameter changes on the space elevator's effective transport capacity QSEeff​​ (consistent with the modeling formula), directly linking the logical chain of "availability - success rate - transport capacity";
Lower subplot: Compares the availability of space elevators, on-orbit rockets, and ground rockets, highlighting the robustness differences between different transport systems and providing data support for subsequent "combined system optimization";
Core value: Transforms the intermediate indicator of "availability" into the actual transport capacity of the system, which is consistent with engineering practice.

**论文可写 / Paper Content:**
有效运输量对关键环境参数的响应规律与可用度一致，进一步验证了参数影响的传导机制。多系统对比表明，太空电梯链路可用性最高，适合承担核心稳定运输任务。

The response law of effective transport capacity to key environmental parameters is consistent with availability, further verifying the transmission mechanism of parameter influence. Multi-system comparison shows that the space elevator link has the highest availability and is suitable for undertaking core stable transport tasks.