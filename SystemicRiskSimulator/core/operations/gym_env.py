"""
基于 Gymnasium 的环境模型模板，用于构建多主体强化学习环境。#TODO 这个现在模型里面直接定义，等待后续条件成熟了再封装到模拟器。
#进度/未开发 #状态/暂停
"""
import gymnasium as gym
import ray
from SystemicRiskSimulator.external_packages import np
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.executer import Executer
# from .content_finance import Content_Finance


# from ray.rllib.agents.ppo import PPOTrainer

class gymnasium_environment (gym.Env):
    """
    多主体强化学习环境，基于 RLlib 的环境模型 #NOW
    """
    pass  # class