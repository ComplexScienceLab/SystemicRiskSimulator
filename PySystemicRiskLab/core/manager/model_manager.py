"""
@File   : model_manager.py
@Author : Ethan Lin
@Date   : 2022/06/14
@Desc   : 
"""

##########################################
# 状态/开发
##########################################

from SystemicRisk.core import ModelComponent, ProcessComponent, StageComponent, ModelContent, ModelRunner, ProcessContent, StageContent, ModelBuilder, ModelScheduler, ModelCollector, ModelSetter


class ModelManager:
    """
    模型管理器
    """
    modelComponent: ModelComponent
    processComponent: ProcessComponent
    stageComponent: StageComponent
    modelContent: ModelContent
    processContent: ProcessContent
    stageContent: StageContent
    run: ModelRunner
    build: ModelBuilder
    schedule: ModelScheduler
    collect: ModelCollector
    set: ModelSetter
    pass
