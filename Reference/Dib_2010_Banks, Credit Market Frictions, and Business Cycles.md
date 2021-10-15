# Banks, Credit Market Frictions, and Business Cycles

## Metadata

* Type: [[Report]]
* Authors: [[Ali Dib]]
* Date: [[2010]]
* Date added: [[2020-08-20]]
* Cite key: Dib_2010_BanksCreditMarketFrictionsAndBusinessCycles
* Topics: [[系统性风险 Dsge]]
* Related: 
* Tags: [[Zotero Import]], [[_tablet]]
* Zotero links: [Local library](zotero://select/items/1_QDB6JNSM)
* PDF Attachments: [Dib_2010_Banks, Credit Market Frictions, and Business Cycles.pdf](zotero://open-pdf/library/items/LBUFY7Q6)







## 摘要

作者提出了一个微观基础的框架，该框架将活跃的银行业纳入具有金融加速器的动态随机一般均衡模型中。他评估了银行业在总冲击的真实影响的传递和传播中的作用，并评估了金融冲击在美国经济周期波动中的重要性。银行业包括两种提供利润最大化的银行，它们提供不同的银行服务并在银行间市场进行交易。贷款是通过银行间借贷和银行资本产生的，但要符合监管资本要求。银行具有垄断权，可以设定名义存款和最优惠贷款利率，选择其杠杆比率和投资组合构成，并且可以内生于部分银行间借款的违约。因为筹集资金以满足监管资本要求的成本很高，所以银行业减弱了金融冲击的实际影响，减少了宏观经济的波动，并有助于稳定经济。该模型还包括两种非常规的货币政策（定量宽松和定性宽松），可以减少金融危机的负面影响。









## 工作

研究银行业在总冲击的真实影响的传递和传播中的作用，评估了金融冲击在美国经济周期波动中的重要性。研究通过构建将活跃的银行业纳入到具有金融加速器的DSGE模型中。



## 模型

#### 参数

消费$C$；

闲时$1-H$；

工时$H$；



#### 假设

假设借款型银行所借的款项公式表达形式满足Leontief技术；



#### 模型的构成









##### 银行

两类异质性的银行。划分以在银行间市场的债权债务状态为依据。



目标：利润最大化；



###### 储蓄型银行（贷款型银行）

- 定义：银行间市场净债权者的银行集合。

- 行为：

  - 收集劳动者的全额保险存款，存款利率$R_{j,t}^D$；

  - 调配资产比例$(1-s_{j,t})$以购买政府债券；

  - 配置资产比例$s_{j,t}$于银行间市场，用以贷给借款型银行；

    



模型：





储蓄型银行资产负债表：

| 资产                     | 负债          |
| ------------------------ | ------------- |
| 同业拆借：$D_{j,t}^{IB}$ | 储户存款：$D_{j,t}$ |
| 政府债券：$B_{j,t}^{sb}$ | |







对单个银行$j$存款$D_{j,t}$供应量：
$$
D_{j, t}=\left(\frac{R_{j, t}^{D}}{R_{t}^{D}}\right)^{\vartheta_{D}} D_{t}
$$
调整利率成本：
$$
A d_{j, t}^{R^{D}}=\frac{\phi_{R^{D}}}{2}\left(\frac{R_{j, t}^{D}}{R_{j, t-1}^{D}}-1\right)^{2} D_{t}
$$
银行间市场监管成本：
$$
\Delta_{j, t}^{s}=\frac{\chi_{s}}{2}\left(\left(s_{j, t}-\bar{s}\right) D_{j, t}\right)^{2}
$$
其中，

$\bar{s}$：监管规定的目标值，偏离该值会产生二次方成本；



最优目标：
$$
\max _{\left\{s_{j, t}, R_{j, t}^{D}\right\}} E_{0} \sum_{t=0}^{\infty} \beta_{b}^{t} \lambda_{t}^{b}\left\{\left[s_{j, t} R_{t}^{I B}\left(1-\delta_{t}^{D}\right)+\left(1-s_{j, t}\right) R_{t}-R_{j, t}^{D}\right] D_{j, t}-A d_{j, t}^{R}-\Delta_{j, t}^{s}\right\}
$$
其中，

$s_{j, t} R_{t}^{I B}\left(1-\delta_{t}^{D}\right) D_{j,t}$：银行收回本息从银行间市场；

$\left(1-s_{j, t}\right) R_{t} D_{j,t}$：银行收回本息从政府债券；

上述二项是总的名义收益之于银行之资产。

$R_{j, t}^{D} D_{j, t}$：银行还给储户本息；

$\delta_{t}^{D}$：贷款型银行违约比率之于银行间市场；



同质均衡时，应有：$s_{j, t}=s_{t}$ and $R_{j, t}^{D}=R_{t}^{D}$ for all $t>0$



F.O.C.
$$
s_{t}=\bar{s}+\frac{R_{t}^{I B}\left(1-\delta_{t}^{D}\right)-R_{t}}{\chi_{s} D_{t}}
$$

$$
\begin{aligned}
\frac{1+\vartheta_{D}}{\vartheta_{D}}\left(R_{t}^{D}-1\right) &=s_{t}\left(R_{t}^{I B}-1\right)\left(1-\delta_{t}^{D}\right)+\left(1-s_{t}\right)\left(R_{t}-1\right)-\chi_{s}\left(s_{t}-\bar{s}\right)^{2} D_{t} \\
&-\frac{\phi_{R^{D}}}{\vartheta_{D}}\left(\frac{R_{t}^{D}}{R_{t-1}^{D}}-1\right) \frac{R_{t}^{D}}{R_{t-1}^{D}}+\frac{\beta_{b} \phi_{R^{D}}}{\vartheta_{D}}\left(\frac{R_{t+1}^{D}}{R_{t}^{D}}-1\right) \frac{R_{t+1}^{D}}{R_{t}^{D}}
\end{aligned}
$$



银行同业拆借、无风险资产持有之间有一个最优配置比例，

存款利率具有名义粘性，即变动成本，影响了跨时期消费的跨期替代；







###### 借款型银行

- 定义：银行间市场净债务者的银行集合。
- 行为：
  - 借款从银行间市场的储蓄银行；
  - 筹集银行资本给银行家以满足资本要求；
  - 接受量化宽松政策来自央行，暨从央行获得资金；
  - 接受定性的货币政策……
  - 贷款Loans给企业部门；





模型：



借款型银行资产负债表：

| 资产                      | 负债                                                         |
| ------------------------- | ------------------------------------------------------------ |
| 贷款：$L_{j, t}-x_{j, t}$ | 同业拆借：$D_{j,t}^{IB}$                                     |
| 政府债务：$B_{j,t}^{sb}$  | 银行资金：$Q_{t}^{Z} Z_{j, t}$                               |
|                           | 央行资金注入： $ m_{j,t}$                                    |
|                           | 其它项目：$\left(\Gamma_{t}-1\right)\left(D_{j, t}^{I B}+x_{j, t}\right)$ |

$$
\begin{array}{l|l}
\hline \text { Assets } & \text { Liabilities } \\
\hline \text { Loans: } L_{j, t}-x_{j, t} & \text { Interbank borrowing: } D_{j, t}^{I B} \\
\text { Government bonds: } B_{j, t}^{l b} & \text { Bank capital: } Q_{t}^{Z} Z_{j, t} \\
& \text { Central bank's money injection: } m_{j, t} \\
& \text { Other terms: }\left(\Gamma_{t}-1\right)\left(D_{j, t}^{I B}+x_{j, t}\right) \\
\hline
\end{array}
$$

备注：

其它项目，$\left(\Gamma_{t}-1\right)\left(D_{j, t}^{I B}+m_{j, t}\right)$，用以平衡偏离资产负债表的操作；

改变资产负债表的比例的方法：

- 通过转换一部分贷款$L_{j,t}$成为政府债券$x_{j, t}$；

扩缩资产负债表的规模的方法：

- 央行注入货币量$m_{j,t}$；
- 金融中介的冲击$\Gamma_t$；





获得借款的方式，以Leontief技术的形式，其贷款需求函数在银行间市场借贷和自有银行资金之间互相替代：
$$
L_{j, t}=\min \left\{D_{j, t}^{I B}+m_{j, t} \; ; \; \kappa_{j, t}\left(Q_{t}^{Z} Z_{j, t}+x_{j, t}\right)\right\} \Gamma_{t}
\tag{17}
$$
暨(28)(29)二者选择最小的那个作为
$$
L_{t} =\Gamma_{t}\left(D_{t}^{I B}+m_{t}\right)
\tag{28}
$$

$$
L_{t} =\Gamma_{t} \kappa_{t}\left(Q_{t}^{Z} Z_{t}+x_{t}\right)
\tag{29}
$$





其中，

$D_{j, t}^{I B}$：借款通过同业拆借；

$m_{j, t}$：银行资本，从央行注资得到，服从AR(1)随机过程；

$\kappa_{j, t}\left(Q_{t}^{Z} Z_{j, t}\right)$：基于杠杆率$\kappa_{j,t} \leq \bar{\kappa}$，借款型银行从银行家；

$x_{j,t}$：从央行借款$x_{j,t}$，服从AR(1)随机过程；

$\Gamma_t$：冲击之金融中介影响信贷供给，服从AR(1)随机过程；



Leontief技术包含了完美的替代性于银行间市场借贷和银行资本之间，并且强化了资本需求，减弱了不同的冲击的实际影响。例如，在积极的技术冲击之后，企业对投资和贷款的需求增加了。 扩大贷款需要更高的银行杠杆率或在金融市场上筹集新的银行资本。 然而，这两个动作对于放贷银行而言代价高昂。 因此，产生贷款的边际成本增加，银行提高了对企业家的贷款利率。 反过来，这增加了外部融资成本，并部分抵消了投资需求的最初增长。此外，采用Leontief技术，产生贷款的边际成本只是银行间市场上借贷成本与筹集银行资本的边际成本的加权总和。



最优化过程



利率调整成本：
$$
A d_{j, t}^{R^{L}}=\frac{\phi_{R^{L}}}{2}\left(\frac{R_{j, t}^{L}}{R_{j, t-1}^{L}}-1\right)^{2} L_{t}
\tag{18}
$$
贷款型银行$j$，面对如下贷款需求函数
$$
L_{j, t}=\left(\frac{R_{j, t}^{L}}{R_{t}^{L}}\right)^{-\vartheta_{L}} L_{t}
\tag{19}
$$
其中，$\vartheta_{L}$表示替代弹性之于两种不同类型；





贷款型银行$j$之二次方收入：
$$
\Delta_{j, t}^{\kappa}=\frac{\chi_{\kappa}}{2}\left(\frac{\bar{\kappa}-\kappa_{j, t}}{\bar{\kappa}} Q_{t}^{Z} Z_{j, t}\right)^{2}
\tag{20}
$$




惩罚之于贷款型银行违约于银行间市场：
$$
\Delta_{j, t}^{D}=\frac{\chi_{\delta^{D}}}{2}\left(\frac{\delta_{j, t-1}^{D} D_{j, t-1}^{I B}}{\pi_{t}}\right)^{2} R_{t-1}^{I B}
\tag{21}
$$
其中，$\delta_{t}^{D}$：贷款型银行违约比率之于银行间市场；



惩罚之于贷款型银行银行家转移部分银行资金作为自身收益：
$$
\Delta_{j, t}^{Z}=\frac{\chi_{\delta^{Z}}}{2}\left(\frac{\delta_{j, t-1}^{Z} Q_{t-1}^{Z} Z_{j, t-1}}{\pi_{t}}\right)^{2} R_{t}^{Z}
\tag{22}
$$
其中，$\delta_{t}^{Z}$：银行家转移资金比率之于贷款型银行；







总之，贷款型银行$j$的最大化其利润：
$$
\max _{\left\{R_{j, t}^{L}, \kappa_{j, t}, \delta_{j, t}^{D}, \delta_{j, t}^{Z}\right\}} E_{0} \sum_{t=0}^{\infty} \beta_{b}^{t} \lambda_{t}^{b}\left\{R_{j, t}^{L} L_{j, t}-\left(1-\delta_{j, t}^{D}\right) R_{t}^{I B} D_{j, t}^{I B}-\left[\left(1-\delta_{j, t}^{Z}\right) R_{t+1}^{Z}-R_{t}\right] Q_{t}^{Z} Z_{j, t}-A d_{j, t}^{R^{L}}-\Delta_{j, t}^{D}-\Delta_{j, t}^{Z}-R_{t} m_{j, t}-\left(R_{j, t}^{L}-R_{t}\right) x_{j, t},\right\}
$$
其中，

$\lambda_{t}^{b}$：边际效用之于银行家消费；

$\left[\left(1-\delta_{j, t}^{Z}\right) R_{t+1}^{Z}-R_{t}\right] Q_{t}^{Z} Z_{j, t}$：边际成本之于持有以单位银行资金以满足资金需求；

$R_{t} m_{j, t}$：总成本之于货币注资从央行；

$\left(R_{j, t}^{L}-R_{t}\right) x_{j, t}$：总成本之于转换一部分债券用于政府债券；



对应约束条件(17)-(22)。



F.O.C.
$$
R_{t}^{L}= 1+\frac{\vartheta_{L}}{\vartheta_{L}-1}\left(\zeta_{t}-1\right)-\frac{\phi_{R^{L}}}{\vartheta_{L}-1}\left(\frac{R_{t}^{L}}{R_{t-1}^{L}}-1\right) \frac{R_{t}^{L}}{R_{t-1}^{L}}+\frac{\beta_{b} \phi_{R^{L}}}{\vartheta_{L}-1} E_{t}\left[\left(\frac{R_{t+1}^{L}}{R_{t}^{L}}-1\right) \frac{R_{t+1}^{L}}{R_{t}^{L}}\right]
\tag{23}
$$
$$
\kappa_{t}= \bar{\kappa}\left(1-\frac{\bar{\kappa} \Gamma_{t}\left(R_{t}^{L}-1\right)}{\chi_{\kappa} Q_{t}^{Z} Z_{t}}\right)
\tag{24}
$$
$$
\delta_{t}^{D}= E_{t}\left[\frac{R_{t} \pi_{t+1}}{\chi_{\delta^{D}} D_{t}^{I B}}\right]
\tag{25}
$$
$$
\delta_{t}^{Z}= E_{t}\left[\frac{R_{t} \pi_{t+1}}{\chi_{\delta^Z}  Q_{t}^{Z} Z_{t}}\right]
\tag{26}
$$

其中，边际成本之于产生贷款：
$$
\zeta_{t}=\Gamma_{t}^{-1}\left[R_{t}^{I B}+\left(E_{t} R_{t+1}^{Z}-R_{t}-\left(R_{t}^{L}-1\right) \frac{\bar{\kappa}-\kappa_{t}}{\bar{\kappa}}\right) \frac{Q_{t}^{Z}}{\kappa_{t}}\right]
$$
此外，Leontief技术形式的需求函数在银行间市场借贷和自有银行资金之间互相替代
$$
L_{t} =\Gamma_{t}\left(D_{t}^{I B}+m_{t}\right)
\tag{28}
$$

$$
L_{t} =\Gamma_{t} \kappa_{t}\left(Q_{t}^{Z} Z_{t}+x_{t}\right)
\tag{29}
$$

对于(24)，如果贷款利率$R^L_t$上升，则意味着银行需要去杠杆。

对于(25)，银行间市场借贷违约率下降，当同业拆借借贷规模扩大时。

> 怎么从经济学角度理解同业拆借借贷规模越大，借贷违约率下降？

对于(27)，其加总如下，由银行间市场拆借利率$R^{IB}_t$
$$
\left(E_{t} R_{t+1}^{Z}-R_{t}-\left(R_{t}^{L}-1\right) \frac{\bar{\kappa}-\kappa_{t}}{\bar{\kappa}}\right) \frac{Q_{t}^{Z}}{\kappa_{t}}
$$


##### 中央银行、政府

- 中央银行
- 政府





##### 家庭

> （略）

- 类型的差异：
  在避险程度、进入金融市场方面不同；.
- 
- 工人$\Box_\Box^w$
  - 行为
    - 提供劳动力
    - 消费$C_t^w$
- 银行家$\Box_\Box^b$
  - 银行家是两类银行的所有者，从中获利；
  - 行为
    - 消费$C_t^b$









##### 生产部门

> （略）

