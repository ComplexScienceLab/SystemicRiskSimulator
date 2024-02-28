"""
基于 Gymnasium 的环境模型模板，用于构建多主体强化学习环境。
#状态/未开发
"""
import gymnasium as gym
import ray

from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.executer import Executer
# from .content_finance import content_Finance


# from ray.rllib.agents.ppo import PPOTrainer

class gymnasium_environment (gym.Env):
    """
    多主体强化学习环境，基于 RLlib 的环境模型 #NOW
    """

    def __init__(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict, env_config=None):
        self.observation_space = gym.spaces.Dict({
            'observation_matrix': gym.spaces.Box(low=0.0, high=1.0, shape=(sgv['num_bank'], sgv['num_bank']), dtype=np.float32),
            'isEnable_observation_matrix': gym.spaces.Box(low=0.0, high=1.0, shape=(sgv['num_bank'], sgv['num_bank']), dtype=bool)
        })  # TODO 这里需要引入模型的可观测观察变量
        self.action_space = gym.spaces.Box(low=0.0, high=1.0, shape=(sgv['num_bank']), dtype=np.float32)  # TODO 这里需要引入模型的动作空间
        pass  # function

    def reset(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        self.banks = A.BB  # TODO
        self.goals = np.zeros(sgv['num_bank'])  # TODO
        pass  # function

    def step(self, action):

        pass  # function #NOW

    def done(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        return sgv['is_continue_process'] == False
        pass  # function

    def get_observations(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        observation = {}
        observation['isEnable_observation_matrix'] = np.zeros((sgv['num_bank'], sgv['num_bank']))
        observation['isEnable_observation_matrix'] = np.full((sgv['num_bank'], sgv['num_bank']), False, dtype=bool)
        indices = np.where(A.IB.A_IB > 0)
        for i in range(len(indices[0])):
            observation['isEnable_observation_matrix'][indices[0][i], indices[1][i]] = True
            pass  # for
        return observation
        pass  # function

    # 定义环境之观察空间
    observation_space = gym.spaces  # TODO 这里需要引入模型

    # 定义环境之动作空间 #TODO 这里需要引入模型动作

    # 定义环境之奖励
    def get_rewards(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        rewards = np.zeros(sgv['num_bank'])
        rewards[A.BB.isv] = -1.0  # TODO 这个值需要提取为超参数
        return rewards
        pass  # function

    pass  # class