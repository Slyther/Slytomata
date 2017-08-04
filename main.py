import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from globals import *
from Automaton import *
from Node import Node
from random import randrange
import math
import pickle
import copy

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.MainWindow = MainWindow
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.originCombo = QtWidgets.QComboBox(self.centralwidget)
        self.originCombo.setObjectName("originCombo")
        self.horizontalLayout_2.addWidget(self.originCombo)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.destinationCombo = QtWidgets.QComboBox(self.centralwidget)
        self.destinationCombo.setObjectName("destinationCombo")
        self.horizontalLayout_2.addWidget(self.destinationCombo)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.transitionNameTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.transitionNameTextBox.setObjectName("transitionNameTextBox")
        self.horizontalLayout_2.addWidget(self.transitionNameTextBox)
        self.addTransitionButton = QtWidgets.QPushButton(self.centralwidget)
        self.addTransitionButton.setObjectName("addTransitionButton")
        self.horizontalLayout_2.addWidget(self.addTransitionButton)
        self.removeTransitionButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeTransitionButton.setObjectName("removeTransitionButton")
        self.horizontalLayout_2.addWidget(self.removeTransitionButton)
        self.modifyTransitionButton = QtWidgets.QPushButton(self.centralwidget)
        self.modifyTransitionButton.setObjectName("modifyTransitionButton")
        self.horizontalLayout_2.addWidget(self.modifyTransitionButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.chainLabel = QLineEdit(self.centralwidget)
        self.chainLabel.setObjectName("chainLabel")
        self.horizontalLayout.addWidget(self.chainLabel)
        self.evaluateButton = QPushButton(self.centralwidget)
        self.evaluateButton.setObjectName("evaluateButton")
        self.horizontalLayout.addWidget(self.evaluateButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.drawArea = QWidget(self.centralwidget)
        self.drawArea.setObjectName("drawArea")
        self.drawArea.setStyleSheet('QWidget#drawArea {color: white}')
        self.drawArea.paintEvent = self.paintDrawArea
        self.verticalLayout_2.addWidget(self.drawArea)
        self.gridLayout.addLayout(self.verticalLayout_2, 6, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionNew)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        self.drawArea.mouseDoubleClickEvent = self.addNode
        self.addTransitionButton.mousePressEvent = self.addTransition
        self.modifyTransitionButton.mousePressEvent = self.modifyTransition
        self.evaluateButton.mousePressEvent = self.evaluate
        self.removeTransitionButton.mousePressEvent = self.removeTransition
        self.drawArea.setContextMenuPolicy(Qt.CustomContextMenu)
        self.drawArea.customContextMenuRequested.connect(self.showContextMenu)
        self.actionOpen.triggered.connect(self.loadFromFile)
        self.actionSave_As.triggered.connect(self.saveToFileAs)
        self.actionSave.triggered.connect(self.saveToFile)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Slytomata - " + ("DFA" if globalProperties["isDfa"] else "NFA")))
        self.label_3.setText(_translate("MainWindow", "Origen"))
        self.label_2.setText(_translate("MainWindow", "Destino"))
        self.label_4.setText(_translate("MainWindow", "Transicion"))
        self.addTransitionButton.setText(_translate("MainWindow", "Agregar Transicion"))
        self.removeTransitionButton.setText(_translate("MainWindow", "Eliminar Transicion"))
        self.modifyTransitionButton.setText(_translate("MainWindow", "Modificar Transicion"))
        self.label.setText(_translate("MainWindow", "Cadena: "))
        self.evaluateButton.setText(_translate("MainWindow", "Evaluar"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))

    def showContextMenu(self, pos):
        contextMenu = QMenu("Context Menu", self.drawArea)
        action1 = QAction("Cambiar a NFA" if globalProperties["isDfa"] else "Cambiar a DFA", self.drawArea)
        action1.triggered.connect(self.switchAutomatonType)
        contextMenu.addAction(action1)
        contextMenu.exec(self.drawArea.mapToGlobal(pos))

    def saveToFileAs(self, event):
        fileName = QFileDialog.getSaveFileName(self.drawArea,
         "Save Automaton to File", "/", "Automaton Files (*.atm)")
        if fileName[1]:
            globalProperties["fileURL"] = fileName[0]
            saveToFile(event)
    
    def saveToFile(self, event):
        if globalProperties.get("fileURL"):
            with open(globalProperties["fileURL"], 'wb') as handle:
                if globalProperties.get("drawArea"):
                    del globalProperties["drawArea"]
                pickle.dump(globalProperties, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.saveToFileAs(event)

    def loadFromFile(self, event):
        global globalProperties
        fileName = QFileDialog.getOpenFileName(self.drawArea,
         "Save Automaton to File", "/", "Automaton Files (*.atm)")
        if fileName[1]:
            while globalProperties["nodes"]:
                node = globalProperties["nodes"].pop()
                node.removeNode(None)
            globalProperties["drawArea"] = self.drawArea
            localProperties = pickle.load(open(fileName[0], "rb"))
            globalProperties.update(localProperties) #seems redundant, but drawArea in globalProperties needs to exist during pickle load
            globalProperties["fileURL"] = fileName[0]
            for node in globalProperties["nodes"]:
                node.setParent(self.drawArea)
            self.drawArea.update()

    def switchAutomatonType(self, event):
        globalProperties["isDfa"] = not globalProperties["isDfa"]
        self.translateAutomaton()
        self.drawArea.update()

    def translateAutomaton(self):
        if globalProperties["isDfa"]:
            try:
                origin = next(node.name for node in globalProperties["nodes"] if node.isInitialState)
            except StopIteration:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error!")
                msgBox.setText('Tiene que elegir un estado inicial!')
                msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
                ret = msgBox.exec_()
                globalProperties["isDfa"] = not globalProperties["isDfa"]
                return
            finals = [node.name for node in globalProperties["nodes"] if node.isAcceptanceState]
            if not finals:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error!")
                msgBox.setText('Tiene que elegir por lo menos un estado estado de aceptacion!')
                msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
                ret = msgBox.exec_()
                globalProperties["isDfa"] = not globalProperties["isDfa"]
                return
            automaton = Nfa(origin, finals, globalProperties["transitions"]).as_dfa()
            states = automaton.get_states()
            while globalProperties["nodes"]:
                n = globalProperties["nodes"].pop()
                n.removeNode(None)
            for state in states:
                pos = QPoint(randrange(0, self.drawArea.rect().width()), randrange(0, self.drawArea.rect().height()))
                globalProperties["nodes"].append(Node(self.drawArea, pos, state, state in automaton.finals, automaton.start == state))
            globalProperties["transitions"] = automaton.transitions
            try:
                next(node for node in globalProperties["nodes"] if node.name == '').removeNode(None)
            except StopIteration:
                pass
            nodesToDelete = []
            for node in globalProperties["nodes"]:
                try:
                    for _, transitionDict in globalProperties["transitions"].items():
                        for _, destinations in transitionDict.items():
                            if node.name in destinations:
                                raise StopIteration
                    if not node.isInitialState:
                        nodesToDelete.append(node)
                except StopIteration:
                    pass
            while nodesToDelete:
                n = nodesToDelete.pop()
                n.removeNode(None)
            self.drawArea.update()

    def updateNodesList(self):
        self.originCombo.clear()
        self.destinationCombo.clear()
        for node in globalProperties["nodes"]:
            self.originCombo.addItem(node.name)
            self.destinationCombo.addItem(node.name)

    def addNode(self, someArg: QMouseEvent):
        self.createNode(self.drawArea, someArg.pos())
    
    def createNode(self, parentWidget, pos, name="default"):
        if name == "default":
            name="Q"+str(globalProperties["nodeCount"])
            globalProperties["nodeCount"] += 1
        globalProperties["nodes"].append(Node(parentWidget, pos, name))
        
    def addTransition(self, event):
        values = globalProperties["transitions"].get(self.originCombo.currentText(), {})
        if self.transitionNameTextBox.text() in values and globalProperties["isDfa"]:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText('Ya existe una transicion con este valor!')
            msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
            ret = msgBox.exec_()
            return
        createTransition(self.originCombo.currentText(), self.destinationCombo.currentText(), self.transitionNameTextBox.text())
        self.drawArea.update()

    def removeTransition(self, event):
        foundTransition = deleteTransition(self.originCombo.currentText(), self.destinationCombo.currentText(), self.transitionNameTextBox.text())
        if not foundTransition:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText("No existe esa transicion!")
            msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
            ret = msgBox.exec_()
            return
        self.drawArea.update()
        
    def modifyTransition(self, event):
        print(event)

    def evaluate(self, event):
        finals = set(node.name for node in globalProperties["nodes"] if node.isAcceptanceState)
        if not finals:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText("No hay estados de aceptacion!")
            msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
            ret = msgBox.exec_()
            return
        try:
            initial = next(node.name for node in globalProperties["nodes"] if node.isInitialState)
        except StopIteration:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText("No hay estado inicial!")
            msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
            ret = msgBox.exec_()
            return
        dfa_transitions = {}
        for origin, state_transitions in globalProperties["transitions"].items():
            dfa_transitions[origin] = {}
            for transition_value, destination in state_transitions.items():
                dfa_transitions[origin][transition_value] = destination
        word = self.chainLabel.text()
        result = Dfa(initial, finals, globalProperties["transitions"]).evaluate(word) if globalProperties["isDfa"] else Nfa(initial, finals, globalProperties["transitions"]).evaluate(word)
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Resultado")
        msgBox.setText(str(result))
        msgBox.addButton(QPushButton('Ok'), QMessageBox.YesRole)
        ret = msgBox.exec_()

    def paintDrawArea(self, paintEvent):
        self.updateNodesList()
        p = QPainter(self.drawArea)
        p.fillRect(self.drawArea.rect(), QBrush(QColor(255, 255, 255)))
        p.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))
        p.drawRect(self.drawArea.rect())
        self.drawTransitions(p)
        _translate = QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Slytomata - " + ("DFA" if globalProperties["isDfa"] else "NFA")))

    def drawTransitions(self, p: QPainter):
        p.setPen(QPen(QBrush(QColor(0, 0, 0)), 1))
        for origin, transitionDict in globalProperties["transitions"].items():
            for transitionName, destinations in transitionDict.items():
                for destination in destinations:
                    originNode = next(node for node in globalProperties["nodes"] if node.name == origin)
                    destinationNode = next(node for node in globalProperties["nodes"] if node.name == destination)
                    p.drawLine(originNode.pos, destinationNode.pos)
                    path = QPainterPath()
                    if(originNode.name == destinationNode.name):
                        p.drawEllipse(originNode.pos-QPoint(25, 0), 30, 10)
                        p.drawText(QPoint(originNode.pos-QPoint(65, 0)), transitionName)
                    else:
                        p.drawLine(originNode.pos, destinationNode.pos)
                        rectangle = QRectF(QPointF(originNode.pos), QPointF(destinationNode.pos))
                        xDiff = destinationNode.pos.x() - originNode.pos.x()
                        yDiff = destinationNode.pos.y() - originNode.pos.y()
                        startAngle = (math.atan2(-yDiff, xDiff) * 180.0 / math.pi) * 16.0
                        spanAngle = 120.0 * 16.0
                        p.drawArc(rectangle, startAngle, spanAngle)
                        p.drawRect(rectangle)
                        p.drawText(QRect(originNode.pos, destinationNode.pos), Qt.AlignCenter, transitionName)
                    #path.arcMoveTo(QRectF(originNode.pos, destinationNode.pos),20)
                    #path.arcTo(QRectF(destinationNode.pos, originNode.pos),20, 90)
                    #p.drawArc(QPoint(originNode.pos().x+25, originNode.pos().y+25), QPoint(destinationNode.pos().x+25, destinationNode.pos().y+25) , 45, 45)
                    #line = QLine(originNode.pos, destinationNode.pos)
                    # angle = acos(line().dx() / line().length())
                    # if (line().dy() >= 0):
                    #     angle = (Pi * 2) - angle
                    # p.drawEllipse(destinationNode.pos-QPoint(50, 50), 5, 5)
                    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
