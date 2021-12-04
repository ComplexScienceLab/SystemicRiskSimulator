# CAUSAL DISCOVERY WITH REINFORCEMENT LEARNING

## Metadata

* Item Type: [[Article]]
* Authors: [[Shengyu Zhu]], [[Ignavier Ng]], [[Zhitang Chen]]
* Date: [[2020]]
* Date Added: [[2021-10-26]]
* Cite key: Zhu.Ng.ea_2020
* Topics: [[因果科学]], [[强化学习]]
* Tags: #【内容】：强化学习, #⛔-No-DOI-found, #【学科】：统计学, #【内容】：因果发现, #【学科】：人工智能, #zotero, #literature-notes, #reference
* PDF Attachments
	- [Zhu_Ng_et-al_2020_CAUSAL DISCOVERY WITH REINFORCEMENT LEARNING.pdf](zotero://open-pdf/library/items/C6YNCIEE)

## Abstract

Discovering causal structure among a set of variables is a fundamental problem in many empirical sciences. Traditional score-based casual discovery methods rely on various local heuristics to search for a Directed Acyclic Graph (DAG) according to a predeﬁned score function. While these methods, e.g., greedy equivalence search, may have attractive results with inﬁnite samples and certain model assumptions, they are less satisfactory in practice due to ﬁnite data and possible violation of assumptions. Motivated by recent advances in neural combinatorial optimization, we propose to use Reinforcement Learning (RL) to search for the DAG with the best scoring. Our encoder-decoder model takes observable data as input and generates graph adjacency matrices that are used to compute rewards. The reward incorporates both the predeﬁned score function and two penalty terms for enforcing acyclicity. In contrast with typical RL applications where the goal is to learn a policy, we use RL as a search strategy and our ﬁnal output would be the graph, among all graphs generated during training, that achieves the best reward. We conduct experiments on both synthetic and real datasets, and show that the proposed approach not only has an improved search ability but also allows a ﬂexible score function under the acyclicity constraint.


##  Zotero links
* [Local library](zotero://select/items/1_37TRMDVV)
* [Cloud library](http://zotero.org/users/6240833/items/37TRMDVV)

