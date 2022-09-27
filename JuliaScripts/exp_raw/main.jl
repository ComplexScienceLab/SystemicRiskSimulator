

## 批处理主程序

## 主程序

##########################################
#状态/维护
##########################################

using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目

include("../include/include_exp_files.jl")

include("../../JuliaSystemicRiskLab/include/SystemicRiskSimulation.jl")

include("../../JuliaSystemicRiskLab/include/Models.jl")

# include("../settings/set_agentsVariables.jl")



# using SystemicRiskSimulation



## 设定参数组合

# list_combinationOfPara = @strdict model kappa_A_P kappa_BI #HACK无用

## 创建主文件夹用于本批次实验
env = setExperimentsFolders!(env)

## 建立文件以记录log
f = open(joinpath(env[:folderpath_of_experiments_output_data], "outputlog.txt"), "w")
@testprintln "\n实验组名称：$(env[:foldername_of_experiments])"

## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
list_combinationOfPara = dict_list(setOfValuesOfParameterVariables) # 组合排列多结构体成为列表
exportParameterData(list_combinationOfPara) # 导出控制参数数据

## 初始化参数变量
@testprintln "\n列出所有实验组："
for (idx_para, para) in enumerate(list_combinationOfPara)
    @testprintln "$(idx_para): $(para);"
    modelContent = eval(Meta.parse("modelContent_" * para[:model_name]))
end

## 构建本次实验组所需的所有模型
models = Dict() # 初始化模型们
for model_name in unique(setOfValuesOfParameterVariables[:model_name])
    modelContent = eval(Meta.parse("modelContent_$(model_name)")) # 依次构建模型们
    local model = buildModel(modelContent)
    models[model_name] = model
end
# end

println("\n实验组开始：\n")

## 主循环
for (i, para) in enumerate(list_combinationOfPara)
    local model = models[para[:model_name]] # 获取当前循环的模型
    env[:id_experiment] = i # 设定当前实验编号
    # 重置环境变量
    env[:index_of_schedule_position] = []
    env[:index_model] = 1
    env[:index_process] = 1
    env[:index_stage] = 1
    env[:saved_index_process] = 1
    env[:saved_index_stage] = 1
    env[:loaded_index_process] = 1
    env[:loaded_index_stage] = 1
    env[:step] = 0
    env[:tau] = 0
    env[:saved_model_name] = ""
    env[:model_name] = model.functionName
    env[:process_name] = ""
    env[:saved_process_name] = ""
    env[:stage_name] = ""
    env[:saved_stage_name] = ""
    env[:is_step] = true
    env[:is_loop] = true
    env[:is_round] = true
    env[:is_stage] = true
    env[:is_process] = true
    env[:is_model] = true
    env[:is_experiment] = true
    env[:state_of_schedule] = :indexing
    env[:state_of_process] = :initializing

    ## 生成模型内容
    # modelComponent = eval(Meta.parse(para[:model_name]))

    ## 调度：生成位置索引
    if env[:state_of_schedule] == :indexing
        env[:index_of_schedule_position], env[:state_of_schedule] = scheduler_indexing(model)
    end

    @testprintln "\n实验$(env[:id_experiment])/$(length(list_combinationOfPara))开始："
    @testprintln "\n相关实验参数：$(para)"

    ## 进行实验
    makesim(model, para, env)

    @testprintln "本次实验结束，还剩下$(length(list_combinationOfPara)-env[:id_experiment])个实验。\n"
end # for

println("实验组结束。")


close(f)

#TODO 加一个自动打开日志文件的代码。


