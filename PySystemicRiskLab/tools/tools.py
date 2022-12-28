"函数区：工具集"

from PySystemicRiskLab import os, time, itertools, pkgutil, importlib, re, logging
from PySystemicRiskLab.core.define.define_type import EnvironmentVariableType
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

        pass  # method

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
        pass  # method

    @classmethod
    def set_experiments_folders(cls, env: EnvironmentVariableType = env, is_datetime: bool = True):
        ## 设定日期时间字符串
        if is_datetime == True:
            str_datetime = "_" + time.strftime("%Y%m%d%H%M%S")
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
        pass  # method

    ## 借鉴来源：[PyCharm项目获取项目路径的方法](https://blog.csdn.net/weixin_42787086/article/details/124625385)
    @classmethod
    def get_project_rootpath(cls):
        """
        获取项目根目录。此函数的能力体现在，不论当前module被import到任何位置，都可以正确获取项目根目录。

        Returns:

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

        pass  # method

    @classmethod
    def import_modules_from_package(cls, folder_path: str, package_modulepath: str, env: EnvironmentVariableType = env):
        """
        从包批量导入模块与方法

        Args:
            folder_path: 文件夹路径
            package_modulepath: 模块路径
            env: 环境变量

        Returns:
            env += env['list_entityData']
        """
        # import os, pkgutil, importlib

        ## 生成文件夹路径
        # folder_path=cls.translatePackagePathToFolderPath(modulepath_package)
        # folderpath_package = os.path.dirname(folder_path)  # 获取包文件夹路径
        package_path = cls.translate_packagepath_to_folderpath(package_modulepath)
        entity_files = []
        entityData = {}  # 实体数据集合
        i = 0
        n = 0
        for _, name, _ in pkgutil.iter_modules([package_path]):
            entity_files.append(importlib.import_module('.' + name, package_modulepath))
            for c in dir(entity_files[i]):
                if not c.startswith("__"):
                    entityData.update({entity_files[i].__dict__.get(c)['attribute']['entity_name']: entity_files[i].__dict__.get(c)})
                    n += 1
                    # globals()[c] = list_entity_files[i].__dict__.get(c)
            i += 1
        env['list_entityData'] = entityData
        return env
        pass  # method

    @classmethod
    def translate_packagepath_to_folderpath(cls, package_modulepath: str):
        """TODO"""
        pattern = r"\."
        repl = r"\/"
        result = re.sub(pattern, repl, package_modulepath)
        os.path.abspath(package_modulepath)
        pass

    # @classmethod TODO 显示模型之实体结构
    # def showModelContent(cls, modelEntity):
    #     """
    #     显示模型之实体结构
    #
    #     Args:
    #         modelEntity:
    #
    #     Returns:
    #
    #     """
    #
    #     print(ModelEntity.text_name)
    #     hierarchy = 1  # 结构层所在层数
    #     for process_com in ModelEntity.content:
    #         print(" " * hierarchy + process_entities.text_name)
    #         hierarchy = 2
    #         for algorithmEntity in process_entities:
    #             pass  # method

    @classmethod
    def test_count_loop_in_model(cls, env):
        """
        测试用，计次单个模型连续循环次数。如果超过已经设定的最大连续循环次数，则抛出异常并退出。

        使用方法：

        ```python
        env = Tools.test_count_loop_in_model(env)  # BUG 用于临时调试
        ```

        Args:
            env (dict): 环境变量

        Returns:

        """
        ## 如果单个模型连续循环计次超过已经设定的最大连续循环次数，则强制退出
        if env['test_continous_loop_of_model'] > env['test_max_count_continous_loop_of_model']:
            logging.error("错误！超过单个模型最大连续循环次数 %s，强制结束运行该模型！", env['test_max_count_continous_loop_of_model'])
            raise Exception("错误！超过单个模型最大连续循环次数 %s，强制结束运行该模型！")
        logging.debug("循环运行到第 %s 步。", str(env['test_continous_loop_of_model']))
        env['test_continous_loop_of_model'] += 1
        return env
        pass  # method

    pass  # class
