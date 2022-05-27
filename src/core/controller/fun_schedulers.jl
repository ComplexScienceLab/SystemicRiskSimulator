"调度器"

## 调度器

##########################################
#状态/开发
##########################################


"""
函数：调度器 #HACK 或将废弃

Argument: 
- modelContent::ModelContent: 被调度的模型内容；
- env::Dict: 环境变量；

Return: 
- env::Dict: 环境变量；
"""
function scheduler!(env::Dict, A::SystemicRiskAgent, A_data::AgentDataCollection)#= component::Union{ModelComponent,ProcessComponent},  =#
    if env[:stateOfSchedule] == :loading
        env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule] = scheduler_loading(env[:indexOfSchedulePosition], env[:indexProcess], env[:savedIndexProcess], env[:stateOfSchedule]) # 读取
    end
    if env[:stateOfSchedule] == :stepping
        env[:step], env[:isStep], env[:stateOfSchedule] = scheduler_stepping(env[:step], env[:stepSize]) # 步进
    end
    if env[:stateOfSchedule] == :saving
        env[:savedIndexProcess], env[:savedIndexStage], env[:stateOfSchedule] = scheduler_saving(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage]) # 存储
    end
    if env[:stateOfSchedule] == :collecting
        env[:stateOfSchedule] = scheduler_collecting(A, A_data)
    end
    # if (stateOfSchedule == :indexing) #HACK 冗余
    #     env[:indexOfSchedulePosition], env[:stateOfSchedule] = scheduler_indexing(component) # 索引
    # end
end # function


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
        append!(indexOfSchedulePosition, [[i, []]])
        for j in 1:length(model.content[i].content)
            push!(indexOfSchedulePosition[i][2], j)
        end
    end
    @testprintln "索引完成。值为：$(indexOfSchedulePosition)"
    stateOfSchedule = :saving
    @testprintln "切换调度运作状态为$(stateOfSchedule)"
    return indexOfSchedulePosition, stateOfSchedule
end


"""
函数：调度读取
TODO Argument: 
- indexOfSchedulePosition::Int: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- savedIndexProcess::Int: 存储的过程之位置；
TODO Return: 
- loadedIndexProcess::Int: 读取的过程之位置；
- loadedIndexStage::Int: 读取的阶段之位置；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_loading(indexOfSchedulePosition::Vector{Any}, indexProcess::Int, indexStage::Int, loadedIndexProcess::Int, loadedIndexStage::Int, stateOfSchedule::Symbol)
    @testprintln "调度读取中……"
    newStateOfSchedule = stateOfSchedule
    if (indexProcess == loadedIndexProcess && indexStage == loadedIndexStage) # 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取
        if (!(indexOfSchedulePosition[indexProcess][1] == length(indexOfSchedulePosition[:, 1]) && indexOfSchedulePosition[indexProcess][2][indexStage] == length(indexOfSchedulePosition[indexProcess][2])) && isProcess == true) # 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运行过程，则继续读取，否则说明程序之模型部分已经运行到终点了，此时应停止读取，然后改状态为idle。
            newStateOfSchedule = :stepping # 切换调度运作状态为步进
        else
            newStateOfSchedule = :idle # 切换调度运作状态为待命
        end
        @testprintln "调度读取完毕。切换调度运作状态为$(newStateOfSchedule)。"
    end
    return newStateOfSchedule
end


# "函数：调度步进"
# function scheduler_stepping(process::Symbol, env::Dict=env, savedIndexProcess::Int)
#     $(process)
#     scheduler_altToSavingState!(env)
# end


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
    if step % stepSize == 0 # 是否完成本次步进
        isStep = false
        stateOfSchedule = :saving # 切换调度运作状态为存储
        @testprintln "步进停止。切换调度运作状态为saving"
    else
        isStep = true
        stateOfSchedule = :stepping
        @testprintln "步进继续："
    end
    return step, isStep, stateOfSchedule
end


"""
函数：调度存储
TODO Argument: 
- indexOfSchedulePosition::Int: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- indexStage::Int: 当前阶段之位置；
TODO Return: 
- savedIndexProcess::Int: 存储的过程之位置；
- savedIndexStage::Int: 存储的阶段之位置；；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_saving(indexOfSchedulePosition::Vector{Any}, indexProcess::Int, indexStage::Int, isProcess::Bool)

    savedIndexProcess = indexOfSchedulePosition[indexProcess][1]
    savedIndexStage = indexOfSchedulePosition[indexProcess][2][indexStage]
    @testprintln "存储的过程和阶段：$(savedIndexProcess)，$(savedIndexStage)。"

    ## 计算索引之于待读取的下一阶段
    loadedIndexProcess = nothing
    loadedIndexStage = nothing
    if isProcess # 如果所处的过程未结束，则继续判断，否则读取下一过程之初始阶段
        if indexOfSchedulePosition[indexProcess][2][indexStage] < indexOfSchedulePosition[indexProcess][2][end] # 如果当前阶段不是其所处过程之最后一个阶段，则读取所处过程之下一阶段，否则读取所处过程过程之第一个阶段
            loadedIndexProcess = indexOfSchedulePosition[indexProcess][1]
            loadedIndexStage = indexOfSchedulePosition[indexProcess][2][indexStage+1]
        else
            loadedIndexProcess = indexOfSchedulePosition[indexProcess][1]
            loadedIndexStage = 1
        end # if
    else # 如果所处的过程结束，则继续判断
        if indexOfSchedulePosition[indexProcess][1] < length(indexOfSchedulePosition[:, 1]) # 如果当前过程不是该模型之最后一个过程，则读取当前过程之下一个过程之第一个阶段，否则只读取当前存储的阶段，暨程序之模型部分已经运行到终点了。
            loadedIndexProcess = indexOfSchedulePosition[indexProcess+1][1]
            loadedIndexStage = 1
        else
            loadedIndexProcess = savedIndexProcess
            loadedIndexStage = savedIndexStage
        end # if
    end # if
    @testprintln "下次读取的过程和阶段：$(loadedIndexProcess)，$(loadedIndexStage)。"

    stateOfSchedule = :collecting # 切换调度运作状态为收集数据
    @testprintln "切换调度运作状态为$(stateOfSchedule)"

    return savedIndexProcess, savedIndexStage, loadedIndexProcess, loadedIndexStage, stateOfSchedule
end



"""
TODO 函数：调度搜集数据
Argument: 

Return: 
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_collecting(A::SystemicRiskAgent, A_data::AgentDataCollection=nothing; env::Dict=env)
    @testprintln "收集数据。"
    env[:dataId] += 1 # 累加数据帧ID号
    collector(A; A_data, stateOfProcess=env[:stateOfProcess]) # 收集数据
    stateOfSchedule = :loading  # 切换调度运作状态为读取
    @testprintln "切换调度运作状态为$(stateOfSchedule)"
    return stateOfSchedule
end



"宏：调度当前过程。" #HACK 或将废弃
macro scheduler_process(process)
    return esc(
        quote
            if (env[:stateOfSchedule] == :loading && env[:processName] == env[:savedProcessName])
                scheduler_loading()
                env[:stateOfSchedule] = :stepping # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
            elseif (env[:stateOfSchedule] == :stepping)
                scheduler_stepping(process; env)
                env[:stateOfSchedule] = :saving # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
            elseif (env[:stateOfSchedule] == :saving)
                env[:savedIndexProcess], env[:savedIndexStage] = scheduler_saving(env[:stateOfSchedule], env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage])
                env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
            elseif (env[:stateOfSchedule] == :collecting)
                scheduler_collecting()
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
            elseif (env[:stateOfSchedule] == :indexing)
                env[:indexOfSchedulePosition] = scheduler_indexing(modelContent, env[:stateOfSchedule])
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
            end # if

        end # quote
    )
    # return :($(content))
end # macro



"宏：调度当前阶段。" #HACK 或将废弃
macro scheduler_stage(stage)
    expr = esc(
        quote
            # @testprintln "阶段：$(env[:stageName])"
            if (env[:stateOfSchedule] == :stepping)
                $(stage)
                scheduler_stepping(env)
            elseif (env[:stateOfSchedule] == :loading && env[:stageName] == env[:savedStageName])
                env[:stateOfSchedule] = :stepping # 切换调度运作状态为步进
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
                env[:isStep] = true
                @testprintln "步进开始"
                $(stage)
                env[:isStep] = scheduler_stepping(env[:step], env[:stepSize])
                stateOfSchedule = :saving # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(stateOfSchedule)"

            elseif (env[:stateOfSchedule] == :saving)
                env[:savedIndexStage] = env[:indexStage]
                @testprintln "下一次步进运行的阶段：$(env[:stageName])。"
                env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
                #TODO 收集数据
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env[:stateOfSchedule])"
                # break
                # elseif (env[:stateOfSchedule] == :indexing)
                #     env[:indexStage] += 1
                #     push!(env[:indexOfSchedulePosition][env[:indexProcess]], env[:indexStage])
                #     @testprintln "env[:indexOfSchedulePosition]=$(env[:indexOfSchedulePosition])"
            end
        end # quote
    )
    return expr
end # macro


"#TODO宏：判断是否继续运行过程"
function isProcess!(BB::BankCommercial, BB_isv_t1::TypeState{1}, BB_Shock_t_t1::TypeMoney{1}, isProcess::Bool, stageFunctionName::Symbol, process::ProcessComponent)
    if stageFunctionName == process.content[end].functionName # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运行。
        if (
            process.functionName == :process_exBank_insolvent ||
            process.functionName == :process_exBank_illiquity ||
            process.functionName == :process_exBank_bankrupt
        )
            isProcess = false
            @testprintln "结束过程：$(env[:processName])。"
        elseif (
            process.functionName == :process_interBank_insolvent
        )
            if BB.isv == BB_isv_t1 # 判断是否继续运行过程 #BUG，可能存在逻辑问题
                isProcess = false
                @testprintln "结束过程：$(env[:processName])。"
            end
        else
            if BB.Shock_t == BB_Shock_t_t1 # 判断是否继续运行过程
                isProcess = false
                @testprintln "结束过程：$(env[:processName])。"
            end
        end # if
    else
        isProcess = true
        println("继续过程：$(env[:processName])。")
    end # if

    return isProcess
end # function

"#TODO函数：判断是否继续运行回合"
function isRound!(env::Dict)
    if (env[:tau] < env[:maxNumOfTau])
        env[:isRound] = true
    else
        env[:isRound] = false
        @testprintln "结束回合$(env[:processName])。"
    end
end

"#TODO函数：判断是否继续步进"
function isStep!(env::Dict)
    if !env[:isStep]
        @testprintln "暂时跳出模型$(env[:modelName])之过程$(env[:processName])之阶段$(env[:stageName])。"
    end
end

"""
TODO函数：判断是否继续运行循环。
只有同时满足继续运行过程、继续步进、继续运行回合时，才继续运行循环。否则跳出循环。
"""
function isLoop!(env::Dict)
    if (env[:isProcess] && env[:isStep] && env[:isRound])
        env[:isLoop] = true
    else
        env[:isLoop] = false
        @testprintln "跳出过程$(env[:processName])之循环。"
    end
end

