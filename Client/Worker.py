from PyQt6.QtCore import *


class WorkerSignals:
    result = None
    finished = pyqtSignal()
    error = pyqtSignal()

class Worker(QRunnable):
    def __init__(self , fn , **kwargs ):
        super().__init__()
        self.fn = fn
        self.kwargs = kwargs
        self.threadPool = QThreadPool()
    @pyqtSlot()
    def run(self):
        print("Inside thread run")
        try:
            response = self.fn(**self.kwargs )
        except Exception as error:
            print(error)
        print("After fn")

