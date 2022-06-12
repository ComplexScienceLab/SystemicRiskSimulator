"函数区：输入输出流"

## 函数区：输入输出流

##########################################
#状态/使用
##########################################

"""
函数：设置实验文件夹
# Arguments: 
- env::EnvironmentVariables: 环境变量；
- isDatetime::Bool = True: 是否加入日期时间；
# Return:
- env::EnvironmentVariables: 环境变量，此时内部内容已经被更新；
"""
import time

def set_experiments_folders(env:dict=env, isDatetime:bool=True):

    ## 设定日期时间字符串
    if isDatetime == True:
        str_datetime = "_" * time.strftime("%Y%m%d%H%M%S")
    else:
        str_datetime = ""
        pass

    ## 设定前缀字符串
    if env[:foldernameTypeOfExperiments] == "default":
        str_manuallyName = "default"
    elif env[:foldernameTypeOfExperiments] == "set manually":
        str_manuallyName = env[:foldernamePrefixOfExperiments]
    else:
        throw(DomainError(env[:foldernameTypeOfExperiments], "关键词取值错误！"))
        pass

    env[:foldernameOfExperiments] = str_manuallyName * str_datetime
    env[:folderpathOfExperiments] = joinpath(env[:rootDirOfExperiments], env[:foldernameOfExperiments])

    mkpath(env[:folderpathOfExperiments]) # 创建文件夹
    env[:folderpathOfExperimentsOutputData] = joinpath(env[:folderpathOfExperiments], env[:foldernameOfExperimentsOutputData])
    # cd("$(env[:folderpathOfExperiments])")
    mkpath(env[:folderpathOfExperimentsOutputData]) # 创建文件夹，以导出实验输出数据

    return env
    pass # functioin



