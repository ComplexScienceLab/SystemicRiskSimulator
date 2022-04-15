# 定义：模型内容结构体
struct ModelContent
    content::String
end

#= 定义：模型生成器
做如下事情：
1. 调取模型核心内容modelContent、模型外围框架modelSkeleton；
2. 插入模型核心内容modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
=#
function modelBuilder!(modelContent::ModelContent)

    file_modelSkeleton = open("model_skeleton.jl", "r")
    string_modelSkeleton = read(file_modelSkeleton, String)
    println("模型外围框架：\n" * string_modelSkeleton * "\n")
    close(file_modelSkeleton)
    
    string_model = string_modelSkeleton
    println("替换前的模型：\n" * string_model * "\n")
    
    re010 = r"##\s插入modelContent"
    string_model = replace(string_model, re010 => modelContent.content)
    
    re020 = """println("我是模型外围架构。虽然我可以运行起来，但是我需要被插入核心内容，才能成为一个有意义的模型。")"""
    string_model = replace(string_model, re020 => """println("我是模型外围架构。")""")
    
    re030 = "modelSkeleton"
    string_model = replace(string_model, re030 => "model")
    
    println("替换后的模型：\n" * string_model * "\n")
    
    run(`touch model.jl`)
    open("model.jl","w") do file_model
        write(file_model, string_model)
    end
   
end

# 定义：运行模型
macro runModel()
    expr = quote
        include("model.jl")
        model()
    end
    println("开始运行模型model：")
    eval(expr)
    println("结束运行模型model。")
end



