from PyQt6 import QtCore, QtWidgets


class NoScrollTableWidget(QtWidgets.QTableWidget):
    def wheelEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass

    def keyReleaseEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def contextMenuEvent(self, event):
        pass

    def dragEnterEvent(self, event):
        pass

    def dragMoveEvent(self, event):
        pass

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        pass


class Ui_Dialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Result")
        Form.resize(802, 428)
        Form.setMinimumSize(QtCore.QSize(800, 452))
        Form.setMaximumSize(QtCore.QSize(800, 452))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = NoScrollTableWidget(Form)
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setFixedHeight(50)
        self.tableWidget.verticalHeader().setDefaultSectionSize(75)
        self.tableWidget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.tableWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        for i in range(self.tableWidget.columnCount()):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        for i in range(self.tableWidget.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Result", "Timetable"))
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        times = [
            "9:00-10:00",
            "10:00-11:00",
            "11:00-12:00",
            "12:00-13:00",
            "13:00-14:00",
            "14:00-15:00",
            "15:00-16:00",
        ]

        for i, day in enumerate(days):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Form", day))

        for i, time in enumerate(times):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Form", time))
