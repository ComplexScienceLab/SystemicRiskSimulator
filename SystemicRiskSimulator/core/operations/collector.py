## 函数区：收集数据
import shutil

from scipy.sparse import csr_array
import pickle
import pandas as pd
from pathlib import Path
from typing import Optional
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_type import *
from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


class Collector:

    ## NOTE 当用 Pandas 之数据结构时：
    @classmethod
    def init_agent_data_collection(cls, A: pd.Series, sgv: dict, para: dict):
        """
        初始化个体众数据集

        Args:
            A (pd.Series): 系统性风险个体众
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A_data: 待收集的数据

        """

        ## 初始化数据框用以存储agent数据

        # #HACK 改之前的收集 agents 数据文件代码，对于未适配的 set_config_variables.py 文件而言，如果没有
        # dict_agents_data = {}
        # for i, agents_data in enumerate(sgv['list_agents_data']):
        #     with open(Path(sgv['folderpath_agents'], 'agents', f"{agents_data}_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
        #         dict_agents_data[agents_data] = pickle.load(f)
        #     pass  # for
        #
        # BB_data = pd.DataFrame()
        # IB_data = pd.DataFrame()
        # A_data = AgentDataCollection(BB_data, IB_data)

        # #HACK 改之后的收集 agents 数据文件代码
        dict_agents_data = {}
        id_agents = para['id_agents']
        for para_01 in sgv['list_agents_data_filename_para_01']:
            agents_filename = f"id={id_agents}-v={para_01}"
            for para_02 in sgv['list_agents_data_filename_para_02']:
                if isinstance(para[para_02], float):
                    agents_filename += f"-{para_02}={float(para[para_02]):.2f}"
                else:
                    agents_filename += f"-{para_02}={para[para_02]}"
                pass  # for
            agents_filename += ".pkl"
            with open(Path(sgv['folderpath_agents'], 'agents', agents_filename), 'rb') as f:
                dict_agents_data[para_01] = pickle.load(f)
            pass  # for

        A_data = pd.Series()
        for k, v in dict_agents_data.items():
            if k == "note":  # 如果是备注变量，则直接用 A 赋值
                A_data[k] = A[k].copy()
            else:
                A_data[k] = pd.DataFrame()
            # for k1, v1 in deepcopy(v).items():  # #HACK 之所以不用这几行是因为这个可能会与模型运行过程的第一步初始化重复初始化赋值。
            #     A_data[k][k1] = v1
            # pass  # for

        # sgv['series_BB'] = pd.Series()
        # for i in A.BB.index:
        #     sgv['series_BB'][i] = A.BB[i].copy()
        # sgv['df_BB'] = sgv['series_BB'].to_frame().transpose()
        # sgv['df_BB'].insert(loc=0, column='process_name', value=sgv['process_name'])
        # sgv['df_BB'].insert(loc=1, column='step', value=sgv['step'])
        # sgv['df_BB'].insert(loc=2, column='turn', value=sgv['turn'])
        # sgv['df_BB'].insert(loc=3, column='phase', value=sgv['phase'])
        # # BB_data = pd.concat([BB_data, sgv['df_BB']], ignore_index=True)
        # A_data.BB = pd.concat([A_data.BB, sgv['df_BB']], ignore_index=True)
        #
        # sgv['series_IB'] = pd.Series()
        # for i in A.IB.index:
        #     sgv['series_IB'][i] = A.IB[i].copy()
        # sgv['df_IB'] = sgv['series_IB'].to_frame().transpose()
        # sgv['df_IB'].insert(loc=0, column='process_name', value=sgv['process_name'])
        # sgv['df_IB'].insert(loc=1, column='step', value=sgv['step'])
        # sgv['df_IB'].insert(loc=2, column='turn', value=sgv['turn'])
        # sgv['df_IB'].insert(loc=3, column='phase', value=sgv['phase'])
        # # IB_data = pd.concat([IB_data, sgv['df_IB']], ignore_index=True)
        # A_data.IB = pd.concat([A_data.IB, sgv['df_IB']], ignore_index=True)
        #
        # # A_data = pd.Series([BB_data, IB_data], index=['BB', 'IB'])

        return A_data
        pass  # function

    @classmethod
    def reset_agent_data_collection(cls, A: pd.Series, A_data, sgv, para):
        """
        重置个体众数据集

        Args:
            A (pd.Series): 系统性风险个体众
            A_data (AgentDataCollection): 个体众数据集
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A_data: 待收集的数据

        """

        ## 初始化数据框用以存储agent数据

        # #HACK 改之前的收集 agents 数据文件代码，对于未适配的 set_config_variables.py 文件而言，如果没有
        # dict_agents_data = {}
        # for i, agents_data in enumerate(sgv['list_agents_data']):
        #     with open(Path(sgv['folderpath_agents'], 'agents', f"{agents_data}_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
        #         dict_agents_data[agents_data] = pickle.load(f)
        #     pass  # for
        #
        # BB_data = pd.DataFrame()
        # IB_data = pd.DataFrame()
        # A_data = AgentDataCollection(BB_data, IB_data)

        # #HACK 改之后的收集 agents 数据文件代码
        dict_agents_data = {}
        id_agents = para['id_agents']
        for para_01 in sgv['list_agents_data_filename_para_01']:
            agents_filename = f"id={id_agents}-v={para_01}"
            for para_02 in sgv['list_agents_data_filename_para_02']:
                if isinstance(para[para_02], float):
                    agents_filename += f"-{para_02}={float(para[para_02]):.2f}"
                else:
                    agents_filename += f"-{para_02}={para[para_02]}"
                pass  # for
            agents_filename += ".pkl"
            with open(Path(sgv['folderpath_agents'], 'agents', agents_filename), 'rb') as f:
                dict_agents_data[para_01] = pickle.load(f)
            pass  # for

        A_data = pd.Series()
        for k, v in dict_agents_data.items():
            if k != "note":
                A_data[k] = pd.DataFrame()
            else:  # 如果是备注变量，则直接用 A 赋值
                A_data[k] = A[k].copy()
            # for k1, v1 in deepcopy(v).items():  # #HACK 之所以不用这几行是因为这个可能会与模型运行过程的第一步初始化重复初始化赋值。
            #     A_data[k][k1] = v1
            # pass  # for

        # sgv['series_BB'] = pd.Series()
        # for i in A.BB.index:
        #     sgv['series_BB'][i] = A.BB[i].copy()
        # sgv['df_BB'] = sgv['series_BB'].to_frame().transpose()
        # sgv['df_BB'].insert(loc=0, column='process_name', value=sgv['process_name'])
        # sgv['df_BB'].insert(loc=1, column='step', value=sgv['step'])
        # sgv['df_BB'].insert(loc=2, column='turn', value=sgv['turn'])
        # sgv['df_BB'].insert(loc=3, column='phase', value=sgv['phase'])
        # # BB_data = pd.concat([BB_data, sgv['df_BB']], ignore_index=True)
        # A_data.BB = pd.concat([A_data.BB, sgv['df_BB']], ignore_index=True)
        #
        # sgv['series_IB'] = pd.Series()
        # for i in A.IB.index:
        #     sgv['series_IB'][i] = A.IB[i].copy()
        # sgv['df_IB'] = sgv['series_IB'].to_frame().transpose()
        # sgv['df_IB'].insert(loc=0, column='process_name', value=sgv['process_name'])
        # sgv['df_IB'].insert(loc=1, column='step', value=sgv['step'])
        # sgv['df_IB'].insert(loc=2, column='turn', value=sgv['turn'])
        # sgv['df_IB'].insert(loc=3, column='phase', value=sgv['phase'])
        # # IB_data = pd.concat([IB_data, sgv['df_IB']], ignore_index=True)
        # A_data.IB = pd.concat([A_data.IB, sgv['df_IB']], ignore_index=True)
        #
        # # A_data = pd.Series([BB_data, IB_data], index=['BB', 'IB'])

        return A_data
        pass  # function

    @classmethod
    def collect_agent_data(cls, A, A_data: AgentDataCollection, sgv: dict, para: dict, collect: Optional[dict] = None):
        """
        收集数据并存储。

        > 注意：不收集备注变量 `note`，因为是静态的，不需要收集。

        Args:
            A (ModelAgent): 系统性风险个体众
            A_data (AgentDataCollection): 个体众数据集
            sgv: 模拟器全局变量
            para (dict): 参数变量
            collect (Optional[dict]): 待收集的数据字段列表字典。默认为 None ，表示收集 A 当前回合的所有字段的数据。如果非 None ，
            举例：
            ```python
            dict(
                BB=['A_IB_all', 'Loss_t', 'hel'],
                IB=['A_IB', 'Shock_IB_def', 'hel']
            )
            ```

        Returns:
            A_data: 待收集的数据

        """
        # BB_data, IB_data = A_data.BB, A_data.IB

        # BB_df = A.BB.to_frame().transpose()
        # BB = deepcopy(A.BB)
        # sgv['series_BB'] = pd.Series()

        # # #HACK 改之前的收集 agents 数据文件代码，对于未适配的 set_config_variables.py 文件而言，如果没有
        # series_BB = pd.Series()
        # for i in A.BB.index:  # TODO 添加需要收集哪些具体给定的字段
        #     series_BB[i] = A.BB[i].copy()
        # df_BB = series_BB.to_frame().transpose()
        # df_BB.insert(loc=0, column='process_name', value=sgv['process_name'])
        # df_BB.insert(loc=1, column='step', value=sgv['step'])
        # df_BB.insert(loc=2, column='turn', value=sgv['turn'])
        # df_BB.insert(loc=3, column='phase', value=sgv['phase'])
        # A_data.BB = pd.concat([A_data.BB, df_BB], ignore_index=True)
        # # BB_data = pd.concat([BB_data, sgv['df_BB']], ignore_index=True)
        #
        # # IB_df = A.IB.to_frame().transpose()
        # # IB = deepcopy(A.IB)
        # series_IB = pd.Series()
        # for i in A.IB.index:
        #     series_IB[i] = A.IB[i].copy()
        # df_IB = series_IB.to_frame().transpose()
        # df_IB.insert(loc=0, column='process_name', value=sgv['process_name'])
        # df_IB.insert(loc=1, column='step', value=sgv['step'])
        # df_IB.insert(loc=2, column='turn', value=sgv['turn'])
        # df_IB.insert(loc=3, column='phase', value=sgv['phase'])
        # A_data.IB = pd.concat([A_data.IB, df_IB], ignore_index=True)
        # # IB_data = pd.concat([IB_data, IB_df], ignore_index=True)
        #
        # # A_data.BB, A_data.IB = BB_data, IB_data
        # # return A_data

        # #HACK 改之后的收集 agents 数据文件代码
        for para_01 in sgv['list_agents_data_filename_para_01']:
            if para_01 == "note":  # 如果是备注变量，则跳过。因为是静态的，不需要收集
                continue
            series = pd.Series()
            for i in A[para_01].index:
                series[i] = A[para_01][i].copy()  # BUG 是否无法实现副本复制？
            df = series.to_frame().transpose()
            df.insert(loc=0, column='process_name', value=sgv['process_name'])
            df.insert(loc=1, column='step', value=sgv['step'])
            df.insert(loc=2, column='turn', value=sgv['turn'])
            df.insert(loc=3, column='phase', value=sgv['phase'])
            if collect is None:
                A_data[para_01] = pd.concat([A_data[para_01], df], ignore_index=True)
            else:
                for variable in collect:
                    for field in variable[variable]:
                        if field in df.columns:
                            A_data[variable] = pd.concat([A_data[variable], df[field]], ignore_index=True)
                        pass  # for
                    pass  # for
                pass  # if

            pass  # for

        pass  # function

    @classmethod
    def export_agent_data(cls, A_data: AgentDataCollection, sgv: dict):
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
            sgv(dict): 模拟器全局变量

        """

        # ## #TODO 查看是否存在整列都是一模一样的全零或者全部 True 或者 False 或者空列表的列，如果存在，则记录该列的值到 A_data.note ，然后删除
        # list_columns_all_nan = A_data.BB.columns[A_data.BB.isnull().all()]
        # list_columns_all_zero = A_data.BB.columns[A_data.BB.applymap(lambda x: (x == 0).all() if isinstance(x, np.ndarray) else x == 0).all()]
        # list_columns_all_True = A_data.BB.columns[A_data.BB.applymap(lambda x: (x == True).all() if isinstance(x, np.ndarray) else x is True).all()]
        # list_columns_all_False = A_data.BB.columns[A_data.BB.applymap(lambda x: (x == False).all() if isinstance(x, np.ndarray) else x is False).all()]
        # list_columns_all_empty = A_data.BB.columns[A_data.BB.applymap(lambda x: (len(x) == 0).all() if isinstance(x, np.ndarray) else len(x) == 0).all()]
        # # 合并上述列表
        # list_columns_can_remove = list_columns_all_nan.union(list_columns_all_zero).union(list_columns_all_True).union(list_columns_all_False).union(list_columns_all_empty)

        ## 压缩数据
        if sgv['is_compress_result_data']:
            A_data = cls.compress_result_data(A_data, sgv)
            pass  # if

        # # 解压数据 #DEBUG 以下用于测试解压后的数据是否与原始数据一致
        # if sgv['is_compress_result_data']:
        #     A_data_decompress = cls.decompress_result_data(A_data, sgv)
        #     pass  # if
        # compare = []  # 验证解压后的数据是否与原始数据一致
        # for i in range(len(A_data.BB)):
        #     compare.append(A_data.BB['Loss_t'][i] - A_data_decompress.BB['Loss_t'][i])
        #     compare.append(A_data.IB['Shock_IB_def'][i] - A_data_decompress.IB['Shock_IB_def'][i])
        #     compare.append(A_data.BB['hel'][i] ^ A_data_decompress.BB['hel'][i])
        #     # #DEBUG 手动检查 exit 等列是否还原回来了
        #     compare.append(A_data.IB['hel'][i] ^ A_data_decompress.IB['hel'][i])

        ## 导出数据
        # for para_01 in list(set(sgv['list_agents_data_filename_para_01']) - {"note"}):
        for para_01 in sgv['list_agents_data_filename_para_01']:
            if para_01 == "note" or para_01 == "AB":  # 如果变量类型是 note 或者 AB ，则只保存成 pkl 文件
                pd.to_pickle(A_data[para_01], Path(sgv['folderpath_experiments_output_data'], f"exp={str(sgv['id_experiment'])}-v={para_01}-aid={sgv['id_agents']}.pkl"))
                continue
            if sgv['is_export_data_to_pkl']:
                pd.to_pickle(A_data[para_01], Path(sgv['folderpath_experiments_output_data'], f"exp={str(sgv['id_experiment'])}-v={para_01}-aid={sgv['id_agents']}.pkl"))
            if sgv['is_export_data_to_xlsx']:
                A_data[para_01].to_excel(Path(sgv['folderpath_experiments_output_data'], f"exp={str(sgv['id_experiment'])}-v={para_01}-aid={sgv['id_agents']}.xlsx"), index=False)
            if sgv['is_export_data_to_csv']:
                A_data[para_01].to_csv(Path(sgv['folderpath_experiments_output_data'], f"exp={str(sgv['id_experiment'])}-v={para_01}-aid={sgv['id_agents']}.csv"), index=False)

        pass  # function

    # ## NOTE 当用对象字段数据结构时：
    # @classmethod
    # def init_agent_data_collection(cls, A, sgv: dict):
    #     """
    #
    #     Args:
    #         A (ModelAgent): 系统性风险个体众
    #         sgv (dict): 模拟器全局变量
    #
    #     Returns:
    #         A_data: 待收集的
    #         数据
    #
    #     """
    #     BB_data_item = dict(
    #         {
    #             list(sgv.keys())[list(sgv.keys()).index('process_name')]: sgv['process_name'],
    #             list(sgv.keys())[list(sgv.keys()).index('step')]: sgv['step'],
    #             list(sgv.keys())[list(sgv.keys()).index('turn')]: sgv['turn'],
    #             list(sgv.keys())[list(sgv.keys()).index('phase')]: sgv['phase'],
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
    #             list(sgv.keys())[list(sgv.keys()).index('process_name')]: sgv['process_name'],
    #             list(sgv.keys())[list(sgv.keys()).index('step')]: sgv['step'],
    #             list(sgv.keys())[list(sgv.keys()).index('turn')]: sgv['turn'],
    #             list(sgv.keys())[list(sgv.keys()).index('phase')]: sgv['phase'],
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
    # def collect_agent_data(cls, A, A_data: AgentDataCollection, sgv: dict):
    #     """
    #     收集数据并存储
    #
    #     Args:
    #         A (ModelAgent):
    #         A_data (AgentDataCollection):
    #         sgv:
    #
    #     Returns:
    #         A_data: 待收集的数据
    #
    #     """
    #     BB_data_item = dict(
    #         {
    #             list(sgv.keys())[list(sgv.keys()).index('process_name')]: sgv['process_name'],
    #             list(sgv.keys())[list(sgv.keys()).index('step')]: sgv['step'],
    #             list(sgv.keys())[list(sgv.keys()).index('turn')]: sgv['turn'],
    #             list(sgv.keys())[list(sgv.keys()).index('phase')]: sgv['phase'],
    #             'dataBB': deepcopy(A.BB)
    #         }
    #     )
    #     A_data.BB.append(BB_data_item)  # 收集banks之数据为一字典数组
    #
    #     IB_data_item = dict(
    #         {
    #             list(sgv.keys())[list(sgv.keys()).index('process_name')]: sgv['process_name'],
    #             list(sgv.keys())[list(sgv.keys()).index('step')]: sgv['step'],
    #             list(sgv.keys())[list(sgv.keys()).index('turn')]: sgv['turn'],
    #             list(sgv.keys())[list(sgv.keys()).index('phase')]: sgv['phase'],
    #             'dataIB': deepcopy(A.IB)
    #         }
    #     )
    #
    #     A_data.IB.append(IB_data_item)  # 收集interbank之数据为一字典数组
    #     return A_data
    #     pass
    #
    # @classmethod
    # def export_agent_data(cls, A_data: AgentDataCollection, sgv: dict):
    #     """
    #     导出实验结果数据
    #
    #     Args:
    #         A_data:
    #         sgv(dict): 模拟器全局变量
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
    #         BB_data['turn'] = np.full(numRow, v1['turn'])
    #         BB_data['phase'] = np.full(numRow, v1['phase'])
    #         fieldNames = list(v1['dataBB'].__dict__.keys())
    #         fieldValues = list(v1['dataBB'].__dict__.values())
    #         for (i2, v2) in enumerate(fieldValues):
    #             BB_data[fieldNames[i2]] = v2
    #             pass
    #         BB_data_export = pd.concat([BB_data_export, BB_data])  # 追加`BB_data`至`BB_data_expert`
    #         pass  # for
    #     BB_data_export.insert(0, 'id', range(len(BB_data_export)))  # 添加id列
    #     BB_data_export.insert(1, 'id_data', np.repeat(range(len(BB_data_export) // sgv['num_bank']), sgv['num_bank']))  # 添加id_data列
    #     BB_data_export.to_csv(path.join(sgv['folderpath_experiments_output_data'], "BB_exp=" + str(sgv['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；
    #
    #
    #     ## 整理interbank之数据为一数据框
    #     IB_data_export = pd.DataFrame()
    #     IB_data = pd.DataFrame()
    #     # numRow, numCol = np.shape(A_data.IB[0]['dataIB'].A_IB)
    #     numRow, numCol = sgv['num_bank'], sgv['num_bank']
    #     for (i1, v1) in enumerate(A_data.IB):
    #         # IB_data['id_data'] = np.full(numRow * numCol, v1['id_data'])
    #         # IB_data['id_data'] = v1['id_data']
    #         IB_data['process_name'] = np.full(numRow * numCol, v1['process_name'])
    #         IB_data['step'] = np.full(numRow * numCol, v1['step'])
    #         IB_data['turn'] = np.full(numRow * numCol, v1['turn'])
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
    #     IB_data_export.insert(1, 'id_data', np.repeat(range(len(IB_data_export) // sgv['num_bank'] ** 2), sgv['num_bank'] ** 2))  # 添加id_data列
    #     IB_data_export.to_csv(path.join(sgv['folderpath_experiments_output_data'], "IB_exp=" + str(sgv['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；
    #
    #     pass  # function
    #

    @classmethod
    def export_parameter_data(cls, sgv: dict, combination_of_para: Union[list, pd.DataFrame], para: Optional[dict] = None):
        """
        导出控制参数数据

        Args:
            sgv (dict): 模拟器全局变量
            combination_of_para (list): 控制参数集之组合
            para (Optional[dict]): 参数变量。默认为 None

        Returns:

        """

        sgv['num_experiment'] = len(combination_of_para)  # 获取实验组之实验个数
        if para is None:  # 如果参数变量为空，则直接从 combination_of_para 中获取参数变量相关的信息
            # df_010 = pd.DataFrame(combination_of_para, columns=combination_of_para[0].keys())  # 转换字典列表为数据框
            pass  # if
        else:
            df_010 = pd.DataFrame(combination_of_para, columns=para.keys())  # 转换字典列表为数据框
            pass  # if

        # # sgv['num_bank'] = len(para['list_id_bank'])  if sgv['num_bank'] is None else sgv['num_bank']
        # list_types = [type(df_010.iloc[0, i]) for i in range(df_010.columns.__len__())]  # 获取列表，元素为数据框之各列之元素之类型
        # id_type_is_array = list_types.index(np.ndarray)  # 获取索引值为类型为数组类型的

        # ## 获取银行个数
        # is_need_to_get_num_bank = False
        # if 'num_bank' in sgv.keys():
        #     if sgv['num_bank'] is None:
        #         is_need_to_get_num_bank = True
        #         pass  # if
        # else:
        #     is_need_to_get_num_bank = True
        #     pass  # if
        #
        # if is_need_to_get_num_bank:
        #     sgv['num_bank'] = len(para[list(para.keys())[id_type_is_array]][0])  # 获取字典 `para` 在索引 `id_type_is_array` 对应的变量。该变量是一个列表。获取该列表第一个元素。该元素是一个数组。获取该数组大小，作为银行个数

        # ## 导出实验参数为 pkl、csv、Excel xlsx格式到输出文件夹
        # df_combinationOfPara = df_010.copy()
        # df_combinationOfPara.insert(loc=0, column='exp_id', value=np.arange(1, sgv['num_experiment'] + 1))  # 添加实验组id
        # df_combinationOfPara.insert(loc=1, column='is_done', value=[False] * sgv['num_experiment'])  # 添加是否完成标记
        # # 检查是否已经存在，如果文件已经存在则不再导出
        # if not Path(sgv['folderpath_experiments_output_parameters'], r"parameters.pkl").exists():
        #     pd.to_pickle(df_combinationOfPara, Path(sgv['folderpath_experiments_output_parameters'], r"parameters.pkl"))
        # if not Path(sgv['folderpath_experiments_output_parameters'], r"parameters.csv").exists():
        #     df_combinationOfPara.to_csv(Path(sgv['folderpath_experiments_output_parameters'], r"parameters.csv"), index=False)
        # if not Path(sgv['folderpath_experiments_output_parameters'], r"parameters.xlsx").exists():
        #     df_combinationOfPara.to_excel(Path(sgv['folderpath_experiments_output_parameters'], r"parameters.xlsx"), index=False)
        #     pass  # if

        ## 导出实验参数为 pkl、csv、Excel xlsx格式到输出文件夹
        df_combinationOfPara = combination_of_para.copy()
        # df_combinationOfPara.insert(loc=0, column='exp_id', value=np.arange(1, sgv['num_experiment'] + 1))  # 添加实验组id
        df_combinationOfPara.insert(loc=1, column='is_done', value=[False] * sgv['num_experiment'])  # 添加是否完成标记

        ### 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续重新生成参数作业数据
        mtime_of_file_parameters_py = Path(sgv['folderpath_parameters'], r"set_parameters_variables.py").resolve().stat().st_mtime
        mtime_of_file_parameters_pkl = Path(sgv['folderpath_parameters'], r"parameters.pkl").resolve().stat().st_mtime
        filepath_parameters_works_pkl = Path(sgv['folderpath_experiments_output_parameters'], r"parameters_works.pkl").resolve()
        if filepath_parameters_works_pkl.exists():  # 检查parameters_works.pkl文件是否存在
            mtime_of_file_parameters_works_pkl = filepath_parameters_works_pkl.stat().st_mtime  # 获取parameters_works.pkl文件的最后修改时间
            if (mtime_of_file_parameters_pkl > mtime_of_file_parameters_works_pkl) or (mtime_of_file_parameters_py > mtime_of_file_parameters_works_pkl):
                is_generate_parameters_works_data = True
                print("参数文件有更新，需要重新导出参数作业数据。")
            else:
                is_generate_parameters_works_data = False
                print("参数文件没有更新，不需要重新导出参数作业数据。")
        else:
            is_generate_parameters_works_data = True
            print("参数作业数据文件不存在，需要重新导出参数作业数据。")
            pass  # if
        if is_generate_parameters_works_data:
            Tools.delete_and_recreate_folder(sgv['folderpath_experiments_output_parameters'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建输出文件夹之参数文件夹
            # Tools.copy_files_from_other_folders(sgv['folderpath_parameters'], sgv['folderpath_experiments_output_parameters'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份参数文件夹到输出文件夹
            shutil.copyfile(sgv['folderpath_parameters'] / "set_parameters_variables.py", sgv['folderpath_experiments_output_parameters'] / "set_parameters_variables.py")
            shutil.copyfile(sgv['folderpath_parameters'] / "parameters.pkl", sgv['folderpath_experiments_output_parameters'] / "parameters.pkl")
            # 如果存在文件名（非格式名）为 parameters 的文件（例如 pkl、xlsx 等格式），就全部复制过去
            for file in Path(sgv['folderpath_parameters']).iterdir():
                if file.stem == "parameters":
                    shutil.copyfile(file, sgv['folderpath_experiments_output_parameters'] / file.name)
                    pass  # if
                pass  # for

            Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建模拟器之 data 文件夹之 parameters 文件夹
            # Tools.copy_files_from_other_folders(sgv['folderpath_parameters'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份参数文件夹到模拟器之 data 文件夹
            shutil.copyfile(sgv['folderpath_parameters'] / "set_parameters_variables.py", sgv['folderpath_simulator'] / "SystemicRiskSimulator/data/parameters" / "set_parameters_variables.py")
            # 如果存在文件名（非格式名）为 parameters 的文件（例如 pkl、xlsx 等格式），就全部复制过去
            for file in Path(sgv['folderpath_parameters']).iterdir():
                if file.stem == "parameters":
                    shutil.copyfile(file, sgv['folderpath_simulator'] / "SystemicRiskSimulator/data/parameters" / file.name)
                    pass  # if
                pass  # for
            pass  # if

        pass  # function

    @classmethod
    def export_config_data(cls, sgv: dict):
        """
        导出字典类型的配置数据（全局数据）为 pkl 格式

        Args:
            config_data (dict): 配置数据

        Returns:

        """

        with open(Path(sgv['folderpath_experiments_output_config'], r"config.pkl"), "wb") as f:
            pickle.dump(sgv, f)

        # pickle.dump(config_data, open(Path(sgv['folderpath_experiments_output_data'], r"config.pkl"), "wb"))  # 导出为pkl格式

    @classmethod
    def compress_result_data(cls, A_data_origin: pd.Series, sgv: dict):
        """
        压缩实验结果数据。

        Args:
            A_data_origin (pd.Series): 原始的实验结果数据

        Returns:
            A_data_compress (pd.Series): 压缩后的实验结果数据

        """

        A_data_compress = pd.Series()

        for para_01 in sgv['list_agents_data_filename_para_01']:
            if para_01 == "note":  # 如果是备注变量，则直接存入 A_data_compress.note
                A_data_compress[para_01] = A_data_origin.note.copy()  # #BUG 可能无法满意地深拷贝。
                A_data_compress[para_01]['compress'] = dict()
                pass  # if
            pass  # for

        for para_01 in sgv['list_agents_data_filename_para_01']:
            if para_01 == "note":  # 如果是备注变量，则已经处理过了，跳过
                continue
                pass  # if

            A_data_compress.note['compress'][para_01] = dict()
            # A_data_compress[para_01] = A_data_origin[para_01].copy()

            if not para_01.startswith("I"):  # 说明是 1D 的数据
                v_1D_origin = A_data_origin[para_01]
                the_column = list(set(v_1D_origin.columns) - set(['process_name', 'step', 'turn', 'phase']))[0]
                len_result_data = len(v_1D_origin)  # 迭代次数（表格行数）
                num_agent = len(v_1D_origin.at[0, the_column])  # 个体数量（表格单元格值之元素个数）
                v_1D_compress = pd.DataFrame(columns=v_1D_origin.columns, index=range(len_result_data))
                ## 全同列压缩
                for column in v_1D_origin.columns:
                    is_compress_all_same = True  # 是否全同列压缩
                    is_compress_diff = False  # 是否差值压缩
                    is_all_same = np.full(len_result_data, False)
                    if (type(v_1D_origin.at[0, column]) == np.ndarray and (type(v_1D_origin.at[0, column][0]) == MoneyType or type(v_1D_origin.at[0, column][0]) == np.float64)):  # 如果是 MoneyType 型的 numpy 数组
                        v_1D_origin_value = 0.0
                    elif (type(v_1D_origin.at[0, column]) == np.ndarray and type(v_1D_origin.at[0, column][0]) == np.bool_):  # 如果是布尔型的 numpy 数组
                        v_1D_origin_value = v_1D_origin.at[0, column][0]
                    elif (type(v_1D_origin.at[0, column]) == np.ndarray and (type(v_1D_origin.at[0, column][0]) == NameType or type(v_1D_origin.at[0, column][0]) == AbbrType or type(v_1D_origin.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
                        v_1D_origin_value = v_1D_origin.at[0, column][0]
                    elif (type(v_1D_origin.at[0, column]) == np.ndarray and v_1D_origin.at[0, column][0] == None):  # 如果值为 None 的 numpy 数组
                        v_1D_origin_value = None
                    else:
                        is_compress_all_same = False
                        is_compress_diff = True
                        pass  # if
                    if is_compress_all_same:  # 如果是全同列压缩
                        for i in range(len_result_data):
                            if (v_1D_origin.at[i, column] == np.full(num_agent, v_1D_origin_value)).all():
                                is_all_same[i] = True
                                pass  # if
                            pass  # for
                        if is_all_same.all():  # 如果整列值作为 numpy 数组是全同数组 ，则标记该列的第一行的值到  A_data.note ，然后删除该列
                            A_data_compress.note['compress'][para_01][column] = v_1D_origin_value  # 记录值到  A_data.note
                            v_1D_compress.drop(columns=[column], inplace=True)  # 删除该列
                        else:
                            is_compress_all_same = False
                            is_compress_diff = True
                            pass  # if
                        pass  # if
                    ## 差值压缩
                    if is_compress_diff:  # 如果是差值压缩
                        if (type(v_1D_origin.at[0, column]) == np.ndarray and (type(v_1D_origin.at[0, column][0]) == MoneyType or type(v_1D_origin.at[0, column][0]) == np.float64)):  # 如果是 MoneyType 型的 numpy 数组
                            v_1D_compress.at[0, column] = v_1D_origin.loc[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算差值
                                diff = v_1D_origin.at[i, column] - v_1D_origin.at[i - 1, column]
                                v_1D_compress.at[i, column] = csr_array(diff.reshape(1, -1))
                                pass  # for
                            v_1D_compress.at[len_result_data - 1, column] = v_1D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_1D_origin.at[0, column]) == np.ndarray and (type(v_1D_origin.at[0, column][0]) == IdsType or type(v_1D_origin.at[0, column][0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
                            v_1D_compress.at[0, column] = v_1D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算不同
                                diff = v_1D_origin.at[i, column] != v_1D_origin.at[i - 1, column]
                                v_1D_compress.at[i, column] = csr_array(diff.astype(IdsType).reshape(1, -1))
                                pass  # for
                            v_1D_compress.at[len_result_data - 1, column] = v_1D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_1D_origin.at[0, column]) == np.ndarray and type(v_1D_origin.at[0, column][0]) == np.bool_):  # 如果是布尔型的 numpy 数组
                            v_1D_compress.at[0, column] = v_1D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):
                                diff = v_1D_origin.at[i, column] != v_1D_origin.at[i - 1, column]
                                v_1D_compress.at[i, column] = csr_array(diff.reshape(1, -1))  # 转换为稀疏数组
                                pass  # for
                            v_1D_compress.at[len_result_data - 1, column] = v_1D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_1D_origin.at[0, column]) == np.ndarray and (type(v_1D_origin.at[0, column][0]) == NameType or type(v_1D_origin.at[0, column][0]) == AbbrType or type(v_1D_origin.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
                            v_1D_compress.at[0, column] = v_1D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):
                                diff = (v_1D_origin.at[i, column] == v_1D_origin.at[i - 1, column])
                                v_1D_compress.at[i, column] = v_1D_origin.at[i, column].copy()
                                v_1D_compress.at[i, column][diff] = ''
                                if diff.all():  # 如果元素全为相同，则整个数组直接设置为 None，否则相同的元素设置为空字符串
                                    v_1D_compress.at[i, column] = None
                                else:
                                    v_1D_compress.at[i, column][diff] = ''
                                    pass  # if
                                pass  # for
                            v_1D_compress.at[len_result_data - 1, column] = v_1D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_1D_origin.at[0, column]) == np.ndarray and v_1D_origin.at[0, column][0] == None):  # 如果值为 None 的 numpy 数组
                            v_1D_compress.at[0, column] = v_1D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):
                                v_1D_compress.at[i, column] = None  # 这里设定，只要元素存在 None，则整个数组都没有被使用，直接设为 None
                                pass  # for
                            v_1D_compress.at[len_result_data - 1, column] = v_1D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_1D_origin.at[0, column]) == str):  # 如果是字符串类型
                            v_1D_compress.at[0, column] = v_1D_origin.at[0, column]
                            for i in range(1, len_result_data - 1, 1):
                                if (v_1D_origin.at[i, column] == v_1D_origin.at[i - 1, column]):
                                    v_1D_compress.at[i, column] = None
                                else:
                                    v_1D_compress.at[i, column] = v_1D_origin.at[i, column]
                                    pass  # if
                                pass  # for
                            v_1D_compress.at[len_result_data - 1, column] = v_1D_origin.at[len_result_data - 1, column]
                        else:  # 如果是其他类型，不压缩
                            v_1D_compress[column] = v_1D_origin[column].copy()
                            pass  # if
                        pass  # if
                    pass  # for

                A_data_compress[para_01] = v_1D_compress

            else:  # 说明是 2D 的数据
                v_2D_origin = A_data_origin[para_01]
                the_column = list(set(v_2D_origin.columns) - set(['process_name', 'step', 'turn', 'phase']))[0]
                len_result_data = len(v_2D_origin)  # 迭代次数（表格行数）
                num_agent_x = v_2D_origin.at[0, the_column].shape[0]  # 行方向个体数量（表格单元格值之行方向元素个数）
                num_agent_y = v_2D_origin.at[0, the_column].shape[1]  # 列方向个体数量（表格单元格值之行方向元素个数）
                v_2D_compress = pd.DataFrame(columns=v_2D_origin.columns, index=range(len_result_data))
                ## 全同列压缩
                for column in v_2D_origin.columns:
                    is_compress_all_same = True  # 是否全同列压缩
                    is_compress_diff = False  # 是否差值压缩
                    is_all_same = np.full(len_result_data, False)
                    if (type(v_2D_origin.at[0, column]) == np.ndarray and (type(v_2D_origin.at[0, column][0, 0]) == MoneyType or type(v_2D_origin.at[0, column][0, 0]) == np.float64)):  # 如果是 MoneyType 型的 numpy 数组
                        v_2D_origin_value = 0.0
                    elif (type(v_2D_origin.at[0, column]) == np.ndarray and type(v_2D_origin.at[0, column][0, 0]) == np.bool_):  # 如果是布尔型的 numpy 数组
                        v_2D_origin_value = v_2D_origin.at[0, column][0, 0]
                    elif (type(v_2D_origin.at[0, column]) == np.ndarray and (type(v_2D_origin.at[0, column][0]) == NameType or type(v_2D_origin.at[0, column][0]) == AbbrType or type(v_2D_origin.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
                        v_2D_origin_value = v_2D_origin.at[0, column][0, 0]
                    elif (type(v_2D_origin.at[0, column]) == np.ndarray and v_2D_origin.at[0, column][0, 0] == None):  # 如果值为 None 的 numpy 数组
                        v_2D_origin_value = None
                    else:
                        is_compress_all_same = False
                        is_compress_diff = True
                        pass  # if
                    if is_compress_all_same:  # 如果是全同列压缩
                        for i in range(len_result_data):
                            if (v_2D_origin.at[i, column] == np.full((num_agent_x, num_agent_y), v_2D_origin_value)).all():
                                is_all_same[i] = True
                                pass  # if
                            pass  # for
                        if is_all_same.all():  # 如果整列值作为 numpy 数组是全同数组 ，则标记该列的第一行的值到  A_data.note ，然后删除该列
                            A_data_compress.note['compress'][para_01][column] = v_2D_origin_value  # 记录值到  A_data.note
                            v_2D_compress.drop(columns=[column], inplace=True)  # 删除该列
                        else:
                            is_compress_all_same = False
                            is_compress_diff = True
                            pass  # if
                        pass  # if
                    ## 差值压缩、稀疏化压缩
                    if is_compress_diff:  # 如果是差值压缩
                        if (type(v_2D_origin.at[0, column]) == np.ndarray and (type(v_2D_origin.at[0, column][0, 0]) == MoneyType or type(v_2D_origin.at[0, column][0, 0]) == np.float64)):  # 如果是 MoneyType 型的 numpy 数组
                            v_2D_compress.at[0, column] = v_2D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算差值
                                diff = v_2D_origin.at[i, column] - v_2D_origin.at[i - 1, column]
                                v_2D_compress.at[i, column] = csr_array(diff)
                                pass  # for
                            v_2D_compress.at[len_result_data - 1, column] = v_2D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_2D_origin.at[0, column]) == np.ndarray and (type(v_2D_origin.at[0, column][0, 0]) == IdsType or type(v_2D_origin.at[0, column][0, 0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
                            v_2D_compress.at[0, column] = v_2D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算不同
                                diff = v_2D_origin.at[i, column] != v_2D_origin.at[i - 1, column]
                                v_2D_compress.at[i, column] = csr_array(diff.astype(IdsType))
                                pass  # for
                            v_2D_compress.at[len_result_data - 1, column] = v_2D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_2D_origin.at[0, column]) == np.ndarray and type(v_2D_origin.at[0, column][0, 0]) == np.bool_):  # 如果是布尔型的 numpy 数组
                            v_2D_compress.at[0, column] = v_2D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):
                                diff = v_2D_origin.at[i, column] != v_2D_origin.at[i - 1, column]
                                v_2D_compress.at[i, column] = csr_array(diff)  # 转换为稀疏数组
                                pass  # for
                            v_2D_compress.at[len_result_data - 1, column] = v_2D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_2D_origin.at[0, column]) == np.ndarray and (type(v_2D_origin.at[0, column][0]) == NameType or type(v_2D_origin.at[0, column][0]) == AbbrType or type(v_2D_origin.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
                            v_2D_compress.at[0, column] = v_2D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):
                                diff = (v_2D_origin.at[i, column] == v_2D_origin.at[i - 1, column])
                                v_2D_compress.at[i, column] = v_2D_origin.at[i, column].copy()
                                v_2D_compress.at[i, column][diff] = ''
                                if diff.all():  # 如果元素全为相同，则整个数组直接设置为 None，否则相同的元素设置为空字符串
                                    v_2D_compress.at[i, column] = None
                                else:
                                    v_2D_compress.at[i, column][diff] = ''
                                    pass  # if
                                pass  # for
                            v_2D_compress.at[len_result_data - 1, column] = v_2D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_2D_origin.at[0, column]) == np.ndarray and v_2D_origin.at[0, column][0, 0] == None):  # 如果值为 None 的 numpy 数组
                            v_2D_compress.at[0, column] = v_2D_origin.at[0, column].copy()
                            for i in range(1, len_result_data - 1, 1):
                                v_2D_compress.at[i, column] = None  # 这里设定，只要元素存在 None，则整个数组都没有被使用，直接设为 None
                                pass  # for
                            v_2D_compress.at[len_result_data - 1, column] = v_2D_origin.at[len_result_data - 1, column].copy()
                        elif (type(v_2D_origin.at[0, column]) == str):  # 如果是字符串类型
                            v_2D_compress.at[0, column] = v_2D_origin.at[0, column]
                            for i in range(1, len_result_data - 1, 1):
                                if (v_2D_origin.at[i, column] == v_2D_origin.at[i - 1, column]):
                                    v_2D_compress.at[i, column] = None
                                else:
                                    v_2D_compress.at[i, column] = v_2D_origin.at[i, column]
                                    pass  # if
                                pass  # for
                            v_2D_compress.at[len_result_data - 1, column] = v_2D_origin.at[len_result_data - 1, column]
                        else:  # 其他数据类型，直接复制原来的数据
                            v_2D_compress[column] = v_2D_origin[column].copy()
                            pass  # if

                        pass  # if
                    pass  # for

                A_data_compress[para_01] = v_2D_compress

                pass  # if

                # A_data_compress[para_01] = pd.concat([A_data_compress[para_01], A_data_origin[para_01][['process_name', 'step', 'turn', 'phase']]], axis=1)

            pass  # for

        return A_data_compress
        pass  # function

    @classmethod
    def decompress_result_data(cls, A_data_compress: pd.Series, sgv: dict):
        """
        解压实验结果数据。

        解压后的数据应该与原始的实验结果数据一样。

        Args:
            A_data_compress (pd.Series): 压缩后的实验结果数据
            sgv (dict): 模拟器全局变量

        Returns:
            A_data_decompress (pd.Series): 解压后的实验结果数据
        """

        A_data_decompress = pd.Series()

        ## 解压差值压缩、稀疏化压缩的数据
        for para_01 in sgv['list_agents_data_filename_para_01']:
            if para_01 == "note":  # 如果是备注变量，则跳过
                continue
            if not para_01.startswith("I"):  # 说明是 1D 的数据
                v_1D_compress = A_data_compress[para_01]
                len_result_data = len(v_1D_compress)
                v_1D_decompress = pd.DataFrame(columns=v_1D_compress.columns, index=range(len_result_data))
                # 遍历每一列
                for column in v_1D_compress.columns:
                    if (type(v_1D_compress.at[0, column]) == np.ndarray and type(v_1D_compress.at[0, column][0]) == MoneyType):  # 如果是 MoneyType 型的 numpy 数组
                        v_1D_decompress.at[0, column] = v_1D_compress.at[0, column].copy()
                        v_1D_decompress.at[1, column] = v_1D_compress.at[0, column] + v_1D_compress.at[1, column].toarray().ravel()
                        for i in range(2, len_result_data - 1, 1):  # 从第三行开始遍历每一行直到倒数第二行，累加差值
                            diff = v_1D_compress.at[i, column].toarray().ravel()
                            v_1D_decompress.at[i, column] = v_1D_decompress.at[i - 1, column] + diff
                            pass  # for
                        v_1D_decompress.at[len_result_data - 1, column] = v_1D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_1D_compress.at[0, column]) == np.ndarray and (type(v_1D_compress.at[0, column][0]) == IdsType or type(v_1D_compress.at[0, column][0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
                        last_not_none = v_1D_compress.at[0, column].copy()
                        v_1D_decompress.at[0, column] = last_not_none.copy()
                        for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
                            diff = v_1D_compress.at[i, column].toarray().ravel()
                            if not diff.all():  # 设定只有这种可能性
                                v_1D_decompress.at[i, column] = last_not_none.copy()
                                pass  # if
                            pass  # for
                        v_1D_decompress.at[len_result_data - 1, column] = v_1D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_1D_compress.at[0, column]) == np.ndarray and type(v_1D_compress.at[0, column][0]) == np.bool_):  # 如果是布尔型的 numpy 数组
                        v_1D_decompress.at[0, column] = v_1D_compress.at[0, column].copy()
                        v_1D_decompress.at[1, column] = v_1D_compress.at[0, column] ^ v_1D_compress.at[1, column].toarray().ravel()
                        for i in range(2, len_result_data - 1, 1):
                            diff = v_1D_compress.at[i, column].toarray().ravel()
                            v_1D_decompress.at[i, column] = v_1D_decompress.at[i - 1, column] ^ diff
                            pass  # for
                        v_1D_decompress.at[len_result_data - 1, column] = v_1D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_1D_compress.at[0, column]) == np.ndarray and (type(v_1D_compress.at[0, column][0]) == NameType or type(v_1D_compress.at[0, column][0]) == AbbrType or type(v_1D_compress.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
                        last_not_none = v_1D_compress.at[0, column].copy()
                        v_1D_decompress.at[0, column] = last_not_none.copy()
                        for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
                            if v_1D_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
                                v_1D_decompress.at[i, column] = last_not_none.copy()
                            else:
                                last_last_not_none = last_not_none.copy()
                                last_not_none = v_1D_compress.at[i, column].copy()
                                diff = (last_not_none == '')
                                v_1D_decompress.at[i, column] = last_not_none.copy()
                                v_1D_decompress.at[i, column][diff] = last_last_not_none[diff]
                                pass  # if
                            pass  # for
                        v_1D_decompress.at[len_result_data - 1, column] = v_1D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_1D_compress.at[0, column]) == np.ndarray and v_1D_compress.at[0, column][0] == None):  # 如果值为 None 的 numpy 数组
                        v_1D_decompress.at[0, column] = v_1D_compress.at[0, column]
                        for i in range(1, len_result_data - 1, 1):
                            v_1D_decompress.at[i, column] = v_1D_compress.at[0, column].copy()  # 直接赋值为第一行的值
                            pass  # for
                        v_1D_decompress.at[len_result_data - 1, column] = v_1D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_1D_compress.at[0, column]) == str):  # 如果是字符串类型
                        last_not_none = v_1D_compress.at[0, column]
                        v_1D_decompress.at[0, column] = last_not_none
                        for i in range(1, len_result_data - 1, 1):
                            if v_1D_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
                                v_1D_decompress.at[i, column] = last_not_none
                            else:
                                last_not_none = v_1D_compress.at[i, column]
                                v_1D_decompress.at[i, column] = last_not_none
                                pass  # if
                            pass  # for
                        v_1D_decompress.at[len_result_data - 1, column] = v_1D_compress.at[len_result_data - 1, column]
                    else:  # 其他数据类型，直接复制原来的数据
                        v_1D_decompress[column] = v_1D_compress[column].copy()
                        pass  # if

                    pass  # for

                A_data_decompress[para_01] = v_1D_decompress

            else:  # 说明是 2D 的数据
                v_2D_compress = A_data_compress[para_01]
                len_result_data = len(v_2D_compress)
                v_2D_decompress = pd.DataFrame(columns=v_2D_compress.columns, index=range(len_result_data))
                # 遍历每一列
                for column in v_2D_compress.columns:
                    if (type(v_2D_compress.at[0, column]) == np.ndarray and type(v_2D_compress.at[0, column][0, 0]) == MoneyType):  # 如果是 MoneyType 型的 numpy 数组
                        v_2D_decompress.at[0, column] = v_2D_compress.at[0, column].copy()
                        v_2D_decompress.at[1, column] = v_2D_compress.at[0, column] + v_2D_compress.at[1, column].toarray()
                        for i in range(2, len_result_data - 1, 1):  # 从第三行开始遍历每一行直到倒数第二行，累加差值
                            diff = v_2D_compress.at[i, column].toarray()
                            v_2D_decompress.at[i, column] = v_2D_decompress.at[i - 1, column] + diff
                            pass  # for
                        v_2D_decompress.at[len_result_data - 1, column] = v_2D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_2D_compress.at[0, column]) == np.ndarray and (type(v_2D_compress.at[0, column][0, 0]) == IdsType or type(v_2D_compress.at[0, column][0, 0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
                        last_not_none = v_2D_compress.at[0, column].copy()
                        v_2D_decompress.at[0, column] = last_not_none.copy()
                        for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
                            diff = v_2D_compress.at[i, column].toarray()
                            if not diff.all():  # 设定只有这种可能性
                                v_2D_decompress.at[i, column] = last_not_none.copy()
                                pass  # if
                            pass  # for
                        v_2D_decompress.at[len_result_data - 1, column] = v_2D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_2D_compress.at[0, column]) == np.ndarray and type(v_2D_compress.at[0, column][0, 0]) == np.bool_):  # 如果是布尔型的 numpy 数组
                        v_2D_decompress.at[0, column] = v_2D_compress.at[0, column].copy()
                        v_2D_decompress.at[1, column] = v_2D_compress.at[0, column] + v_2D_compress.at[1, column].toarray()
                        for i in range(2, len_result_data - 1, 1):
                            diff = v_2D_compress.at[i, column].toarray()
                            v_2D_decompress.at[i, column] = v_2D_decompress.at[i - 1, column] ^ diff
                            pass  # for
                        v_2D_decompress.at[len_result_data - 1, column] = v_2D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_2D_compress.at[0, column]) == np.ndarray and (type(v_2D_compress.at[0, column][0]) == NameType or type(v_2D_compress.at[0, column][0]) == AbbrType or type(v_2D_compress.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
                        last_not_none = v_2D_compress.at[0, column].copy()
                        v_2D_decompress.at[0, column] = last_not_none.copy()
                        for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
                            if v_2D_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
                                v_2D_decompress.at[i, column] = last_not_none.copy()
                            else:
                                last_last_not_none = last_not_none.copy()
                                last_not_none = v_2D_compress.at[i, column].copy()
                                diff = (last_not_none == '')
                                v_2D_decompress.at[i, column] = last_not_none.copy()
                                v_2D_decompress.at[i, column][diff] = last_last_not_none[diff]
                                pass  # if
                            pass  # for
                        v_2D_decompress.at[len_result_data - 1, column] = v_2D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_2D_compress.at[0, column]) == np.ndarray and v_2D_compress.at[0, column][0, 0] == None):  # 如果值为 None 的 numpy 数组
                        v_2D_decompress.at[0, column] = v_2D_compress.at[0, column]
                        for i in range(1, len_result_data - 1, 1):
                            v_2D_decompress.at[i, column] = v_2D_compress.at[0, column].copy()  # 直接赋值为第一行的值
                            pass  # for
                        v_2D_decompress.at[len_result_data - 1, column] = v_2D_compress.at[len_result_data - 1, column].copy()
                    elif (type(v_2D_compress.at[0, column]) == str):  # 如果是字符串类型
                        last_not_none = v_2D_compress.at[0, column]
                        v_2D_decompress.at[0, column] = last_not_none
                        for i in range(1, len_result_data - 1, 1):
                            if v_2D_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
                                v_2D_decompress.at[i, column] = last_not_none
                            else:
                                last_not_none = v_2D_compress.at[i, column]
                                v_2D_decompress.at[i, column] = last_not_none
                                pass  # if
                            pass  # for
                        v_2D_decompress.at[len_result_data - 1, column] = v_2D_compress.at[len_result_data - 1, column]
                    else:  # 其他数据类型，直接复制原来的数据
                        v_2D_decompress[column] = v_2D_compress[column].copy()
                        pass  # if

                    pass  # for

                A_data_decompress[para_01] = v_2D_decompress

                pass  # if
            pass  # for

        ## 解压全同数据
        A_data_compress.note['compress']
        for k1, v1 in A_data_compress.note['compress'].items():
            if k1 == "note":  # 如果是备注变量，则跳过
                continue
            if not k1.startswith("I"):  # 说明是 1D 的数据
                v_1D_compress = A_data_compress[k1]
                the_column = list(set(v_1D_compress.columns) - set(['process_name', 'step', 'turn', 'phase']))[0]
                len_result_data = len(v_1D_compress)  # 迭代次数（表格行数）
                num_agent = len(v_1D_compress.at[0, the_column])  # 个体数量（表格单元格值之元素个数）
                # v_1D_decompress = pd.DataFrame(columns=v_1D_compress.columns, index=range(len_result_data))
                for k2, v2 in v1.items():
                    series = pd.Series()
                    for i in range(len_result_data):
                        series[i] = np.full(num_agent, v2)
                        pass  # for
                    df = series.to_frame()
                    df.columns = [k2]
                    A_data_decompress[k1] = pd.concat([A_data_decompress[k1], df], axis=1, ignore_index=False)
                    pass  # for
            else:  # 说明是 2D 的数据
                v_2D_compress = A_data_compress[k1]
                the_column = list(set(v_2D_compress.columns) - set(['process_name', 'step', 'turn', 'phase']))[0]
                len_result_data = len(v_2D_compress)  # 迭代次数（表格行数）
                num_agent_x = v_2D_compress.at[0, the_column].shape[0]  # 行方向个体数量（表格单元格值之行方向元素个数）
                num_agent_y = v_2D_compress.at[0, the_column].shape[1]  # 列方向个体数量（表格单元格值之行方向元素个数）
                v_2D_compress = pd.DataFrame(columns=v_2D_compress.columns, index=range(len_result_data))
                len_result_data = len(v_2D_compress)
                # v_2D_decompress = pd.DataFrame(columns=v_2D_compress.columns, index=range(len_result_data))
                for k2, v2 in v1.items():
                    series = pd.Series()
                    for i in range(len_result_data):
                        series[i] = np.full((num_agent_x, num_agent_y), v2)
                        pass  # for
                    df = series.to_frame()
                    df.columns = [k2]
                    A_data_decompress[k1] = pd.concat([A_data_decompress[k1], df], axis=1, ignore_index=False)
                    pass  # for
                pass  # if
        return A_data_decompress
        pass  # function

    pass  # class
