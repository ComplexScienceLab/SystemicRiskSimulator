"函数区：收集数据"

## 函数区：收集数据


from PySystemicRiskLab import pd, deepcopy, path, Optional, logging
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import *

# from PySystemicRiskLab.core.operations.scheduler import Scheduler

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
            logging.debug("                收集数据")
            # env['id_data'] += 1  # 累加数据帧ID号
            A_data = Collector.collect_agent_data(A, A_data, env)
            # Scheduler.schedule(env)
            return A_data, env
        elif env['state_of_schedule'] == StateOfScheduleEnum.initializing:
            logging.debug("                初始化数据")
            A_data = Collector.init_agent_data_collection(A, env)
            return A_data
        elif env['state_of_schedule'] == StateOfScheduleEnum.ending:
            logging.debug("                导出数据")
            Collector.export_agent_data(A_data, env)
        else:
            pass
        pass  # method

    # ## NOTE 当用pandas数据结构时：
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
    #
    #     BB_df = A.BB.to_frame().transpose()
    #     BB_df.insert(loc=0, column='id_data', value=env['id_data'])
    #     BB_df.insert(loc=1, column='round', value=env['round'])
    #     BB_df.insert(loc=2, column='index_process', value=env['index_process'])
    #     BB_df.insert(loc=3, column='index_stage', value=env['index_stage'])
    #     BB_data = pd.DataFrame()
    #     BB_data = pd.concat([BB_data, BB_df], ignore_index=True)
    #
    #     IB_df = A.IB.to_frame().transpose()
    #     IB_df.insert(loc=0, column='id_data', value=env['id_data'])
    #     IB_df.insert(loc=1, column='round', value=env['round'])
    #     IB_df.insert(loc=2, column='index_process', value=env['index_process'])
    #     IB_df.insert(loc=3, column='index_stage', value=env['index_stage'])
    #     IB_data = pd.DataFrame()
    #     IB_data = pd.concat([IB_data, IB_df], ignore_index=True)
    #
    #     A_data = AgentDataCollection(BB_data, IB_data)
    #     return A_data
    #     pass
    #
    # @classmethod
    # def collect_agent_data(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, env: dict):
    #     """
    #     收集数据并存储
    #
    #     Args:
    #         A (SystemicRiskAgent): 系统性风险个体众
    #         A_data (AgentDataCollection): 个体众数据集
    #         env: 环境变量
    #
    #     Returns:
    #         A_data: 待收集的数据
    #
    #     """
    #
    #     BB_df = A.BB.to_frame().transpose()
    #     BB_df.insert(loc=0, column='id_data', value=env['id_data'])
    #     BB_df.insert(loc=1, column='round', value=env['round'])
    #     BB_df.insert(loc=2, column='index_process', value=env['index_process'])
    #     BB_df.insert(loc=3, column='index_stage', value=env['index_stage'])
    #     A_data.BB = pd.concat([A_data.BB, BB_df], ignore_index=True)
    #
    #     IB_df = A.IB.to_frame().transpose()
    #     IB_df.insert(loc=0, column='id_data', value=env['id_data'])
    #     IB_df.insert(loc=1, column='round', value=env['round'])
    #     IB_df.insert(loc=2, column='index_process', value=env['index_process'])
    #     IB_df.insert(loc=3, column='index_stage', value=env['index_stage'])
    #     A_data.IB = pd.concat([A_data.IB, IB_df], ignore_index=True)
    #
    #     return A_data
    #     pass
    #
    # @classmethod
    # def export_agent_data(cls, A_data: AgentDataCollection, env: dict):
    #     """
    #     HACK导出实验结果数据
    #
    #     NOTE：查询列具有的数据类型可以用以下语句：
    #
    #     ```python
    #     list_type_of_columns_01 = [A_data.BB[v].dtype for v in A_data.BB.columns]
    #     list_type_of_columns_02 = [A_data.BB[v][0].dtype for v in A_data.BB.columns]
    #     list_type_of_columns_01 = [A_data.IB[v].dtype for v in A_data.IB.columns]
    #     list_type_of_columns_02 = [A_data.IB[v][0].dtype for v in A_data.IB.columns]
    #     ```
    #
    #     Args:
    #         A_data: 个体众数据集
    #         env(dict): 环境变量
    #
    #     """
    #
    #     ## 整理banks之数据为一数据框
    #     num_bank = np.shape(A_data.BB.A_all)[0]  # 导出前更新总agent数
    #
    #     list_columns_for_explode = [
    #         v for i, v in enumerate(A_data.BB.columns) if (
    #                 A_data.BB[v].dtype == np.dtype('O') and (
    #                 A_data.BB[v][0].dtype == np.dtype('int64') or
    #                 A_data.BB[v][0].dtype == np.dtype('<U1') or
    #                 A_data.BB[v][0].dtype == np.dtype('<U6') or
    #                 A_data.BB[v][0].dtype == np.dtype('float64') or
    #                 A_data.BB[v][0].dtype == np.dtype('bool')
    #         )
    #         )
    #     ]  # 获取需要展平的列
    #
    #     BB_data_export = A_data.BB.explode(list_columns_for_explode)  # 展平，面板化数据框
    #     BB_data_export.to_csv(path.join(env['folderpath_of_experiments_output_data'], "BB_exp=" + str(env['id_experiment']) + ".csv"))  # 导出为csv格式；
    #
    #     ## 整理interbank之数据为一数据框
    #     list_columns_for_transform = [
    #         v for i, v in enumerate(A_data.IB.columns) if (
    #                 A_data.IB[v].dtype == np.dtype('O') and
    #                 A_data.IB[v][0].dtype == np.dtype('O')
    #         )
    #     ]  # 获取需要转换形式的列
    #
    #     ## 转换信息列表为矩阵形式，插入数据框  #HACK 能否用现成的功能函数代替？
    #     for v1 in list_columns_for_transform:
    #         for i2 in range(A_data.IB[v1].size):
    #             m = np.full((num_bank, num_bank), False)
    #             if A_data.IB[v1][i2] is []:
    #                 A_data.IB[v1][i2] = np.nan
    #                 continue
    #             for (i3, v3) in enumerate(A_data.IB[v1][i2]):
    #                 if v3 is []:
    #                     m[i3, :] = False
    #                     continue
    #                     pass  # if
    #                 for i4 in v3:
    #                     if i4 in v3:
    #                         m[i3, i4] = True
    #                     else:
    #                         m[i3, i4] = False
    #                         pass  # if
    #                     pass  # for
    #                 pass  # for
    #             A_data.IB[v1][i2] = m  # 赋值矩阵给数据框之元素，于数据框之相应的位置
    #             pass  # for
    #         pass  # for
    #
    #     ## 生成agent矩阵之坐标，以矩阵形式，插入数据框
    #     row_coord, col_coord = np.mgrid[0:num_bank:1, 0:num_bank:1]
    #     A_data.IB.insert(loc=A_data.IB.columns.get_loc('index_stage') + 1, column="col", value=np.dtype('O'))
    #     for i, _ in enumerate(A_data.IB.col):
    #         A_data.IB.col[i] = col_coord.astype('int16')
    #     A_data.IB.insert(loc=A_data.IB.columns.get_loc('index_stage') + 1, column="row", value=np.dtype('O'))
    #     for i, _ in enumerate(A_data.IB.row):
    #         A_data.IB.row[i] = row_coord.astype('int16')
    #
    #     list_columns_for_explode = [
    #         v for i, v in enumerate(A_data.IB.columns) if (
    #                 A_data.IB[v].dtype == np.dtype('O') and (
    #                 A_data.IB[v][0].dtype == np.dtype('int16') or
    #                 A_data.IB[v][0].dtype == np.dtype('int64') or
    #                 A_data.IB[v][0].dtype == np.dtype('<U1') or
    #                 A_data.IB[v][0].dtype == np.dtype('<U6') or
    #                 A_data.IB[v][0].dtype == np.dtype('float64') or
    #                 A_data.IB[v][0].dtype == np.dtype('bool')
    #         )
    #         )
    #     ]  # 获取需要展平的列
    #
    #     IB_data_export = A_data.IB.explode(list_columns_for_explode).explode(list_columns_for_explode)  # 展平相关的列，面板化数据框
    #     IB_data_export.to_csv(path.join(env['folderpath_of_experiments_output_data'], "IB_exp=" + str(env['id_experiment']) + ".csv"))  # 导出为csv格式；
    #
    #     pass  # method

    ## NOTE 当用对象字段数据结构时：
    @classmethod
    def init_agent_data_collection(cls, A: SystemicRiskAgent, env: dict):
        """

        Args:
            A (SystemicRiskAgent): 系统性风险个体众
            env (dict): 环境变量

        Returns:
            A_data: 待收集的数据

        """
        BB_data_item = dict(
            {
                # list(env.keys())[list(env.keys()).index('id_data')]: range(env['step'] , (env['step'] + 1) ),
                list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
                list(env.keys())[list(env.keys()).index('round')]: env['round'],
                list(env.keys())[list(env.keys()).index('step')]: env['step'],
                'dataBB': deepcopy(A.BB)
            }
        )
        BB_data = []
        BB_data.append(BB_data_item)  # 初始化banks之数据为一字典数组

        IB_data_item = dict(
            {
                # list(env.keys())[list(env.keys()).index('id_data')]: range(env['step'] * env['num_bank'] ** 2, (env['step'] + 1) * env['num_bank'] ** 2),
                list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
                list(env.keys())[list(env.keys()).index('round')]: env['round'],
                list(env.keys())[list(env.keys()).index('step')]: env['step'],
                'dataIB': deepcopy(A.IB)
            }
        )
        IB_data = []
        IB_data.append(IB_data_item)  # 初始化interbank之数据为一字典数组

        A_data = AgentDataCollection(deepcopy(BB_data), deepcopy(IB_data))
        return A_data
        pass

    @classmethod
    def collect_agent_data(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, env: dict):
        """
        收集数据并存储

        Args:
            A (SystemicRiskAgent):
            A_data (AgentDataCollection):
            env:

        Returns:
            A_data: 待收集的数据

        """
        BB_data_item = dict(
            {
                # list(env.keys())[list(env.keys()).index('id_data')]: range(env['step'] * env['num_bank'], (env['step'] + 1) * env['num_bank']),
                list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
                list(env.keys())[list(env.keys()).index('round')]: env['round'],
                list(env.keys())[list(env.keys()).index('step')]: env['step'],
                'dataBB': deepcopy(A.BB)
            }
        )
        A_data.BB.append(BB_data_item)  # 收集banks之数据为一字典数组

        IB_data_item = dict(
            {
                # list(env.keys())[list(env.keys()).index('id_data')]: range(env['step'] * env['num_bank'] ** 2, (env['step'] + 1) * env['num_bank'] ** 2),
                list(env.keys())[list(env.keys()).index('process_name')]: env['process_name'],
                list(env.keys())[list(env.keys()).index('round')]: env['round'],
                list(env.keys())[list(env.keys()).index('step')]: env['step'],
                'dataIB': deepcopy(A.IB)
            }
        )

        A_data.IB.append(IB_data_item)  # 收集interbank之数据为一字典数组
        return A_data
        pass

    @classmethod
    def export_agent_data(cls, A_data: AgentDataCollection, env: dict):
        """
        导出实验结果数据

        Args:
            A_data:
            env(dict): 环境变量

        Returns:

        """

        ## 整理banks之数据为一数据框
        BB_data_export = pd.DataFrame()
        BB_data = pd.DataFrame()
        numRow, numCol = np.shape(A_data.BB[0]['dataBB'].A_all)
        for (i1, v1) in enumerate(A_data.BB):
            # BB_data['id_data'] = np.full(numRow, v1['id_data'])
            BB_data['process_name'] = np.full(numRow, v1['process_name'])
            BB_data['round'] = np.full(numRow, v1['round'])
            BB_data['step'] = np.full(numRow, v1['step'])
            fieldNames = list(v1['dataBB'].__dict__.keys())
            fieldValues = list(v1['dataBB'].__dict__.values())
            for (i2, v2) in enumerate(fieldValues):
                BB_data[fieldNames[i2]] = v2
                pass
            BB_data_export = pd.concat([BB_data_export, BB_data])  # 追加`BB_data`至`BB_data_expert`
            pass  # for
        BB_data_export.insert(0, 'id', range(len(BB_data_export)))  # 添加id列
        BB_data_export.insert(1, 'id_data', np.repeat(range(len(BB_data_export) // env['num_bank']), env['num_bank']))  # 添加id_data列
        BB_data_export.to_csv(path.join(env['folderpath_of_experiments_output_data'], "BB_exp=" + str(env['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；

        ## 整理interbank之数据为一数据框
        IB_data_export = pd.DataFrame()
        IB_data = pd.DataFrame()
        # numRow, numCol = np.shape(A_data.IB[0]['dataIB'].A_IB)
        numRow, numCol = env['num_bank'], env['num_bank']
        for (i1, v1) in enumerate(A_data.IB):
            # IB_data['id_data'] = np.full(numRow * numCol, v1['id_data'])
            # IB_data['id_data'] = v1['id_data']
            IB_data['process_name'] = np.full(numRow * numCol, v1['process_name'])
            IB_data['round'] = np.full(numRow * numCol, v1['round'])
            IB_data['step'] = np.full(numRow * numCol, v1['step'])
            IB_data['row'] = np.repeat(range(1, numRow + 1), numCol)
            IB_data['col'] = np.tile(range(1, numCol + 1), numRow)
            fieldNames = list(v1['dataIB'].__dict__.keys())
            fieldValues = list(v1['dataIB'].__dict__.values())
            for (i2, v2) in enumerate(fieldValues):
                # if type(v2)==IdsType:
                #     print("这个是id类型！")
                if (v2.dtype == np.float_ or v2.dtype == np.bool_ or v2.dtype == np.int16):
                    IB_data[fieldNames[i2]] = v2.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                elif v2.dtype == list:
                    ## 转换信息列表为矩阵形式  #HACK能否用现成的功能函数代替？
                    m2 = np.full((numRow, numCol), False)
                    if v2 is []:
                        continue
                    for (i3, v3) in enumerate(v2):
                        if v3 is []:
                            m2[i3, :] = False
                            continue
                            pass  # if
                        for i4 in v3:
                            if i4 in v3:
                                m2[i3, i4] = True
                                pass  # if
                            else:
                                m2[i3, i4] = False
                                pass  # else
                            pass  # for
                    IB_data[fieldNames[i2]] = m2.T.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                    pass  # if
                pass  # for
            IB_data_export = pd.concat([IB_data_export, IB_data])  # 追加当前`IB_data`至`IB_data_expert`
            pass  # for
        IB_data_export.insert(0, 'id', range(len(IB_data_export)))  # 添加id列
        IB_data_export.insert(1, 'id_data', np.repeat(range(len(IB_data_export) // env['num_bank'] ** 2), env['num_bank'] ** 2))  # 添加id_data列
        IB_data_export.to_csv(path.join(env['folderpath_of_experiments_output_data'], "IB_exp=" + str(env['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；

        pass  # method

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
        df_010 = pd.DataFrame(list_combination_of_para, columns=para.keys())  # 转换字典列表为数据框
        li_types = [type(df_010.iloc[0, i]) for i in range(df_010.columns.__len__())]  # 获取列表，元素为数据框之各列之元素之类型
        id_type_is_list = li_types.index(np.ndarray)  # 获取索引值为类型为list的
        df_combinationOfPara = df_010.explode(df_010.keys()[id_type_is_list])
        # li_010 = [df_010.apply(lambda x: pd.Series(x[i]), axis=1).stack().reset_index(level=1, drop=True) for i in range(df_010.columns.__len__())]
        # li_020 = [np.array(li_010[i]) for i in range(li_010.__len__())]
        # df_combinationOfPara = pd.DataFrame(li_020).T
        # df_combinationOfPara.columns = paras.keys()
        df_combinationOfPara.insert(loc=0, column='id', value=np.tile(list(range(1, env['num_bank'] + 1)), reps=env['num_experiment']))  # 添加数据项id
        df_combinationOfPara.insert(loc=0, column='exp_id', value=np.repeat(list(range(1, env['num_experiment'] + 1)), repeats=env['num_bank'], axis=0))  # 添加实验组id
        # df_combinationOfPara.to_csv(os.path.join(env['folderpath_of_experiments_output_data'], "paras.csv"), df_combinationOfPara)  # 导出字段列表为csv格式
        pass  # method
