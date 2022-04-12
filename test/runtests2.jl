## temp文件

##########################################
#用途/草稿；
##########################################


using DataFrames

include("../src/core/define/define_type.jl")
include("../src/core/define/define_model.jl")
include("../src/core/define/define_type.jl")
include("../src/model/models/model_content.jl")
include("../src/model/processes/process_content.jl")
include("../src/model/stages/stage_content.jl")



# expr=quote

# """
# 通用模型框架：
# Argument: 
# - BB::BankCommercial: 商业银行群变量；
# - BI::BankInterbank: 银行间邻接矩阵变量；
# - para::Dict: 参数变量；
# - env::Dict: 环境变量；
# """
# function fun_model_skeleton!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

#     env[:indexProcess] = 0 # 初始化过程所在位置
#     env[:stateOfSchedule] = :stepping
#     @test println("切换调度运作状态为indexing")

#     env[:tau] = 0 # 初始化回合

#     if (!env[:isModel])
#         if (env[:tau] > 0)
#             @test println("继续模型model：\n")
#         else
#             @test println("开始模型model：\n")
#         end
#     end

    
#     ## 运行每一个过程
#     for p in eval(Meta.parse(para[:modelName] * ".listProcess"))
#         env[:processName] = Symbol(p)
#         expr = "BB, BI, env = " * String(p) * "!(BB, BI, para, env)"
#         @scheduler_process Meta.parse(expr)
#     end

#     ## 判断是否结束
#     if !env[:isStep]
#         @test println("步进已结束，跳出$(env[:modelName])。")
#     end

#     if env[:stateOfSchedule] == :standing
#         env[:isModel] = false
#         env[:isExperiment] = false
#     end

#     if (!env[:isModel] || !env[:isExperiment])
#         @test println("$(env[:modelName])结束。")
#     end


#     return BB, BI, para, env
#     # return BB, BI, BB_tau, BI_tau, para, env
# end # function

# # end # module

# end
# 
# 

    # 
# function model_builder(modelContent::Model; skeleton::Function=fun_model_skeleton!)
#     print(skeleton) 
# end

# model_builder(model_BI1111)

function scheduler_indexing(model::Model, stateOfSchedule::Symbol)
    if stateOfSchedule == :indexing
        indexOfSchedulePosition = []
        n=0
        for (i, p) in enumerate(model.listProcess)
            append!(indexOfSchedulePosition, [[]])
            for (j, s) in eval(Meta.parse("enumerate($(p).listStage)"))
                n+=1
                push!(indexOfSchedulePosition[i], n)
            end
        end
    end
    println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
    stateOfSchedule = :stepping
    # for i in indexOfSchedulePosition
    #     println(indexOfSchedulePosition[i])
    # end
    return indexOfSchedulePosition, stateOfSchedule
end



idx,state = scheduler_indexing(model_BI1111,:indexing)

