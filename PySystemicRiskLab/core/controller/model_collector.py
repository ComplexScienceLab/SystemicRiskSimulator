"函数区：收集数据"

## 函数区：收集数据

##########################################
# 状态/开发
##########################################
# from PySystemicRiskLab.core import np, pd, deepcopy, SystemicRiskAgent, AgentDataCollection, StateOfScheduleEnum, env, paras, TypeMoney, TypeState, TypeIds, TypeList
import logging

pass  # end import

import os.path

from PySystemicRiskLab import np, pd, deepcopy
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum, StateOfProcessEnum
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_parameterVariables import para
from PySystemicRiskLab.core.define.define_type import *

pass  # end import


class ModelCollector:

    @classmethod
    def collector(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, stateOfProcess: StateOfProcessEnum = env['state_of_process'], env: dict = env, para: dict = dict([])):
        """

        Args:
            A (SystemicRiskAgent): 系统性风险个体众
            A_data (AgentDataCollection): 待收集的数据之于系统性风险个体众
            stateOfProcess (StateOfScheduleEnum): 过程之状态
            para (dict): 控制参数

        Returns:

        """

        # 如果状态在运行时，则收集数据；如果是初始化，则初始化数据；如果是结束时，则导出数据
        try:
            if stateOfProcess == StateOfProcessEnum.running:
                A_data = cls.collectAgentData(A, A_data, env)
                return A_data
            elif stateOfProcess == StateOfProcessEnum.initializing:
                A_data = cls.initAgentDataCollection(A, env)
                return A_data
            elif stateOfProcess == StateOfProcessEnum.finishing:
                cls.exportAgentData(A_data, env)
            else:
                pass  # if:
        except KeyError:
            logging.error("关键词" + str(stateOfProcess) + "取值错误！")

    pass

    @classmethod
    def initAgentDataCollection(cls, A: SystemicRiskAgent, env: dict):
        """

        Args:
            A (SystemicRiskAgent): 系统性风险个体众
            env (dict): 环境变量

        Returns:

        """
        BB_data_item = dict(
            {
                list(env.keys())[list(env.keys()).index('data_id')]: env['data_id'],
                list(env.keys())[list(env.keys()).index('tau')]: env['tau'],
                list(env.keys())[list(env.keys()).index('index_process')]: env['index_process'],
                list(env.keys())[list(env.keys()).index('index_stage')]: env['index_stage'],
                'dataBB': deepcopy(A.BB)
            }
        )
        BB_data = []
        BB_data.append(BB_data_item)  # 初始化banks之数据为一字典数组

        BI_data_item = dict(
            {
                list(env.keys())[list(env.keys()).index('data_id')]: env['data_id'],
                list(env.keys())[list(env.keys()).index('tau')]: env['tau'],
                list(env.keys())[list(env.keys()).index('index_process')]: env['index_process'],
                list(env.keys())[list(env.keys()).index('index_stage')]: env['index_stage'],
                'dataBI': deepcopy(A.BI)
            }
        )
        BI_data = []
        BI_data.append(BI_data_item)  # 初始化interbank之数据为一字典数组

        A_data = AgentDataCollection(deepcopy(BB_data), deepcopy(BI_data))
        return A_data
        pass

    @classmethod
    def collectAgentData(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, env: dict):
        """
        收集数据并存储

        Args:
            A (SystemicRiskAgent):
            A_data (AgentDataCollection):
            env:

        Returns:

        """
        BB_data_item = dict(
            {
                list(env.keys())[list(env.keys()).index('data_id')]: env['data_id'],
                list(env.keys())[list(env.keys()).index('tau')]: env['tau'],
                list(env.keys())[list(env.keys()).index('index_process')]: env['index_process'],
                list(env.keys())[list(env.keys()).index('index_stage')]: env['index_stage'],
                'dataBB': deepcopy(A.BB)
            }
        )
        A_data.BB.append(BB_data_item)  # 收集banks之数据为一字典数组

        BI_data_item = dict(
            {
                list(env.keys())[list(env.keys()).index('data_id')]: env['data_id'],
                list(env.keys())[list(env.keys()).index('tau')]: env['tau'],
                list(env.keys())[list(env.keys()).index('index_process')]: env['index_process'],
                list(env.keys())[list(env.keys()).index('index_stage')]: env['index_stage'],
                'dataBI': deepcopy(A.BI)
            }
        )

        A_data.BI.append(BI_data_item)  # 收集interbank之数据为一字典数组
        return A_data
        pass

    @classmethod
    def exportAgentData(cls, A_data: AgentDataCollection, env: dict):
        """
        导出实验结果数据

        Args:
            A_data:
            env(dict): 环境参数

        Returns:

        """

        ## 整理banks之数据为一数据框
        BB_data_export = pd.DataFrame()
        BB_data = pd.DataFrame()
        numRow, numCol = np.shape(A_data.BB[0]['dataBB'].A_all)
        for (i1, v1) in enumerate(A_data.BB):
            BB_data['data_id'] = np.full(numRow, v1['data_id'])
            BB_data['tau'] = np.full(numRow, v1['tau'])
            BB_data['index_process'] = np.full(numRow, v1['index_process'])
            BB_data['index_stage'] = np.full(numRow, v1['index_stage'])
            fieldNames = list(v1['dataBB'].__dict__.keys())
            fieldValues = list(v1['dataBB'].__dict__.values())
            for (i2, v2) in enumerate(fieldValues):
                BB_data[fieldNames[i2]] = v2
                pass
            BB_data_export = pd.concat([BB_data_export, BB_data])
            pass
        BB_data_export.to_csv(os.path.join(env['folderpath_of_experiments_output_data'], "BB_exp=" + str(env['id_experiment']) + ".csv"))  # 导出为csv格式；

        ## 整理interbank之数据为一数据框
        BI_data_export = pd.DataFrame()
        BI_data = pd.DataFrame()
        numRow, numCol = np.shape(A_data.BI[0]['dataBI'].A_BI)
        for (i1, v1) in enumerate(A_data.BI):
            BI_data['data_id'] = np.full(numRow * numCol, v1['data_id'])
            BI_data['tau'] = np.full(numRow * numCol, v1['tau'])
            BI_data['index_process'] = np.full(numRow * numCol, v1['index_process'])
            BI_data['index_stage'] = np.full(numRow * numCol, v1['index_stage'])
            BI_data['index_stage'] = np.full(numRow * numCol, v1['index_stage'])
            BI_data['row'] = np.repeat(range(1, numRow + 1), numCol)
            BI_data['col'] = np.tile(range(1, numCol + 1), numRow)
            fieldNames = list(v1['dataBI'].__dict__.keys())
            fieldValues = list(v1['dataBI'].__dict__.values())
            for (i2, v2) in enumerate(fieldValues):
                # if type(v2)==TypeIds:
                #     print("这个是id类型！")
                if (v2.dtype == np.float_ or v2.dtype == np.bool_ or v2.dtype == np.int16):
                    BI_data[fieldNames[i2]] = v2.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                elif v2.dtype == list:
                    ## 转换信息列表为矩阵形式 # HACK能否用现成的功能函数代替？
                    m2 = np.full((numRow, numCol), False)
                    if v2 is []:
                        continue
                    for (i3, v3) in enumerate(v2):
                        if v3 is []:
                            m2[i3, :] = False
                            continue
                        for i4 in v3:
                            if i4 in v3:
                                m2[i3, i4] = True
                                pass
                            else:
                                m2[i3, i4] = False
                            pass
                        pass
                    BI_data[fieldNames[i2]] = m2.T.flatten  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                    pass  # if
                pass  # for
                BI_data_export = pd.concat([BI_data_export, BI_data])
            pass  # for
        BI_data_export.to_csv(os.path.join(env['folderpath_of_experiments_output_data'], "BI_exp=" + str(env['id_experiment']) + ".csv"))  # 导出为csv格式；

        ## 整理env之数据为一数据框，然后导出为csv格式
        # wsave(datadir(env['folderpath_of_experiments_output_data'], savename(paras, "|exp=$(env['id_experiment']).jld2", connector="|", equals="=")), paras)

        pass  # def

    @classmethod
    def exportParameterData(cls, list_combinationOfPara, para=para):
        """
        导出控制参数数据
        :param list_combinationOfPara:
        :type list_combinationOfPara:
        :param para:
        :type para:
        :return:
        :rtype:
        """
        env['num_experiment'] = len(list_combinationOfPara)  # 获取实验组之实验个数
        df_010 = pd.DataFrame(list_combinationOfPara, columns=para.keys())  # 转换字典列表为数据框
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
        pass  # def
