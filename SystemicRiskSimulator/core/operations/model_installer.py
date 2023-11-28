"""
安装模型机
"""

from SystemicRiskSimulator import deepcopy, re, Path
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.core.define.define_environmentVariables import env
from SystemicRiskSimulator.core.define.define_parameterVariables import para
from SystemicRiskSimulator.core.operations.builder import Builder
from SystemicRiskSimulator.tools.tools import Tools

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

        ## 复制模型数据与内容到`SystemicRiskSimulator/models`文件夹下
        Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/models"), is_auto_confirmation=False)
        Tools._copy_files_from_other_folders(env['folderpath_models'], Path(env['folderpath_models'],"SystemicRiskSimulator/models"), is_auto_confirmation=False)

        ## 导入实体数据，生成实体集、内容集并返回
        # entities = Builder.build_entities_by_node_component(env) #BUG还未适配，暂时用不到
        entities = Builder.build_entities_by_process_and_container_component(env)  # NOTE 现在的版本

        ## 生成待运行的模型列表
        return EntityManager.mainModelInstanceEntities

        pass  # function

    pass  # class
