from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from py_ui import Generating as Parent


def show_error(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    msg.setText(f"{message}     ")
    msg.setWindowTitle("Error")
    msg.exec()


class Generating:
    def __init__(self):
        self.dialog = dialog = QtWidgets.QDialog()
        self.parent = parent = Parent.Ui_Generating()
        parent.setupUi(dialog)

    def show(self):
        self.dialog.exec()

    def close(self):
        self.dialog.close()


class Worker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.finished.emit(result)