"函数：通用过程框架"

## 函数：通用过程框架

##########################################
#状态/开发
##########################################

"""
通用过程框架：

Argument: 
- A:SystemicRiskAgent: Agent群变量；
- para:dict: 参数变量；
- env:dict: 环境变量；
- process:ProcessComponent: 过程组件实例；
- A_data:AgentDataCollection: Agent群变量之数据；

Return:
- A:SystemicRiskAgent: Agent群变量；
- para:dict: 参数变量；
- env:dict: 环境变量；
- A_data:AgentDataCollection: Agent群变量之数据；
"""
def fun_process_skeleton(self, A:SystemicRiskAgent, para:dict, env:dict, process:ProcessComponent, A_data:AgentDataCollection):
    # @testprintln "过程$(env['index_process'])：$(env['process_name'])"

    env['index_stage'] = 0 # 初始化阶段所在位置
    env['is_step'] = True # 初始化步进状态
    env['is_round'] = True # 初始化回合状态
    env['is_rocess'] = True # 初始化过程状态
    env['is_loop'] = True # 初始化循环状态
    while env['is_loop'] == True:

        ## 回合数变动
        if (env['loadedIndexStage'] != 1):
            # @testprintln "\n继续回合：$(env['tau'])"
        else:
            env['tau'] += 1 # 回合累加一
            # @testprintln "\n开始回合：$(env['tau'])"
            pass

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(A.BB.Shock_t)
        BB_isv_t1 = deepcopy(A.BB.isv)

        b = TypeState{1}(A.BB.on | A.BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((A.BB.on | A.BB.off) & (A.BB.on | A.BB.off)') # 临时设置BI示性变量

        ## 运行每一个阶段
        for (idx_stage, stage) in enumerate(process.content)
            env['index_stage'] = idx_stage
            env['stage_name'] = Symbol(stage.functionName)
            # @testprintln "阶段$(env['index_stage'])：$(env['stage_name'])"

            ## 调度并运行状态
            if env['state_of_schedule'] == StateOfSchedule.loading:
                env['state_of_schedule'] = scheduler_loading(env['index_of_schedule_position'], env['index_process'], env['index_stage'], env['loadedIndexProcess'], env['loadedIndexStage'], env['state_of_schedule']) # 调度读取
                pass
            if env['state_of_schedule'] == StateOfSchedule.stepping:
                A = runStage(A, b, ib, para, env, stage)
                env['step'], env['is_step'], env['state_of_schedule'] = scheduler_stepping(env['step'], env['step_size']) # 步进
                pass

            is_step() # 判断是否继续运行步进
            if env['is_step'] == False: # 如果步进停止，则跳出该循环:
                break
                pass
            pass # for


        env['is_rocess'] = is_rocess(A.BB, BB_isv_t1, BB_Shock_t_t1, env['is_rocess'], env['stage_name'], process) # 判断是否继续运行过程

        if env['state_of_schedule'] == StateOfSchedule.saving:
            env['saved_index_process'], env['saved_index_stage'], env['loadedIndexProcess'], env['loadedIndexStage'], env['state_of_schedule'] = scheduler_saving(env['index_of_schedule_position'], env['index_process'], env['index_stage'], env['is_rocess']) # 调度存储
            pass
        if (env['state_of_schedule'] == StateOfSchedule.collecting && env['state_of_process'] == StateOfSchedule.running):
            env['state_of_schedule'] = scheduler_collecting(A, A_data)
            pass

        is_round() # 判断是否继续运行回合
        is_loop() # 判断是否继续运行循环
        pass # while

    return A, para, env, A_data

    pass # functions









