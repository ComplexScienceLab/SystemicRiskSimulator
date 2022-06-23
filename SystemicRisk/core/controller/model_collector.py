"函数区：收集数据"

## 函数区：收集数据

##########################################
# 状态/开发
##########################################
from SystemicRisk.core import deepcopy,SystemicRiskAgent, AgentDataCollection, StateOfScheduleEnum, env


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
    BB_data.append(BB_data_item) # 初始化banks之数据为一字典数组

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
    BI_data.append(BI_data_item) # 初始化interbank之数据为一字典数组

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
    BB_data_export = DataFrame()
    BB_data = DataFrame()
    numRow = size(getfield(A_data.BB[1]['dataBB'], fieldnames(typeof(A_data.BB[1]['dataBB']))[1]))[1]
    for (i1, v1) in enumerate(A_data.BB)
        BB_data[!,:data_id] = fill(v1['data_id'], numRow)
        BB_data[!,:tau] = fill(v1['tau'], numRow)
        BB_data[!,:index_process] = fill(v1['index_process'], numRow)
        BB_data[!,:index_stage] = fill(v1['index_stage'], numRow)
        fieldNames = fieldnames(typeof(v1['dataBB']))
        fieldValues = [getfield(v1['dataBB'], fieldName) for fieldName in fieldNames]
        for (i2, v2) in enumerate(fieldValues)
            BB_data[!, fieldNames[i2]] = v2
            pass
        BB_data_export.append(BB_data)
        pass
    CSV.write(datadir("$(env['folderpath_of_experiments_output_data'])", "BB_exp=$(env['id_experiment']).csv"), BB_data_export)  # 导出为csv格式；

    ## 整理interbank之数据为一数据框
    BI_data_export = DataFrame()
    BI_data = DataFrame()
    numRow, numCol = size(getfield(A_data.BI[1]['dataBI'], fieldnames(typeof(A_data.BI[1]['dataBI']))[1]))
    for (i1, v1) in enumerate(A_data.BI)
        BI_data[!,:data_id] = fill(v1['data_id'], numRow * numCol)
        BI_data[!,:tau] = fill(v1['tau'], numRow * numCol)
        BI_data[!,:index_process] = fill(v1['index_process'], numRow * numCol)
        BI_data[!,:index_stage] = fill(v1['index_stage'], numRow * numCol)
        BI_data[!,:index_stage] = fill(v1['index_stage'], numRow * numCol)
        BI_data[!,:row] = repeat(1: numRow, inner = numCol)
        BI_data[!,:col] = repeat(1: numCol, outer = numRow)
        fieldNames = fieldnames(typeof(v1['dataBI']))
        fieldValues = [getfield(v1['dataBI'], fieldName) for fieldName in fieldNames]
        for (i2, v2) in enumerate(fieldValues)
            if (typeof(v2) == TypeMoney{2} | | typeof(v2) == TypeState | | typeof(v2) == TypeIds{2}):
                BI_data[!, fieldNames[i2]] = [v2'...] # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                elif typeof(v2) == TypeList:
                {Any}
                ## 转换信息列表为矩阵形式
                m2 = Matrix
                {Any}(falses(numRow, numCol))
                for (i3, v3) in enumerate(v2)
                for i4 in v3
                m2[i3, i4] = True
                pass
                pass
                BI_data[!, fieldNames[i2]] =[m2'...] # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
                pass
                pass
                BI_data_export.append(BI_data)
                pass
                CSV.write(datadir("$(env['folderpath_of_experiments_output_data'])", "BI_exp=$(env['id_experiment']).csv"), BI_data_export)  # 导出为csv格式

                ## 整理env之数据为一数据框，然后导出为csv格式
                # wsave(datadir(env['folderpath_of_experiments_output_data'], savename(para, "|exp=$(env['id_experiment']).jld2", connector="|", equals="=")), para)

                pass
