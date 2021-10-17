# Vulnerable Banks

## Metadata

* Type: [[Article]]
* Authors: [[Greenwood Robin Marc]], [[Landier Augustin]], [[Thesmar David]]
* Date: [[2015]]
* Date added: [[2020-06-31]]
* Publication: [[Journal of Financial Economics]]
* Cite key: Marc_2015_VulnerableBanks
* Topics: [[系统性风险 传导机制]], [[银行系统性风险 网络分析法]], [[系统性风险 影响因素]]
* Related: [[系统性风险、抛售博弈与宏观审慎政策]], [[系统性风险的传染渠道与度量研究——兼论宏观审慎政策实施]], [[系统性风险的传染渠道与度量研究——兼论宏观审慎政策实施 - 模型借鉴]]
* Tags: [[Zotero Import]]
* PDF Attachments: [Marc et al_2015_Vulnerable Banks.pdf](zotero://open-pdf/library/items/I99XDJ3R)

### Abstract

 When a bank experiences a negative shock to its equity, one way to return to target leverage is to sell assets. If asset sales occur at depressed prices, then one bank’s sales may impact other banks with common exposures, resulting in contagion. We propose a simple framework that accounts for how this effect adds up across the banking sector. Our framework explains how the distribution of bank leverage and risk exposures contributes to a form of systemic risk. We compute bank exposures to system-wide deleveraging, as well as the spillover of a single bank’s deleveraging onto other banks. We show how our model can be used to evaluate a variety of crisis interventions, such as mergers of good and bad banks and equity injections. We apply the framework to European banks vulnerable to sovereign risk in 2010 and 2011.



## 摘要

当银行的权益遭受负面冲击时，恢复目标杠杆的一种方法是出售资产。如果资产销售价格低迷，那么一家银行的销售可能会影响其他有共同风险敞口的银行，从而导致传染。我们提出一个简单的框架，说明这种影响如何在整个银行业中加起来。我们的框架说明了银行杠杆和风险敞口的分布如何导致某种形式的系统性风险。我们计算银行在整个系统范围内的去杠杆化的风险敞口，以及单个银行去杠杆化对其他银行的溢出风险。我们将展示如何使用我们的模型来评估各种危机干预措施，例如好坏银行的合并以及注资。我们将该框架应用于2010年和201年易受主权风险影响的欧洲银行。





## 相关机制

考虑了金融机构持有多种非流动性金融资产的降价抛售线性传染机制。  



实际上银行可能首先出售其流动性最强的资产。恒定的投资组合假设简化了代数和下面的直觉，但我们稍后显示（第四节F），框架可以很容易地修改，以考虑更复杂的清算规则。



## 抛售资产规则  

- 按照初始比例抛售资产  



## 相关文献：





## 模型



#### 解释一些公式：



首先，假设资产交易应对银行回报冲击。

$R_{t}=M F_{t}$

<img src="Marc_Augustin_et-al_2015_Vulnerable Banks.assets/image-20211016220137506.png" alt="image-20211016220137506" style="zoom: 33%;" />





其次，我们必须描述银行如何出售个人资产，以回归目标杠杆。我们做出最简单的假设，即银行出售资产的方式是在日期 1 和 2 之间保持 M 矩阵不变。
$$
\phi=M^{\prime} A_{1} B R_{1}
$$
<img src="Marc_Augustin_et-al_2015_Vulnerable Banks.assets/image-20211017210355254.png" alt="image-20211017210355254" style="zoom:50%;" />



第三，我们假设第二期的资产销售量根据线性模型通过价格影响资产净回报。
$$
R_{2}=M F_{2}=M L \phi=\left(M L M^{\prime} B A_{1}\right) R_{1}
$$






我们结合方程 （1）、（2） 和 （3） 来计算 t=1 中银行未关联资产回报对 t=2 回报的影响
$$
R_{2}=M F_{2}=M L \phi=\left(M L M^{\prime} B A_{1}\right) R_{1}
$$


#### 指标



##### 测度**加总的去杠杆化的风险**

$$
A V=\frac{1^{\prime} A_{1} M L M^{\prime} B A_{1} M F_{1}}{E_{1}}
$$
这个公式忽略了冲击对净资产的直接影响，只强调银行间的溢出效应。







<img src="Marc_Augustin_et-al_2015_Vulnerable Banks.assets/方意_郑子文_2016_系统性风险在银行间的传染路径研究——基于持有共同资产网络模型.svg" alt="方意_郑子文_2016_系统性风险在银行间的传染路径研究——基于持有共同资产网络模型" style="transform: rotate(90deg); zoom: 50%;" />





理解 **连接性**$\Gamma:=1^{\prime} A_{1} M L M^{\prime}$：
$$
\gamma_{n}=\sum_{k} \left( \left(\sum_{m} a_{m} m_{m k}\right) \left( l_{k} m_{n k} \right) \right)
$$
其测度了一家银行的“连接度”。该测度银行将持有更大的资产（当$\left(\sum_{m} a_{m} m_{m k}\right)$更大时），或持有非流动性资产（当$l_{k}$更大时）的资产类别当中哪个更大的。在这种情况下，银行抛售1美元资产将导致银行系统持有的更多金额，因为它将减少更大的资产类别的价格。



<img src="Marc_Augustin_et-al_2015_Vulnerable Banks.assets/方意_郑子文_2016_系统性风险在银行间的传染路径研究——基于持有共同资产网络模型-2.svg" alt="方意_郑子文_2016_系统性风险在银行间的传染路径研究——基于持有共同资产网络模型" style="transform: translate(0px,500px) rotate(90deg); transform-origin:50% 50%; zoom: 50%; " />

























更一般地说，该式之**连接性**$\Gamma:=1^{\prime} A_{1} M L M^{\prime}$、杠杆$B$、大小$A_{1}$、风险敞口$M F_{1}$，四个要素在确定 AV 时会成倍增加。



##### 各银行对去杠杆化的贡献："系统性"

TODO各银行对去杠杆化的贡献："系统性"

