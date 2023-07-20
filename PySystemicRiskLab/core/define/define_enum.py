from enum import Enum


class StateOfScheduleEnum(Enum):
    """
    调度状态枚举类。状态符有以下几种：

    - `idle`：闲置状态；

    - `initializing`：安装状态；

    - `stepping`：步进状态；

    - `running`： 运行状态

    - `saving`：存储状态；

    - `loading`：读取状态；

    - `collecting`：收集数据状态；

    - `running`：运行状态；

    - `ending`: 收尾状态；
    """

    idle = 'idle',
    initializing = 'initializing',
    # indexing = 'indexing',
    stepping = 'stepping',
    running = 'running',
    saving = 'saving',
    loading = 'loading',
    collecting = 'collecting',
    ending = 'ending',
    pass


# class StateOfCollectingEnum(Enum): #TODO 无用可以删除
#     """
#     收集模型数据时，模型所处的状态。状态符有以下几种：
#
#     - ``idle`：闲置状态；
#
#     - `initializing`：初始状态；
#
#     - `running`：运行状态；
#
#     - `ending`：收尾状态；
#     """
#     idle = 'idle'
#     initializing = 'initializing',
#     running = 'running',
#     ending = 'ending',
#     pass
