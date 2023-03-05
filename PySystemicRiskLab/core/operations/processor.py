"""
处理机。
#NOTE：如果不是因为Python语言会出现循环调用的情况，那么会将这里的一些功能和内容放入`operator`。
"""

from PySystemicRiskLab import dataclass, logging
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.operations.collector import Collector
from PySystemicRiskLab.core.operations.executer import Executer
from PySystemicRiskLab.core.operations.scheduler import Scheduler


@dataclass()
class Processor:
    """
    处理机
    """

    @classmethod
    def process_entity(cls, node: Entity, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, env: dict):
        """
        处理所有类型的实体。

        TODO：HACK：目前采用的是以栈的形式处理，这样的缺点是受到python自带的栈深度限制。后续方便的话要改成用遍历动态多叉树生成序列的形式处理。
        NOTE：这里略去了功能：对特殊节点调用`Excuter`。因为就目前的程序来说，没必要进一步复杂化，直接在`Processor`内处理即可。

        Args:
            node (Entity): 节点实体（NOTE：本函数中，特指节点实体而非算法实体。在这里，算法实体简称以`entity`。）
            A (SystemicRiskAgent): Agent群变量
            A_data (AgentDataCollection): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量

        Returns: entity: 算法实体, A: Agent群变量, para: 参数变量, env: 环境变量, A_data: Agent群变量之数据

        """

        ## 如果实体之节点之类型是 content node，且内容之类型是 {"algorithm content"}，则处理：
        if node.attribute.node_type == {"content node"} and node.attribute.content_type == {"algorithm content"}:
            ## 设置临时变量
            b = (A.BB.on | A.BB.off)  # BB示性变量
            ib = (A.BB.on | A.BB.off) & (A.BB.on | A.BB.off).T  # IB示性变量

            # ## 执行终端节点内容 #BUG
            # A = Executer.execute_terminal_entity(A, A_data, para, env, node)
            #
            # ## 收集数据
            # A_data, env = Collector.collect(A, A_data, env)

            ## 执行终端节点内容
            if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
                env = Scheduler.schedule(env, node)
                if env['state_of_schedule'] == StateOfScheduleEnum.running:
                    A, A_data, env = Executer.execute_terminal_entity(A, A_data, para, env, node)

            # ## 执行终端节点内容
            # if env['state_of_schedule'] == StateOfScheduleEnum.running:
            #     A, A_data, env = Executer.execute_terminal_entity(A, A_data, para, env, node)

            ## 标记为已经处理过
            node.attribute.other['process_state'] = "has processed"

            pass  # if

        ## 如果实体之节点之类型是 {"process node", "container node"}，且内容之类型是 {"algorithm content"} 或者 {"model content"} ，则处理：
        if (
                node.attribute.node_type == {"process node", "container node"} and node.attribute.content_type == {"algorithm content"}
        ) or (
                node.attribute.node_type == {"process node", "container node"} and node.attribute.content_type == {"model content"}
        ):
            ## 处理容器内之当前节点实体
            node.attribute.other['process_state'] = "process now"  # 标记为正在处理
            entity = node.content  # 获取节点实体对应的算法实体
            inner_node_name = entity.container['node_START'].attribute.entity_name
            inner_node = entity.container[inner_node_name]  # 获取该节点内层之节点
            inner_node, A, A_data, para, env = Executer.execute_branch_entity(inner_node, A, A_data, para, env)  ## 执行开始节点实体
            inner_node.attribute.other['process_state'] = "has processed"
            node.attribute.other['process_state'] == "process inner"  # 标记节点之处理状态为处理内层节点
            inner_forward_node = inner_node.process[0]['direction']  # 获取开始节点之前向节点
            logging.debug("        方向是【节点：%s，算法：%s %s】", inner_forward_node.attribute.entity_name, inner_forward_node.content.attribute.entity_name, inner_forward_node.content.attribute.text_name)

            ## 继续循环处理该节点之内层的前向的节点，直到处理完结束节点为止。
            while not (inner_forward_node.attribute.other['process_state'] == "has processed" and inner_forward_node.attribute.entity_name == "node_END"):
                ## 处理过程之内容（#NOTE：在设计的时候，就应该保证，同一个`arrow`之各个条件里，只能有一个条件是`True`，然后被处理于后续的时候）
                if inner_forward_node.attribute.node_type == {"content node"} and inner_forward_node.attribute.content_type == {"algorithm content"}:
                    A, A_data, env = Executer.execute_terminal_entity(A, A_data, para, env, inner_forward_node)  ## 执行该节点之内层的前向的节点实体
                elif (
                        inner_forward_node.attribute.node_type == {"process node", "container node"} and inner_forward_node.attribute.content_type == {"algorithm content"}
                ) or (
                        inner_forward_node.attribute.node_type == {"process node", "container node"} and inner_forward_node.attribute.content_type == {"model content"}
                ):
                    inner_forward_node, A, A_data, para, env = Executer.execute_branch_entity(inner_forward_node, A, A_data, para, env)  ## 执行该节点之内层的前向的节点实体
                else:
                    ## 如果是开始节点
                    if inner_forward_node.attribute.entity_name == "node_START":
                        inner_forward_node.attribute.other['process_state'] = "has processed"
                        pass  # if
                    ## 如果是结束节点
                    if inner_forward_node.attribute.entity_name == "node_END":
                        inner_forward_node.attribute.other['process_state'] = "has processed"
                        pass  # if
                    pass  # if

                ## 处理流向
                conditions = []  # 条件结果列表
                if inner_forward_node.process.__len__() is not 0:
                    for arrow in inner_forward_node.process:  ## 判断每个条件
                        condition = eval(arrow['condition'])  # 计算条件值
                        logging.debug("        条件【%s】是 %s", arrow['condition'], condition)
                        conditions.append(condition)
                        pass  # for
                    inner_forward_node = inner_forward_node.process[conditions.index(True)]['direction']  # 判断在当前条件下，符合条件的前向的节点
                    logging.debug("        方向是【节点：%s，算法：%s %s】", inner_forward_node.attribute.entity_name, inner_forward_node.content.attribute.entity_name, inner_forward_node.content.attribute.text_name)
                    pass  # if
                else:  # 结束节点
                    pass  # if

                pass  # while

            node.attribute.other['process_state'] == "has processed"  # 标记节点之处理状态为处理完成 #BUG

        ## 如果实体之节点之类型是 {"process node"}，且内容之类型是 {"process content"}（NOTE：开始节点`node_START`、结束节点`node_END`），则处理：
        if node.attribute.node_type == {"process node"} and node.attribute.content_type == {"process content"}:

            if node.attribute.entity_name == "node_START":  ## 如果是开始节点
                node.attribute.other['process_state'] = "has processed"
                pass  # if
            elif node.attribute.entity_name == "node_END":  ## 如果是结束节点
                node.attribute.other['process_state'] = "has processed"
                pass  # if

            pass  # if

        return node, A, A_data, para, env
        pass  # method

    ## TODO 后续需要用到类似`content_IB1111.content`的时候再继续
    @classmethod
    def process_processEntity(cls, entity: Entity):  # TODO处理过程类型的实体
        """
        Args:
            entity ():
        """
        pass  # method

    @classmethod
    def process_conditionEntity(cls, entity: Entity):  # TODO 处理过程类型的实体之条件
        conditions = []  # 条件列表
        for (i, out_flow_entity) in enumerate(entity.process):  ## 判断每个条件
            condition = eval(out_flow_entity['condition']) if out_flow_entity['condition'] is not None else None  # NOTE 其实判断None这个条件是多余的，因为
            logging.debug("        条件【%s】是 %s", out_flow_entity['condition'], condition)
            conditions.append(condition)
        out_flow_entity = entity.process[conditions.index(True)]['flow']

        return conditions, out_flow_entity
        pass  # method

    pass  # class
