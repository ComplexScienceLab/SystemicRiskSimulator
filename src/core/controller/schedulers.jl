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
function scheduler!(modelContent::ModelContent, env::Dict, process::Symbol, state::Symbol)
    if (env[:stateOfSchedule] == :loading)
        env[:stateOfSchedule] = scheduler_loading(env[:indexProcess], env[:savedIndexProcess])
    elseif (env[:stateOfSchedule] == :stepping)
        scheduler_stepping(process, env, env[:savedIndexProcess])
    elseif (env[:stateOfSchedule] == :saving)
        env[:savedIndexProcess], env[:savedIndexStage] = scheduler_saving(env[:stateOfSchedule], env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage])
        env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
        @test println("切换调度运作状态为collecting")
    elseif (env[:stateOfSchedule] == :collecting)
        scheduler_collecting()
        env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
        @test println("切换调度运作状态为loading")
        # elseif (env[:stateOfSchedule] == :indexing) #HACK 冗余。事实上实验开始就索引了模型。
        #     env[:indexOfSchedulePosition] = scheduler_indexing(modelContent, env[:stateOfSchedule])
        #     env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
        #     @test println("切换调度运作状态为loading")
    end # if
end


"""
函数：调度索引
Argument: 
- modelContent::ModelContent: 被调度的模型内容；
- stateOfSchedule::Symbol: 调度状态；
Return: 
- indexOfSchedulePosition::Array 调度位置索引列表；
"""
function scheduler_indexing(modelContent::ModelContent)
    indexOfSchedulePosition = []
    for (i, p) in enumerate(modelContent.listProcess)
        append!(indexOfSchedulePosition, [[]])
        @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
        for (j, s) in evel(Meta.parse("$(p).listStage"))
            push!(indexOfSchedulePosition[i], j)
            @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
        end
    end
    StateOfSchedule = :stepping
    @test println("切换调度运作状态为stepping")
    return indexOfSchedulePosition, StateOfSchedule
end


"#NOW函数：调度读取"
function scheduler_loading(indexProcess::Int, savedIndexProcess::Int)
    if indexProcess == savedIndexProcess
        stateOfSchedule = :stepping
        @test println("切换调度运作状态为stepping")
    end
    return stateOfSchedule
end


"#NOW函数：调度步进"
function scheduler_stepping(process::Symbol, env::Dict=env, savedIndexProcess::Int)
    $(process)
    scheduler_altToSavingState!(env)
    env[:stateOfSchedule] = :saving # 切换调度运作状态为存储
    @test println("切换调度运作状态为saving")
end



"""
函数：调度存储
Argument: 
- stateOfSchedule::Symbol: 调度状态；
- indexOfSchedulePosition::Int: 调度位置索引列表；
- indexProcess::Int: 当前过程之位置；
- indexStage::Int: 当前阶段之位置；
Return: 
- savedIndexProcess::Int: 存储的过程之位置；
- savedIndexStage::Int: 存储的阶段之位置；；
"""
function scheduler_saving(stateOfSchedule::Symbol, indexOfSchedulePosition::Int, indexProcess::Int, indexStage::Int)

    savedIndexProcess = indexOfSchedulePosition[indexProcess]
    @test println("已存储步进运行的过程：$(processName)。")
    savedIndexStage = indexOfSchedulePosition[indexProcess][indexStage]
    @test println("已存储步进运行的阶段：$(stageName)。")

    #NOW是否冗余？ if length(indexOfSchedulePosition) <= indexOfSchedulePosition[indexProcess+1]
    #     if length(indexOfSchedulePosition[indexProcess]) <= indexOfSchedulePosition[indexProcess][indexStage+1]
    #         savedIndexProcess = indexOfSchedulePosition[indexProcess]
    #         @test println("下一次步进运行的过程：$(processName)。")
    #         savedIndexStage = indexOfSchedulePosition[indexProcess][indexStage]
    #     else
    #         savedIndexProcess = indexOfSchedulePosition[indexProcess+1]
    #         savedIndexStage = 1
    #     end
    # end

    return savedIndexProcess, savedIndexStage
end



"#NOW函数：调度搜集数据"
function scheduler_collecting()
    #TODO 收集数据

end

"#NOW宏：调度当前过程。" #HACK 准备拆分为若干独立调度器函数
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



"#NOW宏：调度当前阶段。"
macro scheduler_stage(stage)
    expr = esc(
        quote
            # @test println("阶段：$(env[:stageName])")
            if (env[:stateOfSchedule] == :stepping)
                $(stage)
                scheduler_altToSavingState!(env)
            elseif (env[:stateOfSchedule] == :loading && env[:stageName] == env[:savedStageName])
                env[:stateOfSchedule] = :stepping # 切换调度运作状态为步进
                @test println("切换调度运作状态为stepping")
                env[:isStep] = true
                @test println("步进开始")
                $(stage)
                scheduler_altToSavingState!(env)
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



"函数：转换阶段状态为存储。"
function scheduler_altToSavingState!(env::Dict)
    env[:step] += 1
    if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
        env[:isStep] = false
        @test println("步进停止")
        env[:stateOfSchedule] = :saving # 切换调度运作状态为存储
        @test println("切换调度运作状态为saving")
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

"函数：判断是否继续运行回合"
function isRound!(env::Dict)
    if (env[:tau] >= env[:maxNumOfTau])
        env[:isRound] = true
    else
        env[:isRound] = false
        @test println("结束回合：$(env[:processName])。\n")
    end
end

"函数：判断是否跳出模型"
function isJumpOutModel!(env::Dict)
    if !env[:isStep]
        @test println("跳出模型之过程：$(env[:processName])之阶段：$(env[:stageName])。\n")
    end
end


