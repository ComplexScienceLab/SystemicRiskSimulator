from enum import Enum

pass  # end import


# StateOfScheduleEnum = Enum('idle', 'indexing', 'stepping', 'saving', 'loading', 'collecting', 'running')


class StateOfScheduleEnum(Enum):
    idle = 'idle',
    initializing = 'initializing'
    indexing = 'indexing',
    stepping = 'stepping',
    saving = 'saving',
    loading = 'loading',
    collecting = 'collecting',
    running = 'running'
    finishing = 'finishing'
    pass
