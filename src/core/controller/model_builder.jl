"模型生成器"

## 模型生成器

##########################################
#状态/开发
##########################################

"""
函数：模型生成器
做如下事情：
1. 调取模型核心内容modelContent、模型外围框架modelSkeleton；
2. 插入模型核心内容modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
Argument: 
- modelContent::ModelContent: 模型核心内容
"""
function modelBuilder!(modelContent::ModelContent)

    ## 读取模型外围框架部分
    file_modelSkeleton = open("model_skeleton.jl", "r")
    string_modelSkeleton = read(file_modelSkeleton, String) 
    println("模型外围框架：\n" * string_modelSkeleton * "\n")
    close(file_modelSkeleton)
    
    ## 待生成模型
    string_model = string_modelSkeleton 
    println("替换前的模型：\n" * string_model * "\n")
    
    ## 依次替换文本内容
    re010 = r"##\s插入modelContent"
    string_model = replace(string_model, re010 => modelContent.content)
    re020 = """println("我是模型外围架构。虽然我可以运行起来，但是我需要被插入核心内容，才能成为一个有意义的模型。")"""
    string_model = replace(string_model, re020 => """println("我是模型外围架构。")""")
    re030 = "modelSkeleton"
    string_model = replace(string_model, re030 => "model")
    println("替换后的模型：\n" * string_model * "\n")
    
    ## 写入文件
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





"""
NOW过程生成器
"""
function process_builder(processContent::ProcessContent; processSkeleton::Function=fun_process_skeleton!)

    return process
end



