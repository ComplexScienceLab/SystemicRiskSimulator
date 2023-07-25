"""
处理机。
#NOTE：如果不是因为Python语言会出现循环调用的情况，那么会将这里的一些功能和内容放入`operator`。
"""

from PySystemicRiskLab import dataclass, logging, re, random
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
    def process_entity_by_process_and_container_component(cls, model: Entity, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, env: dict):
        """
        处理所有类型的实体，通过过程与容器组件。

        NOTE：这里略去了功能：对特殊节点调用`Excuter`。因为就目前的程序来说，没必要进一步复杂化，直接在`Processor`内处理即可。

        Args:
            model (Entity): 模型实体（NOTE：本函数中，特指模型节点实体而非模型算法实体。）
            A (SystemicRiskAgent): Agent群变量
            A_data (AgentDataCollection): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量

        Returns: entity: 算法实体, A: Agent群变量, para: 参数变量, env: 环境变量, A_data: Agent群变量之数据

        """

        ## 根据算法实体之编译后的过程处理每一个指令
        algorithmEntity = model.content
        process = algorithmEntity.process
        line_number = 1  # 当前指令所在行号
        while ((line_number <= len(process)) and (env['state_of_schedule'] == StateOfScheduleEnum.running)):  # 当指令位置在指令序列内时，且满足调度条件时，运行过程指令
            instruction = process[line_number - 1]
            if instruction[1] == 'node':  # 当前指令是标记节点位置语句时
                logging.debug(f"处理行\t{instruction[0]}\t{instruction[1]}\t\t{instruction[2].attribute.entity_name} {instruction[2].attribute.id}")
                line_number += 1
                continue
            elif instruction[1] == 'execute':  # 当前指令是执行语句时
                if not (instruction[2].attribute.entity_name == 'START' or instruction[2].attribute.entity_name == 'END'):
                    logging.debug(f"处理行\t{instruction[0]}\t{instruction[1]}\t\t{instruction[2].attribute.entity_name} {instruction[2].attribute.text_name}")
                    A, A_data, env = Executer.execute_algorithm_entity(A, A_data, para, env, instruction[2])
                    line_number += 1
                else:  # 当前指令开始或结束节点时
                    logging.debug(f"处理行\t{instruction[0]}\t{instruction[1]}\t\t{instruction[2].attribute.entity_name} {instruction[2].attribute.text_name}")
                    line_number += 1
                continue
            elif instruction[1] == 'if' and instruction[3] == 'goto':  # 当前指令是判断跳转语句时
                logging.debug(f"处理行\t{instruction[0]}\t{instruction[1]}\t\t{instruction[2]}\t\t{instruction[3]}\t\t{instruction[4].attribute.entity_name} {instruction[4].attribute.id}\t{instruction[5]}")
                instructions_ifgoto = []  # 该节点对应的 if-goto 指令列表
                line_number_ifgoto = line_number  # 当前指令 if-goto 所在行号
                while True:  # 当前指令是判断跳转语句时
                    if process[line_number_ifgoto - 1][1] == 'if' and process[line_number_ifgoto - 1][3] == 'goto':
                        instructions_ifgoto.append(process[line_number_ifgoto - 1])
                        line_number_ifgoto += 1
                    else:
                        break
                        pass  # if
                    pass  # while

                # DEBUG添加测试用的跳转语句
                # conditions = []  # 条件列表
                # condition01 = (random.sample(range(1, 100), 1)[0] > 10)
                # conditions.append(condition01)
                # condition02 = ~condition01
                # conditions.append(condition02)

                conditions = []  # 条件列表
                for instruction_ifgoto in instructions_ifgoto:  ## 判断每个条件
                    condition = eval(instruction_ifgoto[2]) if instruction_ifgoto[2] is not None else None  # NOTE 其实判断None这个条件是多余的
                    # logging.debug(f"    条件{instruction_ifgoto[2]}是 {condition}") #DEBUG 通用的打印日志，适用于打印所有的条件语句

                    ## DEBUG 以下是专用的日志，适用于打印当前的条件语句
                    condition_str = instruction_ifgoto[2]
                    pattern = re.compile(r"env\[['\"]round['\"]\]-1")
                    matched_str = pattern.search(condition_str)
                    logging.debug(f"    条件{re.sub(pattern.pattern, f'[{eval(matched_str.group())}]', condition_str)}是 {condition}")

                    conditions.append(condition)
                    pass  # for
                line_number = instructions_ifgoto[conditions.index(True)][5]  # 获取下一个节点所在的行号
                logging.debug(f"    流至节点{instructions_ifgoto[conditions.index(True)][4].attribute.entity_name}，对应算法{instructions_ifgoto[conditions.index(True)][4].content.attribute.entity_name} {instructions_ifgoto[conditions.index(True)][4].content.attribute.text_name}，跳转行{line_number}")
                continue
            else:
                raise ValueError("【%s】不是有效的指令类型。" % (instruction))
                pass  # if
            pass  # while

        return model, A, A_data, para, env

        pass  # def

    @classmethod
    def process_entity_by_node_component(cls, node: Entity, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, env: dict):
        """
        处理所有类型的实体，通过节点组件。

        #FIXME 这里没有做适配。因此目前用不到。因为目前还没有用到。以后有需要可以做非递归算法适配。

        #TODO：HACK：目前采用的是以栈的形式处理，这样的缺点是受到python自带的栈深度限制。后续方便的话要改成用遍历动态多叉树生成序列的形式处理。

        #NOTE：这里略去了功能：对特殊节点调用`Excuter`。因为就目前的程序来说，没必要进一步复杂化，直接在`Processor`内处理即可。

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
                Scheduler.schedule(env)
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
                node.attribute.node_type == {"process node", "container node"} and node.attribute.content_type == {"model content", "algorithm content"}
        ):
            ## 处理节点组件内之当前节点实体
            node.attribute.other['process_state'] = "process now"  # 标记为正在处理
            entity = node.content  # 获取节点实体对应的算法实体
            inner_node_name = entity.node['node_START'].attribute.entity_name
            inner_node = entity.node[inner_node_name]  # 获取该节点内层之节点
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
                if inner_forward_node.process.__len__() != 0:
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

    # @classmethod
    # def process_processEntity(cls, entity: Entity):
    #     """
    #     Args:
    #         entity ():
    #     """
    #     pass  # method

    # @classmethod
    # def process_conditionEntity(cls, entity: Entity):  # 处理过程类型的实体之条件
    #     conditions = []  # 条件列表
    #     for (i, out_flow_entity) in enumerate(entity.process):  ## 判断每个条件
    #         condition = eval(out_flow_entity['condition']) if out_flow_entity['condition'] is not None else None  # NOTE 其实判断None这个条件是多余的
    #         logging.debug("        条件【%s】是 %s", out_flow_entity['condition'], condition)
    #         conditions.append(condition)
    #     out_flow_entity = entity.process[conditions.index(True)]['flow']
    #
    #     return conditions, out_flow_entity
    #     pass  # method

    pass  # class
