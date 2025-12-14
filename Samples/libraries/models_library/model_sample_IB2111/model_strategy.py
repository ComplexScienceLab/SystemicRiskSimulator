"""
描述多主体相关的功能
"""
from typing import Any

import numpy as np
import numpy.ma as ma
from numpy import ndarray

from SystemicRiskSimulator.core.define.define_type import StateType, MoneyType


# @dataclass
class ModelStrategy:
    """
    各银行更新计算相关的功能。包括奖励、观测值、动作值等
    """
    from .model_define import ModelAgent
    # from .model_RL_algorithm import ModelAlgorithm

    strategy_presetImported: np.array  # 预置固定的策略变量

    def __init__(self, strategy_presetImported: np.array):
        """
        初始化各银行之更新计算相关的功能。

        Args:
            strategy_presetImported (np.array): 预置固定的策略变量
        """
        self.strategy_presetImported = strategy_presetImported

        # 创建一个字典，映射 by_way 的值到对应的方法
        self.dict_update_methods = {
            # NOTE：功能函数集：更新流之商业银行之预置的或者学习的行为决策相关的功能
            'Strategy_应还尽还': self.update_by_Strategy_应还尽还,
            'Strategy_等级完全相同': self.update_by_Strategy_等级完全相同,
            'Strategy_均匀分布随机': self.update_by_Strategy_均匀分布随机,
            'Strategy_导入预置的': self.update_by_Strategy_导入预置的,
        }
        pass

    def update_strategies_variables(
            self,
            agent_variable_in,
            agent_variable_update,
            agent_strategies_variable,
            agent_interState: StateType,
            ia: StateType,
            A: ModelAgent
    ) -> ndarray | None | Any:
        """
        更新各个体之相关的各策略函数变量。

        - 总体部分：
            - `Strategy_等级完全相同`: self.update_by_Strategy_等级完全相同,
            - `Strategy_均匀分布随机`: self.update_by_Strategy_均匀分布随机,
            - `Strategy_应还尽还`: self.update_by_Strategy_应还尽还,
            - `Strategy_导入预置的`: self.update_by_Strategy_导入预置的,

        Args:
            agent_variable_in (np.ndarray): 个体众之输入的源变量
            agent_variable_update (np.ndarray): 个体众之待更新的变量
            agent_strategies_variable (np.ndarray): 个体众之策略变量
            agent_interState (StateType): 个体众之交互状态之状态示性向量
            ia (StateType): 个体间之传染方对感染方之状态示性邻接矩阵
            A (ModelAgent): 个体众

        Returns:
            agent_variable_out (np.ndarray): 更新后的个体众之变量值
        """
        if agent_interState.sum() != 0:  # 表示存在潜在的需要更新策略的个体
            dict_maskArray_of_strategy = self.calc_dict_maskArray_variable_strategies(agent_strategies_variable)
            # 按照策略类型，依次更新各银行之变量
            for strategy, strategy_maskArray in dict_maskArray_of_strategy.items():
                idxs_row = (strategy_maskArray & agent_interState)  # 获取符合条件的行索引
                if idxs_row.sum() != 0:
                    agent_variable_update[idxs_row, :] = self.dict_update_methods[strategy](agent_variable_in[idxs_row], agent_variable_update[idxs_row, :], A, idxs_row, ia)  # 使用字典来调用对应的方法
                else:
                    agent_variable_update[idxs_row, :] = 0.0  # 如果没有符合条件的行，则返回全 0 的数组
                    pass  # if
                pass  # for
            pass  # if

        return agent_variable_update
        pass  # function


    # NOTE：功能函数集：其它功能函数

    def calc_dict_of_maskArray_of_strategy_style(self, strategy_style, A: ModelAgent):
        """
        计算各银行之智库之决策方式的掩码数组字典。键名是决策方式，键值是对应的掩码数组。

        Args:
            strategy_style (np.ndarray): 银行个体众之决策方式
        Returns:
            dict_maskArray_of_strategy_style (dict): 各银行之决策方式的掩码数组字典
        """
        current_strategy_styles = np.unique(strategy_style)
        dict_maskArray_of_strategy_style = {current_strategy_style: A.note.strategy_method == current_strategy_style for current_strategy_style in current_strategy_styles}
        return dict_maskArray_of_strategy_style
        pass  # function

    def calc_dict_maskArray_variable_strategies(self, array_strategy_bankVariable: np.ndarray):
        """
        计算各银行之智库之银行间在指定的变量之策略之掩码数组字典。键名是决策方式，键值是对应的策略之掩码数组。

        Args:
            array_strategy_bankVariable (np.ndarray): 银行个体众之指定的变量之策略

        Returns:
            dict_maskArray_of_strategy (dict): 银行个体众之指定的变量之策略之掩码数组字典
        """
        current_strategies = np.unique(array_strategy_bankVariable)
        dict_maskArray_of_strategy = {current_strategy: array_strategy_bankVariable == current_strategy for current_strategy in current_strategies}
        return dict_maskArray_of_strategy
        pass  # function

    # NOTE：功能函数集：计算商业银行之预置的行为决策相关的功能
    def calc_Strategy_等级完全相同(self, bank_variable_in, agent_variable_update, A, idxs_row: StateType, ia: StateType):
        """
        计算策略：等级完全相同。
        按照一个指标，等比例分配变量值。如果在银行，就是银行偿付等级完全相同。结果值满足约束条件。

        Args:
            bank_variable_in (np.ndarray): 输入的银行变量。
            agent_variable_update (np.ndarray): 待更新的银行变量。
            A (ModelAgent): 个体众
            idxs_row (StateType): 待运行的行索引
            ia (StateType): 银行间索引

        Returns:
            agent_variable_update (np.ndarray): 待计算的银行变量
        """

        # #HACK 带索引的旧的版本
        #
        # # 计算银行间各资不抵债银行违约比率
        # agent_variable_update[idxs_row, :] = bank_variable_in[idxs_row, None] * np.divide(
        #     A.IB.Z_IB[idxs_row, :],
        #     A.BB.Z_IB_all[idxs_row, np.newaxis],
        #     out=np.zeros_like(A.IB.Z_IB[idxs_row, :]),
        #     where=A.BB.Z_IB_all[idxs_row, np.newaxis] != 0
        # )
        #
        # # 归一化操作
        # agent_variable_update[idxs_row, :] = np.divide(
        #     agent_variable_update[idxs_row, :],
        #     agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True),
        #     out=np.zeros_like(agent_variable_update[idxs_row, :]),
        #     where=agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True) != 0
        # )
        #
        # return agent_variable_update[idxs_row, :]  # 返回对应行的值

        # #HACK 不带索引的现在的版本

        # 计算银行间各资不抵债银行违约比率
        agent_variable_update = bank_variable_in[:, None] * np.divide(
            A.IB.Z_IB[idxs_row, :],
            A.BB.Z_IB_all[idxs_row, np.newaxis],
            out=np.zeros_like(A.IB.Z_IB[idxs_row, :]),
            where=A.BB.Z_IB_all[idxs_row, np.newaxis] != 0
        )

        # 归一化操作
        agent_variable_update = np.divide(
            agent_variable_update,
            agent_variable_update.sum(axis=1, keepdims=True),
            out=np.zeros_like(agent_variable_update),
            where=agent_variable_update.sum(axis=1, keepdims=True) != 0
        )

        return agent_variable_update  # 返回对应行的值
        pass  # function

    def calc_Strategy_均匀分布随机(self, bank_variable_in, agent_variable_update, A: ModelAgent, idxs_row: StateType, ia: StateType):
        """
        计算策略：按照均匀分布随机分配变量值。结果值满足约束条件。

        这里用了狄利克雷分布。

        Args:
            bank_variable_in (np.ndarray): 输入的银行变量。
            agent_variable_update (np.ndarray): 待更新的银行变量。
            A (ModelAgent): 个体众
            idxs_row (StateType): 待运行的行索引
            ia (StateType): 银行间索引

        Returns:
            agent_variable_update (np.ndarray): 待计算的银行变量
        """

        # #HACK 带索引的旧的版本
        #
        # Z_IB_mark = ma.masked_array(A.IB.Z_IB, mask=~ia)  # 获取未被掩码的Z_IB值
        #
        # n_banks_per_row = ia.sum(axis=1)  # 计算每行的有效列数
        #
        # random_ratios = np.zeros_like(Z_IB_mark)
        # default_values = np.zeros_like(Z_IB_mark)
        # for i, n in enumerate(n_banks_per_row):
        #     if n > 0:
        #         random_ratios[i, ia[i]] = np.random.dirichlet(np.ones(n), size=1)  # 生成Dirichlet分布的随机数
        #         default_values[i, ia[i]] = random_ratios[i, ia[i]] * bank_variable_in[i]  # 计算违约值
        #         pass  # if
        #     pass  # for
        #
        # default_values_2 = np.minimum(default_values, Z_IB_mark)  # 限制违约值不超过Z_IB的值
        # # 计算限制违约值之后，违约值的减少量总和
        # default_values_diff = (default_values - default_values_2).filled(0.0)  # 计算违约值的差异
        # default_values_diff_sum = default_values_diff.sum(axis=1, keepdims=True)  # 计算每行的违约值差异总和
        #
        # # 减少的那些违约值统一按照类似等级完全相同的分配算法分配给其余的债权银行 #TODO  这个是权宜之计，后续需要改进尽可能实现均匀分布随机
        # agent_variable_update_2 = np.zeros_like(agent_variable_update)
        # agent_variable_update_2[idxs_row, :] = default_values_diff_sum[idxs_row] * np.divide(
        #     (A.IB.Z_IB[idxs_row, :] - default_values_2[idxs_row, :]),
        #     (A.IB.Z_IB[idxs_row, :] - default_values_2[idxs_row, :]).sum(axis=1, keepdims=True),
        #     out=np.zeros_like(A.IB.Z_IB[idxs_row, :]),
        #     where=(A.IB.Z_IB[idxs_row, :] - default_values_2[idxs_row, :]).sum(axis=1, keepdims=True) != 0
        # )
        #
        # agent_variable_update = default_values_2.filled(0.0) + agent_variable_update_2
        #
        # # 归一化操作
        # agent_variable_update[idxs_row, :] = np.divide(
        #     agent_variable_update[idxs_row, :],
        #     agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True),
        #     out=np.zeros_like(agent_variable_update[idxs_row, :]),
        #     where=agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True) != 0
        # )
        #
        # return agent_variable_update[idxs_row, :]  # 返回对应行的值

        # #HACK 不带索引的现在的版本

        Z_IB_mark = ma.masked_array(A.IB.Z_IB[idxs_row], mask=~ia[idxs_row])  # 获取未被掩码的Z_IB值

        n_banks_per_row = ia[idxs_row].sum(axis=1)  # 计算每行的有效列数

        random_ratios = np.zeros_like(Z_IB_mark)
        default_values = np.zeros_like(Z_IB_mark)
        for i, n in enumerate(n_banks_per_row):
            if n > 0:
                random_ratios[i, ia[idxs_row][i]] = np.random.dirichlet(np.ones(n), size=1)  # 生成 Dirichlet 分布的随机数
                default_values[i, ia[idxs_row][i]] = random_ratios[i, ia[idxs_row][i]] * bank_variable_in[i]  # 计算违约值
                pass  # if
            else:
                default_values[i, ia[idxs_row][i]] = 0.0  # 如果没有有效列，则将违约值设为0
            pass  # for

        default_values_2 = np.minimum(default_values, Z_IB_mark)  # 限制违约值不超过Z_IB的值
        # 计算限制违约值之后，违约值的减少量总和
        default_values_diff = (default_values - default_values_2).filled(0.0)  # 计算违约值的差异
        default_values_diff_sum = default_values_diff.sum(axis=1, keepdims=True)  # 计算每行的违约值差异总和

        # 减少的那些违约值统一按照类似等级完全相同的分配算法分配给其余的债权银行 #TODO  这个是权宜之计，后续需要改进尽可能实现均匀分布随机
        agent_variable_update_2 = default_values_diff_sum * np.divide(
            (A.IB.Z_IB[idxs_row, :] - default_values_2),
            (A.IB.Z_IB[idxs_row, :] - default_values_2).sum(axis=1, keepdims=True),
            out=np.zeros_like(A.IB.Z_IB[idxs_row, :]),
            where=(A.IB.Z_IB[idxs_row, :] - default_values_2).sum(axis=1, keepdims=True) != 0
        )

        agent_variable_update = default_values_2.filled(0.0) + agent_variable_update_2

        # 归一化操作
        agent_variable_update = np.divide(
            agent_variable_update,
            agent_variable_update.sum(axis=1, keepdims=True),
            out=np.zeros_like(agent_variable_update),
            where=agent_variable_update.sum(axis=1, keepdims=True) != 0
        )

        return agent_variable_update  # 返回对应行的值
        pass  # function

    def calc_Strategy_应还尽还(self, bank_variable_in, agent_variable_update, A: ModelAgent, idxs_row: StateType, ia: StateType):
        """
        计算策略：应还尽还。即按照各银行之应还尽还原则，结果值满足约束条件。

        Args:
            bank_variable_in (np.ndarray): 输入的银行变量。
            agent_variable_update (np.ndarray): 待更新的银行变量。
            A (ModelAgent): 个体众
            idxs_row (StateType): 待运行的行索引
            ia (StateType): 银行间索引

        Returns:
            agent_variable_update (np.ndarray): 待计算的银行变量
        """

        # # #HACK 带索引的旧的版本
        #
        # available = np.zeros_like(A.BB.Z_IB_all)
        # # available[idxs_row] = A.BB.A_Q[idxs_row]  # 计算可以偿还的量 #BUG 这里只是计算违约值，不需要 A.BB.A_Q 垫付，所以应该用下面一行的计算式
        # available[idxs_row] = A.BB.Z_IB_all[idxs_row] - bank_variable_in[idxs_row]  # 计算可以偿还的量
        #
        # Z_IB_mark = ma.masked_values(A.IB.Z_IB, A.IB.Z_IB > 0)  # 获取待偿还金额。
        # Z_IB_priority = np.sort(Z_IB_mark, axis=1)  # 待偿还金额越小优先级越高
        # Z_IB_priority_indices = np.argsort(Z_IB_mark, axis=1)
        # Z_IB_priority_cumsum = np.cumsum(Z_IB_priority, axis=1)  # 计算 Z_IB_priority 的累加数组
        # default_values_sort = np.maximum(0.0, np.minimum(Z_IB_priority, Z_IB_priority_cumsum - available[:, np.newaxis]))  # 按照优先级依次计算违约值
        # default_values = np.zeros_like(default_values_sort)
        # np.put_along_axis(default_values, Z_IB_priority_indices, default_values_sort, axis=1)  # 根据 Z_IB_priority_indices 重新排序
        #
        # # #HACK 这段是计算违约比例的。目前不需要。改为下面一段的直接计算违约值然后返回 agent_variable_update
        # # # bank_variable_masked = default_values / Z_IB_mark  # 计算比例  #HACK 旧的计算违约比例，是根据 Z_IB_mark 计算的违约比例，似乎从模型设计的逻辑上来说不合理。
        # # default_values_sum = default_values.sum(axis=1, keepdims=True)  # 获取待偿还金额的行和
        # # bank_variable_masked = np.divide(default_values, default_values_sum, out=np.zeros_like(default_values), where=default_values_sum != 0)  # 计算变量自身分配的比例
        # # agent_variable_update[idxs_row] = bank_variable_masked.filled(0.0)[idxs_row]  # 转换普通数组
        #
        # agent_variable_update[idxs_row] = default_values[idxs_row]  # 直接计算违约值然后返回 agent_variable_update
        #
        # # 归一化操作
        # agent_variable_update[idxs_row, :] = np.divide(
        #     agent_variable_update[idxs_row, :],
        #     agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True),
        #     out=np.zeros_like(agent_variable_update[idxs_row, :]),
        #     where=agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True) != 0
        # )
        #
        # return agent_variable_update[idxs_row, :]  # 返回对应行的值

        # #HACK 不带索引的现在的版本

        # available[idxs_row] = A.BB.A_Q[idxs_row]  # 计算可以偿还的量 #BUG 这里只是计算违约值，不需要 A.BB.A_Q 垫付，所以应该用下面一行的计算式
        available = A.BB.Z_IB_all[idxs_row] - bank_variable_in  # 计算可以偿还的量

        Z_IB_mark = ma.masked_values(A.IB.Z_IB[idxs_row], A.IB.Z_IB[idxs_row] > 0)  # 获取待偿还金额。
        Z_IB_priority = np.sort(Z_IB_mark, axis=1)  # 待偿还金额越小优先级越高
        Z_IB_priority_indices = np.argsort(Z_IB_mark, axis=1)
        Z_IB_priority_cumsum = np.cumsum(Z_IB_priority, axis=1)  # 计算 Z_IB_priority 的累加数组
        default_values_sort = np.maximum(0.0, np.minimum(Z_IB_priority, Z_IB_priority_cumsum - available[:, np.newaxis]))  # 按照优先级依次计算违约值
        default_values = np.zeros_like(default_values_sort)
        np.put_along_axis(default_values, Z_IB_priority_indices, default_values_sort, axis=1)  # 根据 Z_IB_priority_indices 重新排序
        agent_variable_update = default_values  # 直接计算违约值然后返回 agent_variable_update

        # 归一化操作
        agent_variable_update = np.divide(
            agent_variable_update,
            agent_variable_update.sum(axis=1, keepdims=True),
            out=np.zeros_like(agent_variable_update),
            where=agent_variable_update.sum(axis=1, keepdims=True) != 0
        )

        return agent_variable_update  # 返回对应行的值
        pass  # function

    def calc_Strategy_导入预置的(self, bank_variable_in, agent_variable_update, A: ModelAgent, idxs_row: StateType, ia: StateType):
        """
        计算策略：按照预置的策略固定分配占比。各比例之和为1。通过读取获取固定的策略变量。

        这个方法计算完成后还需要根据实际约束条件修正值。

        Args:
            bank_variable_in (np.ndarray): 输入的银行变量。
            agent_variable_update (np.ndarray): 待更新的银行变量。
            A (ModelAgent): 个体众
            idxs_row (StateType): 待运行的行索引
            ia (StateType): 银行间索引

        Returns:
            agent_variable_update (np.ndarray): 待计算的银行变量
        """

        # # #HACK 带索引的旧的版本
        #
        # default_ratio = self.strategy_presetImported  # 导入违约比率
        # # default_variable = default_ratio * (A.IB.Z_IB-(A.IB.Z_IB.sum(axis=1)-bank_variable_in))  # 计算违约值
        # # default_variable = default_ratio * A.IB.Z_IB  # 计算违约值
        # default_variable = default_ratio * bank_variable_in[:, None]  # 计算违约值
        # bank_variable_1 = default_variable
        #
        # banks_preset_allocation_priority_method = '等级完全相同'  # #HACK 这里直接设置分配优先级方法。#TODO 以后再考虑是否用配置项调节分配方式
        # # match banks_preset_allocation_priority_method:
        # #     case '等级完全相同':
        # #         bank_variable = self.calc_Strategy_等级完全相同(bank_variable_1, A, idxs_row, ia)
        # #     case '应还尽还':
        # #         bank_variable = self.calc_Strategy_应还尽还(bank_variable_1, A, idxs_row, ia)
        #
        # # 根据预置的策略变量，计算实际的分配量
        # agent_variable_update[idxs_row, :] = self.calc_allocations(A, idxs_row, ia, A.IB.Z_IB, bank_variable_1, banks_preset_allocation_priority_method=banks_preset_allocation_priority_method)
        #
        # # 归一化操作
        # agent_variable_update[idxs_row, :] = np.divide(
        #     agent_variable_update[idxs_row, :],
        #     agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True),
        #     out=np.zeros_like(agent_variable_update[idxs_row, :]),
        #     where=agent_variable_update[idxs_row, :].sum(axis=1, keepdims=True) != 0
        # )
        #
        # # #HACK 以下是旧的不需要的
        # # # 根据优先级排序各债权银行之 id
        # # list_priority = [np.argsort(A.IB.Z_IB[i, A.IB.Z_IB[i, :] > 0]) for i in range(A.BB.id_agent.size)]
        # # # arr_priority = np.argsort(np.sum(A.IB.Z_IB[b, :], axis=0))
        # #
        # # # 计算对债权银行之需偿还金额
        # # debt_amount = A.IB.Z_IB[b, :], axis=0)
        # #
        # # # 根据优先级计算实际比例
        #
        # return agent_variable_update[idxs_row, :]  # 返回对应行的值

        # #HACK 不带索引的现在的版本

        default_ratio = self.strategy_presetImported[idxs_row]  # 导入违约比率
        # default_variable = default_ratio * (A.IB.Z_IB-(A.IB.Z_IB.sum(axis=1)-bank_variable_in))  # 计算违约值
        # default_variable = default_ratio * A.IB.Z_IB  # 计算违约值
        default_variable = default_ratio * bank_variable_in[:, None]  # 计算违约值
        bank_variable_1 = default_variable

        banks_preset_allocation_priority_method = '等级完全相同'  # #HACK 这里直接设置分配优先级方法。#TODO 以后再考虑是否用配置项调节分配方式
        # match banks_preset_allocation_priority_method:
        #     case '等级完全相同':
        #         bank_variable = self.calc_Strategy_等级完全相同(bank_variable_1, A, idxs_row, ia)
        #     case '应还尽还':
        #         bank_variable = self.calc_Strategy_应还尽还(bank_variable_1, A, idxs_row, ia)

        # 根据预置的策略变量，计算实际的分配量
        agent_variable_update = self.calc_allocations(A, idxs_row, ia, A.IB.Z_IB, bank_variable_1, banks_preset_allocation_priority_method=banks_preset_allocation_priority_method)

        # 归一化操作
        agent_variable_update = np.divide(
            agent_variable_update,
            agent_variable_update.sum(axis=1, keepdims=True),
            out=np.zeros_like(agent_variable_update),
            where=agent_variable_update.sum(axis=1, keepdims=True) != 0
        )

        return agent_variable_update  # 返回对应行的值
        pass  # function

    # NOTE：功能函数集：更新流之商业银行之行为决策相关的功能
    def update_by_Strategy_等级完全相同(self, bank_variable_in, agent_variable_update, A, idxs_row: StateType, ia: StateType):
        bank_variable_out = self.calc_Strategy_等级完全相同(bank_variable_in, agent_variable_update, A, idxs_row, ia)
        return bank_variable_out
        pass  # function

    def update_by_Strategy_均匀分布随机(self, bank_variable_in, agent_variable_update, A: ModelAgent, idxs_row: StateType, ia: StateType):
        bank_variable_out = self.calc_Strategy_均匀分布随机(bank_variable_in, agent_variable_update, A, idxs_row, ia)
        return bank_variable_out
        pass  # function

    def update_by_Strategy_应还尽还(self, bank_variable_in, agent_variable_update, A: ModelAgent, idxs_row: StateType, ia: StateType):
        bank_variable_out = self.calc_Strategy_应还尽还(bank_variable_in, agent_variable_update, A, idxs_row, ia)
        return bank_variable_out
        pass  # function

    def update_by_Strategy_导入预置的(self, bank_variable_in, agent_variable_update, A: ModelAgent, idxs_row: StateType, ia: StateType):
        bank_variable_out = self.calc_Strategy_导入预置的(bank_variable_in, agent_variable_update, A, idxs_row, ia)
        return bank_variable_out
        pass  # function

    # NOTE：功能函数集：根据初始分配量，与各银行之相关变量，计算修正之后的实际的分配量

    def calc_allocations(self, A: ModelAgent, idxs_row: StateType, ia: StateType, banks_variable_subject: np.ndarray, banks_preset_allocations: np.ndarray, banks_preset_allocation_priority_method: np.ndarray = None) -> np.ndarray:
        """
        计算修正之后的实际的分配量。

        对给定的实施分配的个体，对应一系列待分配的个体。对于每一个待分配的个体，计算实际的分配方案。根据给定的初始分配量，分配给待分配的个体。如果分配过剩，则按照给定的分配优先级分配给其他分配不足的待分配的个体。

        banks_preset_allocation_priority_method 可取的值有：

        - `等级完全相同`：按照各银行之应还尽还原则，结果值满足约束条件。
        - `应还尽还`：按照各银行之应还尽还原则，结果值满足约束条件。

        其中，`应还尽还` 采用的分配优先级是：

            - 分配过剩的待分配个体，按照其初始分配量 `banks_preset_allocations` 从大到小排序。
            - 分配不足的待分配个体，按照其调整后的分配量约束变量 `banks_variable` 从大到小排序。

            实际分配优先级实现。

            ### 1. 初始化
            - 首先，创建一个 `banks_allocations` 数组，它是 `banks_preset_allocations` 的副本。
            - 使用 `np.where(banks_variable > 0)[0]` 获取所有待分配的个体（即 `banks_variable` 大于 0 的索引）。
            - 计算 `debts_amount_diff`，即初步分配与实际所能容纳的最大分配额之差 (`banks_preset_allocations - banks_variable`)。
            - 分别获取分配过剩和分配不足的个体索引：
                - `list_i_surplus`：分配过剩的个体索引，这些个体的 `debts_amount_diff` 大于 0。
                - `list_i_deficit`：分配不足的个体索引，这些个体的 `debts_amount_diff` 小于 0。

            ### 2. 分配过剩个体处理
            - 对于分配过剩的个体 (`list_i_surplus`)，直接将它们的实际分配量设置为最大分配额 (`banks_variable[list_i_surplus]`)。
            - 计算总的分配过剩量 `total_surplus`，即所有分配过剩个体的 `debts_amount_diff` 之和。

            ### 3. 分配不足个体处理
            - 根据调整后的分配量约束变量 `banks_variable` 对分配不足的个体进行排序，得到 `list_priority_i_deficit`。这里使用了 `np.argsort` 函数，并且是降序排列（`[::-1]`），这意味着分配不足的个体中，调整后分配量更大的会先被考虑填补。
            - 如果存在分配不足的个体 (`list_priority_i_deficit is not None`)，则进入循环处理：
                - 对于每个分配不足的个体 `i_deficit`，计算其需要填补的金额 `debt_amount_diff`，该金额为 `min(total_surplus, arr_deficit[i_deficit])`，即取当前剩余的总过剩量和该个体需要填补的金额中的较小值。
                - 更新该分配不足个体的实际分配量 `banks_allocations[i_cre]`，并减少相应的过剩量 `arr_deficit[i_deficit]` 和 `total_surplus`。
                - 如果总的过剩量 `total_surplus` 已经变为 0，则退出循环，表示所有的过剩量已经分配完毕。

        Args:
            ia (numpy.ndarray): 个体间之传染方对感染方之状态示性邻接矩阵
            A (ModelAgent): 个体众
            idxs_row (numpy.ndarray): 需要运行的行索引
            banks_variable_subject (np.ndarray): 各银行之调整分配量的约束变量
            banks_preset_allocations (np.ndarray): 各银行之实际分配之前的计划的分配量
            banks_preset_allocation_priority_method (np.ndarray): 各银行之预置的分配优先级方法。可选，默认空缺。

        Returns:
            np.ndarray: 修正之后的实际的分配量
        """

        match banks_preset_allocation_priority_method:
            case '应还尽还':
                banks_allocations = banks_preset_allocations.copy()
                cre = np.where(banks_variable_subject > 0)[0]  # 获取待分配的个体之 id
                debts_amount_diff = banks_preset_allocations - banks_variable_subject  # 计算初步分配与实际所能容纳的最大分配额之差
                list_i_surplus = np.where(debts_amount_diff > 0)[0]  # 分配过剩的待分配的个体 id
                list_i_deficit = np.where(debts_amount_diff < 0)[0]  # 分配不足的待分配的个体 id
                banks_allocations[list_i_surplus] = banks_variable_subject[list_i_surplus]  # 分配过剩的待分配的个体的分配额设为最大分配额
                arr_deficit = -debts_amount_diff[list_i_deficit]  # 计算分配不足的待分配的个体的分配差额
                total_surplus = np.sum(debts_amount_diff[list_i_surplus])  # 计算总的分配过剩量
                # #NOTE 根据优先级排序分配不足的待分配的个体，继续分配直到分配完毕
                list_priority_i_deficit = np.argsort(banks_variable_subject[list_i_deficit])[::-1] if list_i_deficit.size != 0 else None  # #TODO 分配优先级策略应该单独提取出来，作为一个新的行为策略
                if list_priority_i_deficit is not None:
                    # 计算分配不足的待分配的个体的分配额
                    for i in range(len(list_priority_i_deficit)):
                        i_deficit = list_priority_i_deficit[i]  # 分配不足的待分配的个体的 id
                        i_cre = list_i_deficit[i]  # 分配过剩的待分配的个体的 id
                        debt_amount_diff = min(total_surplus, arr_deficit[i_deficit])  # 计算分配不足的待分配的个体的分配额
                        banks_allocations[i_cre] += debt_amount_diff  # 分配不足的待分配的个体的分配额
                        arr_deficit[i_deficit] -= debt_amount_diff  # 更新分配不足的待分配的个体的分配额
                        total_surplus -= debt_amount_diff  # 更新分配过剩的待分配的个体的分配额
                        if total_surplus == 0:
                            break
                        pass  # for
                    pass  # if
            case '等级完全相同':
                # #NOTE 根据等级完全相同分配
                default_values = banks_preset_allocations  # 计算违约值
                default_values_2 = np.minimum(default_values, A.IB.Z_IB[idxs_row])  # 限制违约值不超过Z_IB的值
                # 计算限制违约值之后，违约值的减少量总和
                default_values_diff = default_values - default_values_2  # 计算违约值的差异
                default_values_diff_sum = default_values_diff.sum(axis=1, keepdims=True)  # 计算每行的违约值差异总和

                # agent_variable_update_2 = np.zeros_like(banks_variable_subject)
                agent_variable_update_2 = default_values_diff_sum * np.divide(
                    (banks_variable_subject[idxs_row] - default_values_2),
                    (banks_variable_subject[idxs_row] - default_values_2).sum(axis=1, keepdims=True),
                    out=np.zeros_like(A.IB.Z_IB[idxs_row, :]),
                    where=(A.IB.Z_IB[idxs_row, :] - default_values_2).sum(axis=1, keepdims=True) != 0
                )

                agent_variable_update = default_values_2 + agent_variable_update_2
                banks_allocations = agent_variable_update

            case _:
                raise Exception("关键词取词错误".format(banks_preset_allocation_priority_method))
                pass  # match

        return banks_allocations  # 返回对应行的值
        pass  # function

    pass  # class
