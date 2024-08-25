"""
运作机 #TODO 可以简化掉这个类，将其功能整合到`SystemicRiskSimulator.py`之中
"""

from SystemicRiskSimulator.external_packages import Path, timeit, os, datetime, logging, deepcopy, json, Any, pickle, sqlite3, np, pd, Optional, plt
from SystemicRiskSimulator.tools.logging_tools import log_message, record_work_state
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.operations.data_installer import DataInstaller
from SystemicRiskSimulator.core.operations.builder import Builder

from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


# @dataclass()
class Operator:
    """
    运作机
    """

    @classmethod
    def operate_installing(cls, sgv, para: Optional[dict] = None):
        """
        运作安装

        Args:
            sgv (dict): 模拟器全局变量
            para (Optional[dict]): 参数变量。默认为 None。如果 `init_parameters_method` 为 "set manually"，那么就需要设置此参数。

        Returns:

        """

        ## 设置参数作业列表
        if sgv['init_parameters_method'] == "import data":
            with open(Path(sgv['folderpath_parameters'], "parameters.pkl"), 'rb') as f:
                parameters_works = pd.read_pickle(f)
                num_parameters_works = len(parameters_works)
                ## SQLite 数据库统计实验组之上一次的作业之完成情况
                time_start_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
                # 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续删除原有的作业数据库再重建
                if os.path.exists(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db")):
                    is_exist_experiments_works_status_db = True
                    mtime_of_file_parameters_pkl = Path(sgv['folderpath_parameters'], "parameters.pkl").resolve().stat().st_mtime
                    mtime_of_file_experimentsWorksStatus_db = Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db").resolve().stat().st_mtime
                    if mtime_of_file_parameters_pkl > mtime_of_file_experimentsWorksStatus_db:
                        is_recreate_experiments_works_status_db = True
                    else:
                        is_recreate_experiments_works_status_db = False
                        pass  # if
                else:
                    is_exist_experiments_works_status_db = False
                    is_recreate_experiments_works_status_db = True
                    pass  # if
                if is_exist_experiments_works_status_db:
                    os.remove(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
                    pass  # if
                if is_recreate_experiments_works_status_db:  # 创建数据库并初始化表格
                    conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
                    c = conn.cursor()
                    c.execute("""CREATE TABLE IF NOT EXISTS experiments
                                    (id INTEGER PRIMARY KEY, status_实验组模拟程序 TEXT)""")
                    # 根据实验组总数量，生成实验组作业状态信息。其中，所有实验组作业状态为 "RAW"
                    for i in range(1, num_parameters_works + 1):
                        c.execute("INSERT INTO experiments (id, status_实验组模拟程序) VALUES (?, ?)", (i, "RAW"))
                        pass  # for
                    conn.commit()
                else:
                    # 连接现有数据库
                    conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
                    c = conn.cursor()
                    if sgv['is_rerun_all_done_works_in_the_same_experiments']:
                        c.execute("UPDATE experiments SET status_实验组模拟程序 = 'RAW'")
                        conn.commit()
                        pass  # if
                    pass  # if
                # 检查实验组作业完成状态
                c.execute("SELECT id, status_实验组模拟程序 FROM experiments")
                rows = c.fetchall()
                list_idsExp_DOING = []
                list_idsExp_DONE = []
                list_idsExp_RAW = []
                for row in rows:
                    exp_id, status_实验组模拟程序 = row[0], row[1]
                    if status_实验组模拟程序 == "DOING":
                        list_idsExp_DOING.append(exp_id)
                    elif status_实验组模拟程序 == "DONE":
                        list_idsExp_DONE.append(exp_id)
                    else:
                        list_idsExp_RAW.append(exp_id)
                        pass  # if
                    pass  # for
                list_idsExp_PLAN = sgv['list_idsExperiment_to_run'] if sgv['list_idsExperiment_to_run'] is not None else list(range(1, num_parameters_works + 1))
                list_idsExp_TASK = [i for i in list_idsExp_PLAN if i not in list_idsExp_DONE]
                # 保存实验组作业完成状态信息
                with open(Path(sgv['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
                    json.dump({
                        "计划运行的实验组 id": list_idsExp_TASK,
                        "未运行过的实验组 id": list_idsExp_RAW,
                        "之前运行中被中断的实验组 id": list_idsExp_DOING,
                        "已完成的实验组 id": list_idsExp_DONE,
                        "完成率": len(list_idsExp_DONE) / num_parameters_works,
                        "中断率": len(list_idsExp_DOING) / num_parameters_works,
                    }, f)
                    logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
                        "之前运行中被中断的实验组 id": list_idsExp_DOING,
                        "完成率": len(list_idsExp_DONE) / num_parameters_works,
                        "中断率": len(list_idsExp_DOING) / num_parameters_works,
                    }))
                    pass  # with

                ### 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。#BUG 如果实验组很多，那么绘制图像会占用大量的内存与时间！可以考虑注释不运行这段。
                # ids = [row[0] for row in rows]  # 获取实验组 id
                # status_实验组模拟程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
                # Tools.draw_color_band_before_experiments(ids, status_实验组模拟程序_运行状态, list_idsExp_PLAN, list_idsExp_TASK, Path(sgv['folderpath_experiments_output_log'], "color_band_distribution_before_实验组模拟程序.png"))

                time_end_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
                logging.debug(f"统计参数数据完成，用时：{time_end_统计实验组作业情况 - time_start_统计实验组作业情况} 秒。")  # #DEBUG

                conn.close()  # 关闭数据库连接
                pass  # with

            Collector.export_parameter_data(sgv, parameters_works)  # 导出控制参数数据
        elif sgv['init_parameters_method'] == "set manually":  # #TODO HACK 这个选项几乎被废弃了。可以删除。
            parameters_works = Tools.dict_to_product_list(para)  # 设置字典列表，由 set_parameters_variables 各参数之各可能的取值排列组合而成。此将用于做实验
            Collector.export_parameter_data(parameters_works, para)  # 导出控制参数数据
            pass  # if

        sgv['len_parameters_works'] = num_parameters_works

        ## 构建本次实验组所需的所有模型

        ### 判断属于什么运行模式
        if ~(sgv['is_develope_mode'] and sgv['is_maintain_model_files_in_simulator_when_develope_mode']):
            # 如果处于应用实验状态，则复制模型数据与内容到输出文件夹下
            Tools._delete_and_recreate_folder(sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建输出文件夹之模型文件夹
            Tools._copy_files_from_other_folders(sgv['folderpath_models'], sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 复制模型文件夹到输出文件夹之模型文件夹
            # # 如果处于应用实验状态，则复制模型数据与内容到`SystemicRiskSimulator/models`文件夹下，另外导出一份到输出文件夹之配置文件夹下
            # Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])
            # Tools._copy_files_from_other_folders(sgv['folderpath_models'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])
            # Tools._copy_files_from_other_folders(sgv['folderpath_models'], sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])
        else:
            # 如果处于开发调试模式，则不复制正在开发的模型文件夹
            # # 如果处于开发调试模式，则复制正在开发的模型到输出文件夹之配置文件夹下 #NOW 可以删除
            # Tools._delete_and_recreate_folder(sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])
            # Tools._copy_files_from_other_folders(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])
            pass  # if

        ## 导入实体数据，生成实体集、内容集并返回
        if sgv['is_use_flow_form_version_model']:
            ## NOTE 如果使用`Processor.process_entity_by_process_and_container_component()`
            Builder.build_entities_by_process_and_container_component(sgv)  # NOTE：一次只处理一个模型 #HACK 已经过时，可以删除
        else:
            ## NOTE 如果直接使用非流程版的形式的模型
            Builder.build_entities_by_execute(sgv)
        pass  # if

        ## 导出配置数据
        Collector.export_config_data(sgv)

        return sgv, list_idsExp_TASK, parameters_works, EntityManager.mainModelInstanceEntities

        pass  # function

    @classmethod
    def operate_run_experiment(cls, A: SystemicRiskAgent, A_last: SystemicRiskAgent, A_data: AgentDataCollection, sgv: dict, para: dict, model: Any):
        """
        运作运行实验。用于传统的 ABM 模型。

        Args:
            A (SystemicRiskAgent): 多主体
            A_last (SystemicRiskAgent): 上一回合的多主体
            A_data (AgentDataCollection): 多主体之数据
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量
            model (Any): 模型节点实体

        Returns:

        """

        ## 运行实验

        sgv['experiment_start_time'] = timeit.default_timer()  # 记录此次实验开始时间

        if sgv['is_use_flow_form_version_model']:
            # ## NOTE 如果使用`Processor.process_entity_by_process_and_container_component()` HACK 已经过时，弃用，可删除。
            # # Scheduler.schedule(sgv)  # 调度状态变成`running`
            # model, A, sgv['A_data'], para, sgv = Processor.process_entity_by_process_and_container_component(model, A, sgv['A_data'], para, sgv)  # 执行具体的模型，通过执行模型实体的方式
            # sgv['is_continue_process'] = False  # 不再继续运行过程
            pass
        else:
            ## NOTE 如果直接使用非流程版的形式的模型。HACK 注意这个时候 `env['test_max_num_of_turn']` 失效

            # Scheduler.schedule(sgv)  # 调度状态变成`running`

            # model, A, A_data, para, sgv = Processor.process_entity_by_execute_component(model, A, A_data, para, sgv)  # 执行具体的模型，通过执行模型实体的方式

            modelEntity = model.content  # 获取节点实体对应的模型实体

            content_Finance = modelEntity.content['content_finance']()
            if len(modelEntity.attribute.other) != 0 and modelEntity.attribute.other['agents_strategies'] is not None:
                content_Agents = modelEntity.content['content_agents'](np.array(para['Strategy_default']))  # BUG 不能这样代入参数
                content_Model = modelEntity.content['content_model'](content_Finance, content_Agents)
            else:
                content_Model = modelEntity.content['content_model'](content_Finance)
                pass  # if

            if not sgv['is_enable_multiprocessing']:
                log_message(
                    "    开始执行模型内容：",
                    Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                    f"logger_{sgv['id_experiment']}",
                    is_enable_multiprocessing=sgv['is_enable_multiprocessing']
                )

            # sgv['process_name'] = modelEntity.attribute.entity_name  # 执行的过程之名称（英文名称）

            # modelEntity.execute(A, A_data, para, sgv)
            content_Model.model_content(A, A_last, A_data, para, sgv)

            pass  # if

        pass  # function

    @classmethod
    def operate_reset_experiment_for_PettingZoo(cls, sgv: dict, para: dict):
        """
        运作初始化实验。用于使用基于 PettingZoo 、Gym 等强化学习环境工具包自定义的模型。

        Args:
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A, A_data, sgv, para
        """

        record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DOING", sgv['folderpath_experiments_output_log'])  # 记录本次实验作业的完成状态为 "DOING"

        ## 重置模拟器全局变量  # TODO 需要整理一下这几个待重置的模拟器全局变量
        sgv['index_of_schedule_position'] = []
        sgv['turn'] = 0
        sgv['phase'] = 0
        sgv['step'] = 0
        # sgv['model_name'] = para['model_name']  #HACK 2024-05-14 此时刻版本之 parameters 没有这个配置项了
        sgv['process_name'] = "START"
        sgv['test_continous_loop_of_model'] = 0
        sgv['is_continue_process'] = True
        # sgv['A_data'] = None

        logging.info("重置实验" + str(sgv['id_experiment']) + "/" + str(sgv['len_parameters_works']) + "开始：\n")

        logging.info("\n相关实验参数：" + str(para) + "\n")

        ## 初始化 agents 数据
        A = DataInstaller.install_data(init_data_method=sgv['init_data_method'], sgv=sgv, para=para)  # 安装本次实验所需的多主体数据
        # sgv['A_data'] = Collector.collect(A, sgv['A_data'], sgv)  # 收集初始数据
        logging.debug("                    初始化数据")
        # sgv['A_data'] = Collector.init_agent_data_collection(A, sgv)
        A_data = Collector.init_agent_data_collection(A, sgv)
        # sgv['step'] += 1

        return A, A_data, sgv, para
        pass  # function

    @classmethod
    def operate_reset_experiment(cls, sgv: dict, para: dict, model: Any):
        """
        运作初始化实验。用于使用使用强化学习环境工具包自定义的模型。

        Args:
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A, A_data, sgv, para
        """

        # # 更新实验组作业状态为 "DOING"
        # conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
        # c = conn.cursor()
        # c.execute("INSERT OR REPLACE INTO experiments (id, status_实验组模拟程序) VALUES (?, 'DOING')", (sgv['id_experiment'],))
        # conn.commit()
        # conn.close()

        record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DOING", sgv['folderpath_experiments_output_log'])  # 记录本次实验作业的完成状态为 "DOING"

        modelEntity = model.content  # 获取节点实体对应的模型实体

        ## 重置模拟器全局变量  # TODO 需要整理一下这几个待重置的模拟器全局变量
        sgv['index_of_schedule_position'] = []
        sgv['turn'] = 0
        sgv['phase'] = 0
        sgv['step'] = 0
        sgv['model_name'] = modelEntity.attribute.entity_name
        sgv['process_name'] = "START"
        sgv['test_continous_loop_of_model'] = 0
        sgv['is_continue_process'] = True
        # sgv['A_data'] = None

        if not sgv['is_enable_multiprocessing']:
            log_message(
                "重置实验" + str(sgv['id_experiment']) + "/" + str(sgv['len_parameters_works']) + "开始：\n" + "\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + "\n相关实验参数：" + str(para) + "\n",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing=sgv['is_enable_multiprocessing']
            )

        ## 初始化 agents 数据
        A = DataInstaller.install_data(init_data_method=sgv['init_data_method'], sgv=sgv, para=para)  # 安装本次实验所需的多主体数据
        A_last = SystemicRiskAgent(2, deepcopy(A.BB), deepcopy(A.b), deepcopy(A.IB), deepcopy(A.ib))
        # sgv['A_data'] = Collector.collect(A, sgv['A_data'], sgv)  # 收集初始数据

        ## 计算个体数量
        sgv['num_bank'] = len(A.BB['id_agent'])

        if not sgv['is_enable_multiprocessing']:
            log_message(
                "                    初始化数据",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing=sgv['is_enable_multiprocessing']
            )

        # sgv['A_data'] = Collector.init_agent_data_collection(A, sgv)
        A_data = Collector.init_agent_data_collection(A, sgv)
        # sgv['step'] += 1

        return A, A_last, A_data, sgv, para
        pass  # function

    # @classmethod
    # def operate_step_experiment(cls, sgv: dict, para: dict, model: Any):
    @classmethod
    def operate_step_experiment(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, sgv: dict, para: dict, model: Any):
        """
        运作步进实验。用于使用强化学习环境工具包自定义的模型。

        Args:
            A (SystemicRiskAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            sgv (dict): 模拟器全局变量
            para (dict): 参数字典
            model (Any): 模型节点实体

        Returns:

        """

        ## 运行实验

        sgv['experiment_start_time'] = timeit.default_timer()  # 记录此次实验开始时间

        modelEntity = model.content  # 获取节点实体对应的模型实体

        if not sgv['is_enable_multiprocessing']:
            log_message(
                "    开始执行模型内容：",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing=sgv['is_enable_multiprocessing']
            )

        sgv['process_name'] = modelEntity.attribute.entity_name  # 执行的过程之名称（英文名称）

        process = modelEntity.process
        # modelEntityContent = modelEntity.content

        A, A_data, para, sgv = process(modelEntity, A, A_data, para, sgv)

        return A, A_data, sgv, para

        pass  # function

    @classmethod
    def operate_end_experiment(cls, A_data: AgentDataCollection, sgv: dict):

        # if True:  # #HACK 如果需要调试，请使用这个替换下面的
        if not sgv['is_enable_multiprocessing']:
            log_message(
                "    结束执行模型内容。",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing=sgv['is_enable_multiprocessing']
            )

        sgv['is_continue_process'] = False  # 不再继续运行过程

        sgv['experiment_end_time'] = timeit.default_timer()  # 记录此次实验结束时间
        sgv['experiments_running_time'] += sgv['experiment_end_time'] - sgv['experiment_start_time']  # 累加此次实验运行时长

        ## 导出数据之于已经收集的，然后结束本次实验

        sgv['export_data_start_time'] = timeit.default_timer()  # 记录此次导出数据开始时间

        if not sgv['is_enable_multiprocessing']:
            log_message(
                "                    导出数据",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing=sgv['is_enable_multiprocessing']
            )

        Collector.export_agent_data(A_data, sgv)

        sgv['export_data_end_time'] = timeit.default_timer()  # 记录此次导出数据结束时间
        sgv['export_data_running_time'] += sgv['export_data_end_time'] - sgv['export_data_start_time']  # 累加此次导出数据运行时长

        record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DONE", sgv['folderpath_experiments_output_log'])

        if not sgv['is_enable_multiprocessing']:
            log_message(
                "本次实验结束，还剩下" + str(sgv['len_parameters_works'] - sgv['id_experiment']) + "个实验。\n\n",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing=sgv['is_enable_multiprocessing']
            )

        pass  # function

    pass  # class
