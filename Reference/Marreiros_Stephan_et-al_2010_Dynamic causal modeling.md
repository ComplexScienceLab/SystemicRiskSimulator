# Dynamic causal modeling

## Metadata

* Item Type: [[Article]]
* Authors: [[Andre Marreiros]], [[Klaas Stephan]], [[Karl Friston]]
* Date: [[2010]]
* Date Added: [[2021-10-28]]
* URL: [http://www.scholarpedia.org/article/Dynamic_causal_modeling](http://www.scholarpedia.org/article/Dynamic_causal_modeling)
* DOI: [10/bxd94j](https://doi.org/10/bxd94j)
* Cite key: Marreiros.Stephan.ea_2010
* Topics: [[因果推理]]
, #zotero, #literature-notes, #reference
* PDF Attachments
	- [Marreiros_Stephan_et-al_2010_Dynamic causal modeling.pdf](zotero://open-pdf/library/items/236GRFA4)


##  Zotero links
* [Local library](zotero://select/items/1_BVCWUP8F)
* [Cloud library](http://zotero.org/users/6240833/items/BVCWUP8F)







# Note





对于参数估计：采用贝叶斯方法。

[Dynamic causal modeling - Scholarpedia](http://www.scholarpedia.org/article/Dynamic_causal_modelling)

可以采用EM算法 (Dempster *et al.*, 1977)求解基于高斯分布的贝叶斯估计模型。(Friston *et al.* 2008; Daunizeau *et al.* 2009a)将该方法扩展到随机微分方程。








$$
\begin{gathered}
E-\text { Step }: q \leftarrow \min _{q} F(q, \lambda, m) \\
M-\text { Step }: \lambda \leftarrow \min _{\lambda} F(q, \lambda, m) \\
F(q, \lambda, m)=\langle\ln q(\theta)-\ln p(y \mid \theta, \lambda)-\ln p(\theta \mid m)\rangle_{q} \\
=K L(q \| p(\theta \mid y, \lambda))-\ln (p(y \mid \lambda, m))
\end{gathered}
$$
