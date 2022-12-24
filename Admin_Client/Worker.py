from PyQt6.QtCore import *
import json

class WorkerSignals(QObject):
    image = pyqtSignal(bytes)
    finished = pyqtSignal(dict)
    error = pyqtSignal(tuple)


class Worker(QRunnable):
    def __init__(self , fn , **kwargs ):
        super().__init__()
        self.fn = fn
        self.kwargs = kwargs
        self.threadPool = QThreadPool()
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        print("Inside thread run")
        try:
            response = self.fn(**self.kwargs )
            if(type(response) == bytes):
                self.signals.image.emit(response)
            elif(type(response) == dict):
                self.signals.finished.emit(response)
            #print("After fn", response)
        except Exception as error:
            self.signals.error.emit(error.args)



