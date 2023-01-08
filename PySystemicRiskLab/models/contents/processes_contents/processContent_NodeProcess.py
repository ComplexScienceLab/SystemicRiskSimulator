"过程内容"

# from PySystemicRiskLab.core import SystemicRiskAgent, ModelModule, AgentDataCollection, Operator, StateOfScheduleEnum

pass  # end import

from PySystemicRiskLab import logging, pd, deepcopy,dataclass
from PySystemicRiskLab.core.operations.operator import Operator
from PySystemicRiskLab.core.operations.scheduler import Scheduler
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_module import ModelModule
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum

pass  # end import


class Processor:
    """
    处理机
    """


    def processContent_NodeProcess(A: SystemicRiskAgent, para, env, A_data: AgentDataCollection, entity: Entity):
        """
        节点过程内容

        Args:
            A (SystemicRiskAgent): Agent群变量
            para (dict): 参数变量
            env (dict): 环境变量
            A_data (AgentDataCollection): Agent群变量之数据
            entity (Entity): 实体

        Returns: A, para, env, A_data

        """

        # logging.debug("过程%s：%s", env['index_process'], env['process_name'])

        # env['index_stage'] = 0  # 初始化阶段所在位置
        # env['is_step'] = True  # 初始化步进状态
        # env['is_round'] = True  # 初始化回合状态
        # env['is_process'] = True  # 初始化过程状态
        # env['is_loop'] = True  # 初始化循环状态

        # ## 判断是否继续模型
        # if (env['is_model']):
        #     if (env['round'] > 1):
        #         logging.debug("继续模型：%s\n\n", env['model_name'])
        #         pass
        #     else:
        #         logging.debug("开始模型：%s\n\n", env['model_name'])
        #         pass
        #     pass

        ### 判断实体之类型做相应的处理

        ## 如果实体之节点之类型是 process node，且内容之类型是 model content，且过程条件为空，则：
        if entity.attribute.node_type == {"process node"} and entity.attribute.content_type == {"model content"}:
            ## 运行过程之内容
            for (i, node) in enumerate(entity.process):
                condition = eval(node['condition']) if node['condition'] is not None else None
                if condition is None:
                    A, para, env, A_data = Operator.operate_branch_node(A, para, env, A_data, node['flow'])

        ## 如果实体之节点之类型是 container node，且内容之类型是 algorithm content，则运行：
        if entity.attribute.node_type == {"process node", "container node"} and entity.attribute.content_type == {"algorithm content"}:
            ## 运行容器之内容
            for (i, node) in enumerate(entity.container):
                # A, para, env, A_data = Operator.operate_branch_node(A, para, env, A_data, node)
                if node.attribute.node_type == {"terminal node"} and node.attribute.content_type == {"algorithm content"}:
                    ## 设置临时变量
                    b = (A.BB.on | A.BB.off)  # BB示性变量
                    ib = (A.BB.on | A.BB.off) & (A.BB.on | A.BB.off).T  # BI示性变量
                    # BB_Shock_last = deepcopy(A.BB.Shock_t)  # BB上一时期的冲击变量
                    # BB_isv_last = deepcopy(A.BB.isv)  # BB上一时期的isv变量
                    ## 运行算法
                    A = Operator.operate_terminal_node(A, b, ib, para, env, node)
                    env['round'] += 1  # 计次回合数
                    if (env['state_of_schedule'] == StateOfScheduleEnum.collecting) and (env['state_of_model'] == StateOfModelEnum.running):
                        env['state_of_schedule'] = Scheduler.schedule_collecting(A, env['running_mode'])

            ## 运行过程之内容
            for (i, node) in enumerate(entity.process):
                ## 判断流向
                condition = eval(node['condition']) if node['condition'] is not None else None
                logging.debug("        条件 %s 是 %s", node['condition'], condition)
                if condition and condition is not None and node['flow'] is not None:
                    logging.debug("        流至 %s %s", node['flow'].attribute.text_name, node['flow'].attribute.entity_name)
                    A, para, env, A_data = Operator.operate_branch_node(A, para, env, A_data, node['flow'])

        return A, para, env, A_data
        pass  # method




        #
        # def processContent_TerminalProcess(A: SystemicRiskAgent, para: dict, env: dict, entity: Entity, A_data: AgentDataCollection): #HACK无用，可以仅仅保留作为后续的借鉴
        #     """
        #     终端过程内容
        #
        #     Args:
        #         A (SystemicRiskAgent): Agent群变量
        #         para (dict): 参数变量
        #         env (dict): 环境变量
        #         A_data (AgentDataCollection): Agent群变量之数据
        #         entity (Entity): 实体
        #
        #     Returns: A, para, env, A_data
        #
        #     """
        #
        #     logging.debug("过程%s：%s", env['index_process'], env['process_name'])
        #
        #     env['index_stage'] = 0  # 初始化阶段所在位置
        #     env['is_step'] = True  # 初始化步进状态
        #     env['is_round'] = True  # 初始化回合状态
        #     env['is_process'] = True  # 初始化过程状态
        #     env['is_loop'] = True  # 初始化循环状态
        #     while env['is_loop'] == True:  # TODO
        #
        #         ## 回合数变动
        #         if (env['loaded_index_stage'] != 1):
        #             logging.debug("\n继续回合：%s\n", env['round'])
        #             pass
        #         else:
        #             env['round'] += 1  # 回合累加一
        #             logging.debug("\n开始回合：%s\n", env['round'])
        #             pass
        #
        #         ## 设置临时变量、示性变量
        #         BB_Shock_t_t1 = deepcopy(A.BB.Shock_t)
        #         BB_isv_t1 = deepcopy(A.BB.isv)
        #
        #         b = (A.BB.on | A.BB.off)  # 临时设置BB示性变量
        #         ib = (A.BB.on | A.BB.off) & (A.BB.on | A.BB.off).T  # 临时设置BI示性变量
        #
        #         ## 如果实体之内容之类型是process，且容器有内容，则运行容器之内容
        #         if entity.attribute.content_type == "process" and entity.container is not None:
        #             for (i, node) in enumerate(entity.container):  ## 运行容器内之每个内容
        #                 # logging.debug("过程 = %i，名称 = %s", env['index_process'], env['process_name'])
        #                 A, para, env, A_data = Operator.operate_branch_node(A, para, env, A_data, node)
        #
        #             ## 运行过程内之每个内容
        #             for (i, node) in enumerate(entity.process):
        #                 condition = eval(node['flow'])
        #                 if condition:
        #                     A, para, env, A_data = Operator.operate_terminal_node(A, b, ib, para, env, A_data, node)
        #
        #         ## 运行每一个阶段
        #         for (i, stage) in enumerate(entity.container):
        #             env['index_stage'] = i + 1
        #             env['stage_name'] = str(stage.entity_name)
        #             logging.debug("阶段%s：%s", env['index_stage'], env['stage_name'])
        #
        #             ## 调度并运行状态
        #             if env['state_of_schedule'] == StateOfScheduleEnum.loading:
        #                 env['state_of_schedule'] = Scheduler.schedule_loading(env['index_process'], env['index_stage'], env['loaded_index_process'], env['loaded_index_stage'], env['state_of_schedule'], env['index_of_schedule_position'])  # 调度读取
        #                 pass
        #             if env['state_of_schedule'] == StateOfScheduleEnum.stepping:
        #                 if (entity.attribute.content_type == "algorithm" and entity.container is None and entity.process is None):  # 如果实体之内容之类型是算法，且容器无内容，且过程无内容，则运行算法内容
        #                     A = Operator.operate_terminal_node(A, b, ib, para, env, stage)
        #
        #                 env['step'], env['is_step'], env['state_of_schedule'] = Scheduler.schedule_stepping(env['step'], env['step_size'])  # 步进
        #                 # logging.debug("调度状态 = %s",env['state_of_schedule'])
        #                 pass
        #
        #             Scheduler.is_step()  # 判断是否继续运行步进
        #             # logging.debug("是否继续步进 = %s", env['is_step'])
        #             if env['is_step'] == False:  # 如果步进停止，则跳出该循环:
        #                 break
        #                 pass
        #             pass  # for
        #
        #         env['is_process'] = Scheduler.is_process(A, BB_isv_t1, BB_Shock_t_t1, env['is_process'], env['stage_name'], entity)  # 判断是否继续运行过程
        #
        #         if env['state_of_schedule'] == StateOfScheduleEnum.saving:
        #             env['saved_index_process'], env['saved_index_stage'], env['loaded_index_process'], env['loaded_index_stage'], env['state_of_schedule'] = Scheduler.schedule_saving(env['index_process'], env['index_stage'], env['is_process'], env['index_of_schedule_position'])  # 调度存储
        #             pass
        #         if (env['state_of_schedule'] == StateOfScheduleEnum.collecting) and (env['state_of_model'] == StateOfModelEnum.running):
        #             env['state_of_schedule'] = Scheduler.schedule_collecting(A, A_data)
        #             # logging.debug("调度状态 = %s", env['state_of_schedule'])
        #             pass
        #
        #         Scheduler.is_round()  # 判断是否继续运行回合BUG
        #
        #         Scheduler.is_loop()  # 判断是否继续运行循环BUG
        #         pass  # while
        #
        #     return A, para, env, A_data
        #
        #     pass  # method

        pass  # class
