"函数区：工具集"

## 函数区：工具集

##########################################
# 状态/开发
##########################################

# from SystemicRisk.core import itertools, env
pass  # end import



import itertools
from SystemicRisk.core.define.define_environment_variables import env
pass  # end import




class Tools:

    # TODO"宏：当测试时使用"
    # macro testprintln(content):
    #     if env['is_test']:
    #         return esc(
    #             quote
    #                 write(f,$(content));write(f,"\n");println($(content))
    #                 pass
    #         )
    #         pass
    #     pass

    def test_println(self, content):
        if env['is_test']:
            expr = \
                """
                write
                """

        pass

    def dict_to_product_list(self, d: dict):
        """
        各字典之列表型元素转列表，其元素为字典，列表个元素间关系符合笛卡尔积。
        :param self:
        :param d:dict:参与转换的字典，字典之每个值都是列表。
        :return: pdl:list: 笛卡尔积字典列表 product lict list；
        """
        t = list(d.values())
        l = list(itertools.product(*t, repeat=1))
        pdl = []
        for v in l:
            pdl.append(dict(zip(d.keys(), v)))
            pass
        return pdl
        pass

    pass
