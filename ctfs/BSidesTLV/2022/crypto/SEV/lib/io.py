from typing import Protocol, runtime_checkable

from .data import JoinData, SplitData

@runtime_checkable
class IOBase(Protocol):
    def writeLine(self, line : bytes) -> None: ...
    def readLine(self) -> bytes: ...

class IO:
    def __init__(self, base : IOBase) -> None:
        self.base = base
    
    def readLine(self):
        return self.base.readLine()
    
    def writeLine(self, line : bytes):
        self.base.writeLine(line)
    
    def readData(self):
        return SplitData(self.readLine())
    
    def writeData(self, *data : bytes):
        self.writeLine(JoinData(*data))