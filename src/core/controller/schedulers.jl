"调度器"

## 调度器

##########################################
#状态/开发
##########################################

# "#TODO宏：调度当前模型"
# macro scheduler_model(model, process::String)

#     env[:indexProcess] = 0 # 初始化过程所在位置

#     env[:tau] = 0 # 初始化回合

#     if (!env[:isModel])
#         if (env[:tau] > 0)
#             @test println("继续模型model：\n")
#         else
#             @test println("开始模型model：\n")
#         end
#     end
# for process in processes

# end
#     ## 过程：银行外部违约损失传染冲击 #BUG测试宏和函数正确性
#     env[:processName] = "银行外部违约损失传染冲击过程"
#     @scheduler_process BB, BI, env = process_exBank_insolvent!(BB, BI, para, env)

#     ## 过程：资不抵债银行间违约损失传染冲击
#     env[:processName] = "资不抵债银行间违约损失传染冲击过程"
#     @scheduler_process BB, BI, env = process_interBank_insolvent!(BB, BI, para, env)

#     ## 过程：外部挤兑流动传染冲击
#     @scheduler_process BB, BI, env = process_exBank_illiquity!(BB, BI, para, env)

#     ## 过程：流动性短缺银行间挤兑流动传染冲击
#     @scheduler_process BB, BI, env = process_interBank_illiquity!(BB, BI, para, env)

#     ## 过程：外生破产银行间挤兑流动传染冲击 #HACK暂时不用
#     # @run_process BB, BI, env = process_exBank_bankrupt!(BB, BI, para, env)

#     ## 过程：破产银行间挤兑流动传染冲击
#     @scheduler_process BB, BI, env = process_interBank_bankrupt!(BB, BI, para, env)


#     ## 收尾
#     # update_B_balanceSheet!(BB, BI,b,ib; byWay = "calc all E_all") # 更新计算各银行之所有者权益
#     # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
#     # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据
#     #TODO 最终破产清算

#     if !env[:isStep]
#         @test println("步进已结束，跳出model_BI1111。")
#     end

#     if env[:stateOfSchedule] == :standing
#         env[:isModel] = false
#         env[:isExperiment] = false
#     end

#     if (!env[:isModel] || !env[:isExperiment])
#         @test println("model_BI1111结束。")
#     end

#     return BB, BI, para, env
#     # return BB, BI, BB_tau, BI_tau, para, env

# end

"#NOW函数：调度器"
function scheduler()
    if (env[:stateOfSchedule] == :stepping)
        schedul_stepping()
    elseif (env[:stateOfSchedule] == :loading && env[:processName] == env[:savedProcessName])
        $(process)
    elseif (env[:stateOfSchedule] == :saving)
        if length(env[:indexOfSchedulePosition]) <= env[:indexOfSchedulePosition][env[:indexProcess]+1]
            if length(env[:indexOfSchedulePosition][env[:indexProcess]]) <= env[:indexOfSchedulePosition][env[:indexProcess]][env[:indexStage]+1]
                env[:savedIndexProcess] = env[:indexOfSchedulePosition][env[:indexProcess]]
                @test println("下一次步进运行的过程：$(env[:processName])。")
                env[:savedIndexStage] = env[:indexOfSchedulePosition][env[:indexProcess]][env[:indexStage]]
            else
                env[:savedIndexProcess] = env[:indexOfSchedulePosition][env[:indexProcess]+1]
                env[:savedIndexStage] = 1
            end
        end
        env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
        #TODO 收集数据
        @test println("切换调度运作状态为collecting")
        env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
        @test println("切换调度运作状态为loading")
        # elseif (env[:stateOfSchedule] == :indexing)
        #     env[:indexProcess] += 1
        #     append!(env[:indexOfSchedulePosition], [[]])
        #     @test println("env[:indexOfSchedulePosition]=$(env[:indexOfSchedulePosition])")
        #     $(process)
    end

end

"#NOW函数：调度索引"
function scheduler_indexing(model::Model, stateOfSchedule::Symbol)
    if stateOfSchedule == :indexing
        indexOfSchedulePosition = []
        for (i, p) in enumerate(model.listProcess)
            append!(indexOfSchedulePosition, [[]])
            @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
            for (j, s) in evel(Meta.parse("$(p).listStage"))
                push!(indexOfSchedulePosition[i], j)
                @test println("indexOfSchedulePosition=$(indexOfSchedulePosition)")
            end
        end
    end
    stateOfSchedule = :stepping
    return indexOfSchedulePosition, stateOfSchedule
end


"#NOW函数：调度步进"
function scheduler_stepping()
    
end



"#NOW函数：调度存储"
function scheduler_saving()
    if (env[:stateOfSchedule] == :saving)
        if length(env[:indexOfSchedulePosition]) <= env[:indexOfSchedulePosition][env[:indexProcess]+1]
            if length(env[:indexOfSchedulePosition][env[:indexProcess]]) <= env[:indexOfSchedulePosition][env[:indexProcess]][env[:indexStage]+1]
                env[:savedIndexProcess] = env[:indexOfSchedulePosition][env[:indexProcess]]
                @test println("下一次步进运行的过程：$(env[:processName])。")
                env[:savedIndexStage] = env[:indexOfSchedulePosition][env[:indexProcess]][env[:indexStage]]
            else
                env[:savedIndexProcess] = env[:indexOfSchedulePosition][env[:indexProcess]+1]
                env[:savedIndexStage] = 1
            end
        end
        env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
        #TODO 收集数据
        @test println("切换调度运作状态为collecting")
        env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
        @test println("切换调度运作状态为loading")
        # elseif (env[:stateOfSchedule] == :indexing)
        #     env[:indexProcess] += 1
        #     append!(env[:indexOfSchedulePosition], [[]])
        #     @test println("env[:indexOfSchedulePosition]=$(env[:indexOfSchedulePosition])")
        #     $(process)
    end
end

"#NOW函数：调度读取"
function scheduler_loading()
    
end

"#NOW函数：调度搜集数据"
function scheduler_collecting()
    
end

"#NOW宏：调度当前过程。" #HACK 准备拆分为若干独立调度器函数
macro scheduler_process(process)
    return esc(
        quote
            if (env[:stateOfSchedule] == :stepping)
                $(process)
            elseif (env[:stateOfSchedule] == :loading && env[:processName] == env[:savedProcessName])
                $(process)
            elseif (env[:stateOfSchedule] == :saving)
                if length(env[:indexOfSchedulePosition]) <= env[:indexOfSchedulePosition][env[:indexProcess]+1]
                    if length(env[:indexOfSchedulePosition][env[:indexProcess]]) <= env[:indexOfSchedulePosition][env[:indexProcess]][env[:indexStage]+1]
                        env[:savedIndexProcess] = env[:indexOfSchedulePosition][env[:indexProcess]]
                        @test println("下一次步进运行的过程：$(env[:processName])。")
                        env[:savedIndexStage] = env[:indexOfSchedulePosition][env[:indexProcess]][env[:indexStage]]
                    else
                        env[:savedIndexProcess] = env[:indexOfSchedulePosition][env[:indexProcess]+1]
                        env[:savedIndexStage] = 1
                    end
                end
                env[:stateOfSchedule] = :collecting # 切换调度运作状态为收集数据
                #TODO 收集数据
                @test println("切换调度运作状态为collecting")
                env[:stateOfSchedule] = :loading  # 切换调度运作状态为读取
                @test println("切换调度运作状态为loading")
                # elseif (env[:stateOfSchedule] == :indexing)
                #     env[:indexProcess] += 1
                #     append!(env[:indexOfSchedulePosition], [[]])
                #     @test println("env[:indexOfSchedulePosition]=$(env[:indexOfSchedulePosition])")
                #     $(process)
            end
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


