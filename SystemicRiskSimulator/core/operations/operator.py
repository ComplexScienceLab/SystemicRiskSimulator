"""
运作机
"""

from SystemicRiskSimulator.external_packages import Path, time, logging, dataclass, Any, pickle, pd
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.operations.data_installer import DataInstaller
from SystemicRiskSimulator.core.operations.builder import Builder
from SystemicRiskSimulator.core.operations.processor import Processor

from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


@dataclass()
class Operator:
    """
    运作机
    """

    @classmethod
    def operate_installing(cls, sgv, para):
        """
        运作安装

        Args:
            sgv (dict): 模拟器全局变量

        Returns:

        """

        ## 导出配置数据
        Collector.export_config_data(sgv)

        ## 设置参数集
        if sgv['init_parameters_method'] == "import data":
            with open(Path(sgv['folderpath_parameters'], "parameters.pkl"), 'rb') as f:
                sgv['list_combination_of_para'] = pd.read_pickle(f)
            Collector.export_parameter_data(sgv['list_combination_of_para'])  # 导出控制参数数据
        elif sgv['init_parameters_method'] == "set manually":
            sgv['list_combination_of_para'] = Tools.dict_to_product_list(para)  # 设置字典列表，由 set_parameters_variables 各参数之各可能的取值排列组合而成。此将用于做实验
            Collector.export_parameter_data(sgv['list_combination_of_para'], para)  # 导出控制参数数据

        ## 构建本次实验组所需的所有模型

        ## 复制模型数据与内容到`SystemicRiskSimulator/models`文件夹下，另外导出一份到输出文件夹之配置文件夹下
        Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(sgv['folderpath_models'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(sgv['folderpath_models'], sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])

        ## 导入实体数据，生成实体集、内容集并返回
        if sgv['is_use_flow_form_version_model']:
            ## NOTE 如果使用`Processor.process_entity_by_process_and_container_component()`
            Builder.build_entities_by_process_and_container_component(sgv)  # NOTE：一次只处理一个模型
        else:
            ## NOTE 如果直接使用非流程版的形式的模型
            Builder.build_entities_by_execute(sgv)
            pass  # if

        return sgv, EntityManager.mainModelInstanceEntities

        pass  # function

    @classmethod
    def operate_experiment(cls, sgv: dict, para: dict, model: Any):
        """
        运作实验

        Args:
            sgv (dict): 模拟器全局变量，默认env
            para (dict): 参数变量，默认para
            model (Any): 模型实体

        Returns:

        """


        ## 重置模拟器全局变量  # TODO 需要整理一下这几个待重置的模拟器全局变量
        sgv['index_of_schedule_position'] = []
        sgv['round'] = 0
        sgv['phase'] = 0
        sgv['step'] = 0
        sgv['time'] = 0  # TODO 似乎没有用到
        sgv['model_name'] = para['model_name']
        sgv['process_name'] = "START"
        sgv['test_continous_loop_of_model'] = 0
        sgv['model_process_state'] = "has not process"
        sgv['A_data'] = None

        logging.info("实验" + str(sgv['id_experiment']) + "/" + str(len(sgv['list_combination_of_para'])) + "开始：\n")

        logging.info("\n相关实验参数：" + str(para) + "\n")

        ## 初始化 agents 数据
        A = DataInstaller.install_data(init_data_method=sgv['init_data_method'], sgv=sgv, para=para)  # 安装本次实验所需的多主体数据
        # sgv['A_data'] = Collector.collect(A, sgv['A_data'], sgv)  # 收集初始数据
        logging.debug("                    初始化数据")
        sgv['A_data'] = Collector.init_agent_data_collection(A, sgv)
        sgv['step'] += 1

        ## 运行实验

        sgv['experiment_start_time'] = time.time()  # 记录此次实验开始时间

        if sgv['is_use_flow_form_version_model']:
            # ## NOTE 如果使用`Processor.process_entity_by_process_and_container_component()` HACK 已经过时，弃用，可删除。
            # # Scheduler.schedule(sgv)  # 调度状态变成`running`
            # model, A, sgv['A_data'], para, sgv = Processor.process_entity_by_process_and_container_component(model, A, sgv['A_data'], para, sgv)  # 执行具体的模型，通过执行模型实体的方式
            # sgv['is_continue_process'] = False  # 不再继续运行过程
            pass
        else:
            ## NOTE 如果直接使用非流程版的形式的模型。HACK 注意这个时候 `env['test_max_num_of_round']` 失效
            # Scheduler.schedule(sgv)  # 调度状态变成`running`
            model, A, sgv['A_data'], para, sgv = Processor.process_entity_by_execute_component(model, A, sgv['A_data'], para, sgv)  # 执行具体的模型，通过执行模型实体的方式
            sgv['is_continue_process'] = False  # 不再继续运行过程
            pass  # if

        sgv['experiment_end_time'] = time.time()  # 记录此次实验结束时间
        sgv['experiments_running_time'] += sgv['experiment_end_time'] - sgv['experiment_start_time']  # 累加此次实验运行时长

        ## 导出数据之于已经收集的，然后结束本次实验

        sgv['export_data_start_time'] = time.time()  # 记录此次导出数据开始时间

        logging.debug("                    导出数据")
        Collector.export_agent_data(sgv['A_data'], sgv)

        sgv['export_data_end_time'] = time.time()  # 记录此次导出数据结束时间
        sgv['export_data_running_time'] += sgv['export_data_end_time'] - sgv['export_data_start_time']  # 累加此次导出数据运行时长

        logging.info("本次实验结束，还剩下" + str(len(sgv['list_combination_of_para']) - sgv['id_experiment']) + "个实验。\n\n")

        pass  # function

    pass  # class
