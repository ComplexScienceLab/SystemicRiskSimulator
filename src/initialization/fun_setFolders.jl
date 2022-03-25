"函数区：设置实验文件夹"

## 函数区：设置实验文件夹

##########################################
#状态/开发
##########################################

"""
函数：设置实验文件夹
# Arguments: 
- env::Dict: 环境变量；
- isDatetime::Bool = true: 是否加入日期时间；
"""
function setExperimentsFolders(env::Dict; isDatetime::Bool = true)

    # 设定日期时间字符串
    if isDatetime == true
        str_datetime = "_" * Dates.format(DateTime(now()), "YYYYmmddHHMMSS")
    else
        str_datetime = ""
    end

    ## 设定前缀字符串
    if env[:foldernameTypeOfExperimentsData] == "default"
        str_manuallyName = "default"
    elseif env[:foldernameTypeOfExperimentsData] == "set manually"
        str_manuallyName = env[:foldernamePrefixOfExperimentsData]
    else
        throw(DomainError(env[:foldernameTypeOfExperimentsData], "关键词取值错误！"))
    end

    foldername = str_manuallyName * str_datetime
    folderdir = env[:rootDirOfExperimentsData]
    env[:folderpathOfExperimentsData] = folderdir * foldername

    mkpath(env[:folderpathOfExperimentsData]) # 创建文件夹
return env
end # functioin
