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
    if env[:state_of_schedule] == :loading
        env[:loaded_index_process], env[:loaded_index_stage], env[:state_of_schedule] = scheduler_loading(env[:index_of_schedule_position], env[:index_process], env[:saved_index_process], env[:state_of_schedule]) # 读取
    end
    if env[:state_of_schedule] == :stepping
        env[:step], env[:is_step], env[:state_of_schedule] = scheduler_stepping(env[:step], env[:step_size]) # 步进
    end
    if env[:state_of_schedule] == :saving
        env[:saved_index_process], env[:saved_index_stage], env[:state_of_schedule] = scheduler_saving(env[:index_of_schedule_position], env[:index_process], env[:index_stage]) # 存储
    end
    if env[:state_of_schedule] == :collecting
        env[:state_of_schedule] = scheduler_collecting(A, A_data)
    end
    # if (state_of_schedule == :indexing) #HACK 冗余
    #     env[:index_of_schedule_position], env[:state_of_schedule] = scheduler_indexing(component) # 索引
    # end
end # function


"""
函数：调度索引

Argument: 
- model::ModelContent: 被调度的模型内容；

Return: 
- index_of_schedule_position::Array 调度位置索引列表；
- state_of_schedule::Symbol: 调度状态；
"""
function scheduler_indexing(model::ModelComponent)
    index_of_schedule_position = []
    for i in 1:length(model.content)
        append!(index_of_schedule_position, [[i, []]])
        for j in 1:length(model.content[i].content)
            push!(index_of_schedule_position[i][2], j)
        end
    end
    @testprintln "索引完成。值为：$(index_of_schedule_position)"
    state_of_schedule = :saving
    @testprintln "切换调度运作状态为$(state_of_schedule)"
    return index_of_schedule_position, state_of_schedule
end


"""
函数：调度读取

Argument: 
- index_of_schedule_position::Vector{Any}: 调度位置索引列表；
- index_process::Int: 当前过程之位置；
- index_stage::Int: 当前阶段之位置；
- loadedIndexProcess::Int: 读取的过程之位置；
- loadedIndexStage::Int: 读取的阶段之位置；
- state_of_schedule::Symbol: 调度状态；

Return: 
- newStateOfSchedule::Symbol: 新的调度状态；
"""
function scheduler_loading(index_of_schedule_position::Vector{Any}, index_process::Int, index_stage::Int, loadedIndexProcess::Int, loadedIndexStage::Int, state_of_schedule::Symbol)
    @testprintln "调度读取中……"
    newStateOfSchedule = state_of_schedule
    if (index_process == loadedIndexProcess && index_stage == loadedIndexStage) # 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取
        if (!(index_of_schedule_position[index_process][1] == length(index_of_schedule_position[:, 1]) && index_of_schedule_position[index_process][2][index_stage] == length(index_of_schedule_position[index_process][2])) && is_process == true) # 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运行过程，则继续读取，否则说明程序之模型部分已经运行到终点了，此时应停止读取，然后改状态为idle。
            newStateOfSchedule = :stepping # 切换调度运作状态为步进
        else
            newStateOfSchedule = :idle # 切换调度运作状态为待命
        end
        @testprintln "调度读取完毕。切换调度运作状态为$(newStateOfSchedule)。"
    end
    return newStateOfSchedule
end


# "函数：调度步进"
# function scheduler_stepping(process::Symbol, env::Dict=env, saved_index_process::Int)
#     $(process)
#     scheduler_altToSavingState!(env)
# end


"""
函数：调度步进

Argument: 
- step::Int: 步进步数；
- step_size::Int: 步进尺寸；

Return: 
- is_step::Bool: 是否步进；
- state_of_schedule::Symbol: 调度状态；
"""
function scheduler_stepping(step::Int, step_size::Int)
    step += 1
    if step % step_size == 0 # 是否完成本次步进
        is_step = false
        state_of_schedule = :saving # 切换调度运作状态为存储
        @testprintln "步进停止。切换调度运作状态为saving"
    else
        is_step = true
        state_of_schedule = :stepping
        @testprintln "步进继续："
    end
    return step, is_step, state_of_schedule
end


"""
函数：调度存储

Argument: 
- index_of_schedule_position::Vector{Any}: 调度位置索引列表；
- index_process::Int: 当前过程之位置；
- index_stage::Int: 当前阶段之位置；
- is_process::Bool: 是否在过程状态中；

Return: 
- saved_index_process::Int: 存储的过程之位置；
- saved_index_stage::Int: 存储的阶段之位置；
- loadedIndexProcess::Int: 读取的过程之位置；
- loadedIndexStage::Int: 读取的阶段之位置；
- state_of_schedule::Symbol: 调度状态；
"""
function scheduler_saving(index_of_schedule_position::Vector{Any}, index_process::Int, index_stage::Int, is_process::Bool)

    saved_index_process = index_of_schedule_position[index_process][1]
    saved_index_stage = index_of_schedule_position[index_process][2][index_stage]
    @testprintln "存储的过程和阶段：$(saved_index_process)，$(saved_index_stage)。"

    ## 计算索引之于待读取的下一阶段
    loadedIndexProcess = nothing
    loadedIndexStage = nothing
    if is_process # 如果所处的过程未结束，则继续判断，否则读取下一过程之初始阶段
        if index_of_schedule_position[index_process][2][index_stage] < index_of_schedule_position[index_process][2][end] # 如果当前阶段不是其所处过程之最后一个阶段，则读取所处过程之下一阶段，否则读取所处过程过程之第一个阶段
            loadedIndexProcess = index_of_schedule_position[index_process][1]
            loadedIndexStage = index_of_schedule_position[index_process][2][index_stage+1]
        else
            loadedIndexProcess = index_of_schedule_position[index_process][1]
            loadedIndexStage = 1
        end # if
    else # 如果所处的过程结束，则继续判断
        if index_of_schedule_position[index_process][1] < length(index_of_schedule_position[:, 1]) # 如果当前过程不是该模型之最后一个过程，则读取当前过程之下一个过程之第一个阶段，否则只读取当前存储的阶段，暨程序之模型部分已经运行到终点了。
            loadedIndexProcess = index_of_schedule_position[index_process+1][1]
            loadedIndexStage = 1
        else
            loadedIndexProcess = saved_index_process
            loadedIndexStage = saved_index_stage
        end # if
    end # if
    @testprintln "下次读取的过程和阶段：$(loadedIndexProcess)，$(loadedIndexStage)。"

    state_of_schedule = :collecting # 切换调度运作状态为收集数据
    @testprintln "切换调度运作状态为$(state_of_schedule)"

    return saved_index_process, saved_index_stage, loadedIndexProcess, loadedIndexStage, state_of_schedule
end



"""
函数：调度搜集数据

Argument: 
- A::SystemicRiskAgent: Agent群变量；
- A_data::AgentDataCollection: Agent群变量之数据；

Return: 
- state_of_schedule::Symbol: 调度状态；
"""
function scheduler_collecting(A::SystemicRiskAgent, A_data::AgentDataCollection=nothing; env::Dict=env)
    @testprintln "收集数据。"
    env[:data_id] += 1 # 累加数据帧ID号
    collector(A; A_data, state_of_process=env[:state_of_process]) # 收集数据
    state_of_schedule = :loading  # 切换调度运作状态为读取
    @testprintln "切换调度运作状态为$(state_of_schedule)"
    return state_of_schedule
end



"宏：调度当前过程。" #HACK 或将废弃
macro scheduler_process(process)
    return esc(
        quote
            if (env[:state_of_schedule] == :loading && env[:process_name] == env[:saved_process_name])
                scheduler_loading()
                env[:state_of_schedule] = :stepping # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
            elseif (env[:state_of_schedule] == :stepping)
                scheduler_stepping(process; env)
                env[:state_of_schedule] = :saving # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
            elseif (env[:state_of_schedule] == :saving)
                env[:saved_index_process], env[:saved_index_stage] = scheduler_saving(env[:state_of_schedule], env[:index_of_schedule_position], env[:index_process], env[:index_stage])
                env[:state_of_schedule] = :collecting # 切换调度运作状态为收集数据
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
            elseif (env[:state_of_schedule] == :collecting)
                scheduler_collecting()
                env[:state_of_schedule] = :loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
            elseif (env[:state_of_schedule] == :indexing)
                env[:index_of_schedule_position] = scheduler_indexing(modelContent, env[:state_of_schedule])
                env[:state_of_schedule] = :loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
            end # if

        end # quote
    )
    # return :($(content))
end # macro



"宏：调度当前阶段。" #HACK 或将废弃
macro scheduler_stage(stage)
    expr = esc(
        quote
            # @testprintln "阶段：$(env[:stage_name])"
            if (env[:state_of_schedule] == :stepping)
                $(stage)
                scheduler_stepping(env)
            elseif (env[:state_of_schedule] == :loading && env[:stage_name] == env[:saved_stage_name])
                env[:state_of_schedule] = :stepping # 切换调度运作状态为步进
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
                env[:is_step] = true
                @testprintln "步进开始"
                $(stage)
                env[:is_step] = scheduler_stepping(env[:step], env[:step_size])
                state_of_schedule = :saving # 切换调度运作状态为存储
                @testprintln "切换调度运作状态为$(state_of_schedule)"

            elseif (env[:state_of_schedule] == :saving)
                env[:saved_index_stage] = env[:index_stage]
                @testprintln "下一次步进运行的阶段：$(env[:stage_name])。"
                env[:state_of_schedule] = :collecting # 切换调度运作状态为收集数据
                #TODO 收集数据
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
                env[:state_of_schedule] = :loading  # 切换调度运作状态为读取
                @testprintln "切换调度运作状态为$(env[:state_of_schedule])"
                # break
                # elseif (env[:state_of_schedule] == :indexing)
                #     env[:index_stage] += 1
                #     push!(env[:index_of_schedule_position][env[:index_process]], env[:index_stage])
                #     @testprintln "env[:index_of_schedule_position]=$(env[:index_of_schedule_position])"
            end
        end # quote
    )
    return expr
end # macro


"宏：判断是否继续运行过程" #HACK 或将废弃
function is_process!(BB::BankCommercial, BB_isv_t1::TypeState{1}, BB_Shock_t_t1::TypeMoney{1}, is_process::Bool, stageFunctionName::Symbol, process::ProcessComponent)
    if stageFunctionName == process.content[end].functionName # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运行。
        if (
            process.functionName == :process_exBank_insolvent ||
            process.functionName == :process_exBank_illiquity ||
            process.functionName == :process_exBank_bankrupt
        )
            is_process = false
            @testprintln "结束过程：$(env[:process_name])。"
        elseif (
            process.functionName == :process_interBank_insolvent
        )
            if BB.isv == BB_isv_t1 # 判断是否继续运行过程 #BUG，可能存在逻辑问题
                is_process = false
                @testprintln "结束过程：$(env[:process_name])。"
            end
        else
            if BB.Shock_t == BB_Shock_t_t1 # 判断是否继续运行过程
                is_process = false
                @testprintln "结束过程：$(env[:process_name])。"
            end
        end # if
    else
        is_process = true
        println("继续过程：$(env[:process_name])。")
    end # if

    return is_process
end # function

"函数：判断是否继续运行回合"
function is_round!(; env::Dict=env)
    if (env[:tau] < env[:max_num_of_tau])
        env[:is_round] = true
    else
        env[:is_round] = false
        @testprintln "结束回合$(env[:process_name])。"
    end
end

"函数：判断是否继续步进"
function is_step!(; env::Dict=env)
    if !env[:is_step]
        @testprintln "暂时跳出模型$(env[:model_name])之过程$(env[:process_name])之阶段$(env[:stage_name])。"
    end
end

"""
函数：判断是否继续运行循环。
只有同时满足继续运行过程、继续步进、继续运行回合时，才继续运行循环。否则跳出循环。
"""
function is_loop!(; env::Dict=env)
    if (env[:is_process] && env[:is_step] && env[:is_round])
        env[:is_loop] = true
    else
        env[:is_loop] = false
        @testprintln "跳出过程$(env[:process_name])之循环。"
    end
end

