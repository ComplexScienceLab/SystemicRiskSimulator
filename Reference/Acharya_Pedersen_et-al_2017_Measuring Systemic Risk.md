<!-- Acharya V V, Pedersen L H, Philippon T, 等, 2017. Measuring Systemic Risk[M]. C.E.P.R. Discussion Papers.-->



[toc]



# Measuring Systemic Risk

# Metadata

* Type: [[Book]]
* Authors: [[Viral V Acharya]], [[Lasse H Pedersen]], [[Thomas Philippon]], [[Matthew P Richardson]]
* Date: [[2017]]
* Date added: [[2020-06-19]]
* Cite key: Acharya_2017_MeasuringSystemicRisk
* Topics: [[系统性风险 多因素模型]], [[系统性风险 测度]]
* Related: [[LiZheng_2019_ZhongGuoJinRongBuMenJianXiTongXingFengXianYiChuDeJianCeYuJingYanJiuJiYuXiaXingHeShangXingDCoESZhiBiaoDeShiXianYuYouHua]]
* Tags: [[Zotero Import]], [[_tablet_modified]]
* PDF Attachments: [Acharya_Pedersen et al_2017_Measuring Systemic Risk.pdf](zotero://open-pdf/library/items/HUZAFDQC)

## Abstract

 We present an economic model of systemic risk in which undercapitalization of the ﬁnancial sector as a whole is assumed to harm the real economy, leading to a systemic risk externality. Each ﬁnancial institution’s contribution to systemic risk can be measured as its systemic expected shortfall (SES), that is, its propensity to be undercapitalized when the system as a whole is undercapitalized. SES increases in the institution’s leverage and its marginal expected shortfall (MES), that is, its losses in the tail of the system’s loss distribution. We demonstrate empirically the ability of components of SES to predict emerging systemic risk during the ﬁnancial crisis of 2007–2009. (JEL G01, G21, G28, D62, H23)



# 摘要

我们提出了一种系统性风险的经济模型，其中假定金融部门整体的资本不足会损害实体经济，从而导致系统性风险的外部性。 每个金融机构对系统性风险的贡献都可以用其系统性预期缺口（SES）来衡量，也就是说，当整个系统的资本不足时，其金融不足的倾向。  SES增加了该机构的杠杆作用和其边际预期缺口（MES），即其在系统损失分布末端的损失。 我们从经验上证明了SES的组成部分能够预测2007-2009年金融危机期间出现的系统性风险的能力。



# 工作  

- 制定一个框架，然后衡量系统性风险；  

- 其次，鉴于这一框架，我们制定了管理系统性风险的最佳政策；  

- 最后，对2007-2009年金融危机进行了详细的分析，支持了系统风险的理论分析；  

# 研究的贡献  

## 模型  

- 五因素模型  

- 特点  

  基于通用的平衡模型  

- 基于思想  

  我们通过研究一种理论模型来“弥合差距”，该理论模型基于各种一般均衡模型的公分母，但又足够简单，可以依靠众所周知的统计方法提供清晰的建议。 我们的模型基于以下基本思想：对金融机构进行监管的主要原因是：  （ii）金融系统的资本不足会导致外部性扩散到整个经济体。  3有趣的是，即使是相对简单的模型也足以获得具有丰富经验内容的丰富的系统风险监管新理论。  

# 模型



## 理论部分

### 银行激励

设定：

$N$：银行个数；

$x_j^i$：银行$i$投资于资产$j$的量；







总资产【4】：
$$
a^{i}=\sum_{j=1}^{J} x_{j}^{i} 	\tag{4}
$$



这些投资可以通过债务或股权融资。 尤其是，任何一家银行$i$的所有者都有一个初始禀赋资本$\bar{w}_0^i$，其中$w_0^i$作为股本资本存入银行，其余的作为股利支付（并消耗或用于其他活动）。 银行也可以借债。 自然地，资产$a_i$的总和必须等于权益$w_0^i$和债务$b_i$的总和，预算约束【5】：
$$
w_{0}^{i}+b^{i}=a^{i} \tag{5}
$$
时期1，资产$j$向银行$i$支付的利率是$r_i^j$。我们允许资产回报在投资机会中捕获投资机会中的差异。时期1，银行资产总的市值是$y^i=\hat{y_i}-\phi^i$，其中$\phi^i$表示财务困境成本，$\hat{y}^i$表示财务困境前的收入（利率收入）【6】：
$$
\hat{y}^{i}=\sum_{j=1}^{J} r_{j}^{i} x_{j}^{i} \tag{6}
$$
【7】财务困境成本取决于银行资产的市值和**未偿债务面值**$f^i$：
$$
\phi^{i}=\Phi\left(\hat{y}^{i}, f^{i}\right) \tag{7}
$$
我们对困境成本的表述相当笼统。即使公司没有实际违约，也可能会产生困境成本。该规范涵盖了债务过剩问题以及其他众所周知的财务困境成本。我们将规格限制为$\phi \le \hat{y}$，以使$y \ge 0$。

银行（与其他公司相比）的特殊之处在于：

- 他们享有部分债务的政府担保；

- 财务困境可能会带来系统性风险外部性。

  

我们首先在下一部分中讨论担保债务问题，然后转向系统性风险。为了获得各种类型的政府担保，我们假设一部分债务由政府隐含或显式担保。设置债务的面值，以使债务持有人收支平衡【8】
$$
b^{i}=\alpha^{i} f^{i}+\left(1-\alpha^{i}\right) E\left[\min \left(f^{i}, y^{i}\right)\right] \tag{8}
$$
其中，$\alpha^i$：隐含的债务（政府明确的担保）的比例。

尽管我们的重点是系统性风险，但我们将政府债务担保包括在内，因为它们在经济上很重要，并且因为我们想强调存款保险和系统性风险的不同监管含义。 被政府保险的债务可以解释为存款，但也可以涵盖隐性担保。

【9】时期1的银行净值$w_1^i$：
$$
w_{1}^{i}=\hat{y}^{i}-\phi^{i}-f^{i}
$$
银行股本（权益）的持有者受到有限责任保护，因此它获得$1_{[w_1^i>0]}w_1^i$，由此问题是求解一下最优化问题【10】：
$$
\begin{align}
&\max _{w_{0}^{i}, b^{i},\left\{x_{j}^{i}\right\}_{j}} c \times\left(\bar{w}_{0}^{i}-w_{0}^{i}-\tau^{i}\right)+E\left(u\left(1_{\left[w_{1}^{i}>0\right]} \times w_{1}^{i}\right)\right)
\\
&\text{s.t.} \quad (5)-(9)
\end{align}
\tag{10}
$$

遵循方程式（5）-（9），其中，$u^i(.)$是时间1收入的银行所有者的效用，$\bar{w}_{0}^{i}-w_{0}^{i}-\tau^{i}$是初始禀赋$\bar{w}_0^i$的一部分， 被立即消耗（或用于外部活动），剩余的禀赋被保留为权益资本$w_0 ^i$或用于支付银行税$\tau^i$，我们将在后面描述。 参数c有几种解释。 它可以简单地看作是对即时消费的效用的一种度量，但是从更广泛的意义上讲，它是股权资本的机会成本。 我们可以将所有者视为以成本$c$筹集资本，也可以将债务视为在税收或鼓励努力工作方面提供优势。 对我们而言重要的是，使用资本而不是债务会产生机会成本。



监管者希望最大限度地发挥福利功能$P^1+P^2+P^3$，它由三部分组成

- 第一部分是所有银行所有者的权益为正的效用的总和
  $$
  P^{1}=\sum_{i=1}^{N} c \times\left(\bar{w}_{0}^{i}-w_{0}^{i}-\tau^{i}\right)+E\left[\sum_{i=1}^{N} u^{i}\left(1_{\left[w_{1}^{i}>0\right]} \times w_{1}^{i}\right)\right]
  $$

- 第二部分是债务保险计划的预期成本
  $$
  P^{2}=E\left[g \sum_{i=1}^{N} 1_{\left[w_{1}^{i}<0\right]}{\alpha^{i} w_{1}^{i}}\right]
  $$

- 第三部分是福利函数，其捕获金融危机的外生性特征
  $$
  P^{3}=E\left[e \times 1_{\left[W_{1}<z A\right]} \times\left(z A-W_{1}\right)\right]
  $$
  如果时期1的资本$W_1$低于资产$A$的比例$z$，则$P^3<0$，则发生危机。$e$表示金融部门出现困境时






## 经验部分

### 衡量系统性风险的指标

两类标准用以测度风险水平：

- 在险值（value-at-risk,VaR）：
  在险值满足
  $Pr[R<-VaR_\alpha]=\alpha$
  。在险值是在以一定的置信度$\alpha$的概率下发生风险的时候的损失值。亦即表示银行的损失小于在置信度$\alpha$（例如1%或5%）下的在险值$VaR_\alpha$的概率等于$\alpha$。在这里，在险值$VaR_\alpha$通常用正数表示，损失$R$通常用负数表示，其绝对值越大，表示损失越大。

- 期望损失（expected loss,ES）：
  期望损失$ES_\alpha$表示损失超过在险值的情况下的损失的期望。
  $$
  E S_{\alpha}=-E\left[R \mid R \leq-V a R_{\alpha}\right]
  
  \tag{1}
  $$



ES比VaR好的理由：

- VaR并不稳健。因为不对称但风险很大的下注可能不会产生很大的VaR。 原因是，如果负收益低于1％或5％VaR阈值，则VaR不会捕获它。 的确，在持续危机中，担忧之一是VaR未能弥补AAA级抵押担保债务（CDO）和其他结构性产品中的潜在“尾随”损失。 相反，ES不会遭受此问题的困扰，因为它可以测量超出阈值的所有损耗。 在考虑银行的道德风险时，这种区别尤其重要，因为超出VaR阈值的巨额损失通常由政府的救助承担。
-  VaR不是风险的连贯度量，因为两个投资组合之和的VaR可能高于其各自的VaR的总和，这在ES中是不可能发生的（Artzner等人，1999）。



分解银行回报$R$为其和于每一个组合的回报$r_i$，则$R=\sum_i y_i r_i$，其中$y_i$表示每一个组合的权重。由ES的定义，可得
$$
E S_{\alpha}=-\sum_{i} y_{i} E\left[r_{i} \mid R \leq-V a R_{\alpha}\right]

\tag{2}
$$


定义**边际预期缺口**（marginal expected shortfall,MES）
$$
\frac{\partial E S_{\alpha}}{\partial y_{i}}=-E\left[r_{i} \mid R \leq-V a R_{\alpha}\right] \equiv M E S_{\alpha}^{i}

\tag{3}
$$
边际预期缺口衡量的是投资组合$i$承担风险的方式如何增加银行的整体风险。 换句话说，当机构整体表现不佳时，可以通过估算第$i$组的损失来衡量$MES$。

这些标准的风险管理做法对于系统性风险的思考很有用。 金融体系由许多银行组成，就像银行由许多组成一样。 因此，我们可以通过将$R$表示整个银行业或整个经济体的收益来考虑整个银行体系的预期缺口。然后，每个银行对这一风险的贡献可以通过其$MES$来衡量。







第1.4节制定的最佳政策要求支付费用（即税收），等于两个组成部分的总和：
（一） 机构风险部分，即其担保负债的预期损失；
（二） 系统性风险部分，即危机中的预期系统成本（即当金融部门资本不足时）是金融机构对资本不足的百分比；



使用这些不利的市场结果期间的公司净股本收益率来定义**边际期望缺口**（MES）
$$
M E S_{5 \%}^{i} \equiv-E\left[\frac{w_{1}^{i}}{w_{0}^{i}}-1 \mid I_{5 \%}\right]
$$

银行$i$在资产$j$的回报率

$$
r_{j}^{i}=\eta_{j}^{i}-\delta_{i, j} \varepsilon_{j}^{i}-\beta_{i, j} \varepsilon_{m}
$$
其中，

- $\eta_j^i$：细尾分布（如高斯分布）；
- $\varepsilon_j^i$：特性，服从独立正态幂律分布，拖尾指数$\zeta$；
- $\varepsilon_m$：共性，服从独立正态幂律分布，拖尾指数$\zeta$；

细尾因素捕获了正常的日常变化，而幂律则解释了大事件。

若$\alpha$充分小，则



# 结论



当前的金融法规试图限制每个机构的风险。 除非每个金融机构都将系统性风险的外部成本内部化，否则该机构将有动力承担所有人承担的风险。 一个例证就是当前的危机，在该危机中，金融机构利用了类似的大型证券和贷款组合，这些组合几乎没有特质风险，但有大量系统性风险。

 在本文中，我们认为金融监管应侧重于限制系统性风险，即金融部门发生危机的风险及其对整个经济的溢出。 我们提供了一种简单直观的方法来衡量每家银行对系统性风险的贡献，并提出了限制它的方法。 在使用股票和CDS的市场数据进行的各种测试中（例如2009年的压力测试结果和2007-08年危机期间的公司绩效），我们的系统风险度量似乎能够预测在系统性危机中表现最差的金融公司。

 我们的工作有几个扩展值得在将来追求。 虽然我们使用权益和CDS数据估算和测试了我们建议的系统风险度量，但获取此类信息的另一种方法是通过价外的股票期权和保险合同的价格来抵御整个系统承受的单个企业的损失 。虽然此类保险尚未交易，但可获得有关公司股权和市场期权的数据，并可用于构建对尾部依赖性的度量，例如MES。

 最后，我们调查了杠杆（以资产与普通股之比衡量）在确定公司的系统风险中的作用。 在2007-08年金融危机中影响最大的杠杆形式可以说是短期债务，例如针对投资银行大量使用的风险资产的隔夜担保借贷（“回购”）（Adrian和Shin 2010），以及 由商业银行支持的管道发行的短期（隔夜至周到期）资产支持商业票据（Acharya，Schnabl和Suarez 2013）。 相反，尽管存款原则上是必需的，因此也是短期的，但存款保险的存在意味着有保险存款的商业银行实际上在危机中相对稳定。 因此，从经验上理解短期杠杆如何有助于以市场为基础的金融公司系统风险度量似乎很重要。