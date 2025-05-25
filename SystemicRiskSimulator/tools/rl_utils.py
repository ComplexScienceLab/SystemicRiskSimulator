"""

"""

from dataclasses import dataclass
import json
import logging
from pathlib import Path

import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import collections
import random


class RlUtils:
    """
    强化学习工具类
    """

    @staticmethod
    def moving_average(a, window_size):
        """
        计算滑动平均  #HACK 目前没用到
        """
        cumulative_sum = np.cumsum(np.insert(a, 0, 0))
        middle = (cumulative_sum[window_size:] - cumulative_sum[:-window_size]) / window_size
        r = np.arange(1, window_size - 1, 2)
        begin = np.cumsum(a[:window_size - 1])[::2] / r
        end = (np.cumsum(a[:-window_size:-1])[::2] / r)[::-1]
        return np.concatenate((begin, middle, end))
        pass  # function

    @staticmethod
    def train_on_policy_agent(env, agent, num_episodes):
        """
        训练一个基于策略的代理  #HACK 目前没用到
        """
        return_list = []
        for i in range(10):
            with tqdm(total=int(num_episodes / 10), desc='Iteration %d' % i) as pbar:
                for i_episode in range(int(num_episodes / 10)):
                    episode_return = 0
                    transition_dict = {'states': [], 'actions': [], 'next_states': [], 'rewards': [], 'dones': []}
                    state = env.reset()
                    done = False
                    while not done:
                        action = agent.take_action(state)
                        next_state, reward, done, _ = env.step(action)
                        transition_dict['states'].append(state)
                        transition_dict['actions'].append(action)
                        transition_dict['next_states'].append(next_state)
                        transition_dict['rewards'].append(reward)
                        transition_dict['dones'].append(done)
                        state = next_state
                        episode_return += reward
                    return_list.append(episode_return)
                    agent.update(transition_dict)
                    if (i_episode + 1) % 10 == 0:
                        pbar.set_postfix({'episode': '%d' % (num_episodes / 10 * i + i_episode + 1), 'return': '%.3f' % np.mean(return_list[-10:])})
                    pbar.update(1)
        return return_list
        pass  # function

    @staticmethod
    def train_off_policy_agent(env, agent, num_episodes, replay_buffer, minimal_size, batch_size):
        """
        训练一个基于离策略的代理  #HACK 目前没用到

        Args:

        - env (gym.Env): 环境
        - agent (Agent): 代理
        - num_episodes (int): 训练的总轮数
        - replay_buffer (ReplayBuffer): 经验回放缓冲区
        - minimal_size (int): 经验回放缓冲区的最小大小
        - batch_size (int): 批大小

        Returns:

        - list: 返回列表

        Examples:

        ```python
        env = gym.make('CartPole-v1')
        agent = DQNAgent(env)
        replay_buffer = ReplayBuffer(10000)
        return_list = train_off_policy_agent(env, agent, 1000, replay_buffer, 1000, 32)
        ```


        """
        return_list = []
        for i in range(10):
            with tqdm(total=int(num_episodes / 10), desc='Iteration %d' % i) as pbar:
                for i_episode in range(int(num_episodes / 10)):
                    episode_return = 0
                    state = env.reset()
                    done = False
                    while not done:
                        action = agent.take_action(state)
                        next_state, reward, done, _ = env.step(action)
                        replay_buffer.add(state, action, reward, next_state, done)
                        state = next_state
                        episode_return += reward
                        if replay_buffer.size() > minimal_size:
                            b_s, b_a, b_r, b_ns, b_d = replay_buffer.sample(batch_size)
                            transition_dict = {'states': b_s, 'actions': b_a, 'next_states': b_ns, 'rewards': b_r, 'dones': b_d}
                            agent.update(transition_dict)
                    return_list.append(episode_return)
                    if (i_episode + 1) % 10 == 0:
                        pbar.set_postfix({'episode': '%d' % (num_episodes / 10 * i + i_episode + 1), 'return': '%.3f' % np.mean(return_list[-10:])})
                    pbar.update(1)
        return return_list
        pass  # function

    @staticmethod
    def compute_advantage(gamma, lmbda, td_delta):
        """
        计算优势

        在 JoyRL 书中，相关理论可以在以下部分找到：

        《第 4 章 策略梯度》：

        在 docs/chapter4/chapter4.md 中提到 优势函数（Advantage Function） 的定义和作用：
        优势函数 $A(s, a)$ 的公式为： $$ A(s, a) = Q(s, a) - V(s) $$ 其中 $Q(s, a)$ 是动作价值函数，$V(s)$ 是状态价值函数。
        通过优势函数可以衡量某个动作相对于其他动作的好坏程度。
        《第 5 章 PPO 算法》：

        在 docs/chapter5/chapter5.md 中提到 广义优势估计（GAE） 的公式：
        GAE 的核心公式为： $$ \hat{A}t = \sum{l=0}^\infty (\gamma \lambda)^l \delta_{t+l} $$ 其中 $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$ 是 TD 残差，$\gamma$ 是折扣因子，$\lambda$ 是 GAE 的平滑参数。
        《第 9 章 演员-评论员算法》：

        在 docs/chapter9/chapter9.md 中提到 优势函数的计算：
        提到优势函数的计算公式为： $$ A(s, a) = r + \gamma V(s') - V(s) $$ 并解释了如何通过 TD 残差和 GAE 来估计优势。

        Args:

        - gamma (float): 折扣因子
        - gae_lambda (float): GAE参数
        - td_delta (torch.Tensor): TD误差

        Returns:

        - torch.Tensor: 优势

        """
        td_delta = td_delta.detach().numpy()
        advantage_list = []
        advantage = 0.0
        for delta in td_delta[::-1]:
            advantage = gamma * lmbda * advantage + delta
            advantage_list.append(advantage)
        advantage_list.reverse()
        return torch.tensor(advantage_list, dtype=torch.float)

        pass  # function

    @staticmethod
    def save_training_data(model_algorithm, folderpath_save):
        """
        保存训练数据并打印待保存的参数。

        Args:
            model_algorithm (ModelAlgorithm): 模型算法对象，包含 actor、critic 和优化器。
            folderpath_save (str): 保存文件夹路径。

        Returns:
            None

        Examples:
            >>> RlUtils.save_training_data_with_logging(model_algorithm)
        """

        save_folder_path = Path(folderpath_save)
        save_folder_path.mkdir(parents=True, exist_ok=True)  # 如果文件夹不存在则创建

        # 打印并保存策略网络状态字典
        actor_state_dict_path = save_folder_path / 'actor_state_dict.pth'
        print(f"Saving actor state dict to {actor_state_dict_path}")  # 打印保存路径
        torch.save(model_algorithm.actor.state_dict(), actor_state_dict_path)  # 保存策略网络状态字典

        # 打印并保存价值网络状态字典
        critic_state_dict_path = save_folder_path / 'critic_state_dict.pth'
        print(f"Saving critic state dict to {critic_state_dict_path}")  # 打印保存路径
        torch.save(model_algorithm.critic.state_dict(), critic_state_dict_path)  # 保存价值网络状态字典

        # 打印并保存策略网络优化器状态字典
        actor_optimizer_state_dict_path = save_folder_path / 'actor_optimizer_state_dict.pth'
        print(f"Saving actor optimizer state dict to {actor_optimizer_state_dict_path}")  # 打印保存路径
        torch.save(model_algorithm.actor_optimizer.state_dict(), actor_optimizer_state_dict_path)  # 保存策略网络优化器状态字典

        # 打印并保存价值网络优化器状态字典
        critic_optimizer_state_dict_path = save_folder_path / 'critic_optimizer_state_dict.pth'
        print(f"Saving critic optimizer state dict to {critic_optimizer_state_dict_path}")  # 打印保存路径
        torch.save(model_algorithm.critic_optimizer.state_dict(), critic_optimizer_state_dict_path)  # 保存价值网络优化器状态字典

        # 打印并保存超参数
        hyperparameters = {
            'gamma': model_algorithm.gamma,
            'gae_lambda': model_algorithm.gae_lambda,
            'num_update_epochs': model_algorithm.num_update_epochs,
            'eps': model_algorithm.eps
        }
        hyperparameters_path = save_folder_path / 'hyperparameters.json'
        print(f"Saving hyperparameters to {hyperparameters_path}")  # 打印保存路径
        print(f"Hyperparameters: {json.dumps(hyperparameters, indent=4)}")  # 打印超参数
        with hyperparameters_path.open('w') as f:
            json.dump(hyperparameters, f, indent=4)  # 保存超参数

        pass  # function

    @staticmethod
    def load_training_data(model_algorithm, folderpath_load):
        """
        加载训练数据，包括模型状态字典、优化器状态字典和超参数。

        Args:
            model_algorithm (ModelAlgorithm): 模型算法对象，包含 actor、critic 和优化器。
            folderpath_load (str): 加载文件夹路径。

        Returns:
            dict: 加载的超参数。

        Examples:
            >>> hyperparameters = RlUtils.load_training_data(model_algorithm)
        """

        # 加载策略网络状态字典
        actor_state_dict_path = Path(folderpath_load) / 'actor_state_dict.pth'
        if actor_state_dict_path.exists():
            print(f"Loading actor state dict from {actor_state_dict_path}")  # 打印加载路径
            model_algorithm.actor.load_state_dict(torch.load(actor_state_dict_path))  # 加载策略网络状态字典
        else:
            print(f"Actor state dict not found at {actor_state_dict_path}")  # 打印未找到信息

        # 加载价值网络状态字典
        critic_state_dict_path = Path(folderpath_load) / 'critic_state_dict.pth'
        if critic_state_dict_path.exists():
            print(f"Loading critic state dict from {critic_state_dict_path}")  # 打印加载路径
            model_algorithm.critic.load_state_dict(torch.load(critic_state_dict_path))  # 加载价值网络状态字典
        else:
            print(f"Critic state dict not found at {critic_state_dict_path}")  # 打印未找到信息

        # 加载策略网络优化器状态字典
        actor_optimizer_state_dict_path = Path(folderpath_load) / 'actor_optimizer_state_dict.pth'
        if actor_optimizer_state_dict_path.exists():
            print(f"Loading actor optimizer state dict from {actor_optimizer_state_dict_path}")  # 打印加载路径
            model_algorithm.actor_optimizer.load_state_dict(torch.load(actor_optimizer_state_dict_path))  # 加载策略网络优化器状态字典
        else:
            print(f"Actor optimizer state dict not found at {actor_optimizer_state_dict_path}")  # 打印未找到信息

        # 加载价值网络优化器状态字典
        critic_optimizer_state_dict_path = Path(folderpath_load) / 'critic_optimizer_state_dict.pth'
        if critic_optimizer_state_dict_path.exists():
            print(f"Loading critic state dict from {critic_optimizer_state_dict_path}")  # 打印加载路径
            model_algorithm.critic_optimizer.load_state_dict(torch.load(critic_optimizer_state_dict_path))  # 加载价值网络优化器状态字典
        else:
            print(f"Critic optimizer state dict not found at {critic_optimizer_state_dict_path}")  # 打印未找到信息

        # 加载超参数
        hyperparameters_path = Path(folderpath_load) / 'hyperparameters.json'
        if hyperparameters_path.exists():
            print(f"Loading hyperparameters from {hyperparameters_path}")  # 打印加载路径
            with hyperparameters_path.open('r') as f:
                hyperparameters = json.load(f)  # 加载超参数
            print(f"Loaded hyperparameters: {json.dumps(hyperparameters, indent=4)}")  # 打印加载的超参数
            return hyperparameters
        else:
            print(f"Hyperparameters file not found at {hyperparameters_path}")  # 打印未找到信息
            return {}

        pass  # function

    @staticmethod
    def plot_convergence_curve(arr_reward, save_path=None, agent_id=None, use_moving_average=True, window=10):
        """
        绘制收敛曲线（奖励随episode变化的曲线），可选滑动平均。

        Args:
            arr_reward (list or np.ndarray): 每一局的奖励数据数组。
            save_path (str, optional): 图片保存路径。若为None则直接显示。
            agent_id (int, optional): 代理编号。用于保存文件名时区分不同代理。
            window (int): 滑动平均窗口大小。
            use_moving_average (bool): 是否使用滑动平均。默认False，True为滑动平均，False为传统方式。
        """
        plt.figure()
        if use_moving_average and len(arr_reward) >= window:
            # 计算滑动平均
            rewards_ma = np.convolve(arr_reward, np.ones(window) / window, mode='valid')
            plt.plot(np.arange(len(rewards_ma)) + window - 1, rewards_ma, label=f"{window}步滑动平均")
            plt.plot(arr_reward, alpha=0.3, label="原始奖励")
        else:
            # 传统方式：直接画原始奖励曲线
            plt.plot(arr_reward, label="原始奖励")
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.title("收敛曲线（奖励随episode变化）")
        plt.legend()
        if save_path:
            # 如果传入 agent_id，则在文件名中添加个体编号
            if agent_id is not None:
                save_path = Path(save_path)
                save_path = save_path.with_stem(f"{save_path.stem}-agent={agent_id}")
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()
        pass  # function

    pass  # class
