"""
模型 IB2111 之主文件
"""

# import gymnasium as gym
from copy import deepcopy
import numpy as np
import logging

from SystemicRiskSimulator.core.define.define_type import *
from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.operations.executer import Executer
from SystemicRiskSimulator.tools.tools import Tools
from SystemicRiskSimulator.core.algorithms.cascading_failure_single_mechanism_algorithm import (
    run_single_mechanism_cascade,
    run_bank_interbank_cascade,
)


class ModelMain:
    """
    模型 IB2111
    """

    def __init__(
            self,
            model_dict: dict,
            A,
            A_data,
            para: dict,
            sgv: dict,
    ):
        """
        初始化环境

        Args:
            model_dict (dict): 模型字典，包括：

              - 'model_define',
              - 'model_finance',
              - 'model_main',
              - 'model_strategy',

            A (ModelAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量
            model_content (): 模型内容函数
        """
        self.sgv = sgv
        self.A = A
        self.A_data = A_data
        self.para = para
        self.model_strategy = model_dict['model_strategy'](np.array(para['Strategy_default']))  # 初始化 model_strategy 之实例
        self.model_finance = model_dict['model_finance'](A.note.num_bank)  # 初始化 Content_Finance 之实例
        self._cascade_result = None # 存放单机制级联算法的结果

        pass  # function

    def model_action(self):
        """
        模型之执行模型动作
        """

        ia = self.A.BB.con[:, None] & (self.A.IB.Z_IB > 0.0)

        self.A.IB.theta_IB_def = self.model_strategy.update_strategies_variables(
            agent_variable_in=self.A.BB.Shock_IB_def_s,
            agent_variable_update=self.A.IB.theta_IB_def,
            agent_strategies_variable=self.A.note.strategy_Default_IB_def_s,
            agent_interState=self.A.BB.con,
            ia=ia,
            A=self.A,
        )
        # 获取 agents 动作
        idxs_in_con = np.where(self.A.BB.con)[0]  # 轮到执行动作的 agents 的 idxs
        for i in range(self.A.note.num_bank):
            if i in idxs_in_con:
                # 对于轮到执行动作的 agents ，重新计算其动作
                idxs_ia = np.where(ia[i] > 0)
                self.A.AB.actions[i]['theta_IB_def'].append(self.A.IB.theta_IB_def[i, idxs_ia].ravel())
                self.A.AB.actions[i]['mask'].append(True)
            else:
                # #NOTE 方案一：对于没有轮到执行动作的 agents ，直接继续使用上一次执行动作时的动作策略
                self.A.AB.actions[i]['theta_IB_def'].append(self.A.AB.actions[i]['theta_IB_def'][-1])
                self.A.AB.actions[i]['mask'].append(False)
                # # #NOTE 方案二：对于没有轮到执行动作的 agents ，使用空动作策略
                # num_idxs = (self.A.IB.Z_IB[i] > 0).sum()
                # self.A.AB.actions[i]['theta_IB_def'].append(np.array([None] * num_idxs))
                # self.A.AB.actions[i]['mask'].append(False)
                pass  # if
            pass  # for

        # 旧逻辑：根据 theta_IB_def 计算 Shock_IB_def 并更新金融模块
        # 在接入统一机制算法后，Shock_IB_def 的传播由机制层主导，
        # 这里仍然保持赋值与同步，以尽量减少对下游依赖的破坏。
        self.A.IB.Shock_IB_def = self.A.IB.theta_IB_def * self.A.BB.Shock_IB_def_s[:, None]
        Executer.update_variableStep(self.model_finance, 'Shock_IB_def', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

        pass  # function

    def model_content(self):
        """
        模型之步进内容
        """

        # 当 step > 0 且满足继续的条件时，才进行模型的计算
        # if sgv['turn'] > 1 and (self.A.BB.inf.any() and sgv['is_continue_process']):
        if self.sgv['turn'] > 0:

            # 统一使用单机制算法进行 interbank 级联计算
            self.sgv['turn'] += 1
            self.sgv['phase'] = 1
            self.sgv['process_name'] = "InterBankInsolventContagionShock_SingleMechanism"
            logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}")

            # 使用银行间资产负债变量封装的单机制级联算法
            cascade_result = run_bank_interbank_cascade(
                Z_IB=self.A.IB.Z_IB,
                E_all=self.A.BB.E_all,
                Z_IB_all=self.A.BB.Z_IB_all,
                Loss_exIB_init=self.A.BB.Loss_exIB_def_t,
                Loss_IB_init=self.A.BB.Loss_IB_def_t,
                initial_failed_mask=self.A.BB.isv,
                steps=self.para.get('cascade_steps', 200),
                seed=self.para.get('random_seed', None),
                load_redundancy=self.para.get('load_redundancy', 0.0),
                early_stop_patience=self.para.get('early_stop_patience', 10),
                redistribution_mode=self.para.get('redistribution_mode', 'average'),
                redistribution_weights=None,
                random_dirichlet_alpha=self.para.get('random_dirichlet_alpha', 1.0),
                record_history=False,
            )
            self._cascade_result = cascade_result

            final_failed_mask = cascade_result['final_failed_mask']
            load_final = cascade_result.get('load_init')
            capacity = cascade_result.get('capacity')
            if load_final is None or capacity is None:
                # 理论上不会发生，只是防御性判断
                load_final = self.A.BB.Loss_exIB_def_t + self.A.BB.Loss_IB_def_t
                capacity = self.A.BB.E_all + self.A.BB.Z_IB_all

            # 根据最终失效结果，回填本模型的金融量
            self.A.BB.isv = final_failed_mask.copy()
            self.A.BB.br |= self.A.BB.isv

            # 重新计算最终违约量（沿用原有公式）
            total_loss = load_final
            self.A.BB.Loss_IB_def_t = np.maximum(total_loss - self.A.BB.Loss_exIB_def_t, 0.0)
            Executer.update_variableStep(
                self.model_finance,
                'Loss_IB_def_t',
                self.A,
                self.A_data,
                self.para,
                self.sgv,
                is_collect=self.sgv['is_collect'],
                collect=self.sgv['collect'],
            )

            self.A.BB.Default_IB_def_s = np.minimum(
                np.maximum(self.A.BB.Loss_exIB_def_t + self.A.BB.Loss_IB_def_t - self.A.BB.E_all, 0.0),
                self.A.BB.Z_IB_all,
            )
            Executer.update_variableStep(
                self.model_finance,
                'Default_IB_def_s',
                self.A,
                self.A_data,
                self.para,
                self.sgv,
                is_collect=self.sgv['is_collect'],
                collect=self.sgv['collect'],
            )

            self.A.BB.Default_D_def_s = np.maximum(
                self.A.BB.Loss_exIB_def_t + self.A.BB.Loss_IB_def_t
                - (self.A.BB.E_all + self.A.BB.Z_IB_all),
                0.0,
            )
            Executer.update_variableStep(
                self.model_finance,
                'Default_D_def_s',
                self.A,
                self.A_data,
                self.para,
                self.sgv,
                is_collect=self.sgv['is_collect'],
                collect=self.sgv['collect'],
            )

            # 级联结束后，不再有新的对外冲击
            self.A.BB.Shock_IB_def_s[:] = 0.0
            self.A.BB.Shock_D_def_s[:] = 0.0
            self.A.BB.Shock_IB_def_t[:] = 0.0
            self.A.BB.Shock_P_def_t[:] = 0.0

            Executer.update_variableStep(
                self.model_finance,
                'clear all Shock_source',
                self.A,
                self.A_data,
                self.para,
                self.sgv,
                is_collect=self.sgv['is_collect'],
                collect=self.sgv['collect'],
            )
            Executer.update_variableStep(
                self.model_finance,
                'clear all Shock_target',
                self.A,
                self.A_data,
                self.para,
                self.sgv,
                is_collect=self.sgv['is_collect'],
                collect=self.sgv['collect'],
            )
            Executer.update_variableStep(
                self.model_finance,
                'clear all Shock_interbank',
                self.A,
                self.A_data,
                self.para,
                self.sgv,
                is_collect=self.sgv['is_collect'],
                collect=self.sgv['collect'],
            )

            # 计算奖励并判断是否结束
            self.calc_rewards(
                alpha_reward=self.para['alpha_reward'],
                growth_rate=0.2,
                isv=self.A.BB.isv,
                Loss_IB_def_t=self.A.BB.Loss_IB_def_t,
                Default_IB_def_s=self.A.BB.Default_IB_def_s,
            )
            self.A.BB.inf = self.A.BB.isv.copy()
            self.A.BB.con = np.zeros_like(self.A.BB.con, dtype=bool)

        elif self.sgv['turn'] == 0:
            # node_START
            Executer.update_variableStep(self.model_finance, 'all', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新各银行之所有变量，在第一回合开始时

            # node_010 外部资产违约损失冲击
            self.sgv['process_name'] = "ExBankInsolventShock"
            self.sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
            self.sgv['phase'] = 1  # 逐相复位（起始为1）
            logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}")

            self.A.BB.Shock_P_def_t = self.A.BB.A_P * np.array(self.para['Shock_exIB_def_t_percentage'])  # 厂商贷款违约损失冲击
            Executer.update_variableStep(self.model_finance, 'Shock_P_def_t', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 厂商贷款违约损失冲击传导至银行内资产冲击

            self.A.BB.inf = ~self.A.BB.br & (self.A.BB.Shock_P_def_t > 0.0)
            # logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}，银行遭受感染情况：{self.A.BB.inf}")

            # 不再对破产的银行进行传染
            # self.A.BB.Z_other[~self.A.BB.br] += self.A.BB.Z_other[~self.A.BB.br] + self.A.BB.Z_all[self.A.BB.br]  # 破产清算

            self.A.BB.Loss_exIB_def_t[self.A.BB.inf] = self.A.BB.Shock_P_def_t[self.A.BB.inf]  # 非银行间违约损失冲击损失
            Executer.update_variableStep(self.model_finance, 'Loss_exIB_def_t', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            self.A.BB.Default_IB_def_s[self.A.BB.inf] += np.minimum(np.maximum(self.A.BB.Loss_exIB_def_t[self.A.BB.inf] + self.A.BB.Loss_IB_def_t[self.A.BB.inf] - self.A.BB.E_all[self.A.BB.inf], 0), self.A.BB.Z_IB_all[self.A.BB.inf])  # 银行间违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_IB_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新银行间违约量

            self.A.BB.Default_D_def_s[self.A.BB.inf] = np.maximum(self.A.BB.Loss_exIB_def_t[self.A.BB.inf] + self.A.BB.Loss_IB_def_t[self.A.BB.inf] - (self.A.BB.E_all[self.A.BB.inf] + self.A.BB.Z_IB_all[self.A.BB.inf]), 0)  # 商业银行对居民存款应违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_D_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新商业银行对居民存款应违约量

            self.A.BB.Shock_IB_def_s[self.A.BB.inf] = self.A.BB.Default_IB_def_s[self.A.BB.inf]  # 计算应银行内冲击传导至银行间传染冲击
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新违约损失冲击源头变量Shock_def_s

            # ## 计算奖励值 #HACK 无用可以删除
            # self.calc_rewards(
            #     alpha_reward=self.para['alpha_reward'],
            #     r_min=0.0,
            #     isv=self.A.BB.isv,
            #     Loss_IB_def_t=self.A.BB.Loss_IB_def_t,
            #     Default_IB_def_s=self.A.BB.Default_IB_def_s
            # )

            self.A.BB.con = ~self.A.BB.br & (self.A.BB.Shock_IB_def_s > 0.0)
            logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}，银行传染出去情况：{self.A.BB.con}")
            self.A.BB.br |= self.A.BB.isv  # 更新破产银行

            # Collector.collect_agent_data(self.A, self.A_data, self.sgv, self.para, collect=None)

            Executer.update_variableStep(self.model_finance, 'clear all Shock_target', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有冲击目标变量 Shock_target
            Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有银行间冲击变量 Shock_IB

        else:
            raise ValueError("模型错误，需要修复！")
            pass  # if

        # node_END

        pass  # function

    def model_process(self):
        """
        处理模型的主函数，用于在给定环境中运行指定次数的实验，并根据实验参数执行相应的动作。

        Returns:
            None: 该函数不返回任何值，它通过修改传入的参数来更新状态。
        """
        self.model_content()  # 执行首轮轮次级别的步进更新
        self.A.AB.observations = self.get_observations(agent_variable_update=self.A.AB.observations, Loss_IB_def=self.A.IB.Loss_IB_def)  # 获取首次观测

        # 使用单机制机制后，只需在首轮之后运行一次级联即可
        while self.sgv['is_continue_process']:
            self.model_action()

            # 这里的 model_content 会在 turn>0 时调用单机制级联算法
            self.model_content()
            self.A.AB.observations = self.get_observations(agent_variable_update=self.A.AB.observations, Loss_IB_def=self.A.IB.Loss_IB_def)  # 获取首次观测

            self.calc_dones()


        pass  # function

    def calc_rewards(self, alpha_reward=0.5, gamma_reward=0.2, **kwargs):
        """
        计算 agents 奖励值。

        奖励函数公式：

        - 方案一：

        Rewards^{i} =
        \begin{cases}
        \frac{1}{1 + \lambda \cdot Loss_{IB}^{i}}, & \text{若银行 $i$ 未违约} \\
        R_{min}, & \text{若银行 $i$ 违约}
        \end{cases}

        - 方案二：
        # #TODO 考虑新的计算公式

        Args:
            alpha_reward (float): 调节损失对奖励影响的系数，默认值为 1.0。
            gamma_reward (float): 调节违约对奖励影响的系数，默认值为 0.2。

        Returns:

        """

        r"""
        奖励函数公式：
        Rewards^{i} =
        \begin{cases}
        \frac{1}{1 + \lambda \cdot \left( \alpha \cdot Loss_{IB}^{i} + (1 - \alpha) \cdot Default_{IB}^{i} \right)}, & \text{若银行 $i$ 未违约} \\
        R_{min}, & \text{若银行 $i$ 违约}
        \end{cases}       
        """
        # 获取违约状态和损失值
        isv = kwargs['isv']  # 是否违约 (布尔数组)
        # Loss_IB_def_t = kwargs['Loss_IB_def_t']
        # Default_IB_def_s = kwargs['Default_IB_def_s']

        # 归一化数组变量
        Loss_IB_def_t_normalized = Tools.normalize_array(kwargs['Loss_IB_def_t'])
        Default_IB_def_s_normalized = Tools.normalize_array(kwargs['Default_IB_def_s'])
        # 使用 numpy 矢量化计算奖励值 #BUG 设置不合理
        rewards = np.where(
            ~isv,  # 条件：未违约
            1 / (1 + (alpha_reward * Loss_IB_def_t_normalized + (1 - alpha_reward) * Default_IB_def_s_normalized)),  # 未违约时的奖励计算
            gamma_reward * 1 / (1 + (alpha_reward * Loss_IB_def_t_normalized + (1 - alpha_reward) * Default_IB_def_s_normalized))  # 违约时的奖励值
        )

        idxs_in_con = np.where(self.A.BB.con)[0]  # 轮到执行动作的 agents 的 idxs
        for i in range(self.A.note.num_bank):
            if i in idxs_in_con:
                # 对于轮到执行动作的 agents ，计算奖励值，计入此时奖励
                self.A.AB.rewards[i]['values'].append(rewards[i])
                self.A.AB.rewards[i]['mask'].append(True)
            else:
                # #NOTE 方案一：对于没有轮到执行动作的 agents ，计算奖励值，不计入此时奖励
                self.A.AB.rewards[i]['values'].append(rewards[i])
                self.A.AB.rewards[i]['mask'].append(False)
                # # #NOTE 方案二：对于没有轮到执行动作的 agents ，不计算奖励值，不计入此时奖励
                # self.A.AB.rewards[i]['values'].append(None)
                # self.A.AB.rewards[i]['mask'].append(False)
                pass  # if
            pass  # for

        # return rewards
        pass  # function

    def calc_dones(self):
        """
        计算并更新个体的完成状态。

        如果个体在倒闭状态列表中，则将其完成状态设置为 True。

        Args:
            None

        Returns:
            None: 该函数不返回任何值，仅更新内部状态。
        """

        # 如果个体处于倒闭状态，则 done 是 True，否则即使没有倒闭但是都没有感染的，则其余个体之 done 也为 True。
        dones = np.full(self.A.note.num_bank, False)  # 初始化 dones 数组为 False
        dones[self.A.BB.br] = True
        if not self.A.BB.inf.any():
            dones[~self.A.BB.br] = True
            pass  # if

        # 累计各个个体的完成状态
        idxs_in_con = np.where(self.A.BB.con)[0]  # 轮到执行动作的 agents 的 idxs
        for i in range(self.A.note.num_bank):
            if i in idxs_in_con:
                self.A.AB.dones[i]['values'].append(dones[i])
                self.A.AB.dones[i]['mask'].append(True)
            else:
                # #NOTE 方案一：对于没有轮到执行动作的 observations ，不计入更新
                self.A.AB.dones[i]['values'].append(dones[i])
                self.A.AB.dones[i]['mask'].append(False)
                # # #NOTE 方案二：对于没有轮到执行动作的 observations ，计入更新
                # self.A.AB.dones[i]['values'].append(dones[i])
                # self.A.AB.dones[i]['mask'].append(True)
                pass  # if
            pass  # for

        logging.debug(f"            个体完成状态：{dones}")

        # 当模型运行到最大步数时，中断模型的运行
        truncations = np.full(self.A.note.num_bank, False)  # 初始化 truncations 数组为 False
        if self.sgv['step'] >= self.sgv['test_max_num_of_turn']:
            if self.sgv['is_develope_mode']:  # #HACK 只有在开发模式下才开启这个判断
                logging.error(f"实验{self.sgv['id_experiment']}，模型第{self.sgv['step']}步，模型未能收敛。请检查模型逻辑是否正确！！！")
                truncations[:] = True
                self.sgv['is_continue_process'] = False
            else:
                assert False, f"实验{self.sgv['id_experiment']}，模型第{self.sgv['step']}步，模型未能收敛，程序以非正常方式退出。"  # #BUG 如果遇到并行运行模式，会出现什么情况？
                pass  # if
            pass  # if

        # 累计各个个体的截断状态
        idxs_in_con = np.where(self.A.BB.con)[0]  # 轮到执行动作的 agents 的 idxs
        for i in range(self.A.note.num_bank):
            if i in idxs_in_con:
                self.A.AB.truncations[i]['values'].append(truncations[i])
                self.A.AB.truncations[i]['mask'].append(True)
            else:
                # #NOTE 方案一：对于没有轮到执行动作的 observations ，不计入更新
                self.A.AB.truncations[i]['values'].append(truncations[i])
                self.A.AB.truncations[i]['mask'].append(False)
                # # #NOTE 方案二：对于没有轮到执行动作的 observations ，计入更新
                # self.A.AB.truncations[i]['values'].append(truncations[i])
                # self.A.AB.truncations[i]['mask'].append(True)
                pass  # if
            pass  # for

        if truncations.all() or dones.all():
            self.sgv['is_continue_process'] = False

        pass  # function

    def get_observations(self, agent_variable_update, **kwargs):
        """
        获取各 agents 观测值

        Args:
            agent_variable_update (any): 需要更新的变量
            **kwargs: 自定义的环境模型的动作。包括：

                - 'fullName' (np.ndarray): 银行名称
                - 'Loss_IB_def' (np.ndarray): 银行间资产负债违约损失冲击损失目标
                - 'inf' (np.ndarray): 示性向量之于银行是否资不抵债  #HACK 这个暂时用不到

        Returns:
            numpy.ndarray: PyTorch 可以理解的格式的观测值
        """

        Loss_IB_def = kwargs['Loss_IB_def']  # 银行间资产负债违约损失冲击损失目标

        # #NOTE 方案一：根据邻居数设计成一个列表，列表每一个元素表示一个个体的不同形状的 Numpy 二维数组表示。其中，第一维是数据种类，第二维是观测值向量  #HACK 现在用的
        idxs_in_con = np.where(self.A.BB.con)[0]  # 轮到执行动作的 agents 的 idxs
        mask = self.A.IB.A_IB > 0.0
        for i in range(self.A.note.num_bank):
            agent_observations = np.stack((  # 将不同种类的观测值糅合起来
                Loss_IB_def[i][mask[i]].astype(np.float32),  # 每个个体观测值维度不同
            ), axis=0).ravel()  # 按行展平

            # 将每个个体的观测值添加到列表中
            if i in idxs_in_con:
                agent_variable_update[i]['Loss_IB_def'].append(agent_observations)
                agent_variable_update[i]['mask'].append(True)
            else:
                # #NOTE 方案一：对于没有轮到执行动作的 observations ，仍然使用本次 observations ，但是不计入更新
                agent_variable_update[i]['Loss_IB_def'].append(agent_observations)
                agent_variable_update[i]['mask'].append(False)
                # # #NOTE 方案二：对于没有轮到执行动作的 observations ，仍然使用本次 observations ，也计入更新
                # agent_variable_update[i]['Loss_IB_def'].append(agent_observations)
                # agent_variable_update[i]['mask'].append(True)
                pass  # if
            pass  # for

        # #NOTE 方案二：直接用全量的 Numpy 多维数组表示。其中第一维是个体，第二维是数据种类，第三维是观测值向量
        # # 将不同种类的观测值糅合起来
        # inf = (self.A.IB.Shock_IB_def > 0.0).T
        # agents_observations = np.stack((
        #     self.A.IB.Loss_IB_def,
        #     inf.astype(np.int8)
        # ), axis=0)
        # converted_agents_observations = agents_observations.transpose(1, 0, 2).reshape(-1)  # 按照优先级为先行（个体之变量之向量）、再页（变量）、最后列（个体之间）的顺序展平

        if self.sgv['is_use_Gym_environments']:
            # #NOTE 方案三：用可变字典列表表示  #HACK 如果不再使用 Gym 开发，那么这个不需要，可以删除
            # converted_agents_observations = {}
            # id_agents = kwargs['id_agent']
            # for i in range(self.A.note.num_bank):  # 遍历各家银行
            #     idxs = np.where(self.A.IB.A_IB[i] > 0)
            #     Loss_IB_def = {}
            #     inf = {}
            #     for j in range(len(idxs[0])):  # 遍历银行间关联
            #         Loss_IB_def.update({id_agents[j]: kwargs['Loss_IB_def'][idxs[0][j]]})
            #         inf.update({id_agents[j]: kwargs['inf'][idxs[0][j]]})
            #         pass  # for
            #     gym_agent_observations = dict(
            #         {
            #             'Loss_IB_def': Loss_IB_def,
            #             'inf': inf,
            #         }
            #     )
            #     converted_agents_observations.update({id_agents[i]: gym_agent_observations})
            #     pass  # for

            # #NOTE 方案四：用固定数组和示性数组表示
            converted_agents_observations = []
            id_agents = list(kwargs['id_agent'])
            for i in range(self.A.note.num_bank):  # 遍历各家银行
                idxs = np.where(self.A.IB.A_IB[i] > 0)
                Loss_IB_def = np.zeros_like(self.A.IB.A_IB[i], dtype=MoneyType)
                inf = np.full(len(self.A.IB.A_IB[i]), False, dtype=bool)
                for j in range(len(idxs[0])):  # 遍历银行间关联
                    Loss_IB_def[idxs[0][j]] = kwargs['Loss_IB_def'][idxs[0][j]]
                    inf[idxs[0][j]] = True if kwargs['inf'][idxs[0][j]] is True else False
                    pass  # for
                gym_agent_observations = dict(
                    {
                        'Loss_IB_def': Loss_IB_def,
                        'inf': inf.astype(np.int8)
                    }
                )
                converted_agents_observations.append(gym_agent_observations)
                pass  # for

            pass  # if

        # #NOTE 方案四：用 PyG 数据结构表示 #HACK 以后再考虑
        pass

        converted_agents_observations = agent_variable_update

        return converted_agents_observations
        pass  # function

    pass  # class
