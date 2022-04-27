"调度器"

## 调度器

##########################################
#状态/开发
##########################################


"""
#NOW函数：调度器

Argument: 
- modelContent::ModelContent: 被调度的模型内容；
- env::Dict: 环境变量；

Return: 
- env::Dict: 环境变量；
"""
function scheduler!(env::Dict)#= component::Union{ModelComponent,ProcessComponent},  =#
    if env[:stateOfSchedule] == :loading
        env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule] = scheduler_loading(env[:indexOfSchedulePosition], env[:indexProcess], env[:savedIndexProcess]) # 读取
    end
    if env[:stateOfSchedule] == :stepping
        env[:step], env[:isStep], env[:stateOfSchedule] = scheduler_stepping(env[:step], env[:stepSize]) # 步进
    end
    if env[:stateOfSchedule] == :saving
        env[:savedIndexProcess], env[:savedIndexStage], env[:stateOfSchedule] = scheduler_saving(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage]) # 存储
    end
    if env[:stateOfSchedule] == :collecting
        env[:stateOfSchedule] = scheduler_collecting() #TODO 收集数据
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
    # for (i, _) in enumerate(model.content.listProcessContent)
    for i in 1:length(model.content)
        append!(indexOfSchedulePosition, [[i, []]])
        # @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
        # for (j, _) in eval(Meta.parse("enumerate(model.content.listStage)"))
        for j in 1:length(model.content[i].content)
            push!(indexOfSchedulePosition[i][2], j)
            # @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
        end
    end
    @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
    stateOfSchedule = :loading
    @test println("切换调度运作状态为saving")
    return indexOfSchedulePosition, stateOfSchedule
end


"""
函数：调度读取
Argument: 
- indexOfSchedulePosition::Int: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- savedIndexProcess::Int: 存储的过程之位置；
Return: 
- loadedIndexProcess::Int: 读取的过程之位置；
- loadedIndexStage::Int: 读取的阶段之位置；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_loading(indexOfSchedulePosition::Vector{Any}, indexProcess::Int, savedIndexProcess::Int)
    if indexProcess == savedIndexProcess
        if length(indexOfSchedulePosition[:, 1]) <= indexOfSchedulePosition[indexProcess+1][1] # 如果当前过程不是该模型之最后一个过程
            if length(indexOfSchedulePosition[indexProcess][1]) <= indexOfSchedulePosition[indexProcess][indexStage+1][1]
                loadedIndexProcess = indexOfSchedulePosition[indexProcess][1]
                loadedIndexStage = indexOfSchedulePosition[indexProcess][2][indexStage]
                @test print("读取的过程：$(loadedIndexProcess)，读取的阶段：$(loadedIndexStage)。\n")
            else
                loadedIndexProcess = indexOfSchedulePosition[indexProcess+1][1]
                loadedIndexStage = 1
            end
        end
        stateOfSchedule = :stepping # 切换调度运作状态为步进
        @test println("切换调度运作状态为stepping")
    end
    return loadedIndexProcess, loadedIndexStage, stateOfSchedule
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
    if step % (stepSize + 1) == 0 # 是否完成本次步进
        isStep = false
        stateOfSchedule = :saving # 切换调度运作状态为存储
        @test println("步进停止。切换调度运作状态为saving")
    else
        isStep = true
        stateOfSchedule = :stepping
        @test println("步进继续：")
    end
    return step, isStep, stateOfSchedule
end


"""
函数：调度存储
Argument: 
- indexOfSchedulePosition::Int: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- indexStage::Int: 当前阶段之位置；
Return: 
- savedIndexProcess::Int: 存储的过程之位置；
- savedIndexStage::Int: 存储的阶段之位置；；
- stateOfSchedule::Symbol: 调度状态；
"""
function scheduler_saving(indexOfSchedulePosition::Vector{Any}, indexProcess::Int, indexStage::Int)

    savedIndexProcess = indexOfSchedulePosition[indexProcess][1]
    savedIndexStage = indexOfSchedulePosition[indexProcess][2][indexStage]
    @test println("存储的过程：$(savedIndexProcess)，存储的阶段：$(savedIndexStage)。")
    stateOfSchedule = :collecting # 切换调度运作状态为收集数据
    @test println("切换调度运作状态为collecting")

    return savedIndexProcess, savedIndexStage, stateOfSchedule
end



"""
#NOW函数：调度搜集数据
Argument: 

Return: 
- stateOfSchedule::Symbol: 调度状态；
"""

function scheduler_collecting()
    #TODO 收集数据        
    @test println("收集数据。")

    stateOfSchedule = :loading  # 切换调度运作状态为读取
    @test println("切换调度运作状态为loading")
    return stateOfSchedule
end



"#宏：调度当前过程。" #HACK 或将废弃
macro scheduler_process(process)
    return esc(
        quote
            if (env[:stateOfSchedule] == :loading && env[:processName] == env[:savedProcessName])
                scheduler_loading()
                env[:stateOfSchedule] = :stepping # 切换调度运作状态为存储
                @test println("切换调度运作状态为stepping")
            elseif (env[:stateOfSchedule] == :stepping)
                scheduler_stepping(process; env)
                env[:stateOfSchedule] = :saving # 切换调度运作状态为存储
                @test println("切换调度运作状态为saving")
            elseif (env[:stateOfSchedule] == :saving)
                env[:savedIndexProcess], env[:savedIndexStage] = scheduler_saving(env[:stateOfSchedule], env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage])
                env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
                @test println("切换调度运作状态为collecting")
            elseif (env[:stateOfSchedule] == :collecting)
                scheduler_collecting()
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @test println("切换调度运作状态为loading")
            elseif (env[:stateOfSchedule] == :indexing)
                env[:indexOfSchedulePosition] = scheduler_indexing(modelContent, env[:stateOfSchedule])
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @test println("切换调度运作状态为loading")
            end # if

        end # quote
    )
    # return :($(content))
end # macro



"#宏：调度当前阶段。" #HACK 或将废弃
macro scheduler_stage(stage)
    expr = esc(
        quote
            # @test println("阶段：$(env[:stageName])")
            if (env[:stateOfSchedule] == :stepping)
                $(stage)
                scheduler_stepping(env)
            elseif (env[:stateOfSchedule] == :loading && env[:stageName] == env[:savedStageName])
                env[:stateOfSchedule] = :stepping # 切换调度运作状态为步进
                @test println("切换调度运作状态为stepping")
                env[:isStep] = true
                @test println("步进开始")
                $(stage)
                env[:isStep] = scheduler_stepping(env[:step], env[:stepSize])
                stateOfSchedule = :saving # 切换调度运作状态为存储
                @test println("切换调度运作状态为saving")

            elseif (env[:stateOfSchedule] == :saving)
                env[:savedIndexStage] = env[:indexStage]
                @test println("下一次步进运行的阶段：$(env[:stageName])。")
                env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
                #TODO 收集数据
                @test println("切换调度运作状态为collecting")
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @test println("切换调度运作状态为loading")
                # break
                # elseif (env[:stateOfSchedule] == :indexing)
                #     env[:indexStage] += 1
                #     push!(env[:indexOfSchedulePosition][env[:indexProcess]], env[:indexStage])
                #     @test println("env[:indexOfSchedulePosition]=$(env[:indexOfSchedulePosition])")
            end
        end # quote
    )
    return expr
end # macro


"宏：判断是否结束过程"
function isProcess!(condition01, condition02)
    if condition01 == condition02 # 判断是否结束过程
        env[:isProcess] = false
    end
end

"函数：判断是否继续运行回合"
function isRound!(env::Dict)
    if (env[:tau] < env[:maxNumOfTau])
        env[:isRound] = true
    else
        env[:isRound] = false
        @test println("结束回合：$(env[:processName])。\n")
    end
end

"函数：判断是否继续步进"
function isStep!(env::Dict)
    if !env[:isStep]
        @test println("暂时跳出模型：$(env[:modelName])之过程：$(env[:processName])之阶段：$(env[:stageName])。\n")
    end
end

"函数：判断是否继续运行循环"
function isLoop!(env::Dict)
    if (env[:stateOfSchedule] == :stepping && env[:isProcess] && env[:isStep] && env[:isRound])
        env[:isLoop] = true
    else
        env[:isLoop] = false
        @test println("跳出循环：$(env[:processName])。\n")
    end
end

