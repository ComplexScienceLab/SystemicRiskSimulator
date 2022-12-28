"""集成模型、过程、算法等各个内容文件夹之各文件"""

## 方案1：用于自行导入以下内容
from PySystemicRiskLab import Path, re, pkgutil, importlib
from PySystemicRiskLab.core.define.define_environment_variables import env

folderpath_package = Path(__file__).parent  # 获取包文件夹路径
pattern = r"[\/\\]"
repl = r"."
modulepath_package = re.sub(pattern, repl, Path(folderpath_package).relative_to(Path.cwd()).__str__())
list_modulepath_package = []  # 子包模块路径列表
list_folderpath_package = []  # 子文件夹路径列表
for idx_file, folder in enumerate(Path(folderpath_package).iterdir().__str__()):
    if not folder.startswith("__"):
        list_folderpath_package.append(folderpath_package.joinpath(folder))
        list_modulepath_package.append(modulepath_package + "." + folder)

## 遍历以：导入内容函数
idx_file = 0
list_content_files = []  # 内容列表
list_contents = {}  # 实体之内容数据集合
for module_finder_01, name_01, is_pkg in pkgutil.walk_packages([folderpath_package.__str__()]):
    for module_finder_02, name_02, _ in pkgutil.iter_modules([Path(module_finder_01.path).joinpath(name_01).__str__()]):
        list_content_files.append(importlib.import_module("." + name_02, modulepath_package + "." + Path(module_finder_02.path).name))
        pattern = r"Content_"
        if re.search(pattern, Path(list_content_files[idx_file].__str__()).name) is not None:
            for content in dir(list_content_files[idx_file]):
                if re.search(pattern, content.__str__()) is not None:
                    list_contents.update({name_02: list_content_files[idx_file].__dict__.get(content)})
        idx_file += 1

env['list_contents'] = list_contents

## 方案2：从外部调用方法导入以下内容
# from PySystemicRiskLab.core.operations.model_builder import ModelBuilder
#
# ModelBuilder.importEntityDataFromFolder(__file__, __name__)
