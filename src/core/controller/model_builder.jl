"模型生成器"

## 模型生成器

##########################################
#状态/开发
##########################################

"""
NOW函数：模型生成器
做如下事情：
1. 调取模型核心内容modelContent、模型外围框架modelSkeleton；
2. 插入模型核心内容modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
Argument: 
- modelContent::ModelContent: 模型核心内容
"""
function buildModel(modelName::String, modelContent::ModelContent; modelSkeleton::Function=modelSkeleton)

    ## 获得模型类型
    modelType = Symbol(modelName)

    ## 生成模型model
    model = ModelComponent{modelType}(
        modelName,
        modelContent,
        modelSkeleton
    )
    @test println("已经生成模型$(model.name)")
    return model

end





"""
NOW过程生成器
"""
function process_builder(processContent::ProcessContent; processSkeleton::Function=fun_process_skeleton!)

    return process
end



