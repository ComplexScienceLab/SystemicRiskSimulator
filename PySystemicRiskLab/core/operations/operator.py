"""
运作机
"""

from PySystemicRiskLab import os, logging, dataclass, Optional
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.define.define_parameterVariables import para
from PySystemicRiskLab.core.operations.collector import Collector
from PySystemicRiskLab.core.operations.executer import Executer
from PySystemicRiskLab.core.operations.installer import ModelInstaller, DataInstaller
from PySystemicRiskLab.core.operations.scheduler import Scheduler
from PySystemicRiskLab.tools.tools import Tools

pass  # end import


@dataclass()
class Operator:
    """
    运作机
    """

    @classmethod
    def operate_installing(cls, env):
        """
        运作安装

        Args:
            env (dict): 环境变量

        Returns:

        """

        ## 获取项目路径
        env['folderpath_project'] = Tools.get_project_rootpath()

        ## 生成实验组文件夹用于本批次实验
        env = Tools.set_experiments_folders()

        ## 设置日志
        logging.basicConfig(
            level=env['test_logging'],
            filename=os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"),  # 建立文件以记录log
        )

        logging.debug("\n实验组名称：%s", env['foldername_of_experiments'])

        ## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
        env['list_combination_of_para'] = Tools.dict_to_product_list(para)  # 组合排列多结构体成为列表

        ## 导出控制参数数据
        Collector.export_parameter_data(list_combination_of_para=env['list_combination_of_para'], para=para)

        models = ModelInstaller.install_model()

        # ## 构建、安装本次实验组所需的所有模型
        # ### 导入实体数据，生成实体集、内容集并返回
        # entities, contents = ModelBuilder.build_entities(env)
        # ### 生成模型列表
        # models = {}
        # for (i, model_name) in enumerate(para['model_name']):
        #     model = eval("entities['modelEntity_Model" + model_name + "']")
        #
        #     ### 对于每一个模型，根据已经生成的模型，生成索引序列                                                                                                                                                                                                 遍历序列，用于后序遍历所有节点。
        #     # install_entity_queue = ModelInstaller.build_postorder_traversial(model) #HACK暂时不用
        #     models[model_name] = model  # 模型列表
        #     pass

        return env, models

        pass  # method

    @classmethod
    def operate_experiment(cls, env: dict, para: dict, entity: Entity):
        """
        运作实验

        Args:
            env (dict): 环境变量，默认env
            para (dict): 参数变量，默认para
            entity (Entity): 过程实体

        Returns:

        """

        env = Scheduler.schedule(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.initializing:
            # 重置环境变量
            env['index_of_schedule_position'] = []
            env['index_model'] = 1
            env['index_process'] = 1
            env['index_stage'] = 1
            env['saved_index_process'] = 1
            env['saved_index_stage'] = 1
            env['loaded_index_process'] = 1
            env['loaded_index_stage'] = 1
            env['step'] = 0
            env['round'] = 0
            env['saved_model_name'] = ""
            env['model_name'] = para['model_name']
            env['process_name'] = ""
            env['stage_name'] = ""
            env['is_step'] = False
            env['is_loop'] = True
            env['is_round'] = True
            env['is_terminalProcess'] = True
            env['is_process'] = True
            env['running_mode'] = "continue running mode"
            env['is_continue_process'] = True
            env['is_model'] = True
            env['is_experiment'] = True
            env['test_continous_loop_of_model'] = 0

            logging.info("实验" + str(env['id_experiment']) + "/" + str(len(env['list_combination_of_para'])) + "开始：\n")

            logging.info("相关实验参数：" + str(para) + "\n")

            ## 安装本次实验所需的数据
            A = DataInstaller.install_data(init_method=env['init_method'])
            A_data = Collector.collect(A, None, env)
            pass  # if

        # test_continous_loop_of_model = 0  # 设置模型运行最大步数
        # while (env['is_model'] == True and test_continous_loop_of_model <= env['test_max_count_continous_loop_of_model']):
        #     test_continous_loop_of_model += 1

        env = Scheduler.schedule(env)
        A, A_data, para, env = Executer.execute_branch_node(entity, A, A_data, para, env)  # 执行具体的模型，通过执行模型模块的方式 #BUG
        env['is_continue_process'] = False  # 不再继续运行过程

        # if test_continous_loop_of_model >= env['test_max_count_continous_loop_of_model']:
        #     logging.info("超过该模型最大步进次数，强制跳出循环。")
        #     pass  # if
        #
        # pass # while

        ## 导出数据之于已经收集的
        env = Scheduler.schedule(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.ending:
            Collector.collect(None, A_data, env)

        ## 结束本次实验
        env = Scheduler.schedule(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.idle:
            logging.info("本次实验结束，还剩下" + str(len(env['list_combination_of_para']) - env['id_experiment']) + "个实验。\n\n")

        pass  # method

    # @classmethod
    # def operate_running(cls):
    #
    #     pass  # class

    pass  # class
