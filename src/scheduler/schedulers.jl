"调度器"

## 调度器

##########################################
#状态/开发
##########################################

"#TODO宏：调度当前模型"
macro scheduler_model(model, process::String)



end

"#NOW宏：调度当前过程"
macro scheduler_process(process)
    return esc(
        quote
            if (env[:stateOfProcessStep] == :stepping)
                $(process)
            elseif (env[:stateOfProcessStep] == :loading && env[:processName] == env[:savedProcessName])
                $(process)
            elseif (env[:stateOfProcessStep] == :saving)
                env[:savedProcessName] = env[:processName]
                @test println("下一次步进运行的过程：$(env[:processName])。")
                env[:stateOfProcessStep] = :collecting # 切换过程运作状态为收集数据 #TODO 收集数据
                @test println("切换过程运作状态为collecting")
                env[:stateOfProcessStep] = :loading  # 切换过程运作状态为读取
                @test println("切换过程运作状态为loading")
            elseif (env[:stateOfProcessStep] == :indexing)
                pos_process += 1
                append!(env[:indexOfSchedulePosition], [[]])
            end
        end # quote
    )
    # return :($(content))
end # macro



"#NOW宏：调度当前阶段"
macro scheduler_stage(stage)
    expr = esc(
        quote
            # @test println("阶段：$(env[:stageName])")
            if (env[:stateOfStageStep] == :stepping)
                $(stage)
                isAltToSavingState!(env)
            elseif (env[:stateOfStageStep] == :loading && env[:stageName] == env[:savedStageName])
                env[:stateOfStageStep] = :stepping # 切换阶段运作状态为步进
                @test println("切换阶段运作状态为stepping")
                env[:isStep] = true
                @test println("步进开始：")
                $(stage)
                isAltToSavingState!(env)
            elseif (env[:stateOfStageStep] == :saving)
                env[:savedStageName] = env[:stageName]
                @test println("下一次步进运行的阶段：$(env[:stageName])。")
                env[:stateOfStageStep] = :collecting # 切换阶段运作状态为收集数据 #TODO 收集数据
                @test println("切换阶段运作状态为collecting")
                env[:stateOfStageStep] = :loading  # 切换阶段运作状态为读取
                @test println("切换阶段运作状态为loading")
                # break
            elseif (env[:stateOfStageStep] == :indexing)
                pos_stage += 1
                push!(env[:indexOfSchedulePosition][pos_process], pos_stage)
            end
        end # quote
    )
    return expr
end # macro



"函数：判断是否步进结束"
function isAltToSavingState!(env::Dict)
    env[:step] += 1
    if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
        env[:isStep] = false
        @test println("步进结束。")
        env[:stateOfStageStep] = :saving # 切换阶段运作状态为存储
        @test println("切换阶段运作状态为saving")
        env[:stateOfProcessStep] = :saving # 切换过程运作状态为存储
        @test println("切换过程运作状态为saving")
    end
end

"函数：判断是否结束循环"
function isEndLoop!(env::Dict)
    if (!env[:isProcess] || env[:tau] >= env[:maxNumOfTau])
        env[:isLoop] = false
        env[:isRound] = false
        @test println("结束过程：$(env[:processName])。\n")
    end
end

"函数：判断是否跳出过程"
function isJumpOutProcess!(env::Dict)
    if !env[:isStep]
        env[:isLoop] = false
        @test println("跳出过程：$(env[:processName])。\n")
    end
end
