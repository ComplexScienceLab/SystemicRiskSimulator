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
    @testprintln "过程$(env[:index_process])：$(env[:process_name])"

    env[:index_stage] = 0 # 初始化阶段所在位置
    env[:is_step] = true # 初始化步进状态
    env[:is_round] = true # 初始化回合状态
    env[:is_process] = true # 初始化过程状态
    env[:is_loop] = true # 初始化循环状态
    while env[:is_loop] == true

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
            env[:index_stage] = idx_stage
            env[:stage_name] = Symbol(stage.functionName)
            @testprintln "阶段$(env[:index_stage])：$(env[:stage_name])"

            ## 调度并运行状态
            if env[:state_of_schedule] == :loading
                env[:state_of_schedule] = scheduler_loading(env[:index_of_schedule_position], env[:index_process], env[:index_stage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:state_of_schedule]) # 调度读取
            end
            if env[:state_of_schedule] == :stepping
                #=【插入表达式】=#
                env[:step], env[:is_step], env[:state_of_schedule] = scheduler_stepping(env[:step], env[:step_size]) # 步进
            end

            is_step!() # 判断是否继续运行步进
            if env[:is_step] == false # 如果步进停止，则跳出该循环
                break
            end
        end # for


        env[:is_process] = is_process!(A.BB, BB_isv_t1, BB_Shock_t_t1, env[:is_process], env[:stage_name], process) # 判断是否继续运行过程

        if env[:state_of_schedule] == :saving
            env[:saved_index_process], env[:saved_index_stage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:state_of_schedule] = scheduler_saving(env[:index_of_schedule_position], env[:index_process], env[:index_stage], env[:is_process]) # 调度存储
        end
        if (env[:state_of_schedule] == :collecting && env[:state_of_process] == :running)
            env[:state_of_schedule] = scheduler_collecting(A, A_data)
        end

        is_round!() # 判断是否继续运行回合
        is_loop!() # 判断是否继续运行循环
    end # while

    return A, para, env, A_data

end # function









