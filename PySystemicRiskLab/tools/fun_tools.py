"函数区：工具集"

## 函数区：工具集

##########################################
# 状态/开发
##########################################


from PySystemicRiskLab import os, time, itertools
from PySystemicRiskLab.core.define.define_environment_variables import env

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

    @classmethod
    def test_println(cls, content):
        if env['is_test']:
            expr = \
                """
                write
                """

        pass

    @classmethod
    def dict_to_product_list(cls, d: dict):
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

    @classmethod
    def set_experiments_folders(cls, env: dict = env, isDatetime: bool = True):
        ## 设定日期时间字符串
        if isDatetime == True:
            str_datetime = "_" + time.strftime("%Y%model_name%d%H%M%S")
        else:
            str_datetime = ""
            pass

        ## 设定前缀字符串
        if env['foldername_type_of_experiments'] == "default":
            str_manuallyName = "default"
        elif env['foldername_type_of_experiments'] == "set manually":
            str_manuallyName = env['foldername_prefix_of_experiments']
        else:
            raise Exception("关键词取值错误！".format(env['foldername_type_of_experiments']))
            pass

        env['foldername_of_experiments'] = str_manuallyName + str_datetime
        env['folderpath_of_experiments'] = os.path.join(env['folderpath_project'], env['root_dir_of_experiments'], env['foldername_of_experiments'])

        os.mkdir(env['folderpath_of_experiments'])  # 创建文件夹
        env['folderpath_of_experiments_output_data'] = os.path.join(env['folderpath_of_experiments'], env['foldername_of_experiments_output_data'])
        # cd("$(env['folderpath_of_experiments'])")
        os.mkdir(env['folderpath_of_experiments_output_data'])  # 创建文件夹，以导出实验输出数据

        return env
        pass  # functioin

    ## 借鉴来源：[PyCharm项目获取项目路径的方法](https://blog.csdn.net/weixin_42787086/article/details/124625385)
    @classmethod
    def get_project_rootpath(cls):
        """
        获取项目根目录。此函数的能力体现在，不论当前module被import到任何位置，都可以正确获取项目根目录。
        :return:
        """
        path = os.path.realpath(os.curdir)
        while True:
            for subpath in os.listdir(path):
                # PyCharm项目中，'.idea'是必然存在的，且名称唯一
                if '.idea' in subpath:
                    return path
                elif '.vscode' in subpath:
                    return path
                elif '.git' in subpath:
                    return path
                elif 'PySystemicRiskLab' in subpath:
                    return path
            path = os.path.dirname(path)

    pass  # class
