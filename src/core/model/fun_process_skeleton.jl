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
    @test println("过程$(env[:indexProcess])：$(env[:processName])")

    env[:indexStage] = 0 # 初始化阶段所在位置
    env[:isStep] = true # 初始化步进状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态
    env[:isLoop] = true # 初始化循环状态
    while env[:isLoop] == true

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])：")

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)
        BB_isv_t1 = deepcopy(BB.isv)

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ##NOW 运行每一个阶段
        for (idx_stage, stage) in enumerate(process.content)
            env[:indexStage] = idx_stage
            env[:stageName] = Symbol(stage.functionName)
            @test println("阶段$(env[:indexStage])：$(env[:stageName])")

            ## 调度并运行状态
            if env[:stateOfSchedule] == :loading
                env[:stateOfSchedule] = scheduler_loading(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule]) # 调度读取
            end
            if env[:stateOfSchedule] == :stepping
                runStage!(BB, BI, b, ib, para, env, stage)
                env[:step], env[:isStep], env[:stateOfSchedule] = scheduler_stepping(env[:step], env[:stepSize]) # 步进
            end

            isStep!(env) # 判断是否继续运行步进
            if env[:isStep] == false # 如果步进停止，则跳出该循环
                break
            end
        end # for


        env[:isProcess] = isProcess!(BB, BB_isv_t1, BB_Shock_t_t1, env[:isProcess], env[:stageName], process) # 判断是否继续运行过程

        if env[:stateOfSchedule] == :saving
            env[:savedIndexProcess], env[:savedIndexStage], env[:loadedIndexProcess], env[:loadedIndexStage], env[:stateOfSchedule] = scheduler_saving(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage], env[:isProcess]) # 调度存储
        end
        if env[:stateOfSchedule] == :collecting
            env[:stateOfSchedule] = scheduler_collecting() #TODO 收集数据
        end

        isRound!(env) # 判断是否继续运行回合
        isLoop!(env) # 判断是否继续运行循环
    end # while

    return BB, BI, env

end # function









