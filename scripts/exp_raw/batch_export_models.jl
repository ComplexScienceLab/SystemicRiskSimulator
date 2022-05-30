

## 批处理导出模型

##########################################
#状态/开发
##########################################

using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目


## 构建本次实验组所需的所有模型
model = buildModel(modelContent_BI1111)
if length(setOfValuesOfParameterVariables[:modelName]) > 1
    for modelName in setOfValuesOfParameterVariables[:modelName][2:end]
        modelContent = eval(Meta.parse("modelContent_$(modelName)"))
        # if true # FIXME如果不存在模型文件，则构建模型
        model = buildModel(modelContent)
        # end
    end
end
