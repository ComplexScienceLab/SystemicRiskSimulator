# A model of unconventional monetary policy

![[Gertler2011-zotero#Metadata]]

Other files:

* Mdnotes File Name: [[Gertler2011]]
* Metadata File Name: [[Gertler2011-zotero]]

##  Zotero links

* [Local library](zotero://select/items/1_LG2NB8NM)
* [Cloud library](http://zotero.org/users/6240833/items/LG2NB8NM)

## Notes

- 

# A model of unconventional monetary policy

## Metadata

* Item Type: [[Article]]
* Authors: [[Mark Gertler]], [[Peter Karadi]]
* Date: [[1/2011]]
* Date Added: [[2020-11-13]]
* URL: [https://linkinghub.elsevier.com/retrieve/pii/S0304393210001261](https://linkinghub.elsevier.com/retrieve/pii/S0304393210001261)
* DOI: [10.1016/j.jmoneco.2010.10.004](https://doi.org/10.1016/j.jmoneco.2010.10.004)
* Cite key: Gertler2011
* Topics: [[货币政策]]
* Related: [[MaYong2013]]
* PDF Attachments
  - [Gertler_Karadi_2011_A model of unconventional monetary policy.pdf](zotero://open-pdf/library/items/8V8WIV8V)

## Abstract

We develop a quantitative monetary DSGE model with ﬁnancial intermediaries that face endogenously determined balance sheet constraints. We then use the model to evaluate the eﬀects of the central bank using unconventional monetary policy to combat a simulated ﬁnancial crisis. We interpret unconventional monetary policy as expanding central bank credit intermediation to oﬀset a disruption of private ﬁnancial intermediation. The primary advantage the central bank has over private intermediaries is that it can elastically obtain funds by issuing riskless government debt. During the crisis, the balance sheet constraints on private intermediaries tighten, raising the net beneﬁts from central bank intermediation. We ﬁnd that the welfare beneﬁts from this policy may be substantial if the relative eﬃciency costs of central bank intermediation are modest. Further, in a ﬁnancial crisis there are beneﬁts from credit policy even if the nominal interest has not reached the zero lower bound. In the event the zero lower bound constraint is binding, however, the next beneﬁts from credit policy may be signiﬁcantly enhanced.


##  Zotero links

* [Local library](zotero://select/items/1_LG2NB8NM)
* [Cloud library](http://zotero.org/users/6240833/items/LG2NB8NM)

## Highlights and Annotations

- [[Gertler2011 - 摘要]]

* Mdnotes File Name: [[Gertler2011]]

# 摘要

我们开发了一种金融金融中介机构的定量货币DSGE模型，该模型面临着内生确定的资产负债表约束。然后，我们使用该模型评估央行使用非常规货币政策应对模拟金融危机的影响。我们将非常规货币政策解释为扩大中央银行信贷中介以抵消私人金融中介的破坏。在我们的框架内，中央银行在放贷方面没有私人中介有效，但是它的优点是能够通过发行无风险的政府债务来灵活地获得资金。与私人中介不同，它不受资产负债表的约束。在危机期间，私人中介机构的资产负债表约束变紧，从而增加了央行中介机构的净收益。即使对名义利率的零下限约束没有约束力，这些收益也可能是可观的。如果此约束具有约束力，则这些净收益可能会得到显着增强。



## 特点

考虑了道德激励约束以对银行家。



## 模型



#### 家庭部门

提供劳动力、消费、储蓄。



#### 金融部门

金融部门（金融中介、银行之类的金融部门）提供贷款其从储户来，至非金融公司。持有长期资产和基金



银行吸收家庭存款，从而有资产负债表：
$$
Q_{t} S_{j t}=N_{j t}+B_{j t+1}
$$
其中，$Q$是非金融公司债权价格，$S$是非金融公司债权数量，$N$是财富净值，$B$是获得的存款，从家庭。

对于下一期，财富净值$N$有
$$
\begin{aligned}
N_{j t+1} &=R_{k t+1} Q_{t} S_{j t}-R_{t+1} B_{j t+1} \\
&=\left(R_{k t+1}-R_{t+1}\right) Q_{t} S_{j t}+R_{t+1} N_{j t}
\end{aligned}
$$


银行家只会贷款给企业，仅当其融资贴现回报率利差不为负数时。
$$
E_{t} \beta^{i} \Lambda_{t, t+1+i}\left(R_{k t+1+i}-R_{t+1+i}\right) \geq 0, \quad i \geq 0
$$


对于完美资本市场下，这种关系始终平等：风险调整后的溢价为零。然而，由于资本市场不完善，由于中介机构获得资金的能力受到限制，溢价可能是正的。

只要中介机构能够赚取大于或等于家庭存款回报的风险调整回报，它就支付银行家继续建立资产，直到退出该行业。因此，银行家的目标是最大限度地发挥最终财富，由
$$
V_{j t}=\max E_{t} \sum_{i=0}^{\infty}(1-\theta) \theta^{i} \beta^{i+1} \Lambda_{t, t+1+i}\left(N_{j t+1+i}\right)=\max E_{t} \sum_{i=0}^{\infty}(1-\theta) \theta^{i} \beta^{i+1} \Lambda_{t, t+1+i}\left[\left(R_{k t+1+i}-R_{t+1+i}\right) Q_{t+i} S_{j t+i}+R_{t+1+i} N_{j t+i}\right]
$$


其中，$\theta$表示生存率对于每一期。

注意到，如果$\beta^{i} \Lambda_{t, t+i}\left(R_{k t+1+i}-R_{t+1+i}\right)$是正的，那么作为银行机构，银行家倾向于从储户无限制借款，这样就存在**道德风险问题**：

“在初期，银行家可以选择这样的行为：贪污可用项目资金的一部分，而不是令银行家转移资金给储户以分红股利等形式。银行家的成本是，储户可以迫使金融机构破产，并收回剩余的那部分资产。”

然而，对于储户来说，存在过高的成本用以收回银行家贪污的资金。

解决方法是：设定**激励相容约束**用以保证贷款者（指代储户？）提供资金给银行家
$$
V_{j t} \geq \lambda Q_{t} S_{j t}
$$
其中，式子左侧表示银行家之损失，通过转移部分资产造成。右侧表示净值收入，当金融机构破产之后侵吞一定比例的收益。

银行家认为的价值$V_{jt}$可以表示为：
$$
V_{j t}=v_{t} \cdot Q_{t} S_{j t}+\eta_{t} N_{j t}
$$
其中
$$
\begin{array}{l}
v_{t}=E_{t}\left\{(1-\theta) \beta \Lambda_{t, t+1}\left(R_{k t+1}-R_{t+1}\right)+\beta \Lambda_{t, t+1} \theta x_{t, t+1} v_{t+1}\right\} \\
\eta_{t}=E_{t}\left\{(1-\theta)+\beta \Lambda_{t, t+1} \theta z_{t, t+1} \eta_{t+1}\right\}
\end{array}
$$
。

由上述式子可得
$$
\eta_{t} N_{j t}+v_{t} Q_{t} S_{j t} \geq \lambda Q_{t} S_{j t}
$$
可得
$$
Q _{t} S_{j t}=\frac{\eta_{t}}{\lambda-v_{t}} N_{j t} \triangleq \phi_{t} N_{j}
$$
其中，$\phi_t$：私人杠杆率；

如果$\nu_t$大于$\lambda$，则相容激励约束不起作用。





对于总资产的分类，按照私人和政府援助的性质，分为$Q _{t} S_{t}= Q _{ t } S_{ pt }+ Q _{ t } S _{ g t}$，其中$S_{gt}$表示政府援助。



#### 市场出清



总的经济体的恒等式：
$$
Y_{t}=C_{t}+I_{t}+f\left(\frac{ I_{n t}+I_{s s}}{I_{n_{t-1}}+I_{s s}}\right)\left(\overbrace{I_{n t}}^{净资本创造} +\overbrace{I_{s s}}^{稳态资本创造}\right)+G+\tau \psi_{t} Q_{t} K_{t+1}
$$
其中
$$
I_{n t} \equiv I_{t}-\delta\left(U_{t}\right) \xi_{t} K_{t}
$$

#### 政府部门





政府实施信贷政策过程：

- 渠道1：直接实施。

1. 央行发行政府债券给家庭，以无风险利率$R_{t+1}$。由此获得资本金来自家庭。
1. 然后央行将这些资本金贷给非金融机构（企业），以市场贷款利率$R_{k t+1}$。

假设政府中介设计存在效率成本：每单位信贷成本$\tau$。效率成本过大可能反映了融资成本之于企业。

- 渠道2：间接实施。

1. 央行向金融中介机构（商业银行）发行政府债券。
1. 金融中介机构（商业银行）通过向家庭发行存单，以获得资金，购买政府债券。家庭通过购买存单，以实现存款给银行。

假设政府给商业银行提供的金融服务是不受外界因素限制的。



与基准模型一样，中央银行能够灵活发行政府债务来为私人资产提供资金。可知本模型均衡条件与基准情况下的均衡条件相同。（对私人资产持有的中间资产负债表约束相同）。



政府发行总的债券
$$
Q _{t} S_{t}= Q _{t} S_{p t}+ Q _{t} S_{g t}
$$
假设**央行计划融资中间资本比例**的$\psi_t$的数量：
$$
Q _{t} S_{g t}=\psi_{t} Q_{t} S_{t}=B_{gt}
$$
政府收入来源之一$\left(R_{k t+1}-R_{t+1}\right) B_{g t}$；

其发行的政府债券$B_{gt}$等于$\psi_t Q_t S_t$
$$
Q _{t} S_{t}=\phi_{t} N_{t}+\psi_{t} Q_{t} S_{t}= \overbrace{\phi_{c t}}^{私人杠杆率} N_{t}
$$
这里，$\phi_{ct}$是总杠杆率，包括私人融资和公共融资在内：
$$
\phi_{c t}=\frac{1}{1-\psi_{t}} \phi_{t}
$$
==这里，**央行计划融资中间资本比例**的$\psi_t$，是央行应对危机的关键。央行可以调控的变量以应对金融危机。==







##### 和平时期货币政策：

表现为简单的Taylor规则，包含利率平滑参数$\rho$：
$$
\overbrace{i_{t}}^{净名义利率} =(1-\rho)\left[\overbrace{i}^{稳态名义利率} +\kappa_{\pi} \pi_{t}+\kappa_{y}\left(\log Y_{t}-\log Y_{t}^{*}\right)\right]+\rho i_{t-1}+ \overbrace{\varepsilon_{t}}^{外生冲击}
$$
其中名义利率和实际利率由**费雪关系式**表示：
$$
1+i_{t}=R_{t+1} \frac{E_{t} P_{t+1}}{P_{t}}
$$


##### 危机时期信贷政策：

利率规则足以作为正常时期的货币政策。但是，在危机中允许采取信贷政策。尤其是假设在危机开始时，将宽松定义为信贷利差急剧上升的时期，根据以下反馈规则，中央银行将根据信贷利差的变化注入信贷：
$$
\psi_{t}=\overbrace{\psi}^{央行计划融资中间资本比例之稳态值} +v E_{t}\left[\left(\log R_{k t+1}-\log R_{t+1}\right)-\left(\log R_{k}-\log R\right)\right]
$$


此外，在危机中，央行放弃了平稳利率的倾向。在这种情况下，它设置平滑参数$\rho$等于零。通过这种方式，我们相信，我们正在捕捉中央银行在危机爆发时在实践中的表现。此外，货币政策的大部分效果是通过对未来短期利率的预期路径的影响来实现的。有理由认为，在危机期间，央行认为其管理未来预期的能力已经减弱，导致其以更快的速度调整当前利率。



## 实验





#### 实验

##### 实验目的：

阐述模型行为是怎样的。



- [ ] #### 危机实验

考虑在危机发生时，央行信贷政策有无的影响。











