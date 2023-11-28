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
    stepping = 'stepping',
    running = 'running',
    saving = 'saving',
    loading = 'loading',
    collecting = 'collecting',
    ending = 'ending',
    pass


