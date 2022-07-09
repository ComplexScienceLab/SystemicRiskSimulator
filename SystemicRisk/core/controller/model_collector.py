"函数区：收集数据"

## 函数区：收集数据

##########################################
# 状态/开发
##########################################
# from SystemicRisk.core import np, pd, deepcopy, SystemicRiskAgent, AgentDataCollection, StateOfScheduleEnum, env, para, TypeMoney, TypeState, TypeIds, TypeList
pass  # end import



import os.path
import numpy as np, pandas as pd
from copy import deepcopy
from SystemicRisk.core.define.define_type import *
from SystemicRisk.core.define.define_parameterVariables import para
from SystemicRisk.core.define.define_environment_variables import env
from SystemicRisk.core.define.define_agents import SystemicRiskAgent
from SystemicRisk.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRisk.core.define.define_enum import StateOfScheduleEnum
pass  # end import





class ModelCollector:

    def collector(A: SystemicRiskAgent, A_data: AgentDataCollection = AgentDataCollection([], []), stateOfProcess=StateOfScheduleEnum.running, env: dict = env, para: dict = dict([])):
        try:
            if stateOfProcess == StateOfScheduleEnum.running:
                A_data = collectAgentData(A, A_data)
                return A_data
            elif stateOfProcess == StateOfScheduleEnum.initializing:
                A_data = initAgentDataCollection(A)
                return A_data
            elif stateOfProcess == StateOfScheduleEnum.finishing:
                exportAgentData(A_data, para)
            else:
                pass  # if:
        except KeyError:
            print("关键词" + str(stateOfProcess) + "取值错误！")

    pass


## 方案三 
"""
TODO函数：初始化实验数据容器
"""


def initAgentDataCollection(self, A: SystemicRiskAgent, env: dict = env):
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


"""
TODO函数：收集数据并存储
"""


def collectAgentData(self, A: SystemicRiskAgent, A_data: AgentDataCollection, env: dict = env):
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


"""
TODO函数：导出实验结果数据
"""


def exportAgentData(self, A_data: AgentDataCollection, env: dict = env, para: dict = para):
    ## 整理banks之数据为一数据框
    BB_data_export = pd.DataFrame()
    BB_data = pd.DataFrame()
    numRow = np.size(A_data.BB[0]['dataBB'][0])[0]
    for (i1, v1) in enumerate(A_data.BB):
        BB_data['data_id'] = np.full(v1['data_id'], numRow)
        BB_data['tau'] = np.full(v1['tau'], numRow)
        BB_data['index_process'] = np.full(v1['index_process'], numRow)
        BB_data['index_stage'] = np.full(v1['index_stage'], numRow)
        fieldNames = list(v1['dataBB'].keys())
        fieldValues = list(v1['dataBB'].values())
        for (i2, v2) in enumerate(fieldValues):
            BB_data[fieldNames[i2]] = v2
            pass
        BB_data_export.append(BB_data)
        pass
    BB_data_export.to_csv(os.path.join(env['folderpath_of_experiments_output_data'], "BB_exp=" + env['id_experiment'] + ".csv"))  # 导出为csv格式；

    ## 整理interbank之数据为一数据框
    BI_data_export = pd.DataFrame()
    BI_data = pd.DataFrame()
    numRow, numCol = np.size(A_data.BI[0]['dataBI'][0])
    for (i1, v1) in enumerate(A_data.BI):
        BI_data['data_id'] = np.full(v1['data_id'], numRow * numCol)
        BI_data['tau'] = np.full(v1['tau'], numRow * numCol)
        BI_data['index_process'] = np.full(v1['index_process'], numRow * numCol)
        BI_data['index_stage'] = np.full(v1['index_stage'], numRow * numCol)
        BI_data['index_stage'] = np.full(v1['index_stage'], numRow * numCol)
        BI_data['row'] = np.repeat(range(1, numRow + 1), numCol)
        BI_data['col'] = np.tile(range(1, numCol + 1), numRow)
        fieldNames = list(v1['dataBI'].keys())
        fieldValues = list(v1['dataBI'].values())
        for (i2, v2) in enumerate(fieldValues):
            if (isinstance(v2, TypeMoney) | isinstance(v2, TypeState) | isinstance(v2, TypeIds)):
                BI_data[fieldNames[i2]] = [v2.T]  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
            elif isinstance(v2, TypeList):
                ## 转换信息列表为矩阵形式
                m2 = np.full((numRow, numCol), False)
                for (i3, v3) in enumerate(v2):
                    for i4 in v3:
                        m2[i3, i4] = True
                        pass
                    pass
                BI_data[fieldNames[i2]] = [m2.T]  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                pass  # if
            pass  # for
            BI_data_export.append(BI_data)
        pass  # for
    BI_data_export.to_csv(os.path.join(env['folderpath_of_experiments_output_data'], "BI_exp=" + env['id_experiment'] + ".csv"))  # 导出为csv格式；

    ## 整理env之数据为一数据框，然后导出为csv格式
    # wsave(datadir(env['folderpath_of_experiments_output_data'], savename(para, "|exp=$(env['id_experiment']).jld2", connector="|", equals="=")), para)

    pass  # def
