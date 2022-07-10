"""
@File   : Tools.py
@Author : Ethan Lin
@Date   : 2022/07/10
@Desc   : 相关工具
"""

from PySystemicRiskLab import os

## 借鉴来源：[PyCharm项目获取项目路径的方法](https://blog.csdn.net/weixin_42787086/article/details/124625385)
def get_project_rootpath():
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



if __name__ == "__main__":
    path=get_project_rootpath()
    print('项目路径是：',path)

