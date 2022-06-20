"函数区：输入输出流"

## 函数区：输入输出流

##########################################
#状态/使用
##########################################

"""
函数：设置实验文件夹
# Arguments: 
- env:EnvironmentVariables: 环境变量；
- isDatetime:Bool = True: 是否加入日期时间；
# Return:
- env:EnvironmentVariables: 环境变量，此时内部内容已经被更新；
"""
import time

def set_experiments_folders(self, env:dict=env, isDatetime:bool=True):

    ## 设定日期时间字符串
    if isDatetime == True:
        str_datetime = "_" * time.strftime("%Y%m%d%H%M%S")
    else:
        str_datetime = ""
        pass

    ## 设定前缀字符串
    if env['foldername_type_of_experiments'] == "default":
        str_manuallyName = "default"
    elif env['foldername_type_of_experiments'] == "set manually":
        str_manuallyName = env['foldername_prefix_of_experiments']
    else:
        throw(DomainError(env['foldername_type_of_experiments'], "关键词取值错误！"))
        pass

    env['foldername_of_experiments'] = str_manuallyName * str_datetime
    env['folderpath_of_experiments'] = joinpath(env['root_dir_of_experiments'], env['foldername_of_experiments'])

    mkpath(env['folderpath_of_experiments']) # 创建文件夹
    env['folderpath_of_experiments_output_data'] = joinpath(env['folderpath_of_experiments'], env['foldername_of_experiments_output_data'])
    # cd("$(env['folderpath_of_experiments'])")
    mkpath(env['folderpath_of_experiments_output_data']) # 创建文件夹，以导出实验输出数据

    return env
    pass # functioin



