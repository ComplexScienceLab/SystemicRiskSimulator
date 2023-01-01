## 方案1：用于自行导入以下内容
from PySystemicRiskLab import Path, re, pkgutil, importlib
from PySystemicRiskLab.core.define.define_environmentVariables import env

folderpath_package = Path(__file__).parent  # 获取包文件夹路径
pattern = r"[\/\\]"
repl = r"."
modulepath_package = re.sub(pattern, repl, Path(folderpath_package).relative_to(Path.cwd()).__str__())

## 遍历以：导入文件，获取内容；
list_entity_files = []  # 实体文件
list_entityData = {}  # 实体数据列表
idx_file = 0
for _, name, _ in pkgutil.iter_modules([folderpath_package]):
    list_entity_files.append(importlib.import_module("." + name, modulepath_package))
    for content in dir(list_entity_files[idx_file]):
        if not content.startswith("__"):
            list_entityData.update({list_entity_files[idx_file].__dict__.get(content)['attribute']['entity_name']: list_entity_files[idx_file].__dict__.get(content)})
    idx_file += 1

env['list_entityData'] = list_entityData

## 方案2：从外部调用方法导入以下内容
# from PySystemicRiskLab.core.operations.model_builder import ModelBuilder
#
# ModelBuilder.importEntityDataFromFolder(__file__, __name__)
