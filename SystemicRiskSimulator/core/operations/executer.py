"""
执行机
"""
from SystemicRiskSimulator.external_packages import logging, pd, deepcopy, dataclass
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_entity import Entity
# from SystemicRiskSimulator.data.models.contents.content_finance import Finance
from SystemicRiskSimulator.core.operations.collector import Collector

pass  # end import


@dataclass
class Executer:
    """
    执行机
    """

    # @classmethod
    # def turn_step_update(cls, content, turn: int, process_name: str, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
    #     """
    #     执行一次轮次级别（轮次粒度）的步进更新。对应强化学习的一次步进更新。
    #
    #     Args:
    #         content (class): 相关的需要步进更新的功能类
    #         A (SystemicRiskAgent): 多主体
    #         A_data (AgentDataCollection): 多主体之数据
    #         para (dict): 参数集
    #         sgv (dict): 模拟器全局变量
    #
    #     Returns:
    #         A (SystemicRiskAgent): 多主体
    #         sgv (dict): 模拟器全局变量
    #
    #     """
    #     sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
    #     sgv['phase'] = 1  # 逐相复位（起始为1）
    #     sgv['process_name'] = process_name
    #     logging.debug(f"        轮次：{sgv['turn']}，模型：{sgv['process_name']}")
    #     A, sgv = content.content_model_process(A, A_data, para, sgv)  # 执行一次轮次级别的步进更新
    #     # A, sgv = content.execute_model_content(A, A_data, para, sgv)  # 执行一次轮次级别的步进更新
    #
    #     return A, sgv
    #
    #     pass  # function

    # @classmethod
    # def turn_step_update(cls, content, process_name: str, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):

    @classmethod
    def turn_step_update(cls, content, A: SystemicRiskAgent, A_last: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        #NOTE：执行一次轮次级别（轮次粒度）的步进更新。对应强化学习的一次步进更新。

        Args:
            content (object): 相关的需要步进更新的功能类或者实例
            A (SystemicRiskAgent): 多主体
            A_last (SystemicRiskAgent): 上一回合的多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            A (SystemicRiskAgent): 多主体
            sgv (dict): 模拟器全局变量

        """
        sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
        sgv['phase'] = 1  # 逐相复位（起始为1）
        # sgv['process_name'] = process_name
        logging.debug(f"        轮次：{sgv['turn']}，模型：{sgv['process_name']}")
        content.model_content(A, A_last, A_data, para, sgv)  # 执行一次轮次级别的步进更新

        # 深拷贝一份作为上一回合的数据
        A_last = SystemicRiskAgent(2, deepcopy(A.BB), deepcopy(A.b), deepcopy(A.IB), deepcopy(A.ib))

        return A, A_last, sgv

        pass  # function

    @classmethod
    def variable_step_update(cls, content, update_way: str, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        #NOTE：执行一次变量变更级别的步进更新

        更新方式具体见：`Finance.update_variables` 对应的[文档](SystemicRiskSimulator/core/functions/content_finance.py)。

        Args:
            content (object): 相关的需要步进更新的功能类或者实例
            update_way (str): 更新方式
            A (SystemicRiskAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            None

        """

        logging.debug(f"                步进：{sgv['step']}，相：{sgv['phase']}，更新源：{update_way}")
        # Finance.update_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量
        content.update_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量
        if sgv['RL_state'] is 'using':
            Collector.collect_agent_data(A, A_data, sgv)
            pass  # if

        sgv['step'] += 1  # 步进加一
        sgv['phase'] += 1  # 逐相加一

        # return sgv
        pass  # function

    # @classmethod
    # def agentsRewards_variable_step_update(cls, content, update_way: str, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
    #     """
    #     #NOTE：执行一次个体众奖励函数值变更级别的步进更新
    #
    #     Args:
    #         content (object): 相关的需要步进更新的功能类或者实例
    #         update_way (str): 更新方式
    #         A (SystemicRiskAgent): 多主体
    #         A_data (AgentDataCollection): 多主体之数据
    #         para (dict): 参数集
    #         sgv (dict): 模拟器全局变量
    #
    #     Returns:
    #         None
    #
    #     """
    #
    #     logging.debug(f"                步进：{sgv['step']}，相：{sgv['phase']}，更新源：{update_way}")
    #     # Finance.update_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量
    #     content.update_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量
    #     if sgv['RL_state'] is 'using':
    #         Collector.collect_agent_data(A, A_data, sgv)
    #         pass  # if
    #
    #     sgv['step'] += 1  # 步进加一
    #     sgv['phase'] += 1  # 逐相加一
    #
    #     # return sgv
    #     pass  # function

    @classmethod
    def execute_main_model_entity(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict, entity: Entity):
        """
        执行过程版本（非流程版本）的模型实体（模型模板实体）。#HACK 似乎无用了。

        NOTE：输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            para (dict): 参数变量
            sgv (dict): 模拟器全局变量
            entity (Entity): 模型实体

        Returns: agent

        """
        # entity = node.content  # 获取节点实体对应的模型实体

        logging.debug("    开始执行模型内容：")

        # sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
        # sgv['phase'] = 1  # 逐相复位（起始为1）
        # # sgv['step'] += 1  # 步进加一
        sgv['process_name'] = entity.attribute.entity_name  # 执行的过程之名称（英文名称）
        entity.execute(A, A_data, para, sgv)

        logging.debug("    结束执行模型内容。")

        return A, A_data, sgv
        pass  # function

    pass  # class
