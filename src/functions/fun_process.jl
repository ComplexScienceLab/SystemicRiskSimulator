"函数区：运行过程"

## 函数区：运行过程

##########################################
#状态/开发
##########################################


"#NOW宏：运行当前过程"#HACK不好把握，还不能用
macro run_process(process)
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
            end
        end #quote
    )
    # return :($(content))
end # macro



"#TODO宏：运行当前阶段"#HACK不好把握，还不能用
macro run_stage(stage)
    expr = esc(
        quote
            # @test println("阶段：$(env[:stageName])")
            if (env[:stateOfStageStep] == :stepping || (env[:stateOfStageStep] == :loading && env[:stageName] == env[:savedStageName]))
                env[:isStep] = true
                @test println("步进开始：")
                env[:stateOfStageStep] = :stepping # 切换阶段运作状态为步进
                @test println("切换阶段运作状态为stepping")
                $(stage)
                env[:step] += 1
                if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
                    env[:isStep] = false
                    @test println("步进结束。")
                    env[:stateOfStageStep] = :saving # 切换阶段运作状态为存储
                    @test println("切换阶段运作状态为saving")
                    env[:stateOfProcessStep] = :saving # 切换过程运作状态为存储
                    @test println("切换过程运作状态为saving")
                end
            elseif (env[:stateOfStageStep] == :saving)
                env[:savedStageName] = env[:stageName]
                @test println("下一次步进运行的阶段：$(env[:stageName])。")
                env[:stateOfStageStep] = :collecting # 切换阶段运作状态为收集数据 #TODO 收集数据
                @test println("切换阶段运作状态为collecting")
                env[:stateOfStageStep] = :loading  # 切换阶段运作状态为读取
                @test println("切换阶段运作状态为loading")
                # break
            end
        end # quote
    )
    return expr
end # macro

