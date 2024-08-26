"""
安装、初始化数据机
"""

from SystemicRiskSimulator.external_packages import pd, deepcopy, pickle, Path
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection

# from SystemicRiskSimulator.core.functions.fun_finance import Finance

pass  # end import


class DataInstaller:
    """
    安装、初始化数据机
    """

    A_data = AgentDataCollection([], [])

    @classmethod
    def set_imported_values_to_Bank_variables(cls, para: dict, sgv: dict):
        """
        导入数据以初始化银行主体众、银行间主体众变量

        Args:
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            bank(BankCommercial): 银行主体众
            interbank(BankInterbank): 银行间主体众
        """

        with open(Path(sgv['folderpath_agents'], 'agents', f"BB_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
            dict_bankCommercial = pickle.load(f)
        with open(Path(sgv['folderpath_agents'], 'agents', f"IB_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
            dict_bankInterbank = pickle.load(f)

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：
        bank = pd.Series()
        for k, v in deepcopy(dict_bankCommercial).items():
            bank[k] = v
        interbank = pd.Series()
        for k, v in deepcopy(dict_bankInterbank).items():
            interbank[k] = v

        return bank, interbank

        pass  # function

    @classmethod
    def set_manually_values_to_Bank_variables(cls):
        """手动设置以初始化银行变量"""

        from SystemicRiskSimulator.core.define.define_agentsVariables import dict_bankCommercial, dict_bankInterbank

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：
        bank = pd.Series()
        for k, v in deepcopy(dict_bankCommercial).items():
            bank[k] = v
        interbank = pd.Series()
        for k, v in deepcopy(dict_bankInterbank).items():
            interbank[k] = v

        return bank, interbank
        pass  # function


    @classmethod
    def install_data(cls, init_data_method: str, sgv: dict, para: dict):
        """
        不同的初始化方式。

        参数init_data_method可选项：

        - ``import data``:  导入数据以初始化

        - ``manually``:  手动设置以初始化；

        - ``randomly``:  生成随机数据以初始化； #HACK 按需添加

        - ``only init``:  仅单纯初始化；

        在模型中使用类似`BB.Z[b]`这样的形式，目的是为了提取每个变量字段内部的数值做处理。不直接使用`BB.Z`，这样仅仅处理字段自身。例如`BB.Z[b] = BB.A[b]`将`BB.A`内的数值赋值给`BB.Z`，而`BB.Z = BB.A`是将`BB.A`作为引用赋值给`BB.Z`，而不是将`BB.A`的数值赋值给`BB.Z`。这样的意义是保证各个字段数据不会引用错乱。

        Args:
            init_data_method (str): 初始化数据的方式
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A (pd.Series): 系统性风险个体众
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量


        """

        if init_data_method == "import data":
            BB, IB = cls.set_imported_values_to_Bank_variables(para, sgv)  # 导入数据以初始化银行变量
        elif init_data_method == "set manually":
            BB, IB = cls.set_manually_values_to_Bank_variables()  # 手动设置以初始化银行变量
        elif init_data_method == "randomly":
            BB, IB = cls.set_randomly_values_to_Bank_variables()  # HACK 按需添加
        elif init_data_method == "only init":
            BB, IB = cls.set_default_values_to_Bank_variables()
        else:
            raise ("关键词" + str(init_data_method) + "取值错误！")
            pass  # if

        sgv['num_bank'] = len(BB.on)  # 获取 agents 之个体数量

        # HACK 后续需要统一这两个变量的用法，防止混乱使用
        b = (BB.on | BB.off)  # 临时设置A.BB示性变量
        ib = ((BB.on | BB.off).reshape(-1, 1) & (BB.on | BB.off).reshape(1, -1))  # 临时设置IB示性变量

        ## 构建Agent模型
        # NOTE 注意这时候`b`、`ib`变量在后续过程中没有发生变动。

        ## HACK 当用pandas数据结构时：
        A = pd.Series([BB, IB, b, ib], index=['BB', 'IB', 'b', 'ib'])

        # ## HACK 当用对象字段数据结构时。
        # A = SystemicRiskAgent(
        #     0,  # 编号（必备的）
        #     BB,  # 商业银行群
        #     b,  # 商业银行群示性变量
        #     IB,  # 银行间邻接矩阵
        #     ib,  # 银行间邻接矩阵示性变量
        # )

        # cls.initialize_data(A)  # 更新各银行之变量，在第一回合初始时 #HACK 无用可删除
        return A
        pass  # function

    # @classmethod
    # def initialize_data(cls, A):  #HACK 无用可删除
    #     ## 更新各银行之变量，在第一回合初始时
    #     # update=sgv['update']
    #     # @Executer.execute
    #     # Finance.update_variables(A.BB, A.IB, A.b, A.ib, by_way='clear transfer all')  # 更新各银行之所有交易变量，在第一回合开始时#BUG 删除后是否影响后续实验初始化数据？有影响！
    #     # Finance.update_variables(A.BB, A.IB, A.b, A.ib, by_way='all')  # 更新各银行之所有变量，在第一回合开始时
    #     return A
    #     pass  # function

    pass  # class
