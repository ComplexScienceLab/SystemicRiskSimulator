



# Gertler_Kiyotaki_2015_Banking, Liquidity, and Bank Runs in an Infinite Horizon Economy



[toc]


# Banking, Liquidity, and Bank Runs in an Infinite Horizon Economy

## Metadata

* Type: [[Article]]
* Authors: [[Mark Gertler]], [[Nobuhiro Kiyotaki]]
* Date: [[2015-07-01]]
* Date added: [[2020-07-30]]
* Publication: [[American Economic Review]]
* DOI: [10.1257/aer.20130665](10.1257/aer.20130665)
* Cite key: Gertler_2015_BankingLiquidityandBankRunsinanInfiniteHorizonEconomy
* Topics: [[系统性风险 挤兑]], [[系统性风险 Dsge]]
* Related: 
* Tags: [[Zotero Import]], [[_tablet_modified]], [[Archived]]
* PDF Attachments: [Gertler_Kiyotaki_2015_Banking, Liquidity, and Bank Runs in an Infinite Horizon Economy.pdf](zotero://open-pdf/library/items/RVJYZWDF)

### Abstract

 We develop an infinite horizon macroeconomic model of banking that allows for liquidity mismatch and bank runs. Whether a bank run equilibrium exists depends on bank balance sheets and an endogenous liquidation price for bank assets. While in normal times a bank run equilibrium may not exist, the possibility can arise in recessions. A run leads to a significant contraction in intermediation and aggregate economic activity. Anticipations of a run have harmful effects on the economy even if the run does not occur. We illustrate how the model can shed light on some key aspects of the recent financial crisis. (JEL E23, E32, E44, G01, G21, G33)





## 摘要：

我们开发一个无限水平的银行宏观经济模型，允许流动性不匹配和银行运行。银行运行均衡是否存在取决于银行资产负债表和银行资产的内生清算价格。虽然在正常时期，银行运行均衡可能不存在，但这种可能性可能在衰退中出现。运行导致中介和总体经济活动的显著收缩。对挤兑的预期对经济有有害影响，即使挤兑不出现。我们说明了该模型如何阐明最近金融危机的一些关键方面。



## 目标

目标是开发一个简单的银行不稳定宏观经济模型，它既实现了金融加速器效应，也实现了银行挤兑。我们的方法强调这些机制的互补性。资产负债表条件不仅影响银行信贷成本，还影响是否可能发生挤兑。在这方面，可以关联与宏观经济条件有关挤兑的可能性，反过来又描述挤兑如何反馈到宏观经济。





## 模型



债务展期危机模拟算法。





模型基础：带有银行部门和流动性风险的无限宏观模型。



### 模型的特点

- 引入金融市场的摩擦；
- 描述影子银行；
- 把资本作为一种商品；



#### 模型的关键特征

- 个体：
  - 家庭

    - 家庭的资产变化：
      $$
      \left.\begin{array}{l}
      K_{t}^{h} \text { capital } \\
      f\left(K_{t}^{h}\right) \text { goods }
      \end{array}\right\} \rightarrow\left\{\begin{array}{l}
      Z_{t+1} K_{t}^{h} \text { output } \\
      K_{t}^{h} \text { capital }
      \end{array}\right.
      $$
      其中$f\left(K_{t}^{h}\right) \triangleq \frac{\alpha}{2}\left(K_{t}^{h}\right)^{2},\alpha>0$。

  - 银行家（占极少数）

    - 银行家的资产变化：
      $$
      K_{t}^{b} \text { capital }\} \rightarrow\left\{\begin{array}{l}
      Z_{t+1} K_{t}^{b} \text { output } \\
      K_{t}^{b} \text { capital }
      \end{array}\right.
      $$
  
- 商品：

  - 耐用商品（资本）$K_t$，分别持有于银行$K_t^b$和家庭$K_t^h$，满足约束$K_{t}^{b}+K_{t}^{h}=1$。
  - 易耗商品

  银行家的资产变化：
  $$
  K_{t}^{b} \text { capital }\} \rightarrow\left\{\begin{array}{l}
  Z_{t+1} K_{t}^{b} \text { output } \\
  K_{t}^{b} \text { capital }
  \end{array}\right.
  $$

​	

#### 模型的家庭部门

家庭部门的行为：

- 消费$C_t^h$；

- 储蓄到银行，并且实际获得来自银行的含利息的回报$R_{t+1}$。如果银行出现挤兑，则储户只能收到预期回报$\bar{R}_{t+1}$的分数$x_{t+1}$。
  $$
  R_{t+1}=\left\{\begin{array}{ll}
  R_{t+1} & \text { if no bank run } \\
  x_{t+1} \bar{R}_{t+1} & \text { if run occurs }
  \end{array}\right.
  $$

- 工资收入$Z_tW^h$。其中$Z_t$表示加总的生产冲击随机量。

  > 为什么考虑资助，为了提升模型的计量性能。

  

  

假设，银行挤兑是意外事件。因此，家庭选择消费和储蓄的期望是确定的。

家庭单期效用$U_t$（以前向预期的形式）：
$$
U_{t}=E_{t}\left(\sum_{i=0}^{\infty} \beta^{i} \ln C_{t+i}^{h}\right)
$$
约束条件：
$$
C_{t}^{h}+D_{t}+Q_{t} K_{t}^{h}+f\left(K_{t}^{h}\right)=Z_{t} W^{h}+R_{t} D_{t-1}+\left(Z_{t}+Q_{t}\right) K_{t-1}^{h}
$$




情形1：

**假如银行未出现挤兑**，则：

- 存款的一阶条件：

$$
E_{t}\left(\Lambda_{t, t+1}\right) R_{t+1}=1
$$

  其中，随机折扣因子$\Lambda_{t,t+1}$满足条件：
$$
\Lambda_{t, t+i}=\beta^{i} \frac{C_{t}^{h}}{C_{t+i}^{h}}
$$

- 直接资本持有的一阶条件：
  $$
  E_{t}\left(\Lambda_{t, t+1} R_{t+1}^{h}\right)=1
  $$
  其中
  $$
  R_{t+1}^{h}=\frac{Z_{t+1}+Q_{t+1}}{Q_{t}+f^{\prime}\left(K_{t}^{h}\right)}
  $$

#### 模型的银行部门



银行部门最接近于影子银行系统。



- 特点：

  - 不受监管

  - 可能遭受挤兑

    

- 行为：

  - 持有长期证券；
  - 发行短期债务；
  - 

银行部门子模型的假定



##### 银行家的道德风险问题：
银行家面临道德风险。就是在接受存款之后，面临两个选择：
- 道德的事情：按照约定在到期时发放带息存款；
- 不道德的事情：把资金拿去二级市场投资。为了不被发现，银行家只拿一部分$\theta$比例的资金，慢慢投资。这样做的惩罚是，存款人可以在下一个时期开始时迫使中介机构倒闭。


银行家最优化问题

银行家营收价值的递归表示：
$$
V_{t}=E_{t}\left[\beta(1-\sigma) n_{t+1}+\beta \sigma V_{t+1}\right]
$$

约束：
- 幸存的银行家的获得净值：
$$
n_{t}=\left(Z_{t}+Q_{t}\right) k_{t-1}^{b}-R_{t} d_{t-1}
\tag{11}
$$
- 银行家融资约束：

$$
Q_{t} k_{t}^{b}=d_{t}+n_{t}
\tag{14}
$$