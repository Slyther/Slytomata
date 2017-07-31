from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from globals import *

class Node(QtWidgets.QLabel):
    def __init__(self, parentWidget, pos, name, isAcceptanceState=False, isInitialState=False):
        super().__init__(parentWidget)
        self.setParent(parentWidget)
        self.pos = self.mapFromParent(pos)
        self.name = name
        self.isInitialState = isInitialState
        self.isAcceptanceState = isAcceptanceState
        self.setFixedSize(100, 100)
        self.move(self.mapToParent(self.pos - QPoint(50, 50)))
        self.show()
        self.raise_()
        self.paintEvent = self.drawNode
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.update()
    
    def __getstate__(self):
        toReturn = {"name":self.name, "isInitialState":self.isInitialState, "isAcceptanceState":self.isAcceptanceState,
        "pos":self.pos}
        return toReturn

    def __setstate__(self, state):
        #self.name = state["name"]
        #self.isInitialState = state["isInitialState"]
        #self.isAcceptanceState = state["isAcceptanceState"]
        #self.pos = state["pos"]
        self.__init__(globalProperties["drawArea"], state["pos"], state["name"], state["isAcceptanceState"], state["isInitialState"])

    def drawNode(self, paintEvent):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        if self.isInitialState:
            p.setBrush(QBrush(QColor(64, 128, 64)))
        else:
            p.setBrush(QBrush(QColor(128, 128, 128)))
        p.drawEllipse(25, 25, 50, 50)
        if self.isAcceptanceState:
            p.drawEllipse(30, 30, 40, 40)
        p.drawText(self.rect(), Qt.AlignCenter, self.name)

    def showContextMenu(self, pos):
        contextMenu = QMenu("Context Menu", self)
        action1 = QAction("Seleccionar como Estado Inicial" if not self.isInitialState else "Quitar como Estado Inicial", self)
        action1.triggered.connect(self.setInitialState)
        contextMenu.addAction(action1)
        action2 = QAction("Sleccionar como Estado de Aceptacion" if not self.isAcceptanceState else "Quitar como Estado de Aceptacion", self)
        action2.triggered.connect(self.setAcceptanceState)
        contextMenu.addAction(action2)
        action3 = QAction("Eliminar Nodo", self)
        action3.triggered.connect(self.removeNode)
        contextMenu.addAction(action3)
        contextMenu.exec(self.mapToGlobal(pos))

    def setInitialState(self, event):
        for node in globalProperties["nodes"]:
            if node.isInitialState:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error!")
                msgBox.setText('No puede haber mas de un estado de aceptacion!')
                msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
                ret = msgBox.exec_()
                return
        self.isInitialState = not self.isInitialState
        self.update()

    def setAcceptanceState(self, event):
        self.isAcceptanceState = not self.isAcceptanceState
        self.update()

    def removeNode(self, event):
        if self.name in globalProperties["transitions"]:
            del globalProperties["transitions"][self.name]
        entriesToRemove = {}
        for origin, transitionDict in globalProperties["transitions"].items():
            for transitionName, destinations in transitionDict.items():
                newTrans = [destination for destination in destinations if destination != self.name]
                if(len(newTrans) == 0):
                    entriesToRemove[origin] = transitionName
                globalProperties["transitions"][origin][transitionName] = newTrans
        for origin, transitionName in entriesToRemove.items():
            del globalProperties["transitions"][origin][transitionName]
        for i, node in enumerate(globalProperties["nodes"]):
            if self.name == node.name:
                del globalProperties["nodes"][i]
                break
        self.hide()
