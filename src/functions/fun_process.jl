"函数区：运行过程"

## 函数区：运行过程

##########################################
#状态/开发
##########################################


"""
#NOW函数：运行当前过程: 
# Argument: 
- processContent::String: 待运行的过程之表达式字符串；
"""
# function run_process(content::String)
# # function run_process!(content::String,BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)
#     if env[:processName] == env[:savedProcessName]
#         expr = Meta.parse(content)
#         # eval(expr)#FIXME
#     end
#     # return BB, BI, BB_t1, BI_t1, env
#     return expr
# end


"#NOW宏：运行当前过程"#HACK不好把握，还不能用
macro run_process(content)
    return quote
        if env[:processName] == env[:savedProcessName]
            println(content)
            println(typeof(content))
            $(content)
        end
    end #quote
    # return :($(content))
end # macro


"""
函数：运行当前阶段: 
# Argument: 
- stageContent::String: 待运行的阶段之表达式字符串；
"""
function run_stage!(content::String)
    if env[:stageName] == env[:savedStageName]
        env[:stageName] = "t1 流动性短缺银行间挤兑流动传染冲击阶段"
        @test println("阶段：$(env[:stageName])")
        expr = Meta.parse(content)
        eval(expr) #FIXME
        env[:step] += 1
        if env[:step] % env[:stepSize] == 0
            env[:savedProcessName] = env[:processName]
            env[:savedStageName] = env[:stageName]
            env[:isEndStep] = true
        end
    end
end


"#TODO宏：运行当前阶段"#HACK不好把握，还不能用
macro run_stage(content)
    expr = quote
        if env[:stageName] == env[:savedStageName]
            :(content)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                # break
            end
        end
    end # quote
    return expr
end # macro

