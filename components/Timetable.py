from PyQt6 import QtCore, QtWidgets, QtGui
from components import TableModel
import json

starting_time = 0  # 9:00 AM
ending_time = 7  # 4:00 PM


# Used for displaying toggable timetable
class Timetable:
    def __init__(self, table, data=False):
        self.table = table
        header = [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]
        with open("timeslots.json") as json_file:
            timeslots = json.load(json_file)["timeslots"]
        header.append(timeslots[starting_time:ending_time])
        self.data = data
        if not data:
            self.data = []
            for i in range(ending_time - starting_time):
                self.data.append(
                    [
                        "Available",
                        "Available",
                        "Available",
                        "Available",
                        "Available",
                    ]
                )
        self.model = TimetableModel(header, self.data)
        table.setModel(self.model)
        table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )
        table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Fixed
        )
        table.clicked.connect(self.toggleCells)
        table.horizontalHeader().sectionClicked.connect(self.toggleCells)
        table.verticalHeader().sectionClicked.connect(self.toggleCells)
        table.findChild(QtWidgets.QAbstractButton).clicked.connect(self.toggleCells)

    # Toggles the availability and changes UI color to appropriate color
    def toggleCells(self):
        indexes = self.table.selectionModel().selectedIndexes()
        for i in indexes:
            value = (
                "Available"
                if self.data[i.row()][i.column()] == "Unavailable"
                else "Unavailable"
            )
            if value == "Available":
                self.table.setStyleSheet(
                    "selection-background-color: rgb(46, 204, 113); selection-color: black;"
                )
            else:
                self.table.setStyleSheet(
                    "selection-background-color: rgb(231, 76, 60); selection-color: black;"
                )
            self.model.setData(i, value)

    def getData(self):
        return self.data


# Timetable model that provides color support for availability status
class TimetableModel(TableModel.TableModel):
    def __init__(self, header, data):
        super().__init__(header, data)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if self.data[index.row()][index.column()] == "Available":
                return QtGui.QBrush(QtGui.QColor(46, 204, 113))
            else:
                return QtGui.QBrush(QtGui.QColor(231, 76, 60))
        elif role != QtCore.Qt.ItemDataRole.DisplayRole:
            return QtCore.QVariant()
        return self.data[index.row()][index.column()]
