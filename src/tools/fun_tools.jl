"函数区：工具集"

## 函数区：工具集

##########################################
#状态/使用
##########################################

"宏：当测试时使用"
macro testprintln(content)
    if env[:is_test]
        return esc(
            quote
                write(f,$(content));write(f,"\n");println($(content))
            end
        )
    end
end


"""
函数：设置实验文件夹
# Arguments: 
- env::EnvironmentVariables: 环境变量；
- isDatetime::Bool = true: 是否加入日期时间；
# Return:
- env::EnvironmentVariables: 环境变量，此时内部内容已经被更新；
"""
function setExperimentsFolders!(env::Dict; isDatetime::Bool=true)

    # 设定日期时间字符串
    if isDatetime == true
        str_datetime = "_" * Dates.format(DateTime(now()), "YYYYmmddHHMMSS")
    else
        str_datetime = ""
    end

    ## 设定前缀字符串
    if env[:foldername_type_of_experiments] == "default"
        str_manuallyName = "default"
    elseif env[:foldername_type_of_experiments] == "set manually"
        str_manuallyName = env[:foldername_prefix_of_experiments]
    else
        throw(DomainError(env[:foldername_type_of_experiments], "关键词取值错误！"))
    end

    env[:foldername_of_experiments] = str_manuallyName * str_datetime
    env[:folderpath_of_experiments] = joinpath(env[:root_dir_of_experiments], env[:foldername_of_experiments])

    mkpath(env[:folderpath_of_experiments]) # 创建文件夹
    env[:folderpath_of_experiments_output_data] = joinpath(env[:folderpath_of_experiments], env[:foldername_of_experiments_output_data])
    # cd("$(env[:folderpath_of_experiments])")
    mkpath(env[:folderpath_of_experiments_output_data]) # 创建文件夹，以导出实验输出数据

    return env
end # functioin





