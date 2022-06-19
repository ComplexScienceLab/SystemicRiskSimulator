

## 批处理导出模型

##########################################
#状态/开发
##########################################

using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目

include("../include/include_exp_files.jl")

include("../../src/include/SystemicRiskSimulation.jl")

include("../../src/include/Models.jl")


## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
list_combinationOfPara = dict_list(setOfValuesOfParameterVariables)

## 初始化参数变量
# (i, para) = enumerate(list_combinationOfPara)
println("\n列出所有实验组：")
for (idx_para, para) in enumerate(list_combinationOfPara)
    println("$(idx_para): $(para);")
    modelContent = eval(Meta.parse("modelContent_" * para[:model_name]))

end


## 导出本次实验组所需的所有模型
model = exportModel!(modelContent_BI1111)
if length(setOfValuesOfParameterVariables[:model_name]) > 1
    for model_name in setOfValuesOfParameterVariables[:model_name][2:end]
        modelContent = eval(Meta.parse("modelContent_$(model_name)"))
        # if true # FIXME如果不存在模型文件，则构建模型
        model = exportModel!(modelContent)
        # end
    end
end


