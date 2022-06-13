"调度器"

## 调度器

##########################################
#状态/开发
##########################################


"""
函数：调度器 #HACK 或将废弃

Argument: 
- modelContent::ModelContent: 被调度的模型内容；
- env::dict: 环境变量；

Return: 
- env::dict: 环境变量；
"""
def scheduler(env:dict, A:SystemicRiskAgent, A_data:AgentDataCollection)#= component::Union{ModelComponent,ProcessComponent},  =#:
    if env['stateOfSchedule'] == StateOfSchedule.loading
        env['loadedIndexProcess'], env['loadedIndexStage'], env['stateOfSchedule'] = scheduler_loading(env['indexOfSchedulePosition'], env['indexProcess'], env['savedIndexProcess'], env['stateOfSchedule']) # 读取
        pass
    if env['stateOfSchedule'] == StateOfSchedule.stepping
        env['step'], env['isStep'], env['stateOfSchedule'] = scheduler_stepping(env['step'], env['stepSize']) # 步进
        pass
    if env['stateOfSchedule'] == StateOfSchedule.saving
        env['savedIndexProcess'], env['savedIndexStage'], env['stateOfSchedule'] = scheduler_saving(env['indexOfSchedulePosition'], env['indexProcess'], env['indexStage']) # 存储
        pass
    if env['stateOfSchedule'] == StateOfSchedule.collecting
        env['stateOfSchedule'] = scheduler_collecting(A, A_data)
        pass
    # if (stateOfSchedule == StateOfSchedule.indexing): #HACK 冗余
    #     env['indexOfSchedulePosition'], env['stateOfSchedule'] = scheduler_indexing(component) # 索引
    #     pass
    pass # functions


"""
函数：调度索引

Argument: 
- modelContent::ModelContent: 被调度的模型内容；

Return: 
- indexOfSchedulePosition::Array 调度位置索引列表；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_indexing(model::ModelComponent)
    indexOfSchedulePosition = []
    for i in 1:length(model.content)
        append(indexOfSchedulePosition, [[i, []]])
        for j in 1:length(model.content[i].content)
            push(indexOfSchedulePosition[i][2], j)
            pass
        pass
    @testprintln "索引完成。值为：$(indexOfSchedulePosition)"
    stateOfSchedule = StateOfSchedule.saving
    @testprintln "切换调度运作状态为$(stateOfSchedule)"
    return indexOfSchedulePosition, stateOfSchedule
    pass


"""
函数：调度读取

Argument: 
- indexOfSchedulePosition::Vector{Any}: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- indexStage::Int: 当前阶段之位置；
- loadedIndexProcess::Int: 读取的过程之位置；
- loadedIndexStage::Int: 读取的阶段之位置；
- stateOfSchedule::Symbol: 调度状态；

Return: 
- newStateOfSchedule::Symbol: 新的调度状态；
"""
function scheduler_loading(indexOfSchedulePosition::Vector{Any}, indexProcess::Int, indexStage::Int, loadedIndexProcess::Int, loadedIndexStage::Int, stateOfSchedule::Symbol)
    @testprintln "调度读取中……"
    newStateOfSchedule = stateOfSchedule
    if (indexProcess == loadedIndexProcess && indexStage == loadedIndexStage): # 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取
        if (!(indexOfSchedulePosition[indexProcess][1] == length(indexOfSchedulePosition[:, 1]) && indexOfSchedulePosition[indexProcess][2][indexStage] == length(indexOfSchedulePosition[indexProcess][2])) && isProcess == True): # 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运行过程，则继续读取，否则说明程序之模型部分已经运行到终点了，此时应停止读取，然后改状态为idle。
            newStateOfSchedule = StateOfSchedule.stepping # 切换调度运作状态为步进
        else:
            newStateOfSchedule = StateOfSchedule.idle # 切换调度运作状态为待命
            pass
        @testprintln "调度读取完毕。切换调度运作状态为$(newStateOfSchedule)。"
        pass
    return newStateOfSchedule
    pass


# "函数：调度步进"
# functions scheduler_stepping(process::Symbol, env::dict=env, savedIndexProcess::Int)
#     $(process)
#     scheduler_altToSavingState(env)
#     pass


"""
函数：调度步进

Argument: 
- step::Int: 步进步数；
- stepSize::Int: 步进尺寸；

Return: 
- isStep::Bool: 是否步进；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_stepping(step::Int, stepSize::Int)
    step += 1
    if step % stepSize == 0: # 是否完成本次步进
        isStep = False
        stateOfSchedule = StateOfSchedule.saving # 切换调度运作状态为存储
        @testprintln "步进停止。切换调度运作状态为saving"
    else:
        isStep = True
        stateOfSchedule = StateOfSchedule.stepping
        @testprintln "步进继续："
        pass
    return step, isStep, stateOfSchedule
    pass


"""
函数：调度存储

Argument: 
- indexOfSchedulePosition::Vector{Any}: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- indexStage::Int: 当前阶段之位置；
- isProcess::Bool: 是否在过程状态中；

Return: 
- savedIndexProcess::Int: 存储的过程之位置；
- savedIndexStage::Int: 存储的阶段之位置；
- loadedIndexProcess::Int: 读取的过程之位置；
- loadedIndexStage::Int: 读取的阶段之位置；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_saving(indexOfSchedulePosition::Vector{Any}, indexProcess::Int, indexStage::Int, isProcess::Bool)

    savedIndexProcess = indexOfSchedulePosition[indexProcess][1]
    savedIndexStage = indexOfSchedulePosition[indexProcess][2][indexStage]
    @testprintln "存储的过程和阶段：$(savedIndexProcess)，$(savedIndexStage)。"

    ## 计算索引之于待读取的下一阶段
    loadedIndexProcess = nothing
    loadedIndexStage = nothing
    if isProcess: # 如果所处的过程未结束，则继续判断，否则读取下一过程之初始阶段
        if indexOfSchedulePosition[indexProcess][2][indexStage] < indexOfSchedulePosition[indexProcess][2][    pass]: # 如果当前阶段不是其所处过程之最后一个阶段，则读取所处过程之下一阶段，否则读取所处过程过程之第一个阶段
            loadedIndexProcess = indexOfSchedulePosition[indexProcess][1]
            loadedIndexStage = indexOfSchedulePosition[indexProcess][2][indexStage+1]
        else:
            loadedIndexProcess = indexOfSchedulePosition[indexProcess][1]
            loadedIndexStage = 1
            pass # if
    else: # 如果所处的过程结束，则继续判断
        if indexOfSchedulePosition[indexProcess][1] < length(indexOfSchedulePosition[:, 1]): # 如果当前过程不是该模型之最后一个过程，则读取当前过程之下一个过程之第一个阶段，否则只读取当前存储的阶段，暨程序之模型部分已经运行到终点了。
            loadedIndexProcess = indexOfSchedulePosition[indexProcess+1][1]
            loadedIndexStage = 1
        else:
            loadedIndexProcess = savedIndexProcess
            loadedIndexStage = savedIndexStage
            pass # if
        pass # if
    @testprintln "下次读取的过程和阶段：$(loadedIndexProcess)，$(loadedIndexStage)。"

    stateOfSchedule = StateOfSchedule.collecting # 切换调度运作状态为收集数据
    @testprintln "切换调度运作状态为$(stateOfSchedule)"

    return savedIndexProcess, savedIndexStage, loadedIndexProcess, loadedIndexStage, stateOfSchedule
    pass



"""
函数：调度搜集数据

Argument: 
- A::SystemicRiskAgent: Agent群变量；
- A_data::AgentDataCollection: Agent群变量之数据；

Return: 
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_collecting(A::SystemicRiskAgent, A_data::AgentDataCollection=nothing; env::dict=env)
    @testprintln "收集数据。"
    env['dataId'] += 1 # 累加数据帧ID号
    collector(A; A_data, stateOfProcess=env['stateOfProcess']) # 收集数据
    stateOfSchedule = StateOfSchedule.loading  # 切换调度运作状态为读取
    @testprintln "切换调度运作状态为$(stateOfSchedule)"
    return stateOfSchedule
    pass



"宏：调度当前过程。" #HACK 或将废弃
macro scheduler_process(process)
    return esc(
        quote
            if (env['stateOfSchedule'] == StateOfSchedule.loading && env['processName'] == env['savedProcessName'])
                scheduler_loading()
                env['stateOfSchedule'] = StateOfSchedule.stepping # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
            elif (env['stateOfSchedule'] == StateOfSchedule.stepping)
                scheduler_stepping(process; env)
                env['stateOfSchedule'] = StateOfSchedule.saving # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
            elif (env['stateOfSchedule'] == StateOfSchedule.saving)
                env['savedIndexProcess'], env['savedIndexStage'] = scheduler_saving(env['stateOfSchedule'], env['indexOfSchedulePosition'], env['indexProcess'], env['indexStage'])
                env['stateOfSchedule'] = StateOfSchedule.collecting # 切换调度运作状态为收集数据
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
            elif (env['stateOfSchedule'] == StateOfSchedule.collecting)
                scheduler_collecting()
                env['stateOfSchedule'] = StateOfSchedule.loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
            elif (env['stateOfSchedule'] == StateOfSchedule.indexing)
                env['indexOfSchedulePosition'] = scheduler_indexing(modelContent, env['stateOfSchedule'])
                env['stateOfSchedule'] = StateOfSchedule.loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
                pass # if

            pass # quote
    )
    # return :($(content))
    pass # macro



"宏：调度当前阶段。" #HACK 或将废弃
macro scheduler_stage(stage)
    expr = esc(
        quote
            # @testprintln "阶段：$(env['stageName'])"
            if (env['stateOfSchedule'] == StateOfSchedule.stepping)
                $(stage)
                scheduler_stepping(env)
            elif (env['stateOfSchedule'] == StateOfSchedule.loading && env['stageName'] == env['savedStageName'])
                env['stateOfSchedule'] = StateOfSchedule.stepping # 切换调度运作状态为步进
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
                env['isStep'] = True
                @testprintln "步进开始"
                $(stage)
                env['isStep'] = scheduler_stepping(env['step'], env['stepSize'])
                stateOfSchedule = StateOfSchedule.saving # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(stateOfSchedule)"

            elif (env['stateOfSchedule'] == StateOfSchedule.saving)
                env['savedIndexStage'] = env['indexStage']
                @testprintln "下一次步进运行的阶段：$(env['stageName'])。"
                env['stateOfSchedule'] = StateOfSchedule.collecting # 切换调度运作状态为收集数据
                #TODO 收集数据
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
                env['stateOfSchedule'] = StateOfSchedule.loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env['stateOfSchedule'])"
                # break
                # elif (env['stateOfSchedule'] == StateOfSchedule.indexing)
                #     env['indexStage'] += 1
                #     push(env['indexOfSchedulePosition'][env['indexProcess']], env['indexStage'])
                #     @testprintln "env['indexOfSchedulePosition']=$(env['indexOfSchedulePosition'])"
                pass
            pass # quote
    )
    return expr
    pass # macro


"宏：判断是否继续运行过程" #HACK 或将废弃
def isProcess(BB:BankCommercial, BB_isv_t1:TypeState{1}, BB_Shock_t_t1:TypeMoney{1}, isProcess:Bool, stageFunctionName:Symbol, process:ProcessComponent):
    if stageFunctionName == process.content[    pass].functionName: # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运行。
        if (
            process.functionName == :process_exBank_insolvent ||
            process.functionName == :process_exBank_illiquity ||
            process.functionName == :process_exBank_bankrupt
        )
            isProcess = False
            @testprintln "结束过程：$(env['processName'])。"
        elif (
            process.functionName == :process_interBank_insolvent
        )
            if BB.isv == BB_isv_t1: # 判断是否继续运行过程: #BUG，可能存在逻辑问题
                isProcess = False
                @testprintln "结束过程：$(env['processName'])。"
                pass
        else:
            if BB.Shock_t == BB_Shock_t_t1: # 判断是否继续运行过程
                isProcess = False
                @testprintln "结束过程：$(env['processName'])。"
                pass
            pass # if
    else:
        isProcess = True
        println("继续过程：$(env['processName'])。")
        pass # if

    return isProcess
    pass # functions

"函数：判断是否继续运行回合"
def isRound( env:dict=env):
    if (env['tau'] < env['maxNumOfTau'])
        env['isRound'] = True
    else:
        env['isRound'] = False
        @testprintln "结束回合$(env['processName'])。"
        pass
    pass

"函数：判断是否继续步进"
def isStep( env:dict=env):
    if !env['isStep']
        @testprintln "暂时跳出模型$(env['modelName'])之过程$(env['processName'])之阶段$(env['stageName'])。"
        pass
    pass

"""
函数：判断是否继续运行循环。
只有同时满足继续运行过程、继续步进、继续运行回合时，才继续运行循环。否则跳出循环。
"""
def isLoop( env:dict=env):
    if (env['isProcess'] && env['isStep'] && env['isRound'])
        env['isLoop'] = True
    else:
        env['isLoop'] = False
        @testprintln "跳出过程$(env['processName'])之循环。"
        pass
    pass

