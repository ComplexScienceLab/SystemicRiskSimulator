"""
处理机
"""
from PySystemicRiskLab import logging, pd, deepcopy, dataclass
from PySystemicRiskLab.tools.tools import Tools
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.operations.collector import Collector
from PySystemicRiskLab.core.operations.executer import Executer
from PySystemicRiskLab.core.operations.scheduler import Scheduler


@dataclass()
class Processor:
    """
    处理机
    """

    @classmethod
    def process_NodeProcess(cls, entity: Entity, A: SystemicRiskAgent, A_data: AgentDataCollection, para, env):
        """
        处理节点过程

        Args:
            A (SystemicRiskAgent): Agent群变量
            para (dict): 参数变量
            env (dict): 环境变量
            A_data (AgentDataCollection): Agent群变量之数据
            entity (Entity): 实体

        Returns: A, para, env, A_data

        """

        ## 处理内容类型为`model content`之过程之内容
        if entity.attribute.node_type == {"process node"} and entity.attribute.content_type == {"model content"} and entity.process[0]['condition'] is None:  ## 如果实体之节点之类型是 process node，且内容之类型是 model content，且过程之条件为空，则执行开始节点之内容
            A, A_data, para, env = Executer.execute_branch_node(entity.process[0]['flow'], A, A_data, para, env)  # NOTE 开始节点用关键词`None`标记
            pass  # if

        ## 如果实体之节点之类型是 container node，且内容之类型是 algorithm content，则运作：
        if entity.attribute.node_type == {"process node", "container node"} and entity.attribute.content_type == {"algorithm content"}:
            ## 处理容器之内容
            for (i, out_flow_entity) in enumerate(entity.container):  ## 顺序依次处理容器内之内容
                if out_flow_entity.attribute.node_type == {"terminal node"} and out_flow_entity.attribute.content_type == {"algorithm content"}:
                    ## 设置临时变量
                    b = (A.BB.on | A.BB.off)  # BB示性变量
                    ib = (A.BB.on | A.BB.off) & (A.BB.on | A.BB.off).T  # BI示性变量
                    # BB_Shock_last = deepcopy(A.BB.Shock_t)  # BB上一时期的冲击变量
                    # BB_isv_last = deepcopy(A.BB.isv)  # BB上一时期的isv变量

                    ## 执行终端节点内容
                    if env['state_of_schedule'] == StateOfScheduleEnum.running:
                        A = Executer.execute_terminal_node(A, b, ib, para, env, out_flow_entity)

                    ## 收集数据
                    A_data, env = Collector.collect(A, A_data, env)
                    # A_data = Collector.collect_agent_data(A, A_data, env)

                    pass  # if
                pass  # for

            ## 处理过程之内容（各个条件里，只能有一个条件是符合的并且被处理）
            conditions = []  # 条件列表
            for (i, out_flow_entity) in enumerate(entity.process):  ## 判断每个条件
                condition = eval(out_flow_entity['condition']) if out_flow_entity['condition'] is not None else None  # NOTE 其实判断None这个条件是多余的，因为
                logging.debug("        条件【%s】是 %s", out_flow_entity['condition'], condition)
                conditions.append(condition)
            out_flow_entity = entity.process[conditions.index(True)]['flow']
            if out_flow_entity is not None:  # 如果流向非空，则执行流出的内容
                logging.debug("        流至【%s %s】", out_flow_entity.attribute.text_name, out_flow_entity.attribute.entity_name)
                A, A_data, para, env = Executer.execute_branch_node(out_flow_entity, A, A_data, para, env)
            else:  # 如果流向为空，则执行结束节点 #NOTE 结束节点用关键词`None`标记
                env['is_continue_process'] = False  # 标记继续运行过程为否

        return A, A_data, para, env
        pass  # method

