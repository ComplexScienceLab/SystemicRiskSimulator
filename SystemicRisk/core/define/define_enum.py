from enum import Enum

StateOfSchedule = Enum('idle', 'indexing', 'stepping', 'saving', 'loading', 'collecting', 'running')
