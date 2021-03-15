



# International Reserves and Rollover Risk

![[Bianchi2018-zotero#Metadata]]

Other files:

* Mdnotes File Name: [[Bianchi2018]]
* Metadata File Name: [[Bianchi2018-zotero]]

##  Zotero links

* [Local library](zotero://select/items/1_MQFIYFR3)
* [Cloud library](http://zotero.org/users/6240833/items/MQFIYFR3)

## Notes





[toc]







## 变量定义：

- $y$：国家产出；

- $a$：储备的存量；

- $b$：债券的存量；

- $d$：违约的情况，贷款者不偿还债务；

- $\delta$：债券收益率；

- $m_{t, t+1}=e^{-r-\left(\kappa_{t} \varepsilon_{t+1}+0.5 \kappa_{t}^{2} \sigma_{\varepsilon}^{2}\right)}, \text { with }  \kappa_{t} \geq 0$：贷款者定价的债券收益，表示为随机折现因子。
  其中，
  - $r$：折现因子；
  - $\kappa$：控制风险溢价冲击；
  - 风险溢价冲击过程符合2状态的Markov过程：$\{\kappa_L=0,\kappa_H>0:\pi_{LH},\pi_{HL}\}$；





## 国家的环境

$$
E_{t} \sum_{j=t}^{\infty} \beta^{j-t} u\left(c_{j}\right)
$$

$$
b_{t+1}=(1-\delta) b_{t}+i_{t}
$$

政府的预算约束
$$
c_{t}+g+\delta b_{t}+q_{a} a_{t+1}=y_{t}+a_{t}+i_{t} q_{t}
$$
其中，

- $c_t$：政府财务消费；
- $g$：固定政府开支；
- $\delta b_{t}$：优惠券付款；
- $q_a$：外汇储备的价格；

- $q_{t}$：发行债务价格；
- $y_t$：收入；

## 政府问题表示为递归形式

变量定义：

- $s=\{y,\kappa\}$：表示当前环境的外生状态；

- $V$：表示政府的值函数；

政府的值函数：

对于任何债券价格函数q，政府的最优值函数$V$满足以下方程【V】：

$$
V(a, b, s)=\max \left\{V^{R}(a, b, s), V^{D}(a, s)\right\}
$$

政府的还款的最优值函数$V^R$表示为【V】：

$$
\begin{array}{ll}
V^{R}(a, b, s) & =\max _{c \geq 0, a^{\prime} \geq 0, b^{\prime} \geq 0}\left\{u(c)+\beta E_{s^{\prime} \mid s} V\left(b^{\prime}, a^{\prime}, s^{\prime}\right)\right\}
\\
\mathrm{s.t.}  \quad & c=y-\delta b+a+q\left(a^{\prime}, b^{\prime}, s\right)\left[b^{\prime}-(1-\delta) b\right]-q_{a} a^{\prime}-g
\end{array}
$$

其中，

- $q_a$：外汇储备的价格；

政府违约的最优值函数$V^{D}$表示为【VD】：
$$
\begin{array}{ll}
V^{D}(a, s) & =\max _{c \geq 0, a^{\prime} \geq 0}\left\{u(c)-U^{D}(y)+\beta E_{s^{\prime} \mid s} V\left(0, a^{\prime}, s^{\prime}\right)\right\}, \\
\mathrm{s.t.} \quad & c=y+a-q_{a} a^{\prime}-g
\end{array}
$$

其中，

- $U^D(y)$：违约的时候，政府无法借款，从而遭受的一次性的效用损失；







政府的问题：

解决政府问题的决策的变量包括：

- 违约$\hat{d}(a,b,s)=\{1(政府违约时),0(政府没有违约时)\}$；
- 债务$\hat{b}(a,b,s)$；
- 违约时的储备$\hat{a}^D(a ,b,s)$；
- 没有违约时的储备$\hat{a}^R(a ,b,s)$；
- 违约时的消费$\hat{c}^D(a,s)$；
- 没有违约时的消费$\hat{c}^R(a,b,s)$；

债券价格均衡：为了与贷方的投资组合条件保持一致，债券价格表需要满足【6】：

$$
q\left(a^{\prime}, b^{\prime}, s\right)=E_{s^{\prime} \mid s}\left[m\left[s^{\prime}, s\right]\left(1-\hat{d}\left[a^{\prime}, b^{\prime}, s^{\prime}\right]\right)\left(\delta+(1-\delta) q\left[a^{\prime \prime}, b^{\prime \prime}, s^{\prime}\right]\right)\right]
$$

其中，

- $b^{\prime \prime}=\hat{b}\left(a^{\prime}, b^{\prime}, s^{\prime}\right)$；

- $a^{\prime \prime}=\hat{a}^{R}\left(a^{\prime}, b^{\prime}, s^{\prime}\right)$；

- $\delta$：债券价格的$\delta$份额用于出售，其余部分的债券保留至下一期出售；



## 博弈过程

该博弈是借款政府与贷款政府的在$t+1$时期、$t$时期的重复博弈。借款政府根据贷款政府在$t+1$期的定价，决策本国在$t+1$期$a$、b和是否违约$d$。然后贷款者再根据借款政府的$t+1$期的决策，制定$t$期的价格。然后借款政府再决策。就是这样从时期$t$的未来的时期，一直博弈到时期$t$为止的。

该博弈过程的特殊性在于，就是贷款国，他的决策过程没有要最优化什么目标。公式(6)里面不涉及最优化问题。





## 计算债券定价



外国贷款人期望的债券价格收益：
$$
m_{t, t+1}=e^{-r-\left(\kappa_{t} \varepsilon_{t+1}+0.5 \kappa_{t}^{2} \sigma_{\varepsilon}^{2}\right)}
$$
其中，

- $r$：无风险的市场利率；



确定的无限期息票债券流，以恒定的外生利率$\delta$减少，==在时期$t$发行的债券承诺在$t+j$期间支付$\delta(1-\delta)^{j-1}$单位的可贸易商品==。因此债券量的动态可以描述为公式【2】：
$$
b_{t+1}=(1-\delta) b_{t}+i_{t}
$$
其中，

- $b_{t}$：从时期$t$到期的债券量；
- $i_t$：时期$t$发行的债券量；





息票结构，定义为：
$$
D=\frac{1+i_{b}}{\delta+i_{b}}
$$
其中，

- $D$：麦考利久期；
- $\delta$：外生的递减恒定利率；
- $i_b$：每个时期，债券生成的固定的收益率；



计算债券收益率$i_b$，定义为投资者在持有债券至到期且未违约的情况时将获得的每期的回报率（收益率）。 该结果应满足公式：
$$
\begin{align}
q_{t} & = \sum_{j=1}^{\infty} \delta(1-\delta)^{j-1} e^{-j i_{b}} \\
& = \delta e^{-i_b}+\delta (1-\delta)e^{-2i_b}+\delta (1-\delta)^2 e^{-3i_b}+\dots
\end{align}
$$
其中，

- $q_t$：政府制定的债券价格；

- $\delta$：外生的递减恒定利率；

- $\delta(1-\delta)^{j-1}$：债券的利息，从【2】可得；

- $i_b$：每个时期，债券生成的固定的收益率；

  



在模拟过程中，负债情况$b_t$计算为
$$
b_{t+1}=\frac{\delta}{1-(1-\delta) e^{-r}} b_{t}
$$
其中，

- $r$：无风险的市场利率；


$$
\begin{align}
&=\delta b_t + \delta (1-\delta) e^{-r} b_t + \delta (1-\delta)^2 e^{-2r} b_t \\
&= 
\end{align}
$$

