## temp文件

##########################################
#用途/草稿；
##########################################


using DataFrames

# include("../JuliaSystemicRiskLab/core/controller/fun_tools.jl")
# include("../JuliaSystemicRiskLab/core/define/define_type.jl")
# include("../JuliaSystemicRiskLab/core/define/define_model.jl")
# include("../JuliaSystemicRiskLab/model/models/model_content.jl")
# include("../JuliaSystemicRiskLab/model/processes/process_content.jl")
# include("../JuliaSystemicRiskLab/model/stages/stage_content.jl")
# include("../JuliaSystemicRiskLab/model/models/fun_model_skeleton.jl")
# include("../JuliaSystemicRiskLab/model/models/fun_model_BI1111.jl")


# 模型内容结构体
struct ModelContent
    content::String
end

# 模型内容实例
modelContent = ModelContent(
    "我是模型核心内容。"
)

# 模型外围架构
function modelSkeleton(modelContent)
    println("我是模型外围架构。")
end

# 转换模型外围架构为表达式
macro alterToExpr(expr)
    # esc(
        quote
            $(expr)
        end
    # )
    return expr
end

# 生成表达式模型外围架构
expr = @alterToExpr quote
    function modelSkeleton(modelContent::ModelContent)
        println("我是模型外围架构。")
        if modelContent != nothing
            println("已经插入了模型核心内容。内容是：$(modelContent.content)")
        end
    end
end

println(typeof(expr))
println(expr)

# 模型生成器
function modelBuilder(modelContent::ModelContent, modelSkeleton::Expr)
    # 载入modelSkeleton和modelContent。插modelContent入modelSkeleton，生成新的model，保存为文件："model.jl"
    println("插入模型核心内容。")
    modelSkeleton(modelContent)
end



# 载入模型代码文件
# include("model.jl")

# 运行模型代码文件里的模型






