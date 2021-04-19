[TOC]





# Shadow banking and financial regulation: A small-scale DSGE perspective

## Metadata

* Item Type: [[Article]]
* Authors: [[Patrick Fève]], [[Alban Moura]], [[Olivier Pierrard]]
* Date: [[04/2019]]
* Date Added: [[2021-03-08]]
* URL: [10.1016/j.jedc.2019.02.001](10.1016/j.jedc.2019.02.001)
* DOI: [10.1016/j.jedc.2019.02.001](https://doi.org/10.1016/j.jedc.2019.02.001)
* Cite key: Feve2019
* Topics: [[【_Temp_】]], [[影子银行DSGE]], [[影子银行]], [[国际金融监管]], [[审慎监管]], [[DSGE]]
  , #zotero, #literature-notes, #reference
* PDF Attachments
  - [Fève_Moura et al_2019_Shadow banking and financial regulation - A small-scale DSGE perspective.pdf](zotero://open-pdf/library/items/I77VVVLQ)

## Abstract

This paper estimates a small-scale DSGE model of the US economy with interacting traditional and shadow banks. We ﬁnd that shadow banks amplify the transmission of structural shocks by helping escape constraints from traditional intermediaries. We show how this leakage toward shadow entities reduces the ability of macro-prudential policies targeting traditional credit to reduce economic volatility. A counterfactual experiment suggests that a countercyclical capital buffer, if applied only to traditional banks, would have in fact ampliﬁed the boom-bust cycle associated with the ﬁnancial crisis of 2007-2008. On the other hand, a broader regulation scheme targeting both traditional and shadow credit would have helped stabilize the economy.


##  Zotero links

* [Local library](zotero://select/items/1_RP7B3PPP)
* [Cloud library](http://zotero.org/users/6240833/items/RP7B3PPP)







## 模型



#### 定义

一些变量定义：

GDP：
$$
y_{t} \triangleq c_{t}+i_{t}
$$
影子银行信贷占银行信贷股份比例：
$$
\text { share }_{t} \triangleq \frac{s_{t}}{l_{t}+s_{t}}
$$
传统银行杠杆率：
$$
\text { leverage }_{t} \triangleq \frac{q_{t} l_{t}}{n_{t}}
$$
贷款与储蓄利差：
$$
\text { spread }_{t} \triangleq \frac{r_{t}^{k}+(1-\delta) q_{t}}{q_{t-1}}-\left(1+r_{t-1}^{d}\right)
$$


#### 传统银行部门

资产负债表
$$
q_{t} l_{t}+a b s_{t}=n_{t}+d_{t}
$$
其中，

$q_{t} l_{t}$：长期资产价格与数量乘积；

$a b s_{t}$：ABS资产；

$n_{t}$：权益；

$d_{t}$：居民储蓄；



银行资金运行中，存在如下摩擦性质的成本：



- 资产替代成本：

假设ABS流动性优于长期资产，因此资产间替代调整成本：
$$
\Gamma\left(\frac{a b s_{t}}{q_{t} l_{t}}\right)=\frac{\gamma}{2}\left(\frac{a b s_{t}}{q_{t} l_{t}}-\frac{\overline{a b s}}{\bar{q}_{t} \bar{l}}\right)^{2}
$$
这里设定$\bar{q}_{t}=1$。



- 监管成本：

对于传统银行，由于这里假设ABS暂时不受监管，即资本充足率要求$\bar{\eta}$对其不起作用。

为了计算监管成本，定义银行过剩资产部分$x_t$：
$$
x_{t}:=n_{t}-\overbrace{\bar{\eta} q_{t} l_{t}}^{长期资产\\受监管部分}
$$


因为上式约束式不一定满足约束，因此在实际处理有一定困难以计算，因此改成如下式子：
$$
\Theta\left(x_{t}\right)=-\theta_{1} \ln \left(1+\theta_{2} x_{t}\right)
$$
满足性质：

with $\theta_{1}, \theta_{2} \geq 0$ and $\bar{x}=0$ in steady state. This specification implies that $\Theta(0)=0, \Theta^{\prime}(0)=$
$-\theta_{1} \theta_{2} \leq 0$ and $\Theta^{\prime \prime}(0)=\theta_{1} \theta_{2}^{2} \geq 0$, so that capital costs are decreasing and convex in $x_{t}$ around
the steady state.



- 贷款监测成本：

  每单位提供贷款需要付出监测成本$\epsilon_{t}^{l}$
  $$
  \left(1+\epsilon_{t}^{l}\right) q_{t} l_{t}
  $$



综上，可得银行部门利润函数：
$$
\begin{aligned}
\pi_{t}^{b}=&\left[r_{t}^{k}+(1-\delta) q_{t}\right] l_{t-1}+\left(1+r_{t-1}^{a}\right) a b s_{t-1}+d_{t} \\
&-\Gamma\left[a b s_{t} /\left(q_{t} l_{t}\right)\right]-\Theta\left(x_{t}\right)-\left(1+r_{t-1}^{d}\right) d_{t-1}-\left(1+\epsilon_{t}^{l}\right) q_{t} l_{t}-a b s_{t}
\end{aligned}
\tag{1}
$$
其中，

$\delta$：资产折旧率；



其中，贷款审查成本定义为AR(1)过程：
$$
\epsilon_{t}^{l}=\rho_{l} \epsilon_{t-1}^{l}+\sigma_{l} u_{l, t}
$$




最大化银行部门利润函数，以储蓄$d_t$、贷款$l_t$、ABS资产$abs_t$，可得一阶条件：
$$
\begin{aligned}
1+\Theta_{t}^{\prime} &=E_{t} \Lambda_{t, t+1}\left(1+r_{t}^{d}\right) \\ 
\epsilon_{t}^{l}-\bar{\eta} \Theta_{t}^{\prime}-\Gamma_{t}^{\prime} \frac{a b s_{t}}{\left(q_{t} l_{t}\right)^{2}} &=E_{t} \Lambda_{t, t+1}\left[\frac{(1-\delta) q_{t+1}+r_{t+1}^{k}}{q_{t}}-\left(1+r_{t}^{d}\right)\right] \\
\Gamma_{t}^{\prime} \frac{1}{q_{t} l_{t}} &=E_{t} \Lambda_{t, t+1}\left(r_{t}^{a}-r_{t}^{d}\right)
\end{aligned}
\tag{2}
$$
其中，

$\Lambda_{t,t+1}$：家庭跨期折现因子；



这些条件都有简单的解释：
第一种是平衡通过银行资本 存款发行负债的边际成本；
第二种情况表明，贷款利率和存款利率之间的利差涵盖与传统贷款有关的所有上述三种成本费用（即贷款监测、资产组合替代、监管）；
第三种情况表明，ABS回报与存款利率之间的利差只需要支付投资组合成本，因为ABS持有的资产既没有监控成本，也没有监管成本。该条件是我们模型中传统银行和影子银行之间互动的关键；

上述第三个一阶条件(2)可得稳态：
$$
\frac{\gamma}{\bar{l}}\left(\overline{\frac{a b s_{t}}{q_{t} l_{t}}}\right)=\bar{\Lambda}\left(\hat{r}_{t}^{a}-\hat{r}_{t}^{d}\right)
\tag{3}
$$
接下来，引入影子wedge用以解释影子银行违约冲击。外生假设当影子银行违约率为$\epsilon^a_t$，服从AR(1)随机过程$\epsilon_{t}^{a}=\rho_{a} \epsilon_{t-1}^{a}+\sigma_{a} u_{a, t}$，with $\rho_{a} \in(0,1), \sigma_{a}>0$, and $u_{a, t} \sim i . i . d . N(0,1)$。如果违约，则赔偿传统银行$t_t:=\epsilon_{t}^{a}\left(1+r_{t-1}^{a}\right) a b s_{t-1}$。

则(1)变成
$$
\begin{aligned}
\pi_{t}^{b}=&\left[r_{t}^{k}+(1-\delta) q_{t}\right] l_{t-1}+\color{red}{\left(1-\epsilon_{t}^{a}\right)}\left(1+r_{t-1}^{a}\right) a b s_{t-1}+d_{t}+\color{red}{t_{t}} \\
&-\Gamma\left[a b s_{t} /\left(q_{t} l_{t}\right)\right]-\Theta\left(x_{t}\right)-\left(1+r_{t-1}^{d}\right) d_{t-1}-\left(1+\epsilon_{t}^{l}\right) q_{t} l_{t}-a b s_{t}
\end{aligned}
$$
(2)(3)变成
$$
\Gamma_{t}^{\prime} \frac{1}{q_{t} l_{t}}=E_{t} \Lambda_{t, t+1}\left[\left(1-\epsilon_{t+1}^{a}\right)\left(1+r_{t}^{a}\right)-\left(1+r_{t}^{d}\right)\right]
$$

$$
\frac{\gamma}{\bar{l}}\left(\frac{a b s_{t}}{q_{t} l_{t}}\right)+E_{t} \epsilon_{t+1}^{a}=\bar{\Lambda}\left(\hat{r}_{t}^{a}-\hat{r}_{t}^{d}\right)
\tag{4}
$$







#### 影子银行部门

影子银行建模采用OLG模型结构，生命周期2 。时期1进入市场，发行ABS给非金融机构；时期2获利，还款，退出市场。



##### 假定：

- 影子银行进入时无资产；

- 影子银行退出时期望下一期收益为0：
  $$
  E_{t} \Lambda_{t, t+1} \pi_{t+1}^{s}=0
  \tag{SB1}
  $$
  其中，

  $\Lambda_{t,t+1}$：家庭跨期折现因子；

  $\pi_{t+1}^{s}$：影子银行利润；

- 影子银行存在违约可能性。引入影子wedge用以解释影子银行违约冲击。外生假设当影子银行违约率为$\epsilon^a_t$，服从AR(1)随机过程$\epsilon_{t}^{a}=\rho_{a} \epsilon_{t-1}^{a}+\sigma_{a} u_{a, t}$，with $\rho_{a} \in(0,1), \sigma_{a}>0$, and $u_{a, t} \sim i . i . d . N(0,1)$。如果违约，则赔偿传统银行$t_t:=\epsilon_{t}^{a}\left(1+r_{t-1}^{a}\right) a b s_{t-1}$。



##### 行为：

时期$t=1$，新影子银行进入市场，发行ABS给非金融机构；存在单位发行成本$0<\bar{a}<1$。其资产负债表：
$$
q_{t} s_{t}=(1-\bar{a}) a b s_{t}
\tag{SB2}
$$
其中，左侧是发行的资产，以股份$s_t$和价格$q_t$，右侧是负债，其中扣除了发行成本部分；

时期$t=2$，影子银行得到利润：
$$
\pi_{t}^{ s }=\left[r_{t}^{k}+(1-\delta) q_{t}\right] s_{t-1}-\left(1-\epsilon_{t}^{a}\right)\left(1+r_{t-1}^{a}\right) a b s_{t-1}-t_{t}
\tag{SB3}
$$
然后退出市场。

将(SB2)(SB3)代入(SB1)，整理后可得：
$$
(1-\bar{a}) E_{t} \Lambda_{t, t+1} \frac{r_{t+1}^{k}+(1-\delta) q_{t+1}}{q_{t}}=E_{t} \Lambda_{t, t+1}\left[\left(1-\epsilon_{t+1}^{a}\right)\left(1+r_{t}^{a}\right)+\frac{t_{t+1}}{a b s_{t}}\right]
\tag{SB4}
$$
将$t_{t}:=\epsilon_{t}^{a}\left(1+r_{t-1}^{a}\right) a b s_{t-1}$代入(SB4)可得：
$$
(1-\bar{a}) E_{t} \Lambda_{t, t+1} \frac{r_{t+1}^{k}+(1-\delta) q_{t+1}}{q_{t}}=\left(1+r_{t}^{a}\right) E_{t} \Lambda_{t, t+1}
\tag{5}
$$
条件(5)只是将额外发行 ABS 的预期回报与其边际成本等同起来。根据巴塞尔协议I，影子银行不受该模式的监管。





#### 闭合其模型







#### 方法之于计算模型

采用标准线性化技术，贝叶斯估计方法。



![image-20210416164238796](Feve_Moura%20et%20al_2019_Shadow%20banking%20and%20financial%20regulation%20-%20A%20small-scale%20DSGE%20perspective.assets/image-20210416164238796.png)









| Parameter Description | Parameter Description            | Prior distribution | Posterior distribution | Prior distribution | Posterior distribution | Posterior distribution |
| --------------------- | -------------------------------- | ------------------ | ---------------------- | ------------------ | ---------------------- | ---------------------- |
|                       |                                  | Distribution       | Mean                   | SD                 | Mode                   | [5%, 95%]              |
| φ                     | Labor habits                     | Beta               | 0.60                   | 0.15               | 0.65                   | [ 0.60, 0.69]          |
| γ                     | Portfolio adjustment cost        | Gamma              | 0.20                   | 0.10               | 0.17                   | [ 0.15, 0.19]          |
| $\theta_2$            | Convexity of excess capital cost | Gamma              | 0.20                   | 0.10               | 0.11                   | [ 0.09, 0.14]          |
| $\rho_z$              | AR technology shock              | Beta               | 0.60                   | 0.20               | 0.95                   | [ 0.95, 0.96]          |
| $\rho_i$              | AR investment shock              | Beta               | 0.60                   | 0.20               | 0.24                   | [ 0.17, 0.31]          |
| $\rho_m$              | AR labor wedge shock             | Beta               | 0.60                   | 0.20               | 0.71                   | [ 0.65, 0.77]          |
| $\rho_l$              | AR monitoring cost shock         | Beta               | 0.60                   | 0.20               | 0.96                   | [ 0.95, 0.97]          |
| $\rho_a$              | AR shadow wedge shock            | Beta               | 0.60                   | 0.20               | 0.99                   | [ 0.98, 0.99]          |
| $\rho_d$              | AR deposit preference shock      | Beta               | 0.60                   | 0.20               | 0.89                   | [ 0.86, 0.92]          |
| 100$\sigma_z$         | SD technology shock              | Inv. Gamma         | 1.00                   | 3.00               | 0.60                   | [ 0.56, 0.65]          |
| 1000$\sigma_i$        | SD investment shock              | Inv. Gamma         | 1.00                   | 3.00               | 2.39                   | [ 2.19, 2.62]          |
| 100$\sigma_m$         | SD labor wedge shock             | Inv. Gamma         | 1.00                   | 3.00               | 1.26                   | [ 1.15, 1.39]          |
| 10000$\sigma_l$       | SD monitoring cost shock         | Inv. Gamma         | 1.00                   | 3.00               | 4.05                   | [ 3.71, 4.56]          |
| 10000$\sigma_a$       | SD shadow wedge shock            | Inv. Gamma         | 1.00                   | 3.00               | 4.48                   | [ 4.08, 5.12]          |
| 100$\sigma_d$         | SD deposit preference shock      | Inv. Gamma         | 1.00                   | 3.00               | 1.46                   | [ 1.28, 1.70]          |

Notes. The posterior distribution is constructed from the random-walk Metropolis-Hastings algorithm with a single chain of 250,000 draws, after a burn-in period of 250,000 draws.



![image-20210416165440849](Feve_Moura%20et%20al_2019_Shadow%20banking%20and%20financial%20regulation%20-%20A%20small-scale%20DSGE%20perspective.assets/image-20210416165440849.png)



![image-20210416165422349](Feve_Moura%20et%20al_2019_Shadow%20banking%20and%20financial%20regulation%20-%20A%20small-scale%20DSGE%20perspective.assets/image-20210416165422349.png)

