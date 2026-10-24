# SystemicRiskSimulator 项目指令（canonical）

<!-- aoc:agents-skeleton 请补充本项目专有规则后删除本行 -->

> 本文件是本项目 AI 指令的唯一正文源；CLAUDE.md、.github/copilot-instructions.md 为薄转发壳。
> 详细多根工作区导航见同目录 WORKSPACE_GUIDE.md。

## 身份与写边界（本文件适用范围）

- **本文件适用根**：`/Users/ethan/CoreFiles/ProjectsFile/SystemicRiskSimulator`（绝对路径，唯一）。多根工作区里其他根的指令文件不适用于本根。
- **根清单真源**：`SystemicRiskSimulator.code-workspace`（VSCode 为真源）；工作区增删根后须同步本节，勿凭记忆改。
- **本根可写**：本仓库根目录内的全部内容（源码、`docs/`、配置）；以及下列对应笔记区。
- **对应笔记区（可写）**：
  - 网络级联动力学模型 → `/Users/ethan/Library/Mobile Documents/iCloud~md~obsidian/Documents/CS_notebook/Projects/网络级联动力学模型`
  - SystemicRiskResearch → `/Users/ethan/Library/Mobile Documents/iCloud~md~obsidian/Documents/SystemicRiskResearch`
- **只读依赖（挂载但不可写）**：
  - SystemicRisk-Library → `/Users/ethan/CoreFiles/ProjectsFile/SystemicRiskLab/libraries`
  - relation-entity-component-system → `/Users/ethan/CoreFiles/ProjectsFile/relation-entity-component-system`
  - cascading_dynamics → `/Users/ethan/CoreFiles/ProjectsFile/ComplexSystemLab/ComplexSystemLab/Projects/cascading_dynamics`
  - SystemicRiskLab → `/Users/ethan/CoreFiles/ProjectsFile/SystemicRiskLab`
  - sims_samples → `/Users/ethan/CoreFiles/ProjectsFile/SystemicRiskData/data/sims_samples`
- **禁止写入**：任何未在本节列出的兄弟根；禁止按文档正文出现频次推断归属。
- **归属判据**：笔记项目的工程仓库以其 `_docs-mirror/<仓库名>/` 目录名为准，远程一律取 `git config --get remote.origin.url`（UHW 唯一总设计 §9.16）。

## 项目概述
<!-- TODO: 一到两句说明本项目是什么、技术栈、入口 -->

## 构建与测试
<!-- TODO: 只写非标准命令；AI 搜得到的通用信息不要写 -->

## 禁止与易踩坑
<!-- TODO: 禁改目录、易踩坑、通用性红线等 -->

## 项目结构（速查，详情见 WORKSPACE_GUIDE.md）

- 📚 研究项目 · SystemicRiskSimulator → `./`
