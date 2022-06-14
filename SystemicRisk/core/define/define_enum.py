from enum import Enum

EStateOfSchedule = Enum('idle', 'indexing', 'stepping', 'saving', 'loading', 'collecting', 'running')
