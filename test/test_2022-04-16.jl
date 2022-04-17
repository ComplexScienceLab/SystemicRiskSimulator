

#===== 定义文件头 ======#

## 定义文件类型
struct ModelType end

## 定义模型核心内容
struct ModelContent
    content::Expr
end

## 定义通用模型
struct GeneralModel{ModelType}
    name::String
    content::ModelContent
    fun::Function
end

## 定义模型外围架构
function modelSkeleton(modelContent::ModelContent)
    println("我是模型外围架构。")
    eval(modelContent.content)  # 此处运行模型核心内容
end

## 定义生成模型
function buildModel(modelName::String, modelContent::ModelContent; modelSkeleton::Function=modelSkeleton)
    modelType = Symbol(modelName)
    model = GeneralModel{modelType}(
        modelName,
        modelContent,
        modelSkeleton
    )
    println("已经生成模型$(model.name)")
    return model
end

## 定义运行模型
function runModel(model::GeneralModel)
    model.fun(model.content)
end

#===== 定义文件尾 ======#




#===== 设置文件头 ======#

## 写入模型xxx之名称、核心内容
xxxName="xxx"
xxxContent = ModelContent(
    :(println("我是模型核心内容XXX。\n"))
)

## 写入模型yyy之名称、核心内容
yyyName="yyy"
yyyContent = ModelContent(
    :(println("我是模型核心内容YYY。\n"))
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