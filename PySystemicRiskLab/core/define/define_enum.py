from enum import Enum

class StateOfScheduleEnum(Enum):
    idle = 'idle',
    indexing = 'indexing',
    stepping = 'stepping',
    saving = 'saving',
    loading = 'loading',
    collecting = 'collecting',
    pass


class StateOfProcessEnum(Enum):
    initializing = 'initializing',
    running = 'running',
    finishing = 'finishing',
    pass
