from enum import Enum
pass  # end import





# StateOfScheduleEnum = Enum('idle', 'indexing', 'stepping', 'saving', 'loading', 'collecting', 'running')


class StateOfScheduleEnum(Enum):
    idle = 'idle',
    indexing = 'indexing',
    stepping = 'stepping',
    loading = 'loading',
    collecting = 'collecting',
    running = 'running'
    finishing = 'finishing'
    pass
