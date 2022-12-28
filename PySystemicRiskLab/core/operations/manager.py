"""
程序管理机HACK已经过时需要改，可能会废弃
"""



from SystemicRisk.core import ModelComponent, ProcessComponent, StageComponent, ModelContent, ModelRunner, ProcessContent, StageContent, ModelBuilder, ModelScheduler, ModelCollector, ModelSetter


class ModelManager:
    """
    模型管理机
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
