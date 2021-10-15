# Graph Neural Networks: Methods, Applications, and Opportunities

## Metadata

* Item Type: [[Article]]
* Authors: [[Lilapati Waikhom]], [[Ripon Patgiri]]
* Date: [[2021-09-08]]
* Date Added: [[2021-08-23]]
* URL: [http://arxiv.org/abs/2108.10733](http://arxiv.org/abs/2108.10733)
* Cite key: Waikhom.Patgiri_2021
* Topics: [[图神经网络]]
* Tags: #_tablet, #内容/图神经网络, #文献/综述, #68Txx, #Computer-Science---Artificial-Intelligence, #Computer-Science---Machine-Learning, #I.2, #I.2.6, #I.5, #zotero, #literature-notes, #reference
* PDF Attachments
	- [Waikhom_Patgiri_2021_Graph Neural Networks - Methods, Applications, and Opportunities.pdf](zotero://open-pdf/library/items/PGMQRDII)

## Abstract

In the last decade or so, we have witnessed deep learning reinvigorating the machine learning field. It has solved many problems in the domains of computer vision, speech recognition, natural language processing, and various other tasks with state-of-the-art performance. The data is generally represented in the Euclidean space in these domains. Various other domains conform to non-Euclidean space, for which graph is an ideal representation. Graphs are suitable for representing the dependencies and interrelationships between various entities. Traditionally, handcrafted features for graphs are incapable of providing the necessary inference for various tasks from this complex data representation. Recently, there is an emergence of employing various advances in deep learning to graph data-based tasks. This article provides a comprehensive survey of graph neural networks (GNNs) in each learning setting: supervised, unsupervised, semi-supervised, and self-supervised learning. Taxonomy of each graph based learning setting is provided with logical divisions of methods falling in the given learning setting. The approaches for each learning task are analyzed from both theoretical as well as empirical standpoints. Further, we provide general architecture guidelines for building GNNs. Various applications and benchmark datasets are also provided, along with open challenges still plaguing the general applicability of GNNs. CCS Concepts: • Computing methodologies → Machine learning; Machine learning approaches; Learning paradigms; Machine learning algorithms; Cross-validation; Artificial intelligence.


##  Zotero links
* [Local library](zotero://select/items/1_B8NP239N)
* [Cloud library](http://zotero.org/users/6240833/items/B8NP239N)

## Highlights and Annotations

- [[Waikhom.Patgiri_2021 - ]]
- [[Waikhom.Patgiri_2021 - Comment Submitted to ACM]]







### ![Image](Waikhom_Patgiri_2021_Graph Neural Networks - Methods, Applications, and Opportunities.assets/640-20210923120748328)

###   **报道** 

作者：专知

##### **【导读】**图神经网络一直是业界关注的热点之一。最近来自印度国家理工学院的学者发布了《图神经网络》综述论文。



在过去十年左右的时间里，我们见证了深度学习让机器学习领域重新焕发活力。它以最先进的性能解决了计算机视觉、语音识别、自然语言处理等领域的许多问题。



这些领域的数据一般用欧几里得空间表示。其他许多领域都符合非欧几里得空间，图是其中的理想表示。



图适用于表示各种实体之间的依赖关系和相互关系。传统上，手工制作的图特性无法从复杂的数据表示中为各种任务提供必要的推断。最近，出现了利用深度学习的各种进展来绘制基于数据的任务。



本文提供了图神经网络(GNN)在每种学习设置中的全面综述: 监督学习、无监督学习、半监督学习和自监督学习。每个基于图的学习设置的分类提供了属于给定学习设置的方法的逻辑划分。



从理论和实证两方面分析了每个学习任务的方法。此外，我们还提供了构建GNN的一般架构指导方针。还提供了各种应用程序和基准数据集，以及仍然困扰着GNN的普遍适用性的开放挑战。



![Image](Waikhom_Patgiri_2021_Graph Neural Networks - Methods, Applications, and Opportunities.assets/640-20210923120748284)

https://www.zhuanzhi.ai/paper/4014c909fcaa7d7c7c7d292b6a7febbb



引言





图是定义一组节点及其关系的数据结构。从社交网络[141]到物理互动[209]，我们无处不在地观察它们。图表还可以用来表示不可思议的结构，如原子、分子、生态系统、生物、行星系统[42]等等。



所以，图形结构存在于我们的周围环境和对世界的感知中。它包括实体和相互关系，以建立概念，如推理、沟通、关系、营销等。



随着当今技术的进步，互联网(一个巨大的图表)的使用正在迅速增长。如今，在社交网络、搜索引擎的知识数据库、街道地图、甚至分子、高能物理、生物和化学化合物中也可以找到大量的图表。



图结构表示在这些环境中很常见; 因此，需要有效和新颖的技术来解决基于图的任务。许多传统的机器学习技术都是在使用各种预定义的过程从原始数据表单中提取特征的基础上提出的。提取的特征可以是图像数据中的像素统计，也可以是自然语言数据中的单词出现统计。



在过去的十年中，深度学习(DL)技术获得了巨大的普及，有效地解决了学习问题，从原始数据学习表示，并使用学习的表示同时预测。通常，这是通过探索许多不同的非线性转换(由层执行)和使用基于梯度下降的学习方法对这些模型进行端到端训练来实现的。



尽管DL最近在计算机视觉、自然语言处理、生物医学成像、生物信息学等领域取得了进展，但它仍然缺乏关系和因果推理、智力抽象和其他各种人类能力。



以图的形式构造深度神经网络(DNN)中的计算和表示是解决这些问题的方法之一，这种方法被称为图神经网络(GNN)。



![Image](Waikhom_Patgiri_2021_Graph Neural Networks - Methods, Applications, and Opportunities.assets/640-20210923120748340)



GNN在具有许多学习设置的不同领域的图结构数据集上都是成功的: 有监督、半监督、自监督和无监督。大多数基于图的方法属于无监督学习，通常基于自动编码器、对比学习或随机行走概念。


图自编码器的最新研究成果有:Cao等人[22]在高光谱分类中的特征提取; Yang等人的防止消息传递过平滑[188];Park等人使用消息传递自动编码器进行双曲表示学习[134];用于解决Wu等人[182]提出的当前链路预测方法的局限性。



最近，基于对比学习的方法也很成功，这在许多研究人员的工作中得到了证明。Okuda等[122]是最近出现的一种无监督图表示学习方法，用于发现图像中常见的目标和一组特定目标的定位方法。



学习后的表示可以用于下游的学习任务，如Du等人[41]和Perozzi等人[138]所示。Adhikari等人[2]中的扩展随机游动以及Dong等人[40]中的异构图中的顶点表示也可以捕获子图的嵌入。



本文根据图半监督学习方法的嵌入特征，将其分类为浅图嵌入和深图嵌入。将浅图嵌入分为因子分解、随机游走，将深图嵌入分为自编码器嵌入和GNN嵌入。



本文还提供了对每种方法的进一步解释，以及GNN的类别。基于图的自监督学习方法根据任务和训练策略进行分类。



现有关于GNN的综述论文大多侧重于单一学习设置或一般GNN，如表1所示。这些综述并没有分别解释每种学习环境。Zhou等人[205]最近完成了一项研究，重点研究了图上的各种机器学习算法。



在本文中，我们探讨了每个基于图的学习设置，并将其分为几个类别。本文的主要贡献概述如下: 



- 定义了图的基本术语和变体，以及各种基于图的任务。

- 对GNN进行了全面的综述。我们的工作集中在所有的学习设置，而不同的调查集中在一个单一的学习设置。

- 进一步，每个基于图的学习设置都被探索并划分为所需的类别。

- 给出了GNN体系结构设计的一般指导原则。

- 我们提供许多GNN资源，包括SOTA模型、流行的基于图的数据集和各种应用程序。

- 我们分析了GNN的理论和经验方面，评估了当前技术的挑战，并从模型深度、可扩展性、高阶和复杂结构以及技术的稳健性方面提出了未来可能的研究路线。

  

论文组织





第2节分别介绍GNN的基本术语和概念，然后介绍2.1节和2.2节中基于图结构数据的图的变体和任务。



第3节解释了每个学习设置的基于GNN的方法，并进一步将方法和学习设置分解为逻辑划分。3.1节简要介绍了现有的图监督学习方法。基于图的无监督学习方法在第3.2节中进行了解释，并对现有的学习方法进行了细分。然后我们在第3.3节给出了图半监督学习方法，并通过嵌入方法对这些方法进行了细分。第3.4节介绍了图的自监督学习方法，并根据任务和训练策略对每种方法进行了划分。



GNN的一般step-wise结构在第4节中给出。第6节从理论和实证两个方面对GNN方法进行了分析。



在第5节中，我们介绍了几个在GNN研究中常用的数据集，然后是第7节，介绍了GNN的一些流行应用。第8节总结了在基于GNN的图任务解决方案中仍然存在的尚未解决的问题。最后，在第9部分，我们总结了这项工作。



![Image](Waikhom_Patgiri_2021_Graph Neural Networks - Methods, Applications, and Opportunities.assets/640)





参考资料：

https://www.zhuanzhi.ai/paper/4014c909fcaa7d7c7c7d292b6a7febbb

https://mp.weixin.qq.com/s/RZLWOj-UoWYe588PilVbGw