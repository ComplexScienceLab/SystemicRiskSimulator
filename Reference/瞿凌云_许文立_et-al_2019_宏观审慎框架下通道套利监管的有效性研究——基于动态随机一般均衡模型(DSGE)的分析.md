# 宏观审慎框架下通道套利监管的有效性研究——基于动态随机一般均衡模型(DSGE)的分析

## Metadata

* Item Type: [[Article]]
* Authors: [[ 瞿凌云]], [[ 许文立]], [[ 钱国军]]
* Date: [[2019]]
* Date Added: [[2021-01-01]]
* URL: [https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2020&filename=JIRO201905002&v=](https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2020&filename=JIRO201905002&v=)
* Cite key: QuLingYun2019
* Topics: [[宏微观审慎监管]], [[DSGE]], [[影子银行]]
* Related: [[Angelini2014]], [[Feve2019]]
* Tags: #counterfactual-analysis, #macro-prudential-regulation, #shadow-banking, #反事实分析, #宏观审慎监管, #影子银行, #zotero, #literature-notes, #reference
* PDF Attachments
  - [瞿凌云_许文立 et al_2019_宏观审慎框架下通道套利监管的有效性研究——基于动态随机一般均衡模型(DSGE)的分析.pdf](zotero://open-pdf/library/items/XNIRTB9H)

## Abstract

构建含有影子银行部门的动态随机一般均衡模型,设定满足中国实践的宏观审慎监管规则和同业资管产品的违约概率,研究宏观审慎监管政策的有效性,结果表明:全面宏观审慎监管既能有效防止信贷和同业资管的通道转换,缩短融资链条,又能增强金融机构的稳健性;仅对商业银行进行的单向监管容易衍生新的通道,弱化监管的预期稳定作用,造成杠杆率高企、资金周转复杂;打破同业资管产品的刚性兑付,资管产品利率能够更加准确地反映融资主体的信用风险,提高资金配置的效率。全面监管或者打破刚性兑付在实施过渡期均会加剧宏观经济的下行压力,长期来看,这种负向影响会逐渐消退,宏观经济将平稳增长。建议在宏观审慎监管调控中充分考虑影子银行的替代作...


##  Zotero links

* [Local library](zotero://select/items/1_4PZ2FI7Q)
* [Cloud library](http://zotero.org/users/6240833/items/4PZ2FI7Q)

## Highlights and Annotations

- [[QuLingYun2019 - Extracted Annotations (3102021, 43424 PM)]]









## 模型

> 基础模型借鉴：
>
> Angelini P, Neri S, Panetta F, 2014. The Interaction between Capital Requirements and Monetary Policy: PAOLO ANGELINI, STEFANO NERI, AND FABIO PANETTA[J]. Journal of Money, Credit and Banking, 46(6): 1073–1112. DOI:[10.1111/jmcb.12134](https://doi.org/10.1111/jmcb.12134).



> 影子银行部分借鉴：
>
> Fève P, Moura A, Pierrard O, 2019. Shadow Banking and Financial Regulation: A Small-Scale DSGE Perspective[J]. Journal of Economic Dynamics and Control, 101: 130–144. DOI:[10.1016/j.jedc.2019.02.001](https://doi.org/10.1016/j.jedc.2019.02.001).



### 部门



#### 家庭部门

只存款，不借款。



#### 厂商部门

资本来源是融资。

融资来源：从商业银行、影子银行。

厂商部门。厂商部门生产最终产品, 从商业银行和影子银行获得融资, 雇佣劳动, 并支付利息和工资。其生产函数为 Cobb -​ Douglas 生产函数: $F \left( K _{ t -1}, N _{ t }\right)= Y _{ t }=\varepsilon_{ t } K _{ t -1}^{1-\alpha} N _{ t }^{\alpha}$
其中, $K _{ t }= S _{ t }^{ c }+ S _{ t }^{ s }, S _{ t }^{ c }, S _{ t }^{ s }$ 分别为厂商获得的传统商业银行贷款和影子银行的贷款, 支付
利率分别为 $r _{ t }^{ k }, r _{ t }^{ s } ; \varepsilon_{ t }=\varepsilon_{ t -1}^{ \rho _{\varepsilon}} \exp \left(\sigma_{\varepsilon} u _{\varepsilon, t }\right)$ 是全要素生产率冲击( 技术冲击) $,\left|\rho_{\varepsilon}\right|<1, \sigma_{\varepsilon}>0$,
$u _{\varepsilon, t } \sim i . i . d . N (0,1)$
资本积累方程为 $K _{ t }= I _{ t }+(1-\delta) K _{ t -1}$, 其中 $\delta$ 为资本折旧率。
工厂目标是最大化利润, 利润函数为： $\pi_{ t }^{ f }= Y _{ t }- w _{ t } N _{ t }-\left( r _{ t }^{ k }+\delta\right) S _{ t -1}^{ c }-\left( r _{ t }^{ s }+\delta\right) S _{ t -1}^{ s }$
一阶条件: $r _{ t }^{ k }=(1-\alpha) \varepsilon_{ t }\left( S _{ t -1}^{ c }\right)^{-\alpha} N _{ t }^{\alpha}$
$r _{ t }^{ s }=(1-\alpha) \varepsilon_{ t }\left( S _{ t -1}^{ s }\right)^{-\alpha} N _{ t }^{\alpha}$
$w _{ t }=\alpha \varepsilon_{ t }\left( S _{ t -1}^{ c }+ S _{ t -1}^{ s }\right)^{1-\alpha} N _{ t }^{\alpha-1}$



#### 银行部门

单期利润：
$$
\begin{aligned}
\pi_{t}^{c}=& D_{t}+\left(1+r_{t}^{k}-\delta\right) S_{t-1}^{c}+\left(1-\Gamma_{t}\right)\left(1+r_{t-1}^{a}\right) Z G_{t-1}-\left(1+e_{t}\right) S_{t}^{c}-Z G_{t}-\left(1+r_{t-1}^{d}\right) D_{t-1} \\
&-C\left(x_{t}\right)-p\left(\frac{Z G_{t}}{S_{t}^{c}}\right)
\end{aligned}
$$
暨：利润 = 居民存款 + 收回未违约的贷款 + 收回未违约的资管产品的本息 - 贷出贷款 - 购买资管产品 - 居民提款 - 资本充足率惩罚成本 - 调整资产比例之成本；

其中, $\pi_{t}^{\text {c }}$ 是传统银行部门获得的利润; $r _{ t }^{ k }$ 为银行部门发放贷款获得利息收入; $r _{ t -1}^{\alpha}$ 为购买资管产品获得的利息收入; $r _{ t -1}^{ d }$ 为存款利息; $e _{ t }$ 是单位贷款的审查成本, 即对借款者进行 审查篮选所花费的成本, 直接决定贷款利率的高低。这一成本冲击符合一阶自回归过程 $e _{ t }$ $=\rho_{ e } e _{ t -1}+\sigma_{ e } \mu_{ e , t }$, 其中 $\left|\rho_{ e }\right|<1, \sigma_{ e }>0, u _{ e , t } \sim i . i . d N (0.1)$ 。影子银行的资管违约冲击遵循一阶自回归过程, 即 $\Gamma_{ t }=\rho_{\Gamma} \Gamma_{ t -1}+\varepsilon_{\Gamma, t } $ 违约冲击包含了所有来自于影子银行的扰动,但与经济结构没有直接联系。$C\left(x_{t}\right)$表示资本缺口对应的惩罚成本。

定义$C\left(x_{t}\right)$：
$$
c\left(x_{t}\right)=-p_{1} \ln \left(1+p_{2} x_{t}\right)
$$
其中，资本缺口$x_t$
$$
x _{ t }= n _{ t }-\bar{\eta} S _{ t }^{ C }
$$


传统商业银行追求跨期利润最大化, 其跨期贴现因子为家庭的随机贴现因子 $\Lambda_{ t , t +1}=$ $\beta c_{t} / c_{t+1}$。商业银行会选择存款、贷款和购买资管来实现跨期利润最大化。即它们的一阶 条件为:
$$
\left\{\begin{array}{l}
1+C_{t}^{\prime}=E_{t} \Lambda_{t, t+1}\left(1+r_{t}^{d}\right) \\
\left(1-e_{t}\right)-\left(1-\eta_{t}\right) C_{t}^{\prime}-p^{\prime}_{t} \frac{Z G_{t}}{\left(S_{t}^{c}\right)^{2}}=E_{t} \Lambda_{t, t+1}\left(1+r_{t+1}^{k}-\delta\right) \\
1+C_{t}^{\prime}+p_{t}^{\prime} \frac{1}{S_{t}^{c}}=E_{t} \Lambda_{t, t+1}\left(1-\Gamma_{t+1}\right)\left(1+r_{t}^{\alpha}\right)
\end{array}\right.
$$
式中, $\Lambda_{ t , t +1}=\beta c _{ t } / c _{ t +1}$ 表示 $t$ 至 $t +1$ 期间家庭部门的随机折现因子,其中各个变量
稳态值用 $\overline{ z }$ 来表示, $\hat{ z }= z _{ t }-\overline{ z }$ 。



#### 影子银行部门



两期部门。影子银行在第一期进入市场, 通过向银行发行资管产品 $ZG _{ t }$ 融资, 单位发行成本 为 $a$, 并向企业发放贷款 $S _{ t }^{ c }=(1-\alpha) ZG _{ t }, 0< a <1 ;$ 在第二期获取收益离开市场。其目标函数是第二期收益最大化, 在第二期 $t +1$ 时刻的利润函数为：
$$
\pi_{t+1}^{ s }=\left(1+ r _{ t +1}^{ s }-\delta\right) S _{ t }^{ s }-\left(1+ r _{ t }^{ a }\right) ZG _{ t }
$$


约束条件：
$$
S _{ t }^{ c }=(1-\alpha) ZG _{ t }
$$
一阶条件：
$$
(1-\alpha) E _{ t }\left(1+ r _{ t +1}^{ s }\right)=1+ r _{ t }^{\alpha}
$$



#### 宏观审慎政策



对于宏观审慎监管政策的设定,国际上的宏观审慎政策主要通过考察整体信贷和 GDP 比值与趋势值的偏离程度来确定逆周期资本缓冲,而中国考察的是信贷增速与 GDP 增速 的偏离。据此, 本文将资本充足率的时变形式设置成如下一阶自回归过程：
$$
\eta_{ t }=\eta^{-1-\rho_{\eta}} \eta_{ t -1}^{\rho_{\eta}}\left(\frac{ i _{ t } / i _{ t -1}}{\operatorname{gdp}_{ t } / gdp _{ t -1}}\right)^{\psi\left(1-\rho_{ \eta }\right)} e ^{\varepsilon_{\eta, t }}
$$
其中, $i _{ t }$ 为信贷规模; $gdp _{ t }$ 为国内生产总值。 根据资本充足率的规定，商业银行的自有资本不得低于其贷款的一定比例，即商业银行的资本充足率约束为 $n _{ t } \geq \bar{\eta} S _{ t ^{\circ}}^{ c }$ 其中, $\bar{\eta}$ 为最低资本充足率要求。本文允许商业银行自有资本小于监管要求的最低资本。但监管当局会惩罚商业银行，惩罚成本是资本缺口的函数。定义资本缺口 $x _{ t }= n _{ t }-\bar{\eta} S _{ t }^{ C }$, 参照 Fève and Pierrard( 2017)，本文将惩罚函数设置为$\left( x _{ t }\right)=- p _{1} \ln \left(1+ p _{2} x _{ t }\right)$, 其中 $p _{1}, p _{2} \geq 0$ 。 这意味着 $c ^{\prime}(0)=- p _{1} p _{2} \leq 0, c ^{\prime \prime}(0)=- c ^{\prime}(0) p _{2} \geq 0$。