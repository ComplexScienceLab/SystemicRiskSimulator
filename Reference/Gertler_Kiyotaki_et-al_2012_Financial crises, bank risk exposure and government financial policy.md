



[toc]





> 本笔记结合以下两篇文章：
>
> Gertler M, Kiyotaki N, Queralto A, 2012. Financial Crises, Bank Risk Exposure and Government Financial Policy[J]. Journal of Monetary Economics, 59: S17–S34. DOI:[10.1016/j.jmoneco.2012.11.007](https://doi.org/10.1016/j.jmoneco.2012.11.007).
>
> 及其2010年的工作论文。
>
> 笔记中的公式编号以2010年的工作论文为准。



# Financial crises, bank risk exposure and government financial policy

## Metadata

* Type: [[Article]]
* Authors: [[Mark Gertler]], [[Nobuhiro Kiyotaki]], [[Albert Queralto]]
* Date: [[12/2012]]
* Date added: [[2020-08-14]]
* Publication: [[Journal of Monetary Economics]]
* DOI: [10.1016/j.jmoneco.2012.11.007](10.1016/j.jmoneco.2012.11.007)
* Cite key: Gertler_2012_FinancialCrisesBankRiskExposureAndGovernmentFinancialPolicya
* Topics: [[【_Temp_】]]
* Related: 
* Tags: [[Zotero Import]]
* Zotero links: [Local library](zotero://select/items/1_PHWCFETK)
* PDF Attachments: [Gertler_Kiyotaki et al_2012_Financial crises, bank risk exposure and government financial policy.pdf](zotero://open-pdf/library/items/ZAU993X5)

### Abstract

 A macroeconomic model with ﬁnancial intermediation is developed in which the intermediaries (banks) can issue outside equity as well as short term debt. This makes bank risk exposure an endogenous choice. The goal is to have a model that can not only capture a crisis when banks are highly vulnerable to risk, but can also account for why banks adopt such a risky balance sheet in the ﬁrst place. We use the model to assess quantitatively how perceptions of fundamental risk and of government credit policy in a crisis affect the vulnerability of the ﬁnancial system ex ante. We also study the effects of macro-prudential policies designed to offset the incentives for risk-taking.

## 摘要

建立了具有金融中介作用的宏观经济模型，其中中介（银行）可以发行外部股本和短期债务，这使得银行风险敞口成为一种内生的选择，目标是建立一个不仅可以在发生危机时捕获危机的模型，其银行极易受到风险的影响，而且也可以首先解释为什么银行采用这样的风险资产负债表。我们使用该模型定量评估危机中对基本风险和政府信贷政策的看法如何影响银行的脆弱性。我们还研究了旨在设定冒险动机的宏观审慎政策的效果。



## 工作

- 使用了一个相关的模型来阐明，对金融中介的扰动能够引致经济实体面的危机。该模型中的金融摩擦和扰动源是银行可以因为私人的或者非生产性的动机而挪用它们从银行间市场获得的资金。这会带来资产负债表上的约束，并进而带来信用提供上的约束，从而限制投资支出，影响到实体面。中央银行的作用是通过向银行注入流动性或者通过直接向私人部门注入资金来减轻此类金融约束。
- 金融危机之后，研究了包含金融中介的DSGE模型，集中研究流动性风险，以及政府的政策干预、对资产回报风险的认知等是如何影响金融中介对风险披露的程度的。








## 缺点  

- 该理论可能存在的一个不足是,它假设企业能够将自己的风险转移到银行,因为不存在违约风险,而且银行不对这些贷款收取风险溢价,虽然这些风险是来自于企业权益价值的波动。  

- 没有考虑违约。

- 假定让工人和银行家外生随机流动以限制其银行家之行为。是否不符合现实？





## 模型  

> - 模型中,银行面临的信用风险,来自于银行向企业发放贷款时作为交换而持有的企业权益。 

### 模型基础设定

由**资本折旧率**$\delta$影响的**资本股票**：

$$
S_{t}=(1-\delta) K_{t}+I_{t}
\tag{2}
$$

由**资本质量冲击**$\psi_{t+1}$影响的**资本量**：

$$
K_{t+1}=\psi_{t+1} S_{t}
\tag{3}
$$

由(1)(2)可得

$$
K_{t+1}=\psi_{t+1} (1-\delta) K_{t}+I_{t}
$$





### 家庭

##### 最优化问题：

最大化预期跨期加总效用函数，通过控制**消费**$C_t$、**劳动力供给**$L_t$、无风险债券$D_{ht}$、**外部股本数量**$\bar{e}_t$
$$
\max _{C_{t}, L_{t}, D_{h t}, \bar{e}_{t}} E_{t} \sum_{\tau=t}^{\infty} \beta^{\tau-t} \frac{1}{1-\gamma}\left(C_{\tau}-h C_{\tau-1}-\frac{\chi}{1+\varphi} L_{\tau}^{1+\varphi}\right)^{1-\gamma}
$$
约束条件：

资金流约束
$$
C_{t}+D_{h t}+q_{t} \bar{e}_{t}=W_{t} L_{t}+\Pi_{t}-T_{t}+R_{t} D_{h t-1}+ \underbrace{[\overbrace{Z_{t}}^{单位银行资产之回报量} +\overbrace{(1-\delta) q_{t}}^{外部股权之价格，\\包含相对于上一期折价的} ] \overbrace{\psi_{t}}^{资本质量冲击}  \bar{e}_{t-1}}_{外部股权之收益}
\tag{6}
$$
计算F.O.C.

可以得到：
$$
\begin{array}{l}
E_{t} u_{C t} W_{t}=\chi L_{t}^{\varphi}\left(C_{t}-h C_{t-1}-\frac{\chi}{1+\varphi} L_{t}^{1+\varphi}\right)^{-\gamma} \\
E_{t}\left(\Lambda_{t, t+1}\right) R_{t+1}=1 \\
E_{t}\left(\Lambda_{t, t+1} R_{e t+1}\right)=1
\end{array}
\tag{7,8,9}
$$
其中，
$$
\begin{array}{l}
u_{C t} \equiv\left(C_{t}-h C_{t-1}-\frac{\chi}{1+\varphi} L_{t}^{1+\varphi}\right)^{-\gamma}-\beta h\left(C_{t+1}-h C_{t} \frac{\chi}{1+\varphi} L_{t+1}^{1+\varphi}\right)^{-\gamma} \\
\Lambda_{t, \tau} \equiv \beta^{\tau-t} \frac{u_{C \tau}}{u_{C t}}, \\
R_{e t+1}=\frac{\left[Z_{t+1}+(1-\delta) q_{t+1}\right] \psi_{t+1}}{q_{t}}
\end{array}
$$



假定让工人和银行家外生随机流动以限制其银行家之行为。

> 是否不符合现实？


### 商品生产商







### 资本品生产商







### 银行部门

#### 假设

- 假设无摩擦之于资金流动于银行与生产商之间；



#### 描述

银行资产负债：
$$
\overbrace{Q_{t} s_{t}}^{银行提供融资部分\\（银行资产）} = \overbrace{n_{t}}^{银行净值部分\\（内部权益）} +\overbrace{q_{t} e_{t}}^{银行外部权益从居民\\（外部权益）} + \overbrace{d_{t}}^{接受居民储蓄部分\\（银行负债）}
\tag{13}
$$

For an individual bank, the flow-of-funds constraint implies the value of loans funded within a given period, $Q_{t} s_{t}$, must equal the sum of 银行净资产 ==bank net worth== $n_{t}$, and funds raised from households, consisting of outside equity $q_{t} e_{t}$ and deposits $d_{t}$ :



由于考虑到跨期的资金流变动，可以得到==银行净值与其他变量的关系==：
$$
n_{t}=\left[Z_{t}+(1-\delta) Q_{t}\right] \psi_{t} s_{t-1}-\left[Z_{t}+(1-\delta) q_{t}\right] \psi_{t} e_{t-1}-R_{t} d_{t-1}
$$


定义**银行目标价值**：
$$
V_{t} := E_{t}\left[\sum_{\tau=t+1}^{\infty}(1-\sigma) \sigma^{\tau-t-1} \Lambda_{t, \tau} n_{\tau}\right]
$$
定义**银行外部股本占银行总资产之比**：
$$
x_{t} := \frac{\overbrace{q_{t} e_{t}}^{银行外部权益从居民}}{ \underbrace{Q_{t} s_{t}}_{银行提供部分}}
$$

商业银行存在==道德风险==。

体现为：假定**银行融资后有动机私自转移资产$Q_ts_t$之部分比例**$\Theta$。该转移比例$\Theta$与$x$可能存在这样的凸函数关系：
$$
\Theta\left(x_{t}\right) := \theta\left(1+\varepsilon x_{t}+\frac{\kappa}{2} x_{t}^{2}\right)
$$
大概的==经济含义==是，银行外部股本占总资产比重越大，银行越有动机私自转移更多资产。



##### 最优化问题：

最大化商业银行的目标价值(23)：
$$
V_{t}\left(s_{t}, e_{t}, d_{t}\right)=\mu_{s t} Q_{t} s_{t}+\mu_{e t} q_{t} e_{t}+\nu_{t} n_{t}
\tag{23}
$$


##### 约束条件：

激励相容约束(18)：
$$
V_{t} \geq \Theta\left(x_{t}\right) Q_{t} s_{t}
\tag{18}
$$




##### 求解过程：

最优化问题(23)(18)可写成Bellman方程形式(19)(20)
$$
\begin{aligned}
& V_{t-1}\left(s_{t-1}, e_{t-1}, d_{t-1}\right) \\
=& E_{t-1} \Lambda_{t-1, t}\left\{(1-\sigma) n_{t}+\sigma \operatorname{Max}_{s_{t}, e_{t} \cdot d_{t}}\left[V_{t}\left(s_{t}, e_{t}, d_{t}\right)\right]\right\}
\end{aligned}
\tag{19,20}
$$


用==待定系数法==求解上述方程：

待定系数法中，==假定==线性形式的模型(21)：
$$
V_{t}\left(s_{t}, e_{t}, d_{t}\right)=\nu_{s t} s_{t}-\nu_{e t} e_{t}-\nu_{t} d_{t}
\tag{21}
$$
合并(13)(21)可得(23)。



定义变量：**预期利差空间**（起作用以两种权重参数变量的替换效应）

**预期利差空间之于外部融资（银行资产的超额价值）**
$$
\mu_{s t} := \frac{\nu_{s t}}{Q_{t}}-\nu_{t}
$$
**预期利差空间之于外部股本（银行外部股本的超额价值）**
$$
\mu_{e t} := \nu_{t}-\frac{\nu_{e t}}{q_{t}}
$$
合并(13)(21)可得(23)
$$
V_{t}\left(s_{t}, e_{t}, d_{t}\right)=\mu_{s t} Q_{t} s_{t}+\mu_{e t} q_{t} e_{t}+\nu_{t} n_{t}
\tag{23}
$$




由$x_t$、(23)代入(19)，消除$e_t$，然后改写最优化问题(23)为新的形式。再对**影子银行对商业银行资金需求率**$x_t$、企业融资量$s_t$、相容激励约束价值权重（拉格朗日乘子）$\lambda_t$求F.O.C. ，整理一番后得到：
$$
\begin{array}{c}
\left(1+\lambda_{t}\right) \mu_{e t}=\lambda_{t} \theta\left(\varepsilon+\kappa x_{t}\right) \\
\left(1+\lambda_{t}\right)\left(\mu_{s t}+x_{t} \mu_{e t}\right)=\lambda_{t} \theta\left(1+\varepsilon x_{t}+\frac{\kappa}{2} x_{t}^{2}\right) \\
\left[\mu_{s t}+x_{t} \mu_{e t}\right] Q_{t} s_{t}+\nu_{t} n_{t}=\Theta\left(x_{t}\right) Q_{t} s_{t}
\end{array}
\tag{24,25,26}
$$



###### 分析经济学含义之于上述式子：

(24)左边，$\mu_{et}$是银行用外部股本融资$\frac{\nu_{e t}}{q_{t}}$代替短期债务$\nu_{t}$对银行的边际收益，右边是银行私自转移资产份额的边际量$\theta\left(\varepsilon+\kappa x_{t}\right)$乘以相容激励约束价值$\lambda_t$。

(25)可知，如果$\lambda_t$是0，那么$\left(\mu_{s t}+x_{t} \mu_{e t}\right)$也是0，反之只有当$\left(\mu_{s t}+x_{t} \mu_{e t}\right)>0$，那么$\lambda_t>0$，激励相容约束才能起作用。

(26)可以由(23)变换得来。





###### 继续计算：

结合(24)(25)然后求得$x_t$与$\left(\frac{\mu_{e t}}{\mu_{s t}}\right)$关系式：


$$
\begin{aligned}
x_{t} &=-\left(\frac{\mu_{e t}}{\mu_{s t}}\right)^{-1}+\sqrt{\left(\frac{\mu_{e t}}{\mu_{s t}}\right)^{-2}+\frac{2}{\kappa}\left(1-\varepsilon\left(\frac{\mu_{e t}}{\mu_{s t}}\right)^{-1}\right)} \\
& := x\left(\frac{\mu_{e t}}{\mu_{s t}}\right), \text { where } x^{\prime}>0 \text { given } \kappa>\frac{1}{2} \varepsilon^{2}
\end{aligned}
$$


变换(26)可得：

$$
Q_{t} s_{t}=\frac{\nu_{t}}{\Theta\left(x_{t}\right)-\left(\mu_{s t}+x_{t} \mu_{e t}\right)} n_{t}
\tag{26*}
$$




> 回顾：
>
> **银行外部权益占银行总资产之比**：
> $$
> x_{t} := \frac{q_{t} e_{t}}{Q_{t} s_{t}}
> $$
> 
> 激励相容约束(18)：
> 
> $$
> V_{t} \geq \Theta\left(x_{t}\right) Q_{t} s_{t}
> \tag{18}
> $$
> 
> 价值函数(23)：
> 
> $$
> V_{t}\left(s_{t}, e_{t}, d_{t}\right)=\mu_{s t} Q_{t} s_{t}+\mu_{e t} q_{t} e_{t}+\nu_{t} n_{t}
> \tag{23}
> $$
>
> 



###### 分析经济含义：

首先银行希望净值$n_{t}$越大越好，但是银行总是有动机想要谋取私利，希望$\Theta\left(x_{t}\right)$越大越好。但是，如果$\Theta\left(x_{t}\right)$越大，那么被私自转移的$\Theta\left(x_{t}\right) Q_{t} s_{t}$就会越大，那么根据(23)，$V_t$也会越小，相应的$n_t$也可能越小。最终导致约束(18)起作用，等号成立。

因此，根据(26*)，定义**比率之于银行资产比其净值，当满足最大化条件时，用以满足相容激励约束条件**$\phi_{t}$：
$$
\phi_{t} := \frac{\overbrace{Q_{t} s_{t}}^{银行资产}}{\underbrace{n_{t}}_{银行净值}}
$$
那么，由上述定义式子、(26*)，可以得到$\phi_{t}$：
$$
\phi_{t}=\frac{\overbrace{\nu_{t}}^{成本之于单位净值}}{\underbrace{\Theta\left(x_{t}\right)}_{转移比例} -\underbrace{\left(\mu_{s t}+x_{t} \mu_{e t}\right)}_{银行超额价值} }
\tag{29}
$$
于是得到
$$
Q_{t} s_{t} =\phi_{t} n_{t}
\tag{28}
$$
那么观察(28)(29)，我们会发现设计激励相容约束的作用。银行总是有动机想要谋取私利，希望$\Theta\left(x_{t}\right)$越大越好。但是，如果$\Theta\left(x_{t}\right)$越大，那么由(29)可知，$\phi_{t}$越小，那么由(28)可知，在给定$n_t$时，银行能够提供给企业的融资$Q_t s_t$越小，那么由(23)可知，$V_t$越小，如果$V_t$小到(18)等号满足，暨触发了激励相容约束，那么银行就不能继续使得$\Theta_{t}$越大，暨抑制了银行私自转移资本的动机。







###### 继续计算：



> 回顾
>
> Bellman方程形式(19)(20)
> $$
> \begin{aligned}
> & V_{t-1}\left(s_{t-1}, e_{t-1}, d_{t-1}\right) \\
> =& E_{t-1} \Lambda_{t-1, t}\left\{(1-\sigma) n_{t}+\sigma \operatorname{Max}_{s_{t}, e_{t} \cdot d_{t}}\left[V_{t}\left(s_{t}, e_{t}, d_{t}\right)\right]\right\}
> \end{aligned}
> \tag{19,20}
> $$
> 公式(23)
> $$
> V_{t}\left(s_{t}, e_{t}, d_{t}\right)=\mu_{s t} Q_{t} s_{t}+\mu_{e t} q_{t} e_{t}+\nu_{t} n_{t}
> \tag{23}
> $$



- [ ] 代入(23)至Bellman方程(19,20)可得


$$
\nu_{t}=E_{t}\left(\Lambda_{t, t+1} \Omega_{t+1}\right) R_{t+1}
\tag{30}
$$

$$
\mu_{s t}=E_{t}\left[\Lambda_{t, t+1} \Omega_{t+1}\left(R_{k t+1}-R_{t+1}\right)\right]
\tag{31}
$$

$$
\mu_{e t}=E_{t}\left[\Lambda_{t, t+1} \Omega_{t+1}\left(R_{t+1}-R_{e t+1}\right)\right]
\tag{32}
$$

其中，$\Omega_{t+1}$表示影子价值对于一单位银行净值在时期$t+1$：
$$
\Omega_{t+1}:=1-\sigma+\sigma\left[\nu_{t+1}+\phi_{t+1}\left(\mu_{s t+1}+x_{t+1} \mu_{e t+1}\right)\right]
\tag{33}
$$


$$
R_{k t+1}:=\frac{\left[Z_{t+1}+(1-\delta) Q_{t+1}\right] \psi_{t+1}}{Q_{t}}
\tag{34}
$$



> 回顾
>
> 定义变量：**预期利差空间**（起作用以两种权重参数变量的替换效应）
>
> **预期利差空间之于外部融资（银行资产的超额价值）**
> $$
> \mu_{s t} := \frac{\nu_{s t}}{Q_{t}}-\nu_{t}
> $$
> **预期利差空间之于外部股本（银行外部股本的超额价值）**
> $$
> \mu_{e t} := \nu_{t}-\frac{\nu_{e t}}{q_{t}}
> $$

因为在萧条时期，银行难以获得信贷，面临激励约束要比繁荣时期更严格，所以在经济萧条时期增加银行净值$n_t$的边际价值，比在繁荣时期增加银行净值$n_t$，更有边际价值。因为$\Omega_{t+1}$是逆周期的，所以熨平银行资产的超额价值$\mu_{st}$，从而熨平银行价值$V_t$，从而==降低高杠杆==。

对比银行的预期利差空间公式(32)$\mu_{e t}=E_{t}\left[\Lambda_{t, t+1} \Omega_{t+1}\left(R_{t+1}-R_{e t+1}\right)\right]$与家庭预期利差空间公式$E_{t}\left[\Lambda_{t, t+1}\left(R_{t+1}-R_{e t+1}\right)\right]=0$，可以看出由于，则$\Lambda_{t, t+1}$和$\Omega_{t+1}$都是逆周期的，所以$\Lambda_{t, t+1} \Omega_{t+1}$比$\Lambda_{t, t+1}$拟周期性更大，因此公式(32)比家庭预期利差空间公式对冲价值更大，所以预期利差空间之于外部股本是正的，暨$\mu_{e t}=E_{t}\left[\Lambda_{t, t+1} \Omega_{t+1}\left(R_{t+1}-R_{e t+1}\right)\right] \ge 0$。综上，==之所以银行会发行外部股本，以带来超额价值，是因为融资约束实际上使它比家庭更能规避风险。==



###### 加总银行净值

加总的银行证券需求$S_{pt}$和加总的银行部门资本净值
$$
Q_{t} S_{p t}=\phi_{t} N_{t}
\tag{36}
$$


在模型的动态中，银行部门总体净值$N_t$的演化过程扮演了很重要的角色。





假定让工人和银行家外生随机流动以限制其银行家之行为。

现有银行家之加总净值与新进银行家之加总净值存在一些关系：
$$
N_{t}=N_{o t}+N_{y t}
$$
其中，
$$
N_{o t}=\sigma\left\{\left[Z_{t}+(1-\delta) Q_{t}\right] \psi_{t} S_{p t-1}- \overbrace{\left[Z_{t}+(1-\delta) q_{t}\right] \psi_{t} \bar{e}_{t-1}}^{提供外部股权给家庭} - \overbrace{ R_{t} D_{t-1}}^{家庭取出存款}\right\}
\tag{38}
$$


$$
N_{y t}= \overbrace{\xi}^{新晋银行家获取资金比例} \left[Z_{t}+(1-\delta) Q_{t}\right] \psi_{t} S_{p t-1}
\tag{39}
$$

其中，

$\frac{\xi}{1-\delta}$：新晋银行家获取资金比例，其资金来源由家庭部门从现有银行家之资金量抽取一定比例提供；



合并上述式子得
$$
N_{t}=(\sigma+\xi)\left[Z_{t}+(1-\delta) Q_{t}\right] \psi_{t} S_{p t-1}-\sigma\left[Z_{t}+(1-\delta) q_{t}\right] \psi_{t} \bar{e}_{t-1}-\sigma R_{t} D_{t-1}
\tag{40}
$$


观察到资本质量的下降$\psi_t$直接降低了资产和净资产的回报率。此外，银行的杠杆越高，回报之波动对净值的百分比影响就越大。 但是，使用外部股本减少了收益波动对净值的影响。







### 信贷政策：



此前，我们曾描述过如何确定私人中间资产$Q_t S_{pt}$的总价值。我们现在认为，央行愿意为贷款提供便利。这种信贷政策与央行大规模购买高档私人证券相对应，而私人证券是央行在金融危机高峰期试图稳定信贷市场的核心。让$Q _{t} S_{g t}$成为通过央行中间的资产价值，让$Q_{t} S_{t}$成为中间资产的总价值
$$
Q_{t} S_{t}=Q_{t} S_{p t}+Q_{t} S_{g t}
$$


为实施信贷政策，央行向支付无风险利率$R_{t+1}$的家庭发行短期政府债券，然后按市场贷款利率$R_{kt+1}$向非金融企业发放贷款。我们认为，政府干预涉及效率成本：特别是央行信贷消耗的资源为$\Gamma_{t}\left(Q_{t} S_{g t}\right)$，其中$\Gamma_t$随着政府资产中间数量上增加而递增。这种量级损失可能反映了融资的行政成本，或者央行确定首选私营部门投资的成本。另一方面，政府总是偿还债务：因此，与私人金融机构的情况不同，没有机构冲突可以阻止中央银行从家庭获得资金。因此，假设中央银行愿意为中间资产的一小部分$\zeta_t$提供资金：
$$
Q_{t} S_{t}=Q_{t} S_{p t}+Q_{t} S_{g t}
$$
央行融资占比为外生的时变变量：
$$
S_{g t}=\zeta_{t} S_{t}
$$
正如我们将表明的，通过在金融危机爆发后增加$\zeta_t$，央行可以降低超额回报$(R_{kt+1}-R_{t+1})$。这样，信贷政策可以降低资本成本，从而刺激投资。后来，我们描述了央行如何设定$\zeta_t$以应对金融危机。

政府和央行应满足预算约束：
$$
G_{t}=G+ \overbrace{\Gamma_{t}\left(Q_{t} S_{g t}\right)}^{银行监管成本}
$$
政府预算约束：


$$
G_{t}+Q_{t} S_{g t}+R_{t} D_{g t-1}=T_{t}+ \color{brown}{\left[Z_{t}+(1-\delta) Q_{t}\right] \psi_{t}} S_{g t-1}+D_{g t}
\tag{44}
$$
其中，

$$
\color{brown}{ \overbrace{\left[\underbrace{Z_{t}}_{单位银行资产之回报量} + \underbrace{(1-\delta) Q_{t}}_{外部股本之价格，\\包含相对于上一期折价的} \right] \underbrace{\psi_{t}}_{资本质量冲击}}^{外部股本之单位收益} S_{g t-1}}
$$
表示外部股本之收益。





### 均衡条件



为了闭合模型，要求以下几方面出清：证券市场、外部权益、存款、劳动力。





##### 证券市场均衡出清：



> 回顾：
>
> 公式(2)，由**资本折旧率**$\delta$影响的**资本股票**：
> $$
> S_{t}=(1-\delta) K_{t}+I_{t}
> \tag{2}
> $$
>
> 加总的银行证券需求$S_{pt}$和加总的银行部门资本净值
> $$
> Q_{t} S_{p t}=\phi_{t} N_{t}
> \tag{36}
> $$
>
> 激励相容约束$\phi_{t}$：
> $$
> \phi_{t}=\frac{\overbrace{\nu_{t}}^{成本之于单位净值}}{\underbrace{\Theta\left(x_{t}\right)}_{转移比例} -\underbrace{\left(\mu_{s t}+x_{t} \mu_{e t}\right)}_{银行超额价值} }
> \tag{29}
> $$





证券总供给$S_t$等于证券总需求$S_{pt}$：
$$
S_t=S_{pt}
$$
由证券总供给(2)、证券总需求(36)(29)可得：




$$
Q_{t}\left(S_{t}-S_{g t}\right)=\frac{v_{t}}{\theta\left(1+\varepsilon x_{t}+x_{t}^{2}\right)-\left(\mu_{s t}+x_{t} \mu_{e t}\right)} N_{t}
\tag{45}
$$

##### 外部股本出清：

家庭外部股本需求$\bar{e}_t$等于银行外部股本供给$e_t$：
$$
\bar{e}_t = e_t
$$
整理后可得：
$$
q_{t} \bar{e}_{t}=x_{t} \cdot Q_{t} S_{p t}
\tag{46}
$$

##### 存款（无风险债券）出清：

> 回顾：
>
> 定义**银行外部股本占银行总资产之比**：
> $$
> x_{t} := \frac{\overbrace{q_{t} e_{t}}^{银行外部权益从居民}}{ \underbrace{Q_{t} s_{t}}_{银行提供部分}}
> $$
>
> 银行资产负债：
> $$
> \overbrace{Q_{t} s_{t}}^{银行提供融资部分\\（银行资产）} = \overbrace{n_{t}}^{银行净值部分\\（内部权益）} +\overbrace{q_{t} e_{t}}^{银行外部权益从居民\\（外部权益）} + \overbrace{d_{t}}^{接受居民储蓄部分\\（银行负债）}
> \tag{13}
> $$
>
> 
>
> 由(13)整理可得
$$
D_{t}=D_{h t}-D_{g t}=\left(1-x_{t}\right) Q_{t} S_{p t}-N_{t}
\tag{47}
$$
##### 劳动力均衡出清：

(10)代入(7)整理可得
$$
(1-\alpha) \frac{Y_{t}}{L_{t}} \cdot E_{t}\left[\frac{u_{C t}}{\left(C_{t}-h C_{t-1}-\frac{\chi}{1+\varphi} L_{t}^{1+\varphi}\right)^{-\gamma}}\right]=\chi L_{t}^{\varphi}
\tag{48}
$$





