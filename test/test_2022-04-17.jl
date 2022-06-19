

#===== 定义文件头 ======#

## 定义文件类型
struct ModelType end

## 定义模型核心内容
struct ModelContent
    components::Array{ProcessContent}
end

## 定义通用模型
struct GeneralModel{ModelType}
    name::String
    content::ModelContent
    run::Function
end

## 定义模型外围架构
function modelSkeleton(modelContent::ModelContent)
    println("我是模型外围架构。")
    for i in modelContent.components
        println(i) # 此处运行模型核心内容
    end
    println("\n")
end

## 定义生成模型
function buildModel(model_name::String, modelContent::ModelContent; modelSkeleton::Function=modelSkeleton)
    modelType = Symbol(model_name)
    model = GeneralModel{modelType}(
        model_name,
        modelContent,
        modelSkeleton
    )
    println("已经生成模型$(model.name)")
    return model
end

## 定义运行模型
function runModel(model::GeneralModel)
    model.run(model.content)
end

#===== 定义文件尾 ======#




#===== 设置文件头 ======#

## 写入模型xxx之名称、核心内容
xxxName = "xxx"
xxxContent = ModelContent(
    [
    "我是模型核心组件1。",
    "我是模型核心组件3。",
    "我是模型核心组件5。"
]
)

## 写入模型yyy之名称、核心内容
yyyName = "yyy"
yyyContent = ModelContent(
    [
    "我是模型核心组件1。",
    "我是模型核心组件2。",
    "我是模型核心组件4。"
]
)

#===== 设置文件尾 ======#



#===== 主文件头 ==========#
# include设置文件、定义文件。

## 生成模型xxx
xxxModel = buildModel(xxxName, xxxContent)

## 运行模型xxx
runModel(xxxModel)

## 生成模型yyy
yyyModel = buildModel(yyyName, yyyContent)

## 运行模型yyy
runModel(yyyModel)
#===== 主文件尾 ==========#