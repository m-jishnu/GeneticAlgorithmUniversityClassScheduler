from PyQt6 import QtWidgets
from py_ui import Result as Parent


class Result:
    def __init__(self):
        self.dialog = dialog = QtWidgets.QDialog()
        # From the qt_ui generated UI
        self.parent = parent = Parent.Ui_Dialog()
        parent.setupUi(dialog)

    def fillForm(self, timetable_data):
        for row, (day, entries) in enumerate(timetable_data.items()):
            for column, entry in enumerate(entries):
                self.parent.tableWidget.setItem(
                    row, column, QtWidgets.QTableWidgetItem(entry)
                )
        self.dialog.exec()
