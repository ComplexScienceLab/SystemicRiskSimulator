"函数区：工具集"
from SystemicRiskSimulator import os, time, Path, itertools, pkgutil, importlib, re, logging, np, random, string, shutil, locale, Any
from SystemicRiskSimulator.core.define.define_type import EnvironmentVariableType

# from SystemicRiskSimulator.core.define.define_environmentVariables import env

pass  # end import


class Tools:

    def extract_number(pattern, filename):
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
        else:
            return 0

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
    def set_experiments_folders(cls, foldername_prefix_of_experiments: str, foldername_of_experiments_output_data: str, str_folderpath_root_dir_of_experiments: str, str_folderpath_models: str, str_folderpath_settings_environments: str, str_folderpath_settings_parameters: str, str_folderpath_settings_agents: str, type_of_experiments_foldername: str = "default", is_datetime: bool = True):
        """
        设置实验相关的文件夹。包括实验设置项文件夹、模型文件夹、实验导出数据文件夹。

        根据【实验文件夹根路径】、【实验导出数据文件夹名称】、【实验文件夹前缀名】、【实验文件夹命名方式】，生成【实验文件夹名称】、【实验文件夹路径】、【实验导出数据文件夹路径】。

        Args:
            foldername_prefix_of_experiments (str): 实验文件夹前缀名
            foldername_of_experiments_output_data (str): 实验导出数据文件夹名称
            str_folderpath_root_dir_of_experiments (str): 实验文件夹根相对路径字符串
            str_folderpath_models (str): 模型文件夹相对路径字符串
            str_folderpath_settings_environments (str): 实验设置项之环境设置项文件夹相对路径字符串
            str_folderpath_settings_parameters (str): 实验设置项之参数设置项文件夹相对路径字符串
            str_folderpath_settings_agents (str): 实验设置项之实验个体众数据初始化设置项文件夹相对路径字符串
            type_of_experiments_foldername (str): 实验文件夹命名方式。取值："default": 默认方式，"set manually": 手动设置方式。默认"default"；
            is_datetime (bool): 是否使用日期时间字符串。默认True；

        Returns:
            foldername_of_experiments (str): 实验文件夹名称
            folderpath_of_experiments (str): 实验文件夹路径
            folderpath_of_experiments_output_data (str): 实验导出数据文件夹路径
        """

        ## 设置项目文件夹路径
        folderpath_project = Tools.get_project_rootpath()

        ## 设定实验结果导出文件夹
        if is_datetime is True:  # 设定日期时间字符串
            str_datetime = "_" + time.strftime("%Y%m%d%H%M%S")
        else:
            str_datetime = ""
            pass

        if type_of_experiments_foldername == "default":  # 设定前缀字符串
            str_manuallyName = "default"
        elif type_of_experiments_foldername == "set manually":
            str_manuallyName = foldername_prefix_of_experiments
        else:
            raise Exception("关键词取值错误！".format(type_of_experiments_foldername))
            pass  # if

        foldername_of_experiments = str_manuallyName + str_datetime
        # folderpath_of_experiments = Path(str_folderpath_project, folderpath_root_dir_of_experiments, foldername_of_experiments)
        folderpath_of_experiments = Path(folderpath_project, str_folderpath_root_dir_of_experiments, foldername_of_experiments)

        folderpath_of_experiments.mkdir(parents=True, exist_ok=True)  # BUG 如果文件夹已经存在怎么办？
        folderpath_of_experiments_output_data = Path(folderpath_of_experiments, foldername_of_experiments_output_data)
        # cd("$(folderpath_of_experiments)")
        folderpath_of_experiments_output_data.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出数据

        ## 设定实验输入数据文件夹 #TODO

        ## 设定实验设置项文件夹
        folderpath_settings_environments = Path(folderpath_project, str_folderpath_settings_environments)
        folderpath_settings_parameters = Path(folderpath_project, str_folderpath_settings_parameters)
        folderpath_settings_agents = Path(folderpath_project, str_folderpath_settings_agents)

        ## 设定模型文件夹
        folderpath_models = Path(folderpath_project, str_folderpath_models)

        return (
            foldername_of_experiments,
            folderpath_project,
            folderpath_of_experiments,
            folderpath_of_experiments_output_data,
            folderpath_models,
            folderpath_settings_environments,
            folderpath_settings_parameters,
            folderpath_settings_agents,
        )

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
    def _copy_files_from_other_folders(cls, folderpath_source: Any(str, Path), folderpath_target: Any(str, Path), is_auto_confirmation: bool = False):
        """
        从指定的文件夹复制其全部的子文件夹及其子文件到目标文件夹。

        这个功能比较危险，因为可能会出现复制文件夹到其它位置的操作，所以要求用户确认操作。

        Args:
            folderpath_source Any(str, Path): 源文件夹相对路径字符串或者Path对象
            folderpath_target Any(str, Path): 目标文件夹相对路径字符串或者Path对象
            is_auto_confirmation (bool): 是否自动确认操作。默认False。

        Returns:
            None
        """

        confirmation = 'n'

        folderpath_project = Tools.get_project_rootpath()

        if isinstance(folderpath_source, str):
            folderpath_source = Path(folderpath_project, folderpath_source)
        if isinstance(folderpath_target, str):
            folderpath_target = Path(folderpath_project, folderpath_target)

        if folderpath_source.exists() and folderpath_source.is_dir():
            if is_auto_confirmation == True:
                confirmation = 'y'
            else:
                confirmation = input(rf"确认要复制文件夹{folderpath_source}及其内容到{folderpath_target}吗？(y/[n]): ")

            if confirmation.lower() == 'y':
                for file in folderpath_source.iterdir():
                    if file.is_dir():

                        shutil.copytree(file, Path(folderpath_target, file.name))
                    else:
                        shutil.copy(file, Path(folderpath_target))
                        pass  # if
                    pass  # for
                print(f"文件夹{folderpath_source}已成功复制到{folderpath_target}。")
            else:
                print("操作已取消。")
                pass  # if
        else:
            print(f"{folderpath_source}文件夹不存在。")
            pass  # if

        pass  # function

    @classmethod
    def import_modules_from_package(cls, str_folderpath: str, pattern: str, str_folderpath_project: str):
        """
        从包批量导入模块与方法

        Args:
            str_folderpath (str): 包所在路径字符串
            pattern (str): 匹配模式
            str_folderpath_project (str): 项目文件夹路径字符串

        Returns:
            list_contents: 内容列表
        """

        # str_folderpath = cls._translate_package_form_path_to_folder_form_path(str_package_form_path) # NOTE 仅当如果用到以模块形式的包之路径的时候启用。
        module_form_path_package = cls._translate_folder_form_path_to_package_form_path(str_folderpath[0], str_folderpath_project)

        ## 遍历以导入内容函数
        idx_file = 0
        list_files = []  # 文件列表
        list_contents = {}  # 内容列表

        for module_finder_01, name_01, is_pkg in pkgutil.walk_packages([str_folderpath[0].__str__()]):
            if is_pkg:  # 如果路径下面还有一级子文件夹
                for module_finder_02, name_02, _ in pkgutil.iter_modules([Path(module_finder_01.path).joinpath(name_01).__str__()]):
                    list_files.append(importlib.import_module("." + name_02, module_form_path_package + "." + Path(module_finder_02.path).name))
                    if re.search(pattern, Path(list_files[idx_file].__str__()).name) is not None:
                        for content in dir(list_files[idx_file]):
                            if re.search(pattern, content.__str__()) is not None:
                                list_contents.update({name_02: list_files[idx_file].__dict__.get(content)})
                    idx_file += 1
            else:  # 如果路径下面没有子文件夹
                # for module_finder, name_01, _ in pkgutil.iter_modules([str_folderpath[0].__str__()]):
                list_files.append(importlib.import_module("." + name_01, module_form_path_package))
                for content in dir(list_files[idx_file]):
                    if not content.startswith("__"):
                        list_contents.update({list_files[idx_file].__dict__.get(content)['attribute']['entity_name']: list_files[idx_file].__dict__.get(content)})
                idx_file += 1

        return list_contents

        pass  # function

    @classmethod
    def _translate_folder_form_path_to_package_form_path(cls, str_folder_form_path: str, str_folderpath_project: str):
        """
        转换文件夹形式的包之相对路径为模块形式的包之相对路径

        Args:
            str_folder_form_path (str): 文件夹形式的包之路径字符串
            str_folderpath_project (str): 项目文件夹路径字符串

        Returns: 模块形式的包之相对路径

        """
        str_folder_form_path = Path(str_folder_form_path)  # 获取包文件夹路径
        pattern = r"[\/\\]"
        repl = r"."
        return re.sub(pattern, repl, Path(str_folder_form_path).relative_to(str_folderpath_project).__str__())
        pass  # function

    @classmethod
    def _translate_package_form_path_to_folder_form_path(cls, str_package_form_path: str):
        """
        转换模块形式的包之相对路径为文件夹形式的包之绝对路径

        Args:
            str_package_form_path (str): 以模块形式的包之路径字符串

        Returns: 包所在的绝对路径

        """
        pattern = r"\."
        repl = r"/"
        result = re.sub(pattern, repl, str_package_form_path)
        return os.path.abspath(result)
        pass  # function

    @classmethod
    def _delete_and_recreate_folder(cls, folderpath_target: Any(str, Path), is_auto_confirmation: bool = False):
        """
        删除非空文件夹并重新创建文件夹。

        这个功能比较危险，因为会删除非空文件夹，所以要求用户确认操作。

        Args:
            folderpath_target Any(str, Path): 文件夹相对路径字符串或者Path对象
            is_auto_confirmation (bool): 是否自动确认操作。默认False。

        """
        folderpath_project = Tools.get_project_rootpath()

        if isinstance(folderpath_target, str):
            folderpath_target = Path(folderpath_project, folderpath_target)

        confirmation = 'n'
        folder_path = Path(folderpath_project, folderpath_target)
        if folder_path.exists() and folder_path.is_dir():
            if len(list(folder_path.glob('*'))) > 0:
                if is_auto_confirmation == True:
                    confirmation = 'y'
                else:
                    confirmation = input(rf"确认要删除文件夹{folderpath_target}及其内容吗？(y/[n]): ")

                if confirmation.lower() == 'y':
                    shutil.rmtree(folder_path)
                    folder_path.mkdir()
                    print("文件夹已成功删除并重新创建。")
                else:
                    print("操作已取消。")
            else:
                print("文件夹为空，无需删除。")
        else:
            print("文件夹不存在。")
        pass  # function

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
