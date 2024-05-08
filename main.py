from PyQt6 import QtWidgets, QtGui
from components import Database as db
from containers import Main
import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

# Entry point for application
if __name__ == "__main__":
    if not db.checkSetup():
        db.setup()
    app = QtWidgets.QApplication(sys.argv)
    parent = QtWidgets.QMainWindow()
    Main.MainWindow(parent)
    parent.setWindowIcon(QtGui.QIcon(f"{curr_dir}/assets/main.ico"))
    parent.show()
    sys.exit(app.exec())
