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
        self.mousePressEvent = self.nodePressed
        self.mouseMoveEvent = self.nodeMoved
        self.mouseReleaseEvent = self.nodeReleased
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.update()
    
    def __getstate__(self):
        toReturn = {"name":self.name, "isInitialState":self.isInitialState, "isAcceptanceState":self.isAcceptanceState,
        "pos":self.pos}
        return toReturn

    def __setstate__(self, state):
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

    def nodePressed(self, event):
        print(event)

    def nodeMoved(self, event):
        print(event)

    def nodeReleased(self, event):
        print(event)

    def showContextMenu(self, pos):
        contextMenu = QMenu("Context Menu", self)
        action1 = QAction("Seleccionar como Estado Inicial" if not self.isInitialState else "Quitar como Estado Inicial", self)
        action1.triggered.connect(self.setInitialState)
        contextMenu.addAction(action1)
        action2 = QAction("Sleccionar como Estado de Aceptacion" if not self.isAcceptanceState else "Quitar como Estado de Aceptacion", self)
        action2.triggered.connect(self.setAcceptanceState)
        contextMenu.addAction(action2)
        action4 = QAction("Editar Nodo", self)
        action4.triggered.connect(self.editNode)
        contextMenu.addAction(action4)
        action3 = QAction("Eliminar Nodo", self)
        action3.triggered.connect(self.removeNode)
        contextMenu.addAction(action3)
        contextMenu.exec(self.mapToGlobal(pos))

    def setInitialState(self, event):
        for node in globalProperties["nodes"]:
            if node.isInitialState and node.name != self.name:
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

    def editNode(self, event):
        text = QInputDialog.getText(self, "Modificar Nodo" + self.name,
                                         "Ingrese nuevo nombre:", QLineEdit.Normal,
                                         "")
        if text[1]:
            try:
                next(node for node in globalProperties["nodes"] if node.name == text[1])
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error!")
                msgBox.setText('Ya existe un nodo con ese nombre!')
                msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
                ret = msgBox.exec_()
                return
            except StopIteration:
                for origin, transitionDict in globalProperties["transitions"].items():
                    for transitionName, destinations in transitionDict.items():
                        for destination in destinations:
                            if origin == self.name:
                                dest = next(node for node in globalProperties["nodes"] if node.name == destination)
                                modifyTransition(self.name, dest.name, transitionName, text[0], "origin")
                            elif destination == self.name:
                                orig = next(node for node in globalProperties["nodes"] if node.name == origin)
                                modifyTransition(orig.name, self.name, transitionName, text[0], "destination")
                self.name = text[0]
                self.update()


    def removeNode(self, event):
        for node in globalProperties["nodes"]:
            deleteTransition(self.name, node.name, "")
            deleteTransition(node.name, self.name, "")
        globalProperties["nodes"] = [node for node in globalProperties["nodes"] if node.name != self.name]
        self.parentWidget().update()
        self.hide()
