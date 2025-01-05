"""
执行
"""
from SystemicRiskSimulator.external_packages import logging, pd, deepcopy, dataclass, Optional
from SystemicRiskSimulator.core.define.define_agents import ModelAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
# from SystemicRiskSimulator.data.models.contents.content_finance import Finance
from SystemicRiskSimulator.core.operations.collector import Collector

pass  # end import


@dataclass
class Executer:
    """
    执行
    """

    @classmethod
    def update_turnStep_by_ABM(cls, content, A: ModelAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        #NOTE：执行一次轮次级别（轮次粒度）的步进更新。对应强化学习的一次步进更新。

        注意：如果不想要本轮次之上一回合的数据覆盖现有的上一轮次的数据，那么在使用该函数的时候，返回值可以设置不接收返回值 A_last 。例如 `A, _, sgv = Executer.update_turnStep_by_ABM(...)` 。

        Args:
            content (object): 相关的需要步进更新的功能类或者实例
            A (ModelAgent): 多主体
            A_last (ModelAgent): 上一回合的多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            A (ModelAgent): 多主体
            A_last (ModelAgent): 上一回合的多主体
            sgv (dict): 模拟器全局变量

        """

        # # 深拷贝一份作为上一回合的数据
        # A_last = ModelAgent(2, deepcopy(A.BB), deepcopy(A.b), deepcopy(A.IB), deepcopy(A.ib))

        sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
        sgv['phase'] = 1  # 逐相复位（起始为1）
        # sgv['process_name'] = process_name
        # logging.debug(f"        轮次：{sgv['turn']}，模型：{sgv['process_name']}")
        content(A, A_data, para, sgv)  # 执行一次轮次级别的步进更新

        if sgv['step'] >= sgv['test_max_num_of_turn']:
            if sgv['is_develope_mode']:  # #HACK 只有在开发模式下才开启这个判断
                logging.error(f"实验{sgv['id_experiment']}，模型第{sgv['step']}步，模型未能收敛。请检查模型逻辑是否正确！！！")
                sgv['is_continue_process'] = False
            else:
                assert False, f"实验{sgv['id_experiment']}，模型第{sgv['step']}步，模型未能收敛，程序以非正常方式退出。"  # #BUG 如果遇到并行运行模式，会出现什么情况？
                pass  # if
            pass  # if

        # return A, A_last, sgv
        return A, sgv

    @classmethod
    def update_turnStep_by_RL(cls, content, A: ModelAgent, A_last: ModelAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        #NOTE：执行一次轮次级别（轮次粒度）的步进更新。对应强化学习的一次步进更新。

        Args:
            content (object): 相关的需要步进更新的功能类或者实例
            A (ModelAgent): 多主体
            A_last (ModelAgent): 上一回合的多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            A (ModelAgent): 多主体
            sgv (dict): 模拟器全局变量

        """
        sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
        sgv['phase'] = 1  # 逐相复位（起始为1）
        # sgv['process_name'] = process_name
        logging.debug(f"        轮次：{sgv['turn']}，模型：{sgv['process_name']}")
        content(A, A_last, A_data, para, sgv)  # 执行一次轮次级别的步进更新

        # 深拷贝一份作为上一回合的数据
        A_last = ModelAgent(2, deepcopy(A.BB), deepcopy(A.b), deepcopy(A.IB), deepcopy(A.ib))

        return A, A_last, sgv

        pass  # function

    @classmethod
    def update_variableStep(cls, content, update_way: str, A: ModelAgent, A_data: AgentDataCollection, para: dict, sgv: dict, is_collect=True, collect: Optional[list] = None):
        """
        #NOTE：执行一次变量变更级别的步进更新

        更新方式具体见：`Finance.update_variables` 对应的[文档](SystemicRiskSimulator/core/functions/content_finance.py)。

        Args:
            content (object): 相关的需要步进更新的功能类或者实例
            update_way (str): 更新方式
            A (ModelAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量
            is_collect (bool): 是否收集当前步进之数据。默认为 True。
            collect (dict): 待收集的数据字段列表字典。默认为 None ，表示收集 A 当前回合的所有字段的数据。如果非 None ，则应设置为字典形式。字典的键名是变量名称，键值是该变量对应的数据字段列表。

        Returns:
            None

        """

        logging.debug(f"                步进：{sgv['step']}，相：{sgv['phase']}，更新源：{update_way}")
        # Finance.update_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量
        content.update_variables(A, by_way=update_way)  # 更新金融变量
        if is_collect or sgv['is_use_RLlib_frameworks'] is False or sgv['RL_state'] == 'using':
            Collector.collect_agent_data(A, A_data, sgv, para, collect)
            pass  # if

        sgv['step'] += 1  # 步进加一
        sgv['phase'] += 1  # 逐相加一

        # return sgv
        pass  # function

    # @classmethod
    # def agentsRewards_variable_step_update(cls, content, update_way: str, A: ModelAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
    #     """
    #     #NOTE：执行一次个体众奖励函数值变更级别的步进更新  #HACK 似乎无用了。
    #
    #     Args:
    #         content (object): 相关的需要步进更新的功能类或者实例
    #         update_way (str): 更新方式
    #         A (ModelAgent): 多主体
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

    pass  # class
