"""
@File   : model_manager.py
@Author : Ethan Lin
@Date   : 2022/06/14
@Desc   : 
"""

##########################################
# 状态/开发
##########################################

from SystemicRisk import ModelComponent, ProcessComponent, StageComponent, ModelRunner


class ModelManager:
    """
    模型管理器
    """
    model_component: ModelComponent
    process_component: ProcessComponent
    stage_component: StageComponent
    model_runner: ModelRunner
    pass
