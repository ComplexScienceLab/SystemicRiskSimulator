# Systemic Risk and Stochastic Games with Delay

## Metadata

* Type: [[Article]]
* Authors: [[Rene Carmona]], [[Jean-Pierre Fouque]], [[Seyyed Mostafa Mousavi]], [[Li-Hsien Sun]]
* Date: [[2016-07-21]]
* Date added: [[2020-05-07]]
* Publication: [[arXiv:1607.06373 [q-fin]]]
* Cite key: Carmona_2016_SystemicRiskAndStochasticGamesWithDelaya
* Topics: [[系统性风险 随机最优控制方法]], [[【博士毕业论文开题报告】]]
* Related: 
* Tags: [[Zotero Import]], [[具有延迟的随机博弈]], [[纳什均衡]], [[系统性风险]], [[银行间借贷]]
* Zotero links: [Local library](zotero://select/items/1_95J32N9D)
* PDF Attachments: [Carmona et al_2016_Systemic Risk and Stochastic Games with Delay.pdf](zotero://open-pdf/library/items/6895BAUB)

### Abstract

 We propose a model of inter-bank lending and borrowing which takes into account clearing debt obligations. The evolution of log-monetary reserves of $N$ banks is described by coupled diffusions driven by controls with delay in their drifts. Banks are minimizing their finite-horizon objective functions which take into account a quadratic cost for lending or borrowing and a linear incentive to borrow if the reserve is low or lend if the reserve is high relative to the average capitalization of the system. As such, our problem is an $N$-player linear-quadratic stochastic differential game with delay. An open-loop Nash equilibrium is obtained using a system of fully coupled forward and advanced backward stochastic differential equations. We then describe how the delay affects liquidity and systemic risk characterized by a large number of defaults. We also derive a close-loop Nash equilibrium using an HJB approach.



## 摘要

我们提出了一种考虑到债务清算的银行间借贷模型。 多个银行的对数货币储备的演变是通过耦合扩散来控制的，这些扩散是由具有延迟的控件驱动的。银行正在将其有限水平的目标函数最小化，该函数考虑了借贷或借贷的二次成本以及储备金较低的线性激励（如果储备金相对于系统的平均资本）是借贷的（如果储备金较高）。因此，我们的模型是带有延迟的多个参与者线性二次随机微分博弈。使用完全耦合的前向和后向随机差分方程组可获得开环Nash平衡。然后，我们描述延迟如何影响以大量违约为特征的流动性和系统性风险。我们还使用HJB方法得出闭环Nash平衡。
关键词：系统性风险，银行间借贷，具有延迟的随机博弈，纳什均衡。



## 综述  

- Carmona(2015)  
  - 研究内容  
    - 提出了各银行间与央行向银行借贷的随机博弈模型 ，没有义务偿还贷款，也没有借贷收益。  
  - 研究发现  
    - 在平衡状态下，中央银行充当票据交换所，创造了流动性，从而导致了更稳定的系统。  
  - 研究结论  
    - 在平衡状态下，中央银行充当票据交换所，创造了流动性，从而导致了更稳定的系统。  
- Bensoussan(2016)  
  - 方法  
    - 线性二次方平均场Stackelberg博弈，带延迟，带一个主要参与者和多个小微参与者  

## 文章结构  

## 研究过程  

- 求解开环纳什均衡、闭环纳什均衡  
  - 研究结论  
    - 由于控制存在延迟，需要归还或收取退款而产生的新效果降低了在没有延迟的情况下观察到的流动性。  
  - 方法来源  
    - Peng and Yang(2009)  
      - 过程  
        - 通过FABSDEs求解开环纳什均衡  
    - Gozzi(2009)  
      - 过程  
        - 通过HJB求解闭环纳什均衡  

## 创新  