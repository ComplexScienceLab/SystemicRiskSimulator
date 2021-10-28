[toc]

# MEAN FIELD GAMES AND SYSTEMIC RISK

# Metadata

* Type: [[Article]]
* Authors: [[Rene Carmona]], [[Jean-Pierre Fouque]], [[Li-Hsien Sun]]
* Date: [[2015]]
* Date added: [[2020-05-06]]
* Publication: [[Communications in Mathematical Sciences]]
* DOI: [10.4310/CMS.2015.v13.n4.a4](10.4310/CMS.2015.v13.n4.a4)
* Cite key: Carmona_2015_MEANFIELDGAMESANDSYSTEMICRISK
* Topics: [[系统性风险 随机最优控制方法]], [[博士毕业论文开题报告]]
* Related: 
* Tags: [[Zotero Import]]







# 摘要  

在本文中，我们将考虑金融传染的Eisenberg-Noe模型的广义扩展，以考虑离散时间和连续时间的时间动态。将提供对金融影响的推导和解释。重点将放在连续时间框架上，并将其表述为由经营现金流量驱动的微分方程式。在离散和连续时间模型下，将提供有关企业财富的存在和唯一性的数学结果。最后，将考虑时间动态对金融的影响。重点将放在动态清算解决方案与静态Eisenberg-Noe模型的解决方案之间的差异上。  

# 特点  

- 结合了在该领域主流的两种分析方法  
  - 网络模型基于静态分析  
    - Larry Eisenberg and Thomas H. Noe. Systemic risk in ﬁnancial systems. Management Science, 47(2):236–249, 2001.  
  - 平均场理论基于动态分析  
    - Jean-Pierre Fouque and Tomoyuki Ichiba. Stability in a model of interbank lending. SIAM Journal on Financial Mathematics, 4:784–803, 2013.  

# 未收录  

# 意义  

- 缩小两类研究方向的差距  
- 扩展了Eisenberg and Noe 2001至连续时间  

# 工作  

- 同时考虑离散时间和连续时间的情形。重点将放在连续时间模型的推导和表征上；  
- 集中于在银行间网络方法中增加时间动态，这使平均场模型具有吸引力；  

- 离散时间的清算系统  
  - 设置项  
    - Agostino Capponi_2015_Systemic risk mitigation in financial networks..pdf  
  - 考虑企业的破产清算  
    - Rogers & Veraart_2011_Failure and rescue in an interbank network..pdf  
- 连续时间清算系统  

# 本文结论  

- 扩展了[14]的模型，以使现金流量和债务在时间上是动态的。  
- 我们在离散时间和连续时间内都介绍了该模型，从而扩展了[7，23， [33]只考虑离散时间清算。值得注意的是，我们确定确定性和Itô设置下清算解决方案存在和唯一的条件。这样，我们为Eisenberg-Noe传染模型编写了一个动力学系统，其中可能包括固有的优先级排序方案，具体来说，我们确定如果相对接触量随时间恒定不变，则本文介绍的动态Eisenberg-Noe模型将在终端时间以与路径无关的方式重现静态系统。能够确定真实的默认顺序，而不是确定在计算静态清算模型中广泛使用的虚拟默认算法中找到的虚拟顺序。不管怎样，相对反射率不是随时间变化的，因此我们确定静态Eisenberg-Noe模型可能报告了对金融系统的错误乐观或悲观描述。  

# 扩展  

这个模型有三个明显的扩展对我们来说很明显，并且我们预料会在静态模型和动态模型之间造成进一步的分歧。第一个扩展是流动性资产和火灾销售的包含。在静态模型中，例如[12，1，18 ]，因为所有公司都获得相同的价格，所以清算资产没有先发优势。但是，在动态模型中，为了获得更高的价格，清算可能有优势，但是在清算过程中，可能会导致更大的卖火。其他公司。第二个扩展是包括或有支付和信用违约掉期。[4，38，39]最近在静态环境中考虑了这一点。通过考虑网络动态取决于清算财富的历史，静态工作中报告的许多困难很可能会自然解决；我们参考文献[4]，对此扩展进行了初步讨论，最后扩展，我们认为拟议中的动态模型del在考虑市场参与者的战略或动态行动时尤其有用，例如，将破产成本和债务延期的战略决策结合在一起，我们认为连续时间框架特别适合于这些扩展，因为它使我们能够构建独特的清算解决方案，而无需强大的单调性假设。  

# 模型  

# 综述  

- 系统性风险模型  

  - 基于网络  

    - 离散时间  

      - Larry Eisenberg and Thomas H. Noe. Systemic risk in ﬁnancial systems. Management Science, 47(2):236–249, 2001.  

      - 讨论包含多重清算数据(multiple clearing dates)的情况  

        - Agostino Capponi and Peng-Chu Chen. Systemic risk mitigation in ﬁnancial networks.Journal of Economic Dynamics & Control, 58:152–166, 2015.  
        - Gerardo Ferrara, Sam Langﬁeld, Zijun Liu, and Tomohiro Ota. Systemic illiquidity in the interbank network. Staﬀ Working Paper 586, Bank of England, 2016.  

      - 讨论包含多重到期(multiple maturities)的情况  

        - Michael Kusnetsov and Luitgard A.M. Veraart. Interbank clearing in ﬁnancial networks with multiple maturities. 2018. Working paper.  

      - 破产成本  

        Paul Glasserman and H. Peyton Young. How likely is contagion in ﬁnancial networks?Journal of Banking and Finance, 50:383–399, 2015.  

        Matthew Elliott, Benjamin Golub, and Matthew O. Jackson. Financial networks and contagion. American Economic Review, 104(10):3115–3153, 2014.  

        Agostino Capponi, Peng-Chu Chen, and David D. Yao. Liability concentration and systemic losses in ﬁnancial networks. Operations Research, 64(5):1121–1134, 2016.  

        Stefan Weber and Kerstin Weske. The joint impact of bankruptcy costs, ﬁre sales and crossholdings on systemic risk in ﬁnancial networks. Probability, Uncertainty and Quantitative Risk, 2(1):9, June 2017.  

        Leonard C.G. Rogers and Luitgard A.M. Veraart. Failure and rescue in an interbank network. Management Science, 59(4):882–898, 2013.  

        Helmut Elsinger. Financial networks, cross holdings, and limited liability. Österreichische Nationalbank (Austrian Central Bank), 156, 2009.  

        Luitgard A.M. Veraart. Distress and default contagion in ﬁnancial networks. 2017. Working paper.  

        - Helmut Elsinger. Financial networks, cross holdings, and limited liability. Österreichische Nationalbank (Austrian Central Bank), 156, 2009.  
        - Leonard C.G. Rogers and Luitgard A.M. Veraart. Failure and rescue in an interbank network. Management Science, 59(4):882–898, 2013.  
        - Matthew Elliott, Benjamin Golub, and Matthew O. Jackson. Financial networks and contagion. American Economic Review, 104(10):3115–3153, 2014.  
        - Paul Glasserman and H. Peyton Young. How likely is contagion in ﬁnancial networks?Journal of Banking and Finance, 50:383–399, 2015.  
        - Agostino Capponi, Peng-Chu Chen, and David D. Yao. Liability concentration and systemic losses in ﬁnancial networks. Operations Research, 64(5):1121–1134, 2016.  
        - Luitgard A.M. Veraart. Distress and default contagion in ﬁnancial networks. 2017. Working paper.  
        - Stefan Weber and Kerstin Weske. The joint impact of bankruptcy costs, ﬁre sales and crossholdings on systemic risk in ﬁnancial networks. Probability, Uncertainty and Quantitative Risk, 2(1):9, June 2017.  

      - 跨期持有  

        - Helmut Elsinger. Financial networks, cross holdings, and limited liability. Österreichische Nationalbank (Austrian Central Bank), 156, 2009.  
        - Christian Gouriéroux, J.-C. Héam, and Alain Monfort. Bilateral exposures and systemic solvency risk. Canadian Journal of Economics, 45(4):1273–1309, 2012.  
        - Stefan Weber and Kerstin Weske. The joint impact of bankruptcy costs, ﬁre sales and crossholdings on systemic risk in ﬁnancial networks. Probability, Uncertainty and Quantitative Risk, 2(1):9, June 2017.  
        - Eberhard Zeidler. Nonlinear Functional Analysis and its Applications I: Fixed-Point Theorems. Springer-Verlag, 1986.  

      - 甩卖  

        - 单种非流动性资产  

          - Rodrigo Cifuentes, Hyun Song Shin, and Gianluigi Ferrucci. Liquidity risk and contagion.Journal of the European Economic Association, 3(2-3):556–566, 2005.  
          - ……  

        - 多种非流动资产  

          - Zachary Feinstein. Obligations with physical delivery in a multi-layered ﬁnancial network.2018. Working paper.  

            - 工作  

              通过将每个清算日视为不同的资产，进一步为具有多个到期日的金融网络提供了另一种方法。  

          - Zachary Feinstein. Financial contagion and asset liquidation strategies. Operations Research Letters, 45(2):109–114, 2017.  

          - Zachary Feinstein and Fatena El-Masri. The eﬀects of leverage requirements and ﬁre sales on ﬁnancial contagion via asset liquidation strategies in ﬁnancial networks. Statistics & Risk Modeling, 34(3-4):113–139, 2017.  

      - Grzegorz Hałaj and Christoﬀer Kok. Modelling the emergence of the interbank networks.Quantitative Finance, 15(4):653–671, 2015.  

      - Michael Boss, Helmut Elsinger, Martin Summer, and Stefan Thurner. Network topology of the interbank market. Quantitative Finance, 4(6):677–684, 2004.  

    - 连续时间  

      - Isaac M. Sonin and Konstantin Sonin. Banks as tanks: A continuous-time model of ﬁnancial clearing. 2017. Working paper.  

  - 基于平均场理论  

    - 平均场，不含控制  
      - Josselin Garnier, George Papanicolaou, and Tzu-Wei Yang. Diversiﬁcation in ﬁnancial networks may increase systemic risk. In Handbook on Systemic Risk, pages 432–443. Cambridge University Press, 2013.  
      - Jean-Pierre Fouque and Tomoyuki Ichiba. Stability in a model of interbank lending. SIAM Journal on Financial Mathematics, 4:784–803, 2013.  
      - Josselin Garnier, George Papanicolaou, and Tzu-Wei Yang. Large deviations for a mean ﬁeld model of systemic risk. SIAM Journal on Financial Mathematics, 4:151–184, 2013.  
    - 平均场，随机博弈  
      - 其数量之于机构，其允许借贷于央行，可化为一优化问题，以最小化成本函数。  
        - René Carmona, Jean-Pierre Fouque, Seyyed Mostafa Mousavi, and Li-Hsien Sun. Systemic risk and stochastic games with delay. Journal of Optimization Theory and Applications, Mar 2018.  
        - René Carmona, Jean-Pierre Fouque, and Li-Hsien Sun. Mean ﬁeld games and systemic risk. Communications in Mathematical Sciences, 13(4):911–933, 2015.  
      - Jean-Pierre Fouque and Li-Hsien Sun. Systemic risk illustrated. In Handbook on Systemic Risk, pages 444–452. Cambridge University Press, 2013.  
      - 粒子系统  
        - Sergey Nadtochiy and Mykhaylo Shkolnikov. Particle systems with singular interaction through hitting times: Application in systemic risk modeling. 2017. To appear in Annals of Applied Probability.  

- 关于时间动态性分析  

  - Larry Eisenberg and Thomas H. Noe. Systemic risk in ﬁnancial systems. Management Science, 47(2):236–249, 2001.  

    - 缺点  

      [14]的模型可以分析金融系统的健康状况，但是容易产生错误的乐观或者悲观的估计结论。  

  - Paul Glasserman and H. Peyton Young. How likely is contagion in ﬁnancial networks?Journal of Banking and Finance, 50:383–399, 2015.  

    - 缺点  

      例如[30]的文献采用实证的方式，采用压力测试的方式评估银行体系健康状况，但是无法分析时间动态性。  