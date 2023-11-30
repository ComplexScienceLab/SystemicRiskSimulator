"函数区：收集数据"

## 函数区：收集数据
from SystemicRiskSimulator import pd, Path, Optional, logging
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.core.define.define_environmentVariables import env
from SystemicRiskSimulator.core.define.define_type import *

pass  # end import


class Collector:

    @classmethod
    def collect(cls, A: Optional[SystemicRiskAgent], A_data: Optional[AgentDataCollection], env: dict):
        """
        运作收集数据

        Args:
            A (Optional[SystemicRiskAgent]): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            env (dict): 环境变量

        Returns:
            如果是初始化数据，则返回 A_data；如果是收集数据，则返回 A_data, env；如果是导出数据，则无返回；

        """
        if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
            # Scheduler.schedule(env)
            logging.debug("                    收集数据")
            # env['id_data'] += 1  # 累加数据帧ID号
            A_data = Collector.collect_agent_data(A, A_data, env)
            # Scheduler.schedule(env)
            return A_data, env
        elif env['state_of_schedule'] == StateOfScheduleEnum.initializing:
            logging.debug("                    初始化数据")
            A_data = Collector.init_agent_data_collection(A, env)
            return A_data
        elif env['state_of_schedule'] == StateOfScheduleEnum.ending:
            logging.debug("                    导出数据")
            Collector.export_agent_data(A_data, env)
        else:
            pass
        pass  # function

    ## NOTE 当用 Pandas 之数据结构时：
    @classmethod
    def init_agent_data_collection(cls, A: pd.Series, env: dict):
        """

        Args:
            A (pd.Series): 系统性风险个体众
            env (dict): 环境变量

        Returns:
            A_data: 待收集的数据

        """

        ## 初始化数据框用以存储agent数据
        BB_data = pd.DataFrame()
        IB_data = pd.DataFrame()
        A_data = AgentDataCollection(BB_data, IB_data)

        env['series_BB'] = pd.Series()
        for i in A.BB.index:
            env['series_BB'][i] = A.BB[i].copy()
        env['df_BB'] = env['series_BB'].to_frame().transpose()
        env['df_BB'].insert(loc=0, column='process_name', value=env['process_name'])
        env['df_BB'].insert(loc=1, column='step', value=env['step'])
        env['df_BB'].insert(loc=2, column='round', value=env['round'])
        env['df_BB'].insert(loc=3, column='phase', value=env['phase'])
        # BB_data = pd.concat([BB_data, env['df_BB']], ignore_index=True)
        A_data.BB = pd.concat([A_data.BB, env['df_BB']], ignore_index=True)

        env['series_IB'] = pd.Series()
        for i in A.IB.index:
            env['series_IB'][i] = A.IB[i].copy()
        env['df_IB'] = env['series_IB'].to_frame().transpose()
        env['df_IB'].insert(loc=0, column='process_name', value=env['process_name'])
        env['df_IB'].insert(loc=1, column='step', value=env['step'])
        env['df_IB'].insert(loc=2, column='round', value=env['round'])
        env['df_IB'].insert(loc=3, column='phase', value=env['phase'])
        # IB_data = pd.concat([IB_data, env['df_IB']], ignore_index=True)
        A_data.IB = pd.concat([A_data.IB, env['df_IB']], ignore_index=True)

        # A_data = pd.Series([BB_data, IB_data], index=['BB', 'IB'])
        return A_data
        pass

    @classmethod
    def collect_agent_data(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, env: dict):
        """
        收集数据并存储

        Args:
            A (SystemicRiskAgent): 系统性风险个体众
            A_data (AgentDataCollection): 个体众数据集
            env: 环境变量

        Returns:
            A_data: 待收集的数据

        """
        # BB_data, IB_data = A_data.BB, A_data.IB

        # BB_df = A.BB.to_frame().transpose()
        # BB = deepcopy(A.BB)
        # env['series_BB'] = pd.Series()
        for i in A.BB.index:
            env['series_BB'][i] = A.BB[i].copy()
        env['df_BB'] = env['series_BB'].to_frame().transpose()
        env['df_BB'].insert(loc=0, column='process_name', value=env['process_name'])
        env['df_BB'].insert(loc=1, column='step', value=env['step'])
        env['df_BB'].insert(loc=2, column='round', value=env['round'])
        env['df_BB'].insert(loc=3, column='phase', value=env['phase'])
        A_data.BB = pd.concat([A_data.BB, env['df_BB']], ignore_index=True)
        # BB_data = pd.concat([BB_data, env['df_BB']], ignore_index=True)

        # IB_df = A.IB.to_frame().transpose()
        # IB = deepcopy(A.IB)
        # env['series_IB'] = pd.Series()
        for i in A.IB.index:
            env['series_IB'][i] = A.IB[i].copy()
        env['df_IB'] = env['series_IB'].to_frame().transpose()
        env['df_IB'].insert(loc=0, column='process_name', value=env['process_name'])
        env['df_IB'].insert(loc=1, column='step', value=env['step'])
        env['df_IB'].insert(loc=2, column='round', value=env['round'])
        env['df_IB'].insert(loc=3, column='phase', value=env['phase'])
        A_data.IB = pd.concat([A_data.IB, env['df_IB']], ignore_index=True)
        # IB_data = pd.concat([IB_data, IB_df], ignore_index=True)

        # A_data.BB, A_data.IB = BB_data, IB_data
        return A_data
        pass

    @classmethod
    def export_agent_data(cls, A_data: AgentDataCollection, env: dict):
        """
        HACK导出实验结果数据

        NOTE：查询列具有的数据类型可以用以下语句：

        ```python
        list_type_of_columns_01 = [A_data.BB[v].dtype for v in A_data.BB.columns]
        list_type_of_columns_02 = [A_data.BB[v][0].dtype for v in A_data.BB.columns]
        list_type_of_columns_01 = [A_data.IB[v].dtype for v in A_data.IB.columns]
        list_type_of_columns_02 = [A_data.IB[v][0].dtype for v in A_data.IB.columns]
        ```

        Args:
            A_data: 个体众数据集
            env(dict): 环境变量

        """

        ## 导出为pkl格式
        pd.to_pickle(A_data.BB, Path(env['folderpath_experiments_output_data'], r"BB_exp=" + str(env['id_experiment']) + r".pkl"))  # 导出为pkl格式
        pd.to_pickle(A_data.IB, Path(env['folderpath_experiments_output_data'], r"IB_exp=" + str(env['id_experiment']) + r".pkl"))  # 导出为pkl格式

        pass  # function

    # ## NOTE 当用对象字段数据结构时：
    # @classmethod
    # def init_agent_data_collection(cls, A: SystemicRiskAgent, env: dict):
    #     """
    #
    #     Args:
    #         A (SystemicRiskAgent): 系统性风险个体众
    #         env (dict): 环境变量
    #
    #     Returns:
    #         A_data: 待收集的数据
    #
    #     """
    #     BB_data_item = dict(
    #         {
    #             list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
    #             list(env.keys())[list(env.keys()).index('step')]: env['step'],
    #             list(env.keys())[list(env.keys()).index('round')]: env['round'],
    #             list(env.keys())[list(env.keys()).index('phase')]: env['phase'],
    #             'dataBB': deepcopy(A.BB)
    #         }
    #     )
    #     BB_data = tuple(
    #
    #     )
    #     BB_data.append(BB_data_item)  # 初始化banks之数据为一字典数组
    #
    #     IB_data_item = dict(
    #         {
    #             list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
    #             list(env.keys())[list(env.keys()).index('step')]: env['step'],
    #             list(env.keys())[list(env.keys()).index('round')]: env['round'],
    #             list(env.keys())[list(env.keys()).index('phase')]: env['phase'],
    #             'dataIB': deepcopy(A.IB)
    #         }
    #     )
    #     IB_data = []
    #     IB_data.append(IB_data_item)  # 初始化interbank之数据为一字典数组
    #
    #     A_data = AgentDataCollection(deepcopy(BB_data), deepcopy(IB_data))
    #     return A_data
    #     pass
    #
    # @classmethod
    # def collect_agent_data(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, env: dict):
    #     """
    #     收集数据并存储
    #
    #     Args:
    #         A (SystemicRiskAgent):
    #         A_data (AgentDataCollection):
    #         env:
    #
    #     Returns:
    #         A_data: 待收集的数据
    #
    #     """
    #     BB_data_item = dict(
    #         {
    #             list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
    #             list(env.keys())[list(env.keys()).index('step')]: env['step'],
    #             list(env.keys())[list(env.keys()).index('round')]: env['round'],
    #             list(env.keys())[list(env.keys()).index('phase')]: env['phase'],
    #             'dataBB': deepcopy(A.BB)
    #         }
    #     )
    #     A_data.BB.append(BB_data_item)  # 收集banks之数据为一字典数组
    #
    #     IB_data_item = dict(
    #         {
    #             list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
    #             list(env.keys())[list(env.keys()).index('step')]: env['step'],
    #             list(env.keys())[list(env.keys()).index('round')]: env['round'],
    #             list(env.keys())[list(env.keys()).index('phase')]: env['phase'],
    #             'dataIB': deepcopy(A.IB)
    #         }
    #     )
    #
    #     A_data.IB.append(IB_data_item)  # 收集interbank之数据为一字典数组
    #     return A_data
    #     pass
    #
    # @classmethod
    # def export_agent_data(cls, A_data: AgentDataCollection, env: dict):
    #     """
    #     导出实验结果数据
    #
    #     Args:
    #         A_data:
    #         env(dict): 环境变量
    #
    #     Returns:
    #
    #     """
    #
    #     ## 整理banks之数据为一数据框
    #     BB_data_export = pd.DataFrame()
    #     BB_data = pd.DataFrame()
    #     numRow, numCol = np.shape(A_data.BB[0]['dataBB'].A_all)
    #     for (i1, v1) in enumerate(A_data.BB):
    #         # BB_data['id_data'] = np.full(numRow, v1['id_data'])
    #         BB_data['process_name'] = np.full(numRow, v1['process_name'])
    #         BB_data['step'] = np.full(numRow, v1['step'])
    #         BB_data['round'] = np.full(numRow, v1['round'])
    #         BB_data['phase'] = np.full(numRow, v1['phase'])
    #         fieldNames = list(v1['dataBB'].__dict__.keys())
    #         fieldValues = list(v1['dataBB'].__dict__.values())
    #         for (i2, v2) in enumerate(fieldValues):
    #             BB_data[fieldNames[i2]] = v2
    #             pass
    #         BB_data_export = pd.concat([BB_data_export, BB_data])  # 追加`BB_data`至`BB_data_expert`
    #         pass  # for
    #     BB_data_export.insert(0, 'id', range(len(BB_data_export)))  # 添加id列
    #     BB_data_export.insert(1, 'id_data', np.repeat(range(len(BB_data_export) // env['num_bank']), env['num_bank']))  # 添加id_data列
    #     BB_data_export.to_csv(path.join(env['folderpath_experiments_output_data'], "BB_exp=" + str(env['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；
    #
    #
    #     ## 整理interbank之数据为一数据框
    #     IB_data_export = pd.DataFrame()
    #     IB_data = pd.DataFrame()
    #     # numRow, numCol = np.shape(A_data.IB[0]['dataIB'].A_IB)
    #     numRow, numCol = env['num_bank'], env['num_bank']
    #     for (i1, v1) in enumerate(A_data.IB):
    #         # IB_data['id_data'] = np.full(numRow * numCol, v1['id_data'])
    #         # IB_data['id_data'] = v1['id_data']
    #         IB_data['process_name'] = np.full(numRow * numCol, v1['process_name'])
    #         IB_data['step'] = np.full(numRow * numCol, v1['step'])
    #         IB_data['round'] = np.full(numRow * numCol, v1['round'])
    #         IB_data['phase'] = np.full(numRow * numCol, v1['phase'])
    #         IB_data['row'] = np.repeat(range(1, numRow + 1), numCol)
    #         IB_data['col'] = np.tile(range(1, numCol + 1), numRow)
    #         fieldNames = list(v1['dataIB'].__dict__.keys())
    #         fieldValues = list(v1['dataIB'].__dict__.values())
    #         for (i2, v2) in enumerate(fieldValues):
    #             # if type(v2)==IdsType:
    #             #     print("这个是id类型！")
    #             if (v2.dtype == np.float_ or v2.dtype == np.bool_ or v2.dtype == np.int16):
    #                 IB_data[fieldNames[i2]] = v2.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
    #             elif v2.dtype == list:
    #                 ## 转换信息列表为矩阵形式  #HACK能否用现成的功能函数代替？
    #                 m2 = np.full((numRow, numCol), False)
    #                 if v2 is []:
    #                     continue
    #                 for (i3, v3) in enumerate(v2):
    #                     if v3 is []:
    #                         m2[i3, :] = False
    #                         continue
    #                         pass  # if
    #                     for i4 in v3:
    #                         if i4 in v3:
    #                             m2[i3, i4] = True
    #                             pass  # if
    #                         else:
    #                             m2[i3, i4] = False
    #                             pass  # else
    #                         pass  # for
    #                 IB_data[fieldNames[i2]] = m2.T.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
    #                 pass  # if
    #             pass  # for
    #         IB_data_export = pd.concat([IB_data_export, IB_data])  # 追加当前`IB_data`至`IB_data_expert`
    #         pass  # for
    #     IB_data_export.insert(0, 'id', range(len(IB_data_export)))  # 添加id列
    #     IB_data_export.insert(1, 'id_data', np.repeat(range(len(IB_data_export) // env['num_bank'] ** 2), env['num_bank'] ** 2))  # 添加id_data列
    #     IB_data_export.to_csv(path.join(env['folderpath_experiments_output_data'], "IB_exp=" + str(env['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；
    #
    #     pass  # function
    #

    @classmethod
    def export_parameter_data(cls, list_combination_of_para: list, para: dict):
        """
        导出控制参数数据

        Args:
            list_combination_of_para (list): 控制参数列表
            para (dict): 参数变量

        Returns:

        """
        env['num_experiment'] = len(list_combination_of_para)  # 获取实验组之实验个数

        # env['num_bank'] = len(para['list_id_bank'])  if env['num_bank'] is None else env['num_bank']
        df_010 = pd.DataFrame(list_combination_of_para, columns=para.keys())  # 转换字典列表为数据框
        list_types = [type(df_010.iloc[0, i]) for i in range(df_010.columns.__len__())]  # 获取列表，元素为数据框之各列之元素之类型
        id_type_is_array = list_types.index(np.ndarray)  # 获取索引值为类型为数组类型的

        ## 获取银行个数
        is_need_to_get_num_bank = False
        if 'num_bank' in env.keys():
            if env['num_bank'] is None:
                is_need_to_get_num_bank = True
                pass  # if
        else:
            is_need_to_get_num_bank = True
            pass  # if

        if is_need_to_get_num_bank:
            env['num_bank'] = len(para[list(para.keys())[id_type_is_array]][0])  # 获取字典 `para` 在索引 `id_type_is_array` 对应的变量。该变量是一个列表。获取该列表第一个元素。该元素是一个数组。获取该数组大小，作为银行个数

        ## 展开数组类型的参数，得到一个新的数据框变量。该变量具有所有参数组合。后续在实验组循环中，每次取一行，作为本次实验的参数。
        df_combinationOfPara = df_010.explode(df_010.keys()[id_type_is_array])
        df_combinationOfPara.insert(loc=0, column='id', value=np.tile(list(range(1, env['num_bank'] + 1)), reps=env['num_experiment']))  # 添加数据项id
        df_combinationOfPara.insert(loc=0, column='exp_id', value=np.repeat(list(range(1, env['num_experiment'] + 1)), repeats=env['num_bank'], axis=0))  # 添加实验组id

        ## 导出实验参数为 csv 格式
        df_combinationOfPara.to_csv(Path(env['folderpath_experiments_output_data'], r"paras.csv"))  # 导出字段列表为csv格式
        pass  # function

    pass  # class
