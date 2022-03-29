"函数区：工具集"

## 函数区：工具集

##########################################
#状态/开发
##########################################

"""
函数：设置实验文件夹
# Arguments: 
- env::EnvironmentVariables: 环境变量；
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



"宏：当测试时使用"
macro test(content)
    if env[:isTest]
        # return content
        # return :(content)
        # return $(content)
        return :($(content))
    end
end


"#TODO宏：运行过程"
macro run_process(content)
    if env[:processName] == saveprocess[:savedProcessName]
        return :(content)
    end
end

"函数：运行过程"
function run_process(processName::String,processContent::Expr)
    if env[:processName] == saveprocess[:savedProcessName]
        processContent
    end
end


"#TODO宏：运行阶段"
macro run_stage(content)
    expr = quote
        if env[:stageName] == env[:savedStageName]
            env[:stageName] = "t1 流动性短缺银行间挤兑流动传染冲击阶段"
            @test println("阶段：$(env[:stageName])")
            content
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                break
            end
        end
    end # quote
    return :(expr)
end # macro