"函数：通用过程框架"

## 函数：通用过程框架

##########################################
#状态/开发
##########################################

"""
通用过程框架模板：

Argument: 
- A::SystemicRiskAgent: Agent群变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- process::ProcessComponent: 过程组件实例；
- A_data::AgentDataCollection: Agent群变量之数据；

Return:
- A::SystemicRiskAgent: Agent群变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- A_data::AgentDataCollection: Agent群变量之数据；
"""
function fun_process_skeleton_template!(A::SystemicRiskAgent, para::Dict, env::Dict, process::ProcessComponent, A_data::AgentDataCollection)
    @testprintln "过程$(env[:indexProcess])：$(env[:processName])"

    env[:indexStage] = 0 # 初始化阶段所在位置
    env[:isStep] = true # 初始化步进状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态
    env[:isLoop] = true # 初始化循环状态
    while env[:isLoop] == true

        ## 回合数变动
        if (env[:loadedIndexStage] != 1)
            @testprintln "\n继续回合：$(env[:tau])"
        else
            env[:tau] += 1 # 回合累加一
            @testprintln "\n开始回合：$(env[:tau])"
        end

        env[:tau] += 1 # 回合累加一
        @testprintln "开始回合$(env[:tau])："

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(A.BB.Shock_t)
        BB_isv_t1 = deepcopy(A.BB.isv)

        b = TypeState{1}(A.BB.on .|| A.BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((A.BB.on .|| A.BB.off) .&& (A.BB.on .|| A.BB.off)') # 临时设置BI示性变量

        ## 运行每一个阶段
        for (idx_stage, stage) in enumerate(process.content)
            env[:indexStage] = idx_stage
            env[:stageName] = Symbol(stage.functionName)
            @testprintln "阶段$(env[:indexStage])：$(env[:stageName])"

            ## 调度并运行状态
            if env[:stateOfSchedule] == :loading
                env[:stateOfSchedule] = scheduler_loading(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule]) # 调度读取
            end
            if env[:stateOfSchedule] == :stepping
                runStage!(A.BB, A.BI, b, ib, para, env, stage)
                env[:step], env[:isStep], env[:stateOfSchedule] = scheduler_stepping(env[:step], env[:stepSize]) # 步进
            end

            isStep!() # 判断是否继续运行步进
            if env[:isStep] == false # 如果步进停止，则跳出该循环
                break
            end
        end # for


        env[:isProcess] = isProcess!(A.BB, BB_isv_t1, BB_Shock_t_t1, env[:isProcess], env[:stageName], process) # 判断是否继续运行过程

        if env[:stateOfSchedule] == :saving
            env[:savedIndexProcess], env[:savedIndexStage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule] = scheduler_saving(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage], env[:isProcess]) # 调度存储
        end
        if (env[:stateOfSchedule] == :collecting && env[:stateOfProcess] == :running)
            env[:stateOfSchedule] = scheduler_collecting(A, A_data)
        end

        isRound!() # 判断是否继续运行回合
        isLoop!() # 判断是否继续运行循环
    end # while

    return A, para, env, A_data

end # function









