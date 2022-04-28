"函数：通用过程框架"

## 函数：通用过程框架

##########################################
#状态/开发
##########################################

"""
通用过程框架：

Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- processComponent::ProcessComponent: 过程组件实例；

Return:
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
"""
function fun_process_skeleton!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict, process::ProcessComponent)
    @test println("开始过程：$(env[:processName])：")

    env[:indexStage] = 0 # 初始化阶段所在位置
    env[:isLoop] = true # 初始化循环状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态
    while env[:isLoop] == true

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)
        BB_isv_t1 = deepcopy(BB.isv)

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ##NOW 运行每一个阶段
        # for (idx_stage, stageComponent) in processComponent.content.listStageComponent
        for (idx_stage, stage) in enumerate(process.content)
            env[:indexStage] = idx_stage
            env[:stageName] = Symbol(stage.functionName)
            @test println("env[:indexStage] = $(env[:indexStage]),  env[:stageName] = $(env[:stageName])")

            ## 调度状态
            if env[:stateOfSchedule] == :loading
                env[:stateOfSchedule] = scheduler_loading(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule]) # 读取
            else
                if env[:stateOfSchedule] == :stepping
                    runStage!(BB, BI, b, ib, para, env, stage)
                    env[:step], env[:isStep], env[:stateOfSchedule] = scheduler_stepping(env[:step], env[:stepSize]) # 步进
                end
                if env[:stateOfSchedule] == :saving
                    env[:savedIndexProcess], env[:savedIndexStage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule] = scheduler_saving(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage]) # 存储
                end
                if env[:stateOfSchedule] == :collecting
                    env[:stateOfSchedule] = scheduler_collecting() #TODO 收集数据
                end
            end

            # scheduler!(#= process,  =#env) # 调度状态
            # BB, BI, env = runStage!(stageComponent)(BB, BI, para, env)
            # BB, BI = processContent.listStageContent[idx_stage].run(BB, BI, b, ib, para)
            # expr = "BB, BI = " * String(s) * "!(BB, BI, b, ib, para)"
            # @scheduler_stage Meta.parse(expr)


        end

        # ## 判断是否结束
        # if !env[:isStep]
        #     @test println("步进已结束，跳出$(env[:modelName])。")
        # end

        # if env[:stateOfSchedule] == :idle
        #     env[:isModel] = false
        #     env[:isExperiment] = false
        # end

        # if (!env[:isModel] || !env[:isExperiment])
        #     @test println("$(env[:modelName])结束。")
        # end

        # ## 设置临时变量
        # BB_t1 = deepcopy(BB)
        # BI_t1 = deepcopy(BI)

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        if (process.functionName == :process_exBank_insolvent || process.functionName == :process_interBank_insolvent)
            isProcess!(BB.isv, BB_isv_t1) # 判断是否结束过程
        else
            isProcess!(BB.Shock_t, BB_Shock_t_t1) # 判断是否结束过程
        end
        # @isProcess! eval(process.conditionToContinueProcess) # 判断是否结束过程
        isRound!(env) # 判断是否结束回合
        isStep!(env) # 判断是否结束步进
        isLoop!(env) # 判断是否结束循环

    end # while

    return BB, BI, env

end # function









