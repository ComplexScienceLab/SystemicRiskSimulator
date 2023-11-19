"模型导出机"

## 模型导出机

##########################################
#状态/暂停
##########################################

# TODO 描述已经过时了。
"""
预制行为 
做如下事情：
1. 调取模型核心实体modelEntity、模型外围框架modelSkeleton；
2. 插入模型核心实体modelEntity至模型外围框架modelSkeleton内，生成模型模块modelComponent，作为模型本身；
3. 写出模型model为文件model.jl；
Argument: 
- processEntity:ProcessEntity: 过程核心实体
"""
def exportProcess(self, processContent:ModelContent; filepath_processSkeleton:String="src/core/template/fun_process_skeleton_template.jl"):

    ## 读取过程外围框架部分
    file_processSkeleton = open(filepath_processSkeleton, "r")
    string_processSkeleton = read(file_processSkeleton, String)
    println("过程外围框架：\n" * string_processSkeleton * "\n")
    close(file_processSkeleton)

    ## 待生成过程
    string_process = string_processSkeleton
    println("替换前的过程：\n" * string_process * "\n")

    ## 依次替换文本内容
    re010 = "fun_model_skeleton_template" # 替换模型名称
    string_model = replace(string_process, re010 = > String(modelContent.entity_name) * "!")
    # re020 = "#=【插入过程列表】=#"
<<<<<<<< HEAD:draft/model_exporter.jl
    # target020 = """enumerate(para[:model_name] * ".listProcess")"""
========
    # target020 = """enumerate(para['model_name'] * ".listProcess")"""
>>>>>>>> python:SystemicRisk/core/template/fun_exporter.py
    # string_model = replace(string_model, re020 => target020)
    re030 = "#=【插入表达式】=#"
    target030 = ""
    for p in modelContent.listProcess
        target030 *= """
<<<<<<<< HEAD:draft/model_exporter.jl
        env[:process_name] = "$(p.text_name)"
        data, IB, env = $(String(p.entity_name))!(data, IB, para, env)
        scheduler!(env)
        if env[:state_of_schedule] == :stepping:
            eval(Meta.parse(expr))
        end
        if env[:state_of_schedule] == :collecting:
========
        env['process_name'] = "$(p.text_name)"
        BB, IB, env = $(String(p.entity_name))!(BB, IB, para, env)
        scheduler(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.stepping:
            eval(Meta.parse(expr))
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
>>>>>>>> python:SystemicRisk/core/template/fun_exporter.py
            #TODO 收集数据
            pass

        """
        pass
    string_model = replace(string_model, re030 => target030)
    println("替换后的模型：\n" * string_model * "\n")

    ## 写入文件
    run(`touch $(String(modelContent.entity_name)).jl`)
    open("test/$(String(modelEntity.entity_name)).jl", "w") do file_model
        write(file_model, string_model)
        pass

    pass


"""
模型导出机
做如下事情：
1. 调取模型核心实体modelContent、模型外围框架modelSkeleton；
2. 插入模型核心实体modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
Argument: 
- modelEntity:ModelEntity: 模型核心实体
"""
def exportModel(self, modelContent:ModelContent; filepath_modelSkeleton:String="test/fun_model_skeleton_template.jl"):

    ## 读取模型外围框架部分
    file_modelSkeleton = open(filepath_modelSkeleton, "r")
    string_modelSkeleton = read(file_modelSkeleton, String)
    println("模型外围框架：\n" * string_modelSkeleton * "\n")
    close(file_modelSkeleton)

    ## 待生成模型
    string_model = string_modelSkeleton
    println("替换前的模型：\n" * string_model * "\n")

    ## 依次替换文本内容
    re010 = "nodeProcessComponent" # 替换模型名称
    string_model = replace(string_model, re010 = > String(modelContent.entity_name) * "!")
    # re020 = "#=【插入过程列表】=#"
<<<<<<<< HEAD:draft/model_exporter.jl
    # target020 = """enumerate(para[:model_name] * ".listProcess")"""
========
    # target020 = """enumerate(para['model_name'] * ".listProcess")"""
>>>>>>>> python:SystemicRisk/core/template/fun_exporter.py
    # string_model = replace(string_model, re020 => target020)
    re030 = "#=【插入表达式】=#"
    target030 = ""
    for p in modelContent.listProcess
        target030 *= """
<<<<<<<< HEAD:draft/model_exporter.jl
        env[:process_name] = "$(p.text_name)"
        data, IB, env = $(String(p.entity_name))!(data, IB, para, env)
        scheduler!(env)
        if env[:state_of_schedule] == :stepping:
            eval(Meta.parse(expr))
        end
        if env[:state_of_schedule] == :collecting:
========
        env['process_name'] = "$(p.text_name)"
        BB, IB, env = $(String(p.entity_name))!(BB, IB, para, env)
        scheduler(env)
        if env['state_of_schedule'] == StateOfScheduleEnum.stepping:
            eval(Meta.parse(expr))
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
>>>>>>>> python:SystemicRisk/core/template/fun_exporter.py
            #TODO 收集数据
            pass

        """
        pass
    string_model = replace(string_model, re030 => target030)
    println("替换后的模型：\n" * string_model * "\n")

    ## 写入文件
    run(`touch $(String(modelContent.entity_name)).jl`)
    open("test/$(String(modelEntity.entity_name)).jl", "w") do file_model
        write(file_model, string_model)
        pass

    pass




