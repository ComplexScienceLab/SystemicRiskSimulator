
from enum import Enum

StateOfSchedule:Enum = Enum('idle', 'indexing', 'stepping', 'saving', 'loading', 'collecting', 'running')