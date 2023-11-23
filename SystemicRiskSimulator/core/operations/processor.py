"""
处理机。
#NOTE：如果不是因为Python语言会出现循环调用的情况，那么会将这里的一些功能和内容放入`operator`。
"""

from SystemicRiskSimulator import dataclass, logging, re, random
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.core.define.define_type import StateType
from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.operations.executer import Executer
from SystemicRiskSimulator.core.operations.scheduler import Scheduler


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
            model (Entity): 模型实体（NOTE：本函数中，特指模型实例实体而不是主模型模板实体。）
            A (SystemicRiskAgent): Agent群变量
            A_data (AgentDataCollection): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量

        Returns: entity: 模型模板实体, A: Agent群变量, para: 参数变量, env: 环境变量, A_data: Agent群变量之数据

        """

        ## 根据模型模板实体之编译后的过程处理每一个指令
        modelEntity = model.content
        process = modelEntity.process
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
                    A, A_data, env = Executer.execute_model_entity(A, A_data, para, env, instruction[2])
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

                    A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1]
                    ## DEBUG 以下是专用的日志，适用于打印当前的条件语句
                    condition_str = instruction_ifgoto[2]
                    pattern = re.compile(r"env\[['\"]round['\"]\] - 1")
                    matched_str = pattern.search(condition_str)
                    logging.debug(f"    条件{re.sub(pattern.pattern, f'[{eval(matched_str.group())}]', condition_str)}是 {condition}")

                    conditions.append(condition)
                    pass  # for
                line_number = instructions_ifgoto[conditions.index(True)][5]  # 获取下一个节点所在的行号
                logging.debug(f"    流至节点{instructions_ifgoto[conditions.index(True)][4].attribute.entity_name}，对应模型{instructions_ifgoto[conditions.index(True)][4].content.attribute.entity_name} {instructions_ifgoto[conditions.index(True)][4].content.attribute.text_name}，跳转行{line_number}")
                continue
            else:
                raise ValueError("【%s】不是有效的指令类型。" % (instruction))
                pass  # if
            pass  # while

        return model, A, A_data, para, env

        pass  # function



    pass  # class
