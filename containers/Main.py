from containers import Instructor, Room, Subject, Section, Generate
from py_ui import Main


class MainWindow(Main.Ui_MainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(parent)
        self.connectButtons()
        self.drawTrees()
        self.tabWidget.currentChanged.connect(self.tabListener)
        self.tabWidget.setCurrentIndex(0)

    # Connect Main component buttons to respective actions
    def connectButtons(self):
        self.btnInstrAdd.clicked.connect(lambda: self.openInstructor())
        self.btnRoomAdd.clicked.connect(lambda: self.openRoom())
        self.btnSubjAdd.clicked.connect(lambda: self.openSubject())
        self.btnSecAdd.clicked.connect(lambda: self.openSection())
        self.actionSettings.triggered.connect(lambda: self.tabWidget.setCurrentIndex(4))
        self.btnScenGenerate.clicked.connect(lambda: self.openGenerate())

    # Initialize trees and tables
    def drawTrees(self):
        self.instrTree = Instructor.Tree(self.treeInstr)
        self.roomTree = Room.Tree(self.treeRoom)
        self.subjTree = Subject.Tree(self.treeSubj)
        self.secTree = Section.Tree(self.treeSec)

    # Handle component openings

    def openInstructor(self, id=False):
        Instructor.Instructor(id)
        self.instrTree.display()

    def openRoom(self, id=False):
        Room.Room(id)
        self.roomTree.display()

    def openSubject(self, id=False):
        Subject.Subject(id)
        self.subjTree.display()

    def openSection(self, id=False):
        Section.Section(id)
        self.secTree.display()

    def tabListener(self, index):
        self.instrTree.display()
        self.roomTree.display()
        self.subjTree.display()
        self.secTree.display()

    def openGenerate(self):
        Generate.Generate().generate()
