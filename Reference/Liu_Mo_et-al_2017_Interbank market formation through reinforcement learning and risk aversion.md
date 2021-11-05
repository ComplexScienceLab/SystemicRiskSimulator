# Interbank market formation through reinforcement learning and risk aversion

# Metadata

* Type: [[Article]]
* Authors: [[Anqi Liu]], [[Cheuk Yin Jeﬀrey Mo]], [[Mark Paddrik]], [[Steve Y Yang]]
* Date: [[2017]]
* Date added: [[2020-07-08]]
* Cite key: Liu_2017_InterbankMarketFormationThroughReinforcementLearningAndRiskAversion
* Topics: [[系统性风险 强化学习]]
* Related: 
* Tags: [[Zotero Import]], [[Interbank Lending Market]], [[Contagion Risk]], [[Multi-Agent System]], [[Reinforcement Learning Agent]]
* PDF Attachments: [Liu_Mo et al_2017_Interbank market formation through reinforcement learning and risk aversion.pdf](zotero://open-pdf/library/items/9KA39UPC)

## Abstract

 In this study, we propose a multi-agent model to examine bank lending and borrowing risk behaviors and their implications to interbank market dynamics. Using data from 2001 to 2014 that covers around U.S. 6600 banks, we model individual bank decisions using the temporal diﬀerence reinforcement learning algorithm based on banks’ lending preferences and environment, and we then generate the interbank market dynamics from the empirical data. This dynamic model allows us to construct interbank networks as they change with bank risk preferences, and thus facilitates the analysis of the banking systems stability. The model successfully replicates the key characteristics of interbank lending and borrowing relationships that have been documented in the recent literature. A key ﬁnding of this study is that the risk aversion choice of individual bank leads to unique interbank market structures that suggest the macro risk preference of the market. Combined with the use of balance sheet data, this modeling framework helps central banks and regulators building more functional models for examining the interbank market stability problems.



# 摘要

在这项研究中，我们提出了一种多主体模型来研究银行借贷风险行为及其对银行间市场动态的影响。利用2001年至2014年涵盖美国6600多家银行的数据，我们使用基于银行贷款偏好和环境的时间差异强化学习算法对单个银行的决策进行建模，然后根据经验数据生成银行间市场动态。这种动态模型使我们能够构建随着银行风险偏好而变化的银行间网络，从而有助于对银行系统稳定性的分析。该模型成功复制了最近文献中记载的银行间借贷关系的关键特征。这项研究的关键发现是，单个银行的风险规避选择会导致独特的银行间市场结构，从而提示市场的宏观风险偏好。结合使用资产负债表数据，此建模框架可帮助中央银行和监管机构建立更多功能性模型，以检查银行间市场稳定性问题。





# 研究贡献

本研究的主要贡献是与学习代理一起开发动态的银行间市场模型，以基于银行绩效数据和行为模式重建银行间网络。从基于网络的模型的角度来看，我们设计了两个实验来回答以下问题：



1. 具有学习代理的多代理系统可以重建银行间网络的动态吗？

2. 代理风险偏好的改变是否会导致系统不易传染？

# 研究结果

结果表明，随着网络稳定在一定程度的风险偏好，随着银行代理继续收紧贷款政策，网络程度开始下降。我们发现以下内容：1）银行间贷款市场功能更好，因为它避免了对代理商流动性的冲击；2）由于故障银行网络是孤立的，冲击传播减少。总体而言，我们的模型为金融体系传染问题建模带来了数据，并弥合了银行间网络传染文献中现有文献中的空白，在这些文献中，大多数现有压力测试方法隐含地假设银行高度风格化，没有次优行为。

# 模型

- [ ] TODO



初始化：

两类银行：大型、小型银行；

三种债务：隔夜拆借、短期债务、长期债务；



![image-20211105101959961](Liu_Mo_et-al_2017_Interbank market formation through reinforcement learning and risk aversion.assets/image-20211105101959961.png)

初始借贷网络数据由最大熵值法（maximum entropy approach）由资产负债表数据计算得。

























