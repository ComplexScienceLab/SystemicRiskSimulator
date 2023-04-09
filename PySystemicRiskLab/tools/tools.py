"函数区：工具集"

from PySystemicRiskLab import os, time, Path, itertools, pkgutil, importlib, re, logging, np
from PySystemicRiskLab.core.define.define_type import EnvironmentVariableType
from PySystemicRiskLab.core.define.define_environmentVariables import env

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

    def extract_number(pattern, filename):
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
        else:
            return 0


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
    def import_modules_from_package(cls, folderpath: str, pattern: str):
        """
        从包批量导入模块与方法

        Args:
            folderpath: 包所在路径
            env: 环境变量

        Returns:
            env += env['list_entityData']
        """

        # folderpath = cls._translate_package_form_path_to_folder_form_path(package_form_path) # NOTE 仅当如果用到以模块形式的包之路径的时候启用。
        module_form_path_package = cls._translate_folder_form_path_to_package_form_path(folderpath[0])

        ## 遍历以导入内容函数
        idx_file = 0
        list_files = []  # 文件列表
        list_contents = {}  # 内容列表

        for module_finder_01, name_01, is_pkg in pkgutil.walk_packages([folderpath[0].__str__()]):
            if is_pkg:  # 如果路径下面还有一级子文件夹
                for module_finder_02, name_02, _ in pkgutil.iter_modules([Path(module_finder_01.path).joinpath(name_01).__str__()]):
                    list_files.append(importlib.import_module("." + name_02, module_form_path_package + "." + Path(module_finder_02.path).name))
                    if re.search(pattern, Path(list_files[idx_file].__str__()).name) is not None:
                        for content in dir(list_files[idx_file]):
                            if re.search(pattern, content.__str__()) is not None:
                                list_contents.update({name_02: list_files[idx_file].__dict__.get(content)})
                    idx_file += 1
            else:  # 如果路径下面没有子文件夹
                # for module_finder, name_01, _ in pkgutil.iter_modules([folderpath[0].__str__()]):
                list_files.append(importlib.import_module("." + name_01, module_form_path_package))
                for content in dir(list_files[idx_file]):
                    if not content.startswith("__"):
                        list_contents.update({list_files[idx_file].__dict__.get(content)['attribute']['entity_name']: list_files[idx_file].__dict__.get(content)})
                idx_file += 1

        return list_contents

        ## HACK无用
        # # import os, pkgutil, importlib
        #
        # ## 生成文件夹路径
        # # folderpath=cls._translate_package_form_path_to_folder_form_path(package_form_path)
        # # folder_form_path = os.path.dirname(folderpath)  # 获取包文件夹路径
        # package_path = cls._translate_package_form_path_to_folder_form_path(package_form_path)
        # entity_files = []
        # entityData = {}  # 实体数据集合
        # i = 0
        # n = 0
        # for _, name, _ in pkgutil.iter_modules([package_path]):
        #     entity_files.append(importlib.import_module('.' + name, package_form_path))
        #     for c in dir(entity_files[i]):
        #         if not c.startswith("__"):
        #             entityData.update({entity_files[i].__dict__.get(c)['attribute']['entity_name']: entity_files[i].__dict__.get(c)})
        #             n += 1
        #             # globals()[c] = list_entity_files[i].__dict__.get(c)
        #     i += 1
        # env['list_entityData'] = entityData
        # return env

        pass  # method

    @classmethod
    def _translate_folder_form_path_to_package_form_path(cls, folder_form_path: str):
        """
        转换文件夹形式的包之相对路径为模块形式的包之相对路径

        Args:
            folder_form_path (): 文件夹形式的包之相对路径

        Returns: 模块形式的包之相对路径

        """
        folder_form_path = Path(folder_form_path)  # 获取包文件夹路径
        pattern = r"[\/\\]"
        repl = r"."
        return re.sub(pattern, repl, Path(folder_form_path).relative_to(Path.cwd()).__str__())
        pass  # method

    @classmethod
    def _translate_package_form_path_to_folder_form_path(cls, package_form_path: str):
        """
        转换模块形式的包之相对路径为文件夹形式的包之绝对路径

        Args:
            package_form_path (str): 以模块形式的包之路径

        Returns: 包所在的绝对路径

        """
        pattern = r"\."
        repl = r"/"
        result = re.sub(pattern, repl, package_form_path)
        return os.path.abspath(result)
        pass  # method

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

    @classmethod
    def MinMaxScaler(cls, data: list, min_max_range: tuple):
        """
        指定范围，归一化数组之各元素到范围内。
        
        Args:
            data (list): 待处理的列表
            min_max_range (tuple): 范围，(最小范围, 最大范围)

        Returns: 列表形式的归一化数组。
        """

        data_numpy = np.asarray(data)
        transformed_data = ((data_numpy - np.min(data_numpy)) / (np.max(data_numpy) - np.min(data_numpy))) * (min_max_range[1] - min_max_range[0]) + min_max_range[0]
        return (list(transformed_data))
        # list(MinMaxScaler(feature_range=(0.1, 5)).fit_transform(np.asarray(A_IB).reshape(-1, 1)))
        pass  # method

    pass  # class
