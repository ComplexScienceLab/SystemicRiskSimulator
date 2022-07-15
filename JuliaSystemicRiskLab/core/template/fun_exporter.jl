"模型导出器"

## 模型导出器

##########################################
#状态/开发
##########################################


"""
函数：过程导出器
做如下事情：
1. 调取模型核心内容modelContent、模型外围框架modelSkeleton；
2. 插入模型核心内容modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
Argument: 
- processContent::ProcessContent: 过程核心内容
"""
function exportProcess!(processContent::ModelContent; filepath_processSkeleton::String="src/core/template/fun_process_skeleton_template.jl")

    ## 读取过程外围框架部分
    file_processSkeleton = open(filepath_processSkeleton, "r")
    string_processSkeleton = read(file_processSkeleton, String)
    println("过程外围框架：\n" * string_processSkeleton * "\n")
    close(file_processSkeleton)

    ## 待生成过程
    string_process = string_processSkeleton
    println("替换前的过程：\n" * string_process * "\n")

    ## 依次替换文本内容
    re010 = "fun_model_skeleton_template!" # 替换模型名称
    string_model = replace(string_process, re010 => String(modelContent.functionName) * "!")
    # re020 = "#=【插入过程列表】=#"
    # target020 = """enumerate(para[:model_name] * ".listProcess")"""
    # string_model = replace(string_model, re020 => target020)
    re030 = "#=【插入表达式】=#"
    target030 = ""
    for p in modelContent.listProcess
        target030 *= """
        env[:process_name] = "$(p.textName)"
        BB, BI, env = $(String(p.functionName))!(BB, BI, para, env)
        scheduler!(env)
        if env[:state_of_schedule] == :stepping
            eval(Meta.parse(expr))
        end
        if env[:state_of_schedule] == :collecting
            #TODO 收集数据
        end

        """
    end
    string_model = replace(string_model, re030 => target030)
    println("替换后的模型：\n" * string_model * "\n")

    ## 写入文件
    run(`touch $(String(modelContent.functionName)).jl`)
    open("test/$(String(modelContent.functionName)).jl", "w") do file_model
        write(file_model, string_model)
    end

end


"""
函数：模型导出器
做如下事情：
1. 调取模型核心内容modelContent、模型外围框架modelSkeleton；
2. 插入模型核心内容modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
Argument: 
- modelContent::ModelContent: 模型核心内容
"""
function exportModel!(modelContent::ModelContent; filepath_modelSkeleton::String="test/fun_model_skeleton_template.jl")

    ## 读取模型外围框架部分
    file_modelSkeleton = open(filepath_modelSkeleton, "r")
    string_modelSkeleton = read(file_modelSkeleton, String)
    println("模型外围框架：\n" * string_modelSkeleton * "\n")
    close(file_modelSkeleton)

    ## 待生成模型
    string_model = string_modelSkeleton
    println("替换前的模型：\n" * string_model * "\n")

    ## 依次替换文本内容
    re010 = "fun_model_skeleton!" # 替换模型名称
    string_model = replace(string_model, re010 => String(modelContent.functionName) * "!")
    # re020 = "#=【插入过程列表】=#"
    # target020 = """enumerate(para[:model_name] * ".listProcess")"""
    # string_model = replace(string_model, re020 => target020)
    re030 = "#=【插入表达式】=#"
    target030 = ""
    for p in modelContent.listProcess
        target030 *= """
        env[:process_name] = "$(p.textName)"
        BB, BI, env = $(String(p.functionName))!(BB, BI, para, env)
        scheduler!(env)
        if env[:state_of_schedule] == :stepping
            eval(Meta.parse(expr))
        end
        if env[:state_of_schedule] == :collecting
            #TODO 收集数据
        end

        """
    end
    string_model = replace(string_model, re030 => target030)
    println("替换后的模型：\n" * string_model * "\n")

    ## 写入文件
    run(`touch $(String(modelContent.functionName)).jl`)
    open("test/$(String(modelContent.functionName)).jl", "w") do file_model
        write(file_model, string_model)
    end

end




