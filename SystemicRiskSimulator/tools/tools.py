"函数区：工具集"

from SystemicRiskSimulator import os, time, Path, itertools, pkgutil, importlib, re, logging, np, random, string, shutil, locale
from SystemicRiskSimulator.core.define.define_type import EnvironmentVariableType
from SystemicRiskSimulator.core.define.define_environmentVariables import env

pass  # end import


class Tools:

    def extract_number(pattern, filename):
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
        else:
            return 0

    # @classmethod
    # def test_println(cls, content): # TODO 无用，可以删除
    #     if env['is_test']:
    #         expr = \
    #             """
    #             write
    #             """
    #
    #     pass  # function

    @classmethod
    class Tools:
        @classmethod
        def dict_to_product_list(cls, d: dict) -> list:
            """
            将字典的值转换为字典列表，其中列表的元素表示字典的笛卡尔积。输入字典中的每个值都应该是一个列表。

            Args:
                d (dict): 要转换的字典。

            Returns:
                list: 表示笛卡尔积的字典列表。

            Example:
                ```python
                 d = {'a': [1, 2], 'b': [3, 4]}
                 Tools.dict_to_product_list(d)
                [{'a': 1, 'b': 3}, {'a': 1, 'b': 4}, {'a': 2, 'b': 3}, {'a': 2, 'b': 4}]
                ```
            """
            t = list(d.values())
            l = list(itertools.product(*t, repeat=1))
            pdl = [dict(zip(d.keys(), v)) for v in l]
            return pdl
            pass  # function
        
    # def dict_to_product_list(cls, d: dict):
    #     """
    #     各字典之列表型元素转列表，其元素为字典，列表个元素间关系符合笛卡尔积。
    #     :param self:
    #     :param d:dict:参与转换的字典，字典之每个值都是列表。
    #     :return: pdl:list: 笛卡尔积字典列表 product lict list；
    #     """
    #     t = list(d.values())
    #     l = list(itertools.product(*t, repeat=1))
    #     pdl = []
    #     for v in l:
    #         pdl.append(dict(zip(d.keys(), v)))
    #         pass
    #     return pdl
    #     pass  # function

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
        env['folderpath_of_experiments'] = Path(env['folderpath_project'], env['root_dir_of_experiments'], env['foldername_of_experiments'])
        env['folderpath_of_experiments'] = Path(env['folderpath_project'], env['root_dir_of_experiments'], env['foldername_of_experiments'])

        env['folderpath_of_experiments'].mkdir(parents=True, exist_ok=True)  # 创建文件夹
        env['folderpath_of_experiments_output_data'] = Path(env['folderpath_of_experiments'], env['foldername_of_experiments_output_data'])
        # cd("$(env['folderpath_of_experiments'])")
        env['folderpath_of_experiments_output_data'].mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出数据

        return env
        pass  # function

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
                elif 'SystemicRiskSimulator' in subpath:
                    return path
            path = os.path.dirname(path)

        pass  # function

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

        pass  # function

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
        return re.sub(pattern, repl, Path(folder_form_path).relative_to(env['folderpath_project']).__str__())
        pass  # function

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
        pass  # function

    @classmethod
    def delete_and_recreate_folder(cls, folderpath):
        """
        删除非空文件夹并重新创建文件夹。

        这个功能比较危险，因为会删除非空文件夹，所以要求用户确认操作。

        Args:
            folderpath (Path): 文件夹路径

        """
        folder_path = Path(folderpath)
        if folder_path.exists() and folder_path.is_dir():
            confirmation = input("确认要删除文件夹及其内容吗？(y/n): ")
            if confirmation.lower() == 'y':
                shutil.rmtree(folder_path)
                folder_path.mkdir()
                print("文件夹已成功删除并重新创建。")
            else:
                print("操作已取消。")
        else:
            print("文件夹不存在。")
        pass  # function

    # @classmethod
    # def test_count_loop_in_model(cls, env):
    #     """
    #     测试用，计次单个模型连续循环次数。如果超过已经设定的最大连续循环次数，则抛出异常并退出。 #TODO 无用，待删除
    #
    #     使用方法：
    #
    #     ```python
    #     env = Tools.test_count_loop_in_model(env)  # BUG 用于临时调试
    #     ```
    #
    #     Args:
    #         env (dict): 环境变量
    #
    #     Returns:
    #
    #     """
    #     ## 如果单个模型连续循环计次超过已经设定的最大连续循环次数，则强制退出
    #     if env['round'] > env['test_max_num_of_round']:
    #         logging.error("错误！超过单个模型最大连续循环次数 %s，强制结束运行该模型！", env['test_max_num_of_round'])
    #         raise Exception("错误！超过单个模型最大连续循环次数 %s，强制结束运行该模型！")
    #     logging.debug("循环运行到第 %s 步。", str(env['round']))
    #     env['round'] += 1
    #     return env
    #     pass  # function

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
        pass  # function

    @classmethod
    def generate_unique_identifier(cls):
        """
        随机生成一个8位的英文大小写字母和阿拉伯数字混合的字符串作为id。

        注意，区分大小写。

        Returns:
            str: id字符串
        """
        while True:
            # 生成一个随机的字符串
            new_identifier = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            return new_identifier
        pass  # function

    @classmethod
    def get_folder_info(cls, work_address, folder_source, folder_target, suffix_source, suffix_target):
        """
        获取文件夹及其子文件信息

        Args:
            work_address (str): 工作路径
            folder_source (str): 源文件夹名称
            folder_target (str): 目标文件夹名称
            suffix_source (str): 源文件后缀名
            suffix_target (str): 目标文件后缀名

        Returns:
            dict: 文件夹及其子文件信息
        """
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')  # 设置中文拼音排序
        rootPath_source = os.path.join(work_address, folder_source)  # 原始文件根路径
        rootPath_target = os.path.join(work_address, folder_target)  # 目标文件根路径
        fileNamesWithSuffix = [f for f in os.listdir(rootPath_source) if f.endswith(suffix_source)]  # 文件名含后缀名
        regularPattern = re.compile(f".*[^(\\.{suffix_source})]")
        fileNames = [re.search(regularPattern, f).group() for f in fileNamesWithSuffix]  # 纯文件名
        filePath_source = [os.path.join(rootPath_source, f) for f in fileNamesWithSuffix]  # 文件路径
        filePath_target = [os.path.join(rootPath_target, f"{name}{suffix_target}") for name in fileNames]  # 目标文件路径
        # 排序列表
        fileNames.sort(key=locale.strxfrm)
        fileNamesWithSuffix.sort(key=locale.strxfrm)
        filePath_source.sort(key=locale.strxfrm)
        filePath_target.sort(key=locale.strxfrm)

        results = {
            "fileNames": fileNames,
            "fileNamesWithSuffix": fileNamesWithSuffix,
            "filePath_source": filePath_source,
            "filePath_target": filePath_target
        }

        return results
        pass  # function

    @classmethod
    def get_fields_info(cls, list_tibble):
        """
        获取表头字段

        Args:
            list_tibble (list): 表格列表

        Returns:
            list: 表头字段列表
        """
        list_string_field = []
        for i in range(len(list_tibble)):
            list_string_field.append(list_tibble[i].iloc[0, :].astype(str).tolist())
        return list_string_field
        pass  # function

    pass  # class
