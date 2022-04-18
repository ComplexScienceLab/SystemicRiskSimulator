"过程生成器"


##########################################
#状态/开发
##########################################

"""
NOW函数：过程生成器
做如下事情：
1. 调取过程核心内容processContent、过程外围框架processSkeleton；
2. 插入过程核心内容processContent至过程外围框架processSkeleton内，组合成过程process；
3. 写出过程process为文件process.jl；
Argument: 
- processContent::ProcessContent: 过程核心内容
"""
function buildProcess(processName::String, processContent::ProcessContent; processSkeleton::Function=processSkeleton)
    ## 获得过程类型
    processInstanceType = Symbol(processName)

    ## 生成过程process
    process = ProcessComponent{processInstanceType}(
        processName,
        processContent,
        processSkeleton
    )

    @test println("已经生成过程$(process.name)")

    return process
end





"""
NOW过程生成器
"""
function process_builder(processContent::ProcessContent; processSkeleton::Function=fun_process_skeleton!)

    return process
end



