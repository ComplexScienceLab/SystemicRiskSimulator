

# The financial accelerator in an estimated New Keynesian model

![[Christensen2008-zotero#Metadata]]

Other files:

* Mdnotes File Name: [[Christensen2008]]
* Metadata File Name: [[Christensen2008-zotero]]

##  Zotero links

* [Local library](zotero://select/items/1_8F36HGAF)
* [Cloud library](http://zotero.org/users/6240833/items/8F36HGAF)

## Notes





##### 企业家


企业家的假设：

- 每时期存在固定的生存率（退出率）；



企业家存在的行为：

- 根据一些判据，企业家决策是否还贷或者违约；



企业家最大化：
$$
n_{t+1}=\color{blue}{\nu v_{t}}+ \color{red}{(1-\nu) g_{t}}
\tag{14}
$$
其中，

$n$：资本净值；

红色表示获得所有资本，从失败退出的企业家那；

蓝色表示自身从上一期获得的净值；

where $v_{t}$ denotes the 净值 of surviving entrepreneurs net of borrowing costs carried over from the previous period, $1-\nu$ is the share of new entrepreneurs entering the economy, and $g_{t}$ is the transfer or "seed money" that newly entering entrepreneurs receive from entrepreneurs who die and depart from the scene. $v_{t}$ is given by
$$
v_{t}=\left[f_{t} q_{t-1} k_{t}-E_{t-1} f_{t}\left(q_{t-1} k_{t}-n_{t}\right)\right]
\tag{15}
$$




企业家的资本需求量，依赖于：

1. 期望边际回报；
2. 期望边际外部融资成本$E_{t} f_{t+1}$，于下一期。

$$
E_{t} f_{t+1}=E_{t}\left[\frac{\color{blue}{z_{t+1}}+\color{green}{(1-\delta)} q_{t+1}}{q_{t}}\right]
\tag{10}
$$
其中，分子表示下一期资本，其中，蓝色表示资本产出，绿色表示上一期资本折余，分母表示这一期资本。



其中，借款成本（实际利率隐含为在时期$t-1$签署的贷款合同）：
$$
E_{t} f_{t+1}=E_{t}\left[S(\cdot) R_{t} / \pi_{t+1}\right]
\tag{11}
$$
$f_t$：事后的实际回报，对于持有的资本在$t$时期来说；

其中，外部融资溢价：
$$
\begin{array}{l}
S(\cdot)=S\left(\frac{n_{t+1}}{q_{t} k_{t+1}}\right), \\
S^{\prime}(\cdot)<0 \text { and } S(1)=1
\end{array}
\tag{12}
$$
当分式的比值$\frac{n_{t+1}}{q_{t} k_{t+1}}$下降时，企业家身为借款者，依赖于无担保借款（高杠杆）在更大程度上为项目融资，这样使得借贷风险增加。

结合(11)(12)，可以得对数线性化的外部融资率：
$$
\hat{f}_{t+1}=\hat{R}_{t}-\hat{\pi}_{t+1}+\psi\left(\hat{q}_{t}+\hat{k}_{t+1}-\hat{n}_{t+1}\right)
$$
其中，$\psi$表示弹性，即外部融资溢价相对于企业家的杠杆状况变化的弹性。









约束条件：

资本需求约束：
$$
E_{t} f_{t+1}=E_{t}\left[S(\cdot) R_{t} / \pi_{t+1}\right]
$$
技术约束：规模报酬不变的技术：
$$
y_{t} \leqslant k_{t}^{\alpha}\left(A_{t} h_{t}\right)^{1-\alpha}, \quad \alpha \in(0,1)
\tag{16}
$$


企业家的资本需求由以下决定：
$$
E_{t} f_{t+1}=E_{t}\left[S(\cdot) R_{t} / \pi_{t+1}\right]
\tag{11}
$$




standard Tobin’s Q equation
$$
E_{t}\left[q_{t} x_{t}-1-\chi\left(\frac{i_{t}}{k_{t}}-\delta\right)\right]=0
\tag{22}
$$
资本家的资本供给给企业家，由以下决定：
$$
E_{t}\left[q_{t} x_{t}-1-\chi\left(\frac{i_{t}}{k_{t}}-\delta\right)\right]=0
\tag{22}
$$
其中，
$$
k_{t+1}=x_{t} i_{t}+(1-\delta) k_{t}
$$

$$
\log \left(x_{t}\right)=\rho_{x} \log \left(x_{t-1}\right)+\varepsilon_{x t}
$$

where $\rho_{x} \in(-1,1)$ is an autoregressive coefficient, and $\varepsilon_{x t}$ is normally distributed with mean zero and standard deviation $\sigma_{x}$





##### 零售商

零售业仅用于将名义刚性引入该经济体。 零售商以等于企业家名义边际成本的价格从企业家那里购买批发商品，并无成本地区分它们。 然后，他们在垄断竞争的市场中出售这些差异化的零售产品。 根据Calvo（1983）和Yun（1996），我们假设除非零售商收到随机信号，否则他们无法重新优化其销售价格。 接收到这样的信号的恒定概率为（1-φ）。 因此，每个零售商j设置价格，～p t（j），该价格在l个时期内使预期利润最大化。 因此，l = 1 /（1-φ）是价格保持不变的平均时间长度。 但是，零售商j必须以概率φ收取前一时期以稳态总通货膨胀率π为指标的有效价格。 在时间t处，如果零售商j收到重新优化的信号，它会选择价格～p t（j），以使其折扣最大化，即在其价格固定的间隔内的预期实际总利润。


$$
\max _{\left\{\tilde{p}_{t}(j)\right\}} E_{0}\left[\sum_{l=0}^{\infty}(\beta \phi)^{l} \lambda_{t+l} \Omega_{t+l}(j) / p_{t+l}\right]
\tag{25}
$$






















