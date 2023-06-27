import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from a3a5 import *
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
try:
    with open('paths.txt', 'r') as f:
        contents = f.readlines()
except FileNotFoundError:
    with open('paths.txt', 'w') as f:
        f.write(f'a3a5_path = {desktop}\ncells_path = {desktop}\nsave_path = {desktop}')
with open('paths.txt', 'r') as f:
    contents = f.readlines()
a3a5_path = contents[0]
cells_path = contents[1]
save_path = contents[2]
a3a5_path = a3a5_path.replace('a3a5_path = ', '').strip()
cells_path = cells_path.replace('cells_path = ', '').strip()
save_path = save_path.replace('save_path = ', '').strip()



class Worker(QObject):
    finished = pyqtSignal() # сигнал, който се пуска при край на функцията
    a3a5_update = pyqtSignal(object)
    distance_update = pyqtSignal(object)

    # функция за създаване на threaded некомбиниран вороной
    def createA3A5(self, a3a5Path, label, result_path):
        result_a3a5 = createOutputA3A5(a3a5Path=a3a5Path, label = label)
        savePath = result_path.text()
        savePath = savePath[6::]
        a3a5Path_Name = fileNamer(savePath, 'A3A5_Result', 'xlsx')
        result_a3a5.to_excel(a3a5Path_Name)
        self.finished.emit()
        self.a3a5_update.emit(result_a3a5)

    def createDistance(self, cellsPath, result_a3a5, distanceThreshold, countThreshold, label, result_path):
        result_distance = createOutputDistance(cellsPath=cellsPath, result_a3a5=result_a3a5, dist_threshold=distanceThreshold, c_threshold=countThreshold, label = label)
        savePath = result_path.text()
        savePath = savePath[6 : :]
        distancePath_Name = fileNamer(savePath, 'A3A5_Distance_Result', 'xlsx')
        result_distance.to_excel(distancePath_Name)
        self.finished.emit()
        self.distance_update.emit(result_distance)

class Ui_MainWindow(object):
    def __init__(self):
        self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.saveLocation = None
        self.result_a3a5 = pd.DataFrame()
        self.result_distance = pd.DataFrame()

    def update_a3a5(self, a3a5_updated):
        self.result_a3a5 = a3a5_updated

    def update_distance(self, distance_updated):
        self.result_distance = distance_updated

    def distanceUpdated(self):
        props = [self.input_path, self.input_Label, self.browse_input,
                 self.cellsFilePath, self.cellsFileLabel, self.cellsFileOpener,
                 self.result_Label, self.browse_saveDir, self.result_path,
                 self.closestLabel, self.yesRadioButton, self.noRadioButton,
                 self.distanceThresholdLabel, self.distanceThresholdLineEdit,
                 self.countThresholdLineEdit, self.countThresholdLabel]
        for prop in props:
            prop.setEnabled(True)
        self.label.setText("Distance result is done.")

    def a3a5updated(self):
        if self.yesRadioButton.isChecked():
            props = [self.input_path, self.input_Label, self.browse_input,
                     self.cellsFilePath, self.cellsFileLabel, self.cellsFileOpener,
                     self.result_Label, self.browse_saveDir, self.result_path,
                     self.closestLabel, self.yesRadioButton, self.noRadioButton,
                     self.distanceThresholdLabel, self.distanceThresholdLineEdit,
                     self.countThresholdLineEdit, self.countThresholdLabel]
            for prop in props:
                prop.setEnabled(True)
        else:
            props = [self.input_path, self.input_Label, self.browse_input,
                     self.cellsFilePath, self.cellsFileLabel, self.cellsFileOpener,
                     self.result_Label, self.browse_saveDir, self.result_path,
                     self.closestLabel, self.yesRadioButton, self.noRadioButton]
            for prop in props:
                prop.setEnabled(True)
        self.label.setText("A3A5 result is done.")
        if self.yesRadioButton.isChecked():
            self.start2PushButton.setEnabled(True)

    def create_output_Distance(self):
        cellsPath = self.cellsFilePath.text()
        cellsPath = cellsPath[6::]
        if os.path.exists(cellsPath):
            self.label.setText('Progress: Creating distance result file...')
            self.thread = QThread()
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(partial(self.worker.createDistance, cellsPath, self.result_a3a5,
                                                self.distanceThresholdLineEdit.text(),
                                                self.countThresholdLineEdit.text(), self.label, self.result_path))
            props = [self.input_path, self.input_Label, self.browse_input,
                     self.cellsFilePath, self.cellsFileLabel, self.cellsFileOpener,
                     self.result_Label, self.browse_saveDir, self.result_path,
                     self.closestLabel, self.yesRadioButton, self.noRadioButton,
                     self.distanceThresholdLabel, self.distanceThresholdLineEdit,
                     self.countThresholdLineEdit, self.countThresholdLabel, self.start2PushButton, self.startPushButton]
            for prop in props:
                prop.setDisabled(True)
            self.worker.distance_update.connect(self.update_distance)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
            self.thread.finished.connect(self.distanceUpdated)
        else:
            self.label.setText("5G cells file does not exist\n or the path is wrong!")

    def create_output_A3A5(self):
        if self.input_path.text() == '' or self.cellsFilePath.text() == '' or self.input_path.text() == 'Path:' or self.cellsFilePath.text() == 'Path':
            self.label.setText("Open files in order to begin!")
        else:
            self.label.setText('Progress: Creating A3A5 result file...')
            a3a5Path = self.input_path.text()
            a3a5Path = a3a5Path[6 : :]
            if os.path.exists(a3a5Path):
                self.thread = QThread()
                self.worker = Worker()
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(partial(self.worker.createA3A5, a3a5Path, self.label, self.result_path))
                props = [self.input_path, self.input_Label, self.browse_input,
                         self.cellsFilePath, self.cellsFileLabel, self.cellsFileOpener,
                         self.result_Label, self.browse_saveDir, self.result_path,
                         self.closestLabel, self.yesRadioButton, self.noRadioButton,
                         self.distanceThresholdLabel, self.distanceThresholdLineEdit,
                         self.countThresholdLineEdit, self.countThresholdLabel, self.start2PushButton, self.startPushButton]
                for prop in props:
                    prop.setDisabled(True)
                self.worker.a3a5_update.connect(self.update_a3a5)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()
                self.thread.finished.connect(self.a3a5updated)
            else: self.label.setText("A3A5 file does not exist\n or the path is wrong!")

    def open_a3a5(self):
        global a3a5_path
        fname = QFileDialog.getOpenFileName(None, "Open file", a3a5_path, "Excel Files(*.xlsx)")
        if fname[0] == '':
            return
        else:
            path = 'Path: ' + fname[0]
            self.input_path.setText(path)
            with open('paths.txt', 'r') as file:
                data = file.readlines()
            fname = fname[0].split('/')
            fname.pop(-1)
            fname = '/'.join(fname)
            data[0] = 'a3a5_path = ' + fname + '\n'
            # and write everything back
            with open('paths.txt', 'w') as file:
                file.writelines(data)

    def open_cells(self):
        global cells_path
        fname = QFileDialog.getOpenFileName(None, "Open file", cells_path, "Excel Files(*.xlsx)")
        if fname[0] == '':
            return
        else:
            path = 'Path: ' + fname[0]
            self.cellsFilePath.setText(path)
            with open('paths.txt', 'r') as file:
                data = file.readlines()
            fname = fname[0].split('/')
            fname.pop(-1)
            fname = '/'.join(fname)
            data[1] = 'cells_path = ' + fname + '\n'
            # and write everything back
            with open('paths.txt', 'w') as file:
                file.writelines(data)

    def open_saveLoc(self):
        global save_path
        self.saveLocation = QFileDialog.getExistingDirectory(None, "Select Location", save_path)
        path = 'Path: ' + self.saveLocation
        self.result_path.setText(path)
        with open('paths.txt', 'r') as file:
            data = file.readlines()
        data[2] = 'save_path = ' + self.saveLocation
        # and write everything back
        with open('paths.txt', 'w') as file:
            file.writelines(data)

    def enableDistance(self):
        props = [self.distanceThresholdLabel, self.distanceThresholdLineEdit,
                 self.countThresholdLineEdit, self.countThresholdLabel,
                 self.cellsFileOpener, self.cellsFilePath, self.cellsFileLabel]
        for prop in props:
            prop.setEnabled(True)
        self.distanceThresholdLineEdit.setText('30')
        self.countThresholdLineEdit.setText('0')

    def disableDistance(self):
        props = [self.distanceThresholdLabel, self.distanceThresholdLineEdit,
                 self.countThresholdLineEdit, self.countThresholdLabel,
                 self.cellsFileOpener, self.cellsFilePath, self.cellsFileLabel]
        for prop in props:
            prop.setEnabled(False)
        self.distanceThresholdLineEdit.clear()
        self.countThresholdLineEdit.clear()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 337)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cells_Layout = QtWidgets.QHBoxLayout()
        self.cells_Layout.setObjectName("cells_Layout")
        self.cellsFileLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.cellsFileLabel.setFont(font)
        self.cellsFileLabel.setObjectName("cellsFileLabel")
        self.cells_Layout.addWidget(self.cellsFileLabel, 0, QtCore.Qt.AlignVCenter)
        self.cellsFileOpener = QtWidgets.QPushButton(self.centralwidget)
        self.cellsFileOpener.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.cellsFileOpener.setFont(font)
        self.cellsFileOpener.setObjectName("cellsFileOpener")
        self.cells_Layout.addWidget(self.cellsFileOpener)
        self.cellsFileOpener.clicked.connect(self.open_cells)
        self.gridLayout.addLayout(self.cells_Layout, 7, 0, 1, 1)
        self.action_Layout = QtWidgets.QHBoxLayout()
        self.action_Layout.setObjectName("action_Layout")
        self.startPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startPushButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.startPushButton.setFont(font)
        self.startPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startPushButton.setObjectName("startPushButton")
        self.action_Layout.addWidget(self.startPushButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.startPushButton.clicked.connect(self.create_output_A3A5)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.start2PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.start2PushButton.setObjectName(u"start2PushButton")
        self.start2PushButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.start2PushButton.setFont(font)
        self.start2PushButton.setDisabled(True)
        self.start2PushButton.clicked.connect(self.create_output_Distance)
        self.action_Layout.addWidget(self.start2PushButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.action_Layout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.action_Layout, 11, 0, 1, 1)
        self.input_path = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.input_path.setFont(font)
        self.input_path.setObjectName("input_path")
        self.gridLayout.addWidget(self.input_path, 1, 0, 1, 1)
        self.addClosest_Layout = QtWidgets.QHBoxLayout()
        self.addClosest_Layout.setObjectName("addClosest_Layout")
        self.closestLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.closestLabel.setFont(font)
        self.closestLabel.setObjectName("closestLabel")
        self.addClosest_Layout.addWidget(self.closestLabel)
        self.yesRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.yesRadioButton.setFont(font)
        self.yesRadioButton.setObjectName("yesRadioButton")
        self.yes_no_buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.yes_no_buttonGroup.setObjectName("yes_no_buttonGroup")
        self.yes_no_buttonGroup.addButton(self.yesRadioButton)
        self.addClosest_Layout.addWidget(self.yesRadioButton, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.yesRadioButton.toggled.connect(self.enableDistance)
        self.noRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.noRadioButton.setFont(font)
        self.noRadioButton.setChecked(True)
        self.noRadioButton.setObjectName("noRadioButton")
        self.yes_no_buttonGroup.addButton(self.noRadioButton)
        self.addClosest_Layout.addWidget(self.noRadioButton, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.noRadioButton.toggled.connect(self.disableDistance)
        self.gridLayout.addLayout(self.addClosest_Layout, 6, 0, 1, 1)
        self.count_Layout = QtWidgets.QHBoxLayout()
        self.count_Layout.setObjectName("count_Layout")
        self.countThresholdLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.countThresholdLabel.setFont(font)
        self.countThresholdLabel.setObjectName("countThresholdLabel")
        self.count_Layout.addWidget(self.countThresholdLabel)
        self.countThresholdLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.countThresholdLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.countThresholdLineEdit.setFont(font)
        self.countThresholdLineEdit.setObjectName("countThresholdLineEdit")
        self.count_Layout.addWidget(self.countThresholdLineEdit)
        self.countThresholdLineEdit.setText('0')
        self.gridLayout.addLayout(self.count_Layout, 9, 0, 1, 1)
        self.input_Layout = QtWidgets.QHBoxLayout()
        self.input_Layout.setObjectName("input_Layout")
        self.input_Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.input_Label.setFont(font)
        self.input_Label.setObjectName("input_Label")
        self.input_Layout.addWidget(self.input_Label)
        self.browse_input = QtWidgets.QPushButton(self.centralwidget)
        self.browse_input.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browse_input.setFont(font)
        self.browse_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browse_input.setObjectName("browse_input")
        self.input_Layout.addWidget(self.browse_input)
        self.browse_input.clicked.connect(self.open_a3a5)
        self.gridLayout.addLayout(self.input_Layout, 0, 0, 1, 1)
        self.result_path = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.result_path.setFont(font)
        self.result_path.setObjectName("result_path")
        self.gridLayout.addWidget(self.result_path, 5, 0, 1, 1)
        self.cellsFilePath = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.cellsFilePath.setFont(font)
        self.cellsFilePath.setObjectName("cellsFilePath")
        self.gridLayout.addWidget(self.cellsFilePath, 8, 0, 1, 1)
        self.result_layout = QtWidgets.QHBoxLayout()
        self.result_layout.setObjectName("result_layout")
        self.result_Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.result_Label.setFont(font)
        self.result_Label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.result_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_Label.setObjectName("result_Label")
        self.result_layout.addWidget(self.result_Label, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.browse_saveDir = QtWidgets.QPushButton(self.centralwidget)
        self.browse_saveDir.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browse_saveDir.setFont(font)
        self.browse_saveDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browse_saveDir.setObjectName("browse_saveDir")
        self.browse_saveDir.clicked.connect(self.open_saveLoc)
        self.result_layout.addWidget(self.browse_saveDir)
        self.gridLayout.addLayout(self.result_layout, 4, 0, 1, 1)
        self.distance_Layout = QtWidgets.QHBoxLayout()
        self.distance_Layout.setObjectName("distance_Layout")
        self.distanceThresholdLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.distanceThresholdLabel.setFont(font)
        self.distanceThresholdLabel.setObjectName("distanceThresholdLabel")
        self.distance_Layout.addWidget(self.distanceThresholdLabel)
        self.distanceThresholdLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.distanceThresholdLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.distanceThresholdLineEdit.setFont(font)
        self.distanceThresholdLineEdit.setObjectName("distanceThresholdLineEdit")
        self.distanceThresholdLineEdit.setText('30')
        self.distance_Layout.addWidget(self.distanceThresholdLineEdit)
        self.gridLayout.addLayout(self.distance_Layout, 10, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.countThresholdLabel.setDisabled(True)
        self.countThresholdLineEdit.setDisabled(True)
        self.distanceThresholdLineEdit.setDisabled(True)
        self.distanceThresholdLabel.setDisabled(True)
        self.cellsFileOpener.setDisabled(True)
        self.cellsFilePath.setDisabled(True)
        self.cellsFileLabel.setDisabled(True)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cellsFileLabel.setText(_translate("MainWindow", "Open 5G Cells File"))
        self.cellsFileOpener.setText(_translate("MainWindow", "Open"))
        self.startPushButton.setText(_translate("MainWindow", "Create A3A5_Result"))
        self.start2PushButton.setText(_translate("MainWindow", "Create Distance File"))
        self.label.setText(_translate("MainWindow", "Progress: None"))
        self.input_path.setText(_translate("MainWindow", "Path:"))
        self.closestLabel.setText(_translate("MainWindow", "Add closest cell file"))
        self.yesRadioButton.setText(_translate("MainWindow", "Yes"))
        self.noRadioButton.setText(_translate("MainWindow", "No"))
        self.countThresholdLabel.setText(_translate("MainWindow", "Count threshold (int)"))
        self.input_Label.setText(_translate("MainWindow", "Open A3A5 File"))
        self.browse_input.setText(_translate("MainWindow", "Open"))
        self.result_path.setText(_translate("MainWindow", "Path:"))
        self.cellsFilePath.setText(_translate("MainWindow", "Path:"))
        self.result_Label.setText(_translate("MainWindow", "Open save directory\n"
                                                           "(default: last selected/desktop)"))
        self.browse_saveDir.setText(_translate("MainWindow", "Browse"))
        self.distanceThresholdLabel.setText(
            _translate("MainWindow", "Distance threshold in % (float; default: 30%)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
