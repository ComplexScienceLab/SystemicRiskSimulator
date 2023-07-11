"""
运作机
"""

from PySystemicRiskLab import os, logging, dataclass, Any
from PySystemicRiskLab.core.operations.entity_manager import EntityManager
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
# from PySystemicRiskLab.core.define.define_parameterVariables import para
from PySystemicRiskLab.core.operations.collector import Collector
# from PySystemicRiskLab.core.operations.executer import Executer
# from PySystemicRiskLab.core.operations.model_installer import ModelInstaller
from PySystemicRiskLab.core.operations.data_installer import DataInstaller
from PySystemicRiskLab.core.operations.scheduler import Scheduler
from PySystemicRiskLab.core.operations.builder import Builder
from PySystemicRiskLab.core.operations.processor import Processor
# from PySystemicRiskLab.core.functions.fun_finance import Finance

from PySystemicRiskLab.tools.tools import Tools

pass  # end import


@dataclass()
class Operator:
    """
    运作机
    """

    @classmethod
    def operate_installing(cls, env, para):
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

        ## 构建本次实验组所需的所有模型
        ## 导入实体数据，生成实体集、内容集并返回
        Builder.build_entities_by_process_and_container_component(env)  # BUG 会不会出现不能处理多个模型的情形？

        return env, EntityManager.modelEntities

        pass  # method

    @classmethod
    def operate_experiment(cls, env: dict, para: dict, model: Any):
        """
        运作实验

        Args:
            env (dict): 环境变量，默认env
            para (dict): 参数变量，默认para
            model (Entity): 模型实体

        Returns:

        """

        env = Scheduler.schedule(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.initializing:
            # 重置环境变量
            env['index_of_schedule_position'] = []
            env['step'] = 0
            env['round'] = 0
            env['model_name'] = para['model_name']
            env['process_name'] = "START"
            env['is_continue_process'] = True
            env['test_continous_loop_of_model'] = 0
            env['model_process_state'] = "has not process"
            env['A_data'] = None

            logging.info("实验" + str(env['id_experiment']) + "/" + str(len(env['list_combination_of_para'])) + "开始：\n")

            logging.info("相关实验参数：" + str(para) + "\n")

            ## 初始化
            A = DataInstaller.install_data(init_method=env['init_method'])  # 安装本次实验所需的多主体数据
            env['A_data'] = Collector.collect(A, env['A_data'], env)  # 收集初始数据

            # ## 构建本次实验所需的状态数据
            # Finance.build_state_const_variables(A.BB, A.IB)

            # ## 初始化本次实验所需的多主体数据
            # A = DataInstaller.initialize_data(A, para, env)
            pass  # if

        ## HACK 如果使用`Processor.process_entity_by_process_and_container_component()`
        env = Scheduler.schedule(env)  # 调度状态变成`running`
        model, A, env['A_data'], para, env = Processor.process_entity_by_process_and_container_component(model, A, env['A_data'], para, env)  # 执行具体的模型，通过执行模型实体的方式
        env['is_continue_process'] = False  # 不再继续运行过程

        # ## HACK 如果使用`Processor.process_entity_by_node_component()`
        # env = Scheduler.schedule(env)
        # model, A, A_data, para, env = Executer.execute_branch_entity(model, A, A_data, para, env)  # 执行具体的模型，通过执行模型实体的方式
        # env['is_continue_process'] = False  # 不再继续运行过程

        ## 导出数据之于已经收集的
        env = Scheduler.schedule(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.ending:
            Collector.collect(None, env['A_data'], env)

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
