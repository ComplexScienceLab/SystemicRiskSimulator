"调度器"

## 调度器

##########################################
# 状态/开发
##########################################

from SystemicRisk.core import np, env, SystemicRiskAgent, AgentDataCollection, StateOfScheduleEnum, ModelComponent, ModelCollector


class ModelScheduler:
    """
    函数：调度器 #HACK 或将废弃

    Argument:
    - modelContent:ModelContent: 被调度的模型内容；
    - env:dict: 环境变量；

    Return:
    - env:dict: 环境变量；
    """

    def scheduler(self, env: dict, A: SystemicRiskAgent, A_data: AgentDataCollection):
        if env['state_of_schedule'] == StateOfScheduleEnum.loading:
            env['loadedIndexProcess'], env['loadedIndexStage'], env['state_of_schedule'] = self.scheduler_loading(env['index_of_schedule_position'], env['index_process'], env['saved_index_process'], env['state_of_schedule'])  # 读取
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.stepping:
            env['step'], env['is_step'], env['state_of_schedule'] = self.scheduler_stepping(env['step'], env['step_size'])  # 步进
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.saving:
            env['saved_index_process'], env['saved_index_stage'], env['state_of_schedule'] = self.scheduler_saving(env['index_of_schedule_position'], env['index_process'], env['index_stage'])  # 存储
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
            env['state_of_schedule'] = self.scheduler_collecting(A, A_data)
            pass
        # if (state_of_schedule == StateOfScheduleEnum.indexing): #HACK 冗余:
        #     env['index_of_schedule_position'], env['state_of_schedule'] = self.scheduler_indexing(component) # 索引
        #     pass
        pass  # functions

    """
    函数：调度索引
    
    Argument: 
    - modelContent:ModelContent: 被调度的模型内容；
    
    Return: 
    - index_of_schedule_position:Array 调度位置索引列表；
    - state_of_schedule:Symbol: 调度状态；
    """

    def scheduler_indexing(self, model: ModelComponent):
        index_of_schedule_position = []
        for i in range(len(model.content)):
            index_of_schedule_position.append([i, []])
            for j in len(model.content[i].content):
                index_of_schedule_position[i][0].append(j)
                pass
            pass
        # @testprintln "索引完成。值为：$(index_of_schedule_position)"
        state_of_schedule = StateOfScheduleEnum.saving
        # @testprintln "切换调度运作状态为$(state_of_schedule)"
        return index_of_schedule_position, state_of_schedule
        pass

    """
    函数：调度读取
    
    Argument: 
    - index_of_schedule_position:list: 调度位置索引列表；
    - index_process:int: 当前过程之位置；
    - index_stage:int: 当前阶段之位置；
    - loadedIndexProcess:int: 读取的过程之位置；
    - loadedIndexStage:int: 读取的阶段之位置；
    - state_of_schedule:Symbol: 调度状态；
    
    Return: 
    - newStateOfSchedule:Symbol: 新的调度状态；
    """

    def scheduler_loading(index_of_schedule_position: list, index_process: int, index_stage: int, loadedIndexProcess: int, loadedIndexStage: int, state_of_schedule: StateOfScheduleEnum):
        # @testprintln "调度读取中……"
        newStateOfSchedule = state_of_schedule
        if (index_process == loadedIndexProcess & index_stage == loadedIndexStage):  # 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取:
            if (~(index_of_schedule_position[index_process][0] == len(index_of_schedule_position[:, 1]) & index_of_schedule_position[index_process][1][index_stage] == len(index_of_schedule_position[index_process][1])) & env['is_rocess'] == True):  # 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运行过程，则继续读取，否则说明程序之模型部分已经运行到终点了，此时应停止读取，然后改状态为idle。:
                newStateOfSchedule = StateOfScheduleEnum.stepping  # 切换调度运作状态为步进
            else:
                newStateOfSchedule = StateOfScheduleEnum.idle  # 切换调度运作状态为待命
                pass
            # @testprintln "调度读取完毕。切换调度运作状态为$(newStateOfSchedule)。"
            pass
        return newStateOfSchedule
        pass

    # "函数：调度步进"
    # functions self.scheduler_stepping(process:Symbol, env:dict=env, saved_index_process:int)
    #     $(process)
    #     self.scheduler_altToSavingState(env)
    #     pass

    """
    函数：调度步进
    
    Argument: 
    - step:int: 步进步数；
    - step_size:int: 步进尺寸；
    
    Return: 
    - is_step:bool: 是否步进；
    - state_of_schedule:Symbol: 调度状态；
    """

    def scheduler_stepping(step: int, step_size: int):
        step += 1
        if step % step_size == 0:  # 是否完成本次步进:
            is_step = False
            state_of_schedule = StateOfScheduleEnum.saving  # 切换调度运作状态为存储
            # @testprintln "步进停止。切换调度运作状态为saving"
        else:
            is_step = True
            state_of_schedule = StateOfScheduleEnum.stepping
            # @testprintln "步进继续："
            pass
        return step, is_step, state_of_schedule
        pass

    """
    函数：调度存储
    
    Argument: 
    - index_of_schedule_position:list: 调度位置索引列表；
    - index_process:int: 当前过程之位置；
    - index_stage:int: 当前阶段之位置；
    - is_rocess:bool: 是否在过程状态中；
    
    Return: 
    - saved_index_process:int: 存储的过程之位置；
    - saved_index_stage:int: 存储的阶段之位置；
    - loadedIndexProcess:int: 读取的过程之位置；
    - loadedIndexStage:int: 读取的阶段之位置；
    - state_of_schedule:Symbol: 调度状态；
    """

    def scheduler_saving(index_of_schedule_position: list, index_process: int, index_stage: int, is_rocess: bool):

        saved_index_process = index_of_schedule_position[index_process][0]
        saved_index_stage = index_of_schedule_position[index_process][1][index_stage]
        # @testprintln "存储的过程和阶段：$(saved_index_process)，$(saved_index_stage)。"

        ## 计算索引之于待读取的下一阶段
        loadedIndexProcess = np.nan
        loadedIndexStage = np.nan
        if is_rocess:  # 如果所处的过程未结束，则继续判断，否则读取下一过程之初始阶段:
            if index_of_schedule_position[index_process][1][index_stage] < index_of_schedule_position[index_process][1][-1]:  # 如果当前阶段不是其所处过程之最后一个阶段，则读取所处过程之下一阶段，否则读取所处过程过程之第一个阶段:
                loadedIndexProcess = index_of_schedule_position[index_process][0]
                loadedIndexStage = index_of_schedule_position[index_process][1][index_stage + 1]
            else:
                loadedIndexProcess = index_of_schedule_position[index_process][0]
                loadedIndexStage = 0
                pass  # if:
        else:  # 如果所处的过程结束，则继续判断
            if index_of_schedule_position[index_process][0] < len(index_of_schedule_position[:, 1]):  # 如果当前过程不是该模型之最后一个过程，则读取当前过程之下一个过程之第一个阶段，否则只读取当前存储的阶段，暨程序之模型部分已经运行到终点了。:
                loadedIndexProcess = index_of_schedule_position[index_process + 1][0]
                loadedIndexStage = 0
            else:
                loadedIndexProcess = saved_index_process
                loadedIndexStage = saved_index_stage
                pass  # if:
            pass  # if:
        # @testprintln "下次读取的过程和阶段：$(loadedIndexProcess)，$(loadedIndexStage)。"

        state_of_schedule = StateOfScheduleEnum.collecting  # 切换调度运作状态为收集数据
        # @testprintln "切换调度运作状态为$(state_of_schedule)"

        return saved_index_process, saved_index_stage, loadedIndexProcess, loadedIndexStage, state_of_schedule
        pass

    """
    函数：调度搜集数据
    
    Argument: 
    - A:SystemicRiskAgent: Agent群变量；
    - A_data:AgentDataCollection: Agent群变量之数据；
    
    Return: 
    - state_of_schedule:Symbol: 调度状态；
    """

    def scheduler_collecting(self, A: SystemicRiskAgent, A_data: AgentDataCollection = np.nan, env: dict = env):
        # @testprintln "收集数据。"
        env['data_id'] += 1  # 累加数据帧ID号
        ModelCollector.collector(A, A_data, state_of_process=env['state_of_process'])  # 收集数据
        state_of_schedule = StateOfScheduleEnum.loading  # 切换调度运作状态为读取
        # @testprintln "切换调度运作状态为$(state_of_schedule)"
        return state_of_schedule
        pass

    # "宏：调度当前过程。" #HACK 或将废弃
    # macro self.scheduler_process(process)
    #     return esc(
    #         quote
    #             if (env['state_of_schedule'] == StateOfScheduleEnum.loading & env['process_name'] == env['savedProcessName']):
    #                 self.scheduler_loading()
    #                 env['state_of_schedule'] = StateOfScheduleEnum.stepping # 切换调度运作状态为存储
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #             elif (env['state_of_schedule'] == StateOfScheduleEnum.stepping):
    #                 self.scheduler_stepping(process; env)
    #                 env['state_of_schedule'] = StateOfScheduleEnum.saving # 切换调度运作状态为存储
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #             elif (env['state_of_schedule'] == StateOfScheduleEnum.saving):
    #                 env['saved_index_process'], env['saved_index_stage'] = self.scheduler_saving(env['state_of_schedule'], env['index_of_schedule_position'], env['index_process'], env['index_stage'])
    #                 env['state_of_schedule'] = StateOfScheduleEnum.collecting # 切换调度运作状态为收集数据
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #             elif (env['state_of_schedule'] == StateOfScheduleEnum.collecting):
    #                 self.scheduler_collecting()
    #                 env['state_of_schedule'] = StateOfScheduleEnum.loading  # 切换调度运作状态为读取
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #             elif (env['state_of_schedule'] == StateOfScheduleEnum.indexing):
    #                 env['index_of_schedule_position'] = self.scheduler_indexing(modelContent, env['state_of_schedule'])
    #                 env['state_of_schedule'] = StateOfScheduleEnum.loading  # 切换调度运作状态为读取
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #                 pass # if:
    #
    #             pass # quote
    #     )
    #     # return :($(content))
    #     pass # macro

    # "宏：调度当前阶段。" #HACK 或将废弃
    # macro scheduler_stage(stage)
    #     expr = esc(
    #         quote
    #             # # @testprintln "阶段：$(env['stage_name'])"
    #             if (env['state_of_schedule'] == StateOfScheduleEnum.stepping):
    #                 $(stage)
    #                 self.scheduler_stepping(env)
    #             elif (env['state_of_schedule'] == StateOfScheduleEnum.loading & env['stage_name'] == env['savedStageName']):
    #                 env['state_of_schedule'] = StateOfScheduleEnum.stepping # 切换调度运作状态为步进
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #                 env['is_step'] = True
    #                 # @testprintln "步进开始"
    #                 $(stage)
    #                 env['is_step'] = self.scheduler_stepping(env['step'], env['step_size'])
    #                 state_of_schedule = StateOfScheduleEnum.saving # 切换调度运作状态为存储
    #                 # @testprintln "切换调度运作状态为$(state_of_schedule)"
    #
    #             elif (env['state_of_schedule'] == StateOfScheduleEnum.saving):
    #                 env['saved_index_stage'] = env['index_stage']
    #                 # @testprintln "下一次步进运行的阶段：$(env['stage_name'])。"
    #                 env['state_of_schedule'] = StateOfScheduleEnum.collecting # 切换调度运作状态为收集数据
    #                 #TODO 收集数据
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #                 env['state_of_schedule'] = StateOfScheduleEnum.loading  # 切换调度运作状态为读取
    #                 # @testprintln "切换调度运作状态为$(env['state_of_schedule'])"
    #                 # break
    #                 # elif (env['state_of_schedule'] == StateOfScheduleEnum.indexing):
    #                 #     env['index_stage'] += 1
    #                 #     push(env['index_of_schedule_position'][env['index_process']], env['index_stage'])
    #                 #     # @testprintln "env['index_of_schedule_position']=$(env['index_of_schedule_position'])"
    #                 pass
    #             pass # quote
    #     )
    #     return expr
    #     pass # macro

    # "宏：判断是否继续运行过程" #HACK 或将废弃
    # def is_rocess(self, BB:BankCommercial, BB_isv_t1:TypeState, BB_Shock_t_t1:TypeMoney{1}, is_rocess:bool, stageFunctionName:Symbol, process:ProcessComponent):
    #     if stageFunctionName == process.content[    pass].functionName: # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运行。:
    #         if (:
    #             process.functionName == :process_exBank_insolvent |
    #             process.functionName == :process_exBank_illiquity |
    #             process.functionName == :process_exBank_bankrupt
    #         )
    #             is_rocess = False
    #             # @testprintln "结束过程：$(env['process_name'])。"
    #         elif (:
    #                 process.functionName == :process_interBank_insolvent
    #         )
    #             if BB.isv == BB_isv_t1: # 判断是否继续运行过程: #BUG，可能存在逻辑问题:
    #                 is_rocess = False
    #                 # @testprintln "结束过程：$(env['process_name'])。"
    #                 pass
    #         else:
    #             if BB.Shock_t == BB_Shock_t_t1: # 判断是否继续运行过程:
    #                 is_rocess = False
    #                 # @testprintln "结束过程：$(env['process_name'])。"
    #                 pass
    #             pass # if:
    #     else:
    #         is_rocess = True
    #         println("继续过程：$(env['process_name'])。")
    #         pass # if:
    #
    #     return is_rocess
    #     pass # functions

    "函数：判断是否继续运行回合"

    def is_round(self, env: dict = env):
        if (env['tau'] < env['max_num_of_tau']):
            env['is_round'] = True
        else:
            env['is_round'] = False
            # @testprintln "结束回合$(env['process_name'])。"
            pass
        pass

    "函数：判断是否继续步进"

    def is_step(self, env: dict = env):
        if ~env['is_step']:
            # @testprintln "暂时跳出模型$(env['model_name'])之过程$(env['process_name'])之阶段$(env['stage_name'])。"
            pass
        pass

    """
    函数：判断是否继续运行循环。
    只有同时满足继续运行过程、继续步进、继续运行回合时，才继续运行循环。否则跳出循环。
    """

    def is_loop(self, env: dict = env):
        if (env['is_rocess'] & env['is_step'] & env['is_round']):
            env['is_loop'] = True
        else:
            env['is_loop'] = False
            # @testprintln "跳出过程$(env['process_name'])之循环。"
            pass
        pass

    pass  # class
