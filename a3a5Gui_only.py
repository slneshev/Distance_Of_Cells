# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'a3a5Gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
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
        self.gridLayout.addLayout(self.cells_Layout, 2, 0, 1, 1)
        self.action_Layout = QtWidgets.QHBoxLayout()
        self.action_Layout.setObjectName("action_Layout")
        self.startPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.startPushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.startPushButton.setFont(font)
        self.startPushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startPushButton.setObjectName("startPushButton")
        self.action_Layout.addWidget(self.startPushButton, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.action_Layout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.action_Layout, 9, 0, 1, 1)
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
        self.addClosest_Layout.addWidget(self.yesRadioButton, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.noRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.noRadioButton.setFont(font)
        self.noRadioButton.setChecked(True)
        self.noRadioButton.setObjectName("noRadioButton")
        self.yes_no_buttonGroup.addButton(self.noRadioButton)
        self.addClosest_Layout.addWidget(self.noRadioButton, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
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
        self.gridLayout.addLayout(self.count_Layout, 7, 0, 1, 1)
        self.input_Layout = QtWidgets.QHBoxLayout()
        self.input_Layout.setObjectName("input_Layout")
        self.input_Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.input_Label.setFont(font)
        self.input_Label.setObjectName("input_Label")
        self.input_Layout.addWidget(self.input_Label, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.browse_input = QtWidgets.QPushButton(self.centralwidget)
        self.browse_input.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browse_input.setFont(font)
        self.browse_input.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browse_input.setObjectName("browse_input")
        self.input_Layout.addWidget(self.browse_input)
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
        self.gridLayout.addWidget(self.cellsFilePath, 3, 0, 1, 1)
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
        self.result_layout.addWidget(self.result_Label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.browse_saveDir = QtWidgets.QPushButton(self.centralwidget)
        self.browse_saveDir.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.browse_saveDir.setFont(font)
        self.browse_saveDir.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browse_saveDir.setObjectName("browse_saveDir")
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
        self.distance_Layout.addWidget(self.distanceThresholdLineEdit)
        self.gridLayout.addLayout(self.distance_Layout, 8, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cellsFileLabel.setText(_translate("MainWindow", "Open 5G Cells File"))
        self.cellsFileOpener.setText(_translate("MainWindow", "Open"))
        self.startPushButton.setText(_translate("MainWindow", "Start"))
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
        self.distanceThresholdLabel.setText(_translate("MainWindow", "Distance threshold in % (float; default: 30%)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
