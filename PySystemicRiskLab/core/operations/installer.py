"""
安装机
"""
from PySystemicRiskLab import deepcopy, Node, np, re
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_agentsVariables import dict_bankCommercial, dict_bankInterbank
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_parameterVariables import para
from PySystemicRiskLab.core.define.define_type import IdsType
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState
from PySystemicRiskLab.core.operations.builder import ModelBuilder

pass  # end import


class ModelInstaller:
    """安装模型机"""

    @classmethod
    def install_model(cls):
        """
        安装模型

        Returns:
            models: 模型字典集
        """
        ## 构建、安装本次实验组所需的所有模型
        ### 导入实体数据，生成实体集、内容集并返回
        entities, contents = ModelBuilder.build_entities(env)
        ### 生成模型列表
        models = {}
        for (i, model_name) in enumerate(para['model_name']):
            model = eval("entities['modelEntity_Model" + model_name + "']")

            ## 对于每一个模型，根据已经生成的模型，生成索引遍历序列，用于后序遍历所有节点。                                                                                                                                                                                                 遍历序列，用于后序遍历所有节点。
            # install_entity_queue = cls.build_postorder_traversial(model)  # HACK暂时不需要用  #FIXME 程序运行错误

            ## 模型列表
            models[model_name] = model
            pass

        return models
        pass  # method

    @classmethod
    def build_postorder_traversial(cls, modelEntity: Entity):
        """
        根据已经生成的模型，生成遍历序列，用于后序遍历所有节点。

        Args:
            modelEntity: 模型实体

        Returns: result 结果遍历序列

        """
        stack_entity = []  # 定义一个栈，存储实体
        stack_entity.append(modelEntity)  # 入栈根实体，即模型实体
        queue_entities = {}  # 定义一个字典序列，存储实体遍历顺序
        if modelEntity != None:
            stack_entity.append(modelEntity)
        while not len(stack_entity) == 0:
            entity: Entity = stack_entity[-1]
            if entity is not None:  # 只有当实体节点不是空时，才将子节点入栈
                stack_entity.pop()  # 将该节点弹出，避免重复操作，下面再将右中左节点添加到栈中
                stack_entity.append(entity)  # 添加根节点（空节点不入栈）
                stack_entity.append(None)  # 根节点被访问过，但是还没有处理，加入空节点做为标记。
                sub_nodes = deepcopy(entity.container)  # 获取实体容器之子节点
                sub_nodes.reverse()  # 反序子节点 #FIXME运行出错AttributeError: 'NoneType' object has no attribute 'reverse'
                for sub_node in sub_nodes:  # 入栈子节点（不入栈空节点）
                    if sub_node is not None:
                        stack_entity.append(sub_node)
            else:  # 只有遇到空节点的时候，才放下一个节点进结果序列
                stack_entity.pop()  # 弹出空节点
                entity = stack_entity.pop()  # 重新取出栈里的节点
                queue_entities[entity.attribute.entity_name] = deepcopy(entity)  # 该节点之内容加入结果集
        return queue_entities

        pass  # method

    @classmethod
    def get_info_of_init_entity_that_corresponding_of_entity(cls, entity: Entity):  # HACK 无用
        """
        获取实体对应的初始态实体之信息

        Args:
            entity: 实体

        Returns: initEntity: 初始态实体, initEntity_name: 初始态实体名称, container: 容器内容, content_type: 内容类型
        """

        entity_name = entity.attribute.entity_name
        pattern = r".*" + "Entity" + ".*"
        splited_entity_name = re.split(pattern, entity_name)
        initEntity_name = splited_entity_name[0] + "Component" + splited_entity_name[1]
        initEntity = eval(initEntity_name)
        container_content = initEntity['container']
        content_type = initEntity['property_content']['content_type']

        return initEntity, initEntity_name, container_content, content_type
        pass  # method

    @classmethod
    def build_node(cls, entity: Entity):  # HACK 无用
        """
        构建单个节点

        Args:
            entity (Entity): 实体

        Returns:
            node: 节点
        """
        is_expand = True if entity.attribute.content_type is not "algorithm" else False  # 如果内容类型是算法，则节点是叶子节点，不可展开
        node = Node(tag=entity.attribute.entity_name, expanded=is_expand, data=entity.content)
        node.fpointer = entity.container
        return node
        pass  # method

    pass  # class


class DataInstaller:
    """
    安装、初始化数据机
    """

    A_data = AgentDataCollection([], [])

    # @property
    @classmethod
    def set_default_values_to_B_variables(cls):
        bank: BankCommercial = BankCommercial(
            id_agent=np.arange(1, env['num_bank'], step=1),  # agent 之编号 id
            abbr=np.full((env['num_bank'], 1), ""),  # 缩写 abbr
            name=np.full((env['num_bank'], 1), ""),  # 全名 name
            A_all=np.zeros((env['num_bank'], 1)),  # 总资产 A_all: $A_all=A_BI+A_exBI$
            A_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间资产加总 A_BI_all
            A_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
            A_P=np.zeros((env['num_bank'], 1)),  # 银行贷款给生产部门之资产（非流动性资产） A_P
            A_Q=np.zeros((env['num_bank'], 1)),  # 银行持有超额准备金（流动性资产） A_Q
            A_R=np.zeros((env['num_bank'], 1)),  # 银行持有法定准备金（非流动性资产） A_R
            A_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其它资产（非流动性资产） A_other
            Z_all=np.zeros((env['num_bank'], 1)),  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
            Z_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间负债加总 Z_BI_all
            Z_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
            Z_D=np.zeros((env['num_bank'], 1)),  # 银行获得居民部门存款（非流动性负债） Z_D
            Z_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其他负债（非流动性负债） Z_other
            E_all=np.zeros((env['num_bank'], 1)),  # 所有者权益 E_all
            T_all=np.zeros((env['num_bank'], 1)),  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
            Lo_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流出 Lo_BI_all
            Lo_BI_all=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
            Lo_exBI=np.zeros((env['num_bank'], 1)),  # 银行贷款流出给生产部门 Lo_P
            Lo_P=np.zeros((env['num_bank'], 1)),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
            Li_all=np.zeros((env['num_bank'], 1)),  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
            Li_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流入 Li_BI_all
            Li_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
            Li_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流入从生产部门 Li_P
            Bi_all=np.zeros((env['num_bank'], 1)),  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
            Bi_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流入 Bi_BI_all
            Bi_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
            Bi_D=np.zeros((env['num_bank'], 1)),  # 银行借款流入从居民部门 Bi_D
            Bo_all=np.zeros((env['num_bank'], 1)),  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
            Bo_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流出 Bo_BI_all
            Bo_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
            Bo_D=np.zeros((env['num_bank'], 1)),  # 银行借款流出给居民部门 Bo_D
            Shock_t=np.zeros((env['num_bank'], 1)),  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
            Shock_s=np.zeros((env['num_bank'], 1)),  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
            Shock_def_t=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
            Shock_def_s=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
            Shock_run_t=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
            Shock_run_s=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
            Shock_exBI_t=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
            Shock_exBI_s=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
            Shock_P_run_s=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
            Shock_P_def_t=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
            Shock_D_def_s=np.zeros((env['num_bank'], 1)),  # 银行存款违约损失冲击源头 Shock_D_def_s
            Shock_D_run_t=np.zeros((env['num_bank'], 1)),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
            Shock_B=np.zeros((env['num_bank'], 1)),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
            Shock_B_A=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
            Shock_B_Z=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
            Shock_BI_s=np.zeros((env['num_bank'], 1)),  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
            Shock_BI_t=np.zeros((env['num_bank'], 1)),  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
            Shock_BI_def_s=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击源头 Shock_BI_def_s
            Shock_BI_def_t=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击目标 Shock_BI_def_t
            Shock_BI_run_s=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
            Shock_BI_run_t=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
            Shock_BI_run_ilq_s=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
            Shock_BI_run_ilq_t=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
            Shock_BI_run_br_s=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
            Shock_BI_run_br_t=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
            Loss_BI=np.zeros((env['num_bank'], 1)),  # 银行间市场冲击损失 Loss_BI
            Loss_BI_def_t=np.zeros((env['num_bank'], 1)),  # 银行间资产负债违约冲击损失 Loss_BI_def_t
            Loss_BI_run_t=np.zeros((env['num_bank'], 1)),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
            # FIXME 以下带注释部分，用于测试几种不同的形状之影响
            # on=np.full(env['num_bank'], True),  # 示性向量之于银行是否存在 is_on
            # off=np.full(env['num_bank'], False),  # 示性向量之于银行是否已退出不存在 is_off
            # hel=np.full(env['num_bank'], True),  # 示性向量之于银行是否健康 is_healthy
            # isv=np.full(env['num_bank'], False),  # 示性向量之于银行是否资不抵债 is_insolvent
            # ilq=np.full(env['num_bank'], False),  # 示性向量之于银行是否流动性短缺 is_illiquid
            # br=np.full(env['num_bank'], False),  # 示性向量之于银行是否破产 is_bankrupt
            # is_needed_BoBI=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还借款 is_needed_BoBI
            # is_enabled_BoBI=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoBI
            # is_needed_BoD=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
            # is_enabled_BoD=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
            # is_needed_LiP=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
            # is_enabled_LiP=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
            # is_allocated_Shock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
            on=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否存在 is_on
            off=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已退出不存在 is_off
            hel=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否健康 is_healthy
            isv=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否资不抵债 is_insolvent
            ilq=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否流动性短缺 is_illiquid
            br=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否破产 is_bankrupt
            is_needed_BoBI=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还借款 is_needed_BoBI
            is_enabled_BoBI=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoBI
            is_needed_BoD=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
            is_enabled_BoD=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
            is_needed_LiP=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
            is_enabled_LiP=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
            is_allocated_Shock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
            list_exist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 list_exist
            list_insolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 list_insolvent
            list_illiquid=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 list_illiquid
            list_bankrupt=np.full(env['num_bank'], list),  # 列表之于破产的银行编号 list_bankrupt

        )

        interbank: BankInterbank = BankInterbank(
            id_agent=np.array(np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])), dtype=IdsType),  # agent 之间之关联编号 id
            A_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产邻接矩阵 A_BI
            Z_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债邻接矩阵 Z_BI
            Lo_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流出邻接矩阵 Lo_BI
            Li_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流入邻接矩阵 Li_BI
            Bo_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流入邻接矩阵 Bo_BI
            Bi_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流出邻接矩阵 Bi_BI
            Shock_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
            Shock_BI_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间违约损失冲击 Shock_BI_def
            Shock_BI_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
            Shock_BI_run_ilq=np.zeros((env['num_bank'], env['num_bank'])),  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
            Shock_BI_run_br=np.zeros((env['num_bank'], env['num_bank'])),  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
            Loss_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间市场冲击损失 Loss_BI
            Loss_BI_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_BI_def
            Loss_BI_run=np.full((env['num_bank'], env['num_bank']), True),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
            is_exposure=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于是否有银行间敞口 is_exposure
            on=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 is_on
            off=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 is_off
            hel=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间健康的 is_healthy
            isv=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 is_insolvent
            ilq=np.array([]),  # 信息邻接矩阵之于银行间流动性短缺的 is_illiquid
            br=np.array([]),  # 信息邻接矩阵之于银行间破产的 is_bankrupt
            cre=np.array([]),  # 信息列表之于各银行之债权方银行编号 list_creditors
            deb=np.array([]),  # 信息列表之于各银行之债务方银行编号 list_debtors
            cre_isv=[],  # 信息列表之于资不抵债的银行之债权方银行编号 list_creditors_in_insolvent
            deb_isv=[],  # 信息列表之于资不抵债的银行之债务方银行编号 list_debtors_in_insolvent
            cre_ilq=[],  # 信息列表之于流动性短缺的银行之债权方银行编号 list_creditors_in_illiquid
            deb_ilq=[],  # 信息列表之于流动性短缺的银行之债务方银行编号 list_debtors_in_illiquid
            cre_br=[],  # 信息列表之于破产的银行之债权方银行编号 list_creditors_in_bankrupt
            deb_br=[],  # 信息列表之于破产的银行之债务方银行编号 list_debtors_in_bankrupt
        )

        return bank, interbank
        pass  # fun

    @classmethod
    def set_randomly_values_to_Bank_variables(cls):
        # TODO """随机化初始化银行变量"""
        bank, interbank = cls.set_default_values_to_B_variables()
        pass

        pass

    @classmethod
    def set_imported_values_to_Bank_variables(cls):
        # TODO """导入数据以初始化银行变量"""
        bank, interbank = cls.set_default_values_to_B_variables
        pass

    @classmethod
    def set_manually_values_to_Bank_variables(cls):
        """手动设置以初始化银行变量"""  # FIXME 须提取手动初始化方式为单独的方式
        bank, interbank = cls.set_default_values_to_B_variables()

        bank.__dict__.update(dict_bankCommercial)
        interbank.__dict__.update(dict_bankInterbank)

        return bank, interbank
        pass  # method

    @classmethod
    def init_B_and_BI(cls, init_method: str):
        """
        不同的初始化方式。

        参数init_method可选项：

        - ``only init``:  仅单纯初始化；

        - ``randomly``:  生成随机数据以初始化；

        - ``import data``:  导入数据以初始化

        - ``manually``:  手动设置以初始化；

        Args:
            init_method ():

        Returns: A

        """

        if init_method == "only init":
            BB, BI = cls.set_default_values_to_B_variables()
        elif init_method == "randomly":
            BB, BI = cls.set_randomly_values_to_Bank_variables()  # TODO 按需添加
        elif init_method == "import data":
            BB, BI, cls.A_data.BB, cls.A_data.BI = cls.set_imported_values_to_Bank_variables()  # 导入数据以初始化银行变量 #TODO 按需添加
        elif init_method == "set manually":
            BB, BI = cls.set_default_values_to_B_variables()
            BB, BI = cls.set_manually_values_to_Bank_variables()  # 手动设置以初始化银行变量
        else:
            raise ("关键词" + str(init_method) + "取值错误！")
            pass

        ## 构建Agent模型
        A = SystemicRiskAgent(
            1,  # 编号（必备的）
            BB,  # 商业银行群
            BI  # 银行间邻接矩阵
        )

        # # 初始化带回合变量的商业银行实例数组、初始化带回合变量的银行间市场实例数组 #HACK无用
        # A_data = Collector.collect(A, None, env)

        ## 更新各银行之变量，在第一回合初始时
        b = (BB.on | BB.off).reshape(-1, 1)  # 临时设置BB示性变量
        ib = ((BB.on | BB.off).reshape(-1, 1) & (BB.on | BB.off).reshape(1, -1))  # 临时设置BI示性变量
        Shock.update_B_Shock(BB, BI, b, ib, by_way='all')  # 更新各银行之所有冲击变量，在第一回合开始时
        Shock.update_B_Shock(BB, BI, b, ib, by_way='all')  # 更新各银行之所有冲击变量，在第一回合开始时
        BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='all')  # 更新各银行之资产负债表变量
        BankState.update_B_state(BB, BI, target='any', source='any')  # 更新各银行之状态示性变量

        ## 存储初始数据
        # A_data.BB_0 = deepcopy(BB)
        # A_data.BI_0 = deepcopy(BI)
        # A_data_0 = deepcopy(A)

        return A
        pass  # method

    pass  # class
