# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qProg.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(300, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(300, 400))
        MainWindow.setMaximumSize(QtCore.QSize(300, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connection_status = QtWidgets.QLabel(self.centralwidget)
        self.connection_status.setAutoFillBackground(False)
        self.connection_status.setStyleSheet("")
        self.connection_status.setAlignment(QtCore.Qt.AlignCenter)
        self.connection_status.setObjectName("connection_status")
        self.verticalLayout.addWidget(self.connection_status)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(70, 50))
        self.tabWidget.setObjectName("tabWidget")
        self.wire_tab = QtWidgets.QWidget()
        self.wire_tab.setObjectName("wire_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.wire_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.wire_label = QtWidgets.QLabel(self.wire_tab)
        self.wire_label.setObjectName("wire_label")
        self.verticalLayout_2.addWidget(self.wire_label)
        self.wire_select = QtWidgets.QComboBox(self.wire_tab)
        self.wire_select.setObjectName("wire_select")
        self.verticalLayout_2.addWidget(self.wire_select)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.wire_progress = QtWidgets.QProgressBar(self.wire_tab)
        self.wire_progress.setProperty("value", 0)
        self.wire_progress.setTextVisible(False)
        self.wire_progress.setObjectName("wire_progress")
        self.verticalLayout_2.addWidget(self.wire_progress)
        self.frame_2 = QtWidgets.QFrame(self.wire_tab)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.wire_btn = QtWidgets.QToolButton(self.frame_2)
        self.wire_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.wire_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.wire_btn.setText("")
        self.wire_btn.setObjectName("wire_btn")
        self.horizontalLayout_2.addWidget(self.wire_btn)
        self.wire_read_btn = QtWidgets.QToolButton(self.frame_2)
        self.wire_read_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.wire_read_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.wire_read_btn.setObjectName("wire_read_btn")
        self.horizontalLayout_2.addWidget(self.wire_read_btn)
        self.wire_write_btn = QtWidgets.QToolButton(self.frame_2)
        self.wire_write_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.wire_write_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.wire_write_btn.setObjectName("wire_write_btn")
        self.horizontalLayout_2.addWidget(self.wire_write_btn)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.tabWidget.addTab(self.wire_tab, "")
        self.rom_tab = QtWidgets.QWidget()
        self.rom_tab.setObjectName("rom_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.rom_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rom_label = QtWidgets.QLabel(self.rom_tab)
        self.rom_label.setObjectName("rom_label")
        self.verticalLayout_3.addWidget(self.rom_label)
        self.rom_select = QtWidgets.QComboBox(self.rom_tab)
        self.rom_select.setObjectName("rom_select")
        self.verticalLayout_3.addWidget(self.rom_select)
        spacerItem1 = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.rom_progress = QtWidgets.QProgressBar(self.rom_tab)
        self.rom_progress.setProperty("value", 0)
        self.rom_progress.setTextVisible(False)
        self.rom_progress.setObjectName("rom_progress")
        self.verticalLayout_3.addWidget(self.rom_progress)
        self.frame = QtWidgets.QFrame(self.rom_tab)
        self.frame.setMinimumSize(QtCore.QSize(0, 70))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rom_clear_btn = QtWidgets.QToolButton(self.frame)
        self.rom_clear_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.rom_clear_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.rom_clear_btn.setObjectName("rom_clear_btn")
        self.horizontalLayout.addWidget(self.rom_clear_btn)
        self.rom_read_btn = QtWidgets.QToolButton(self.frame)
        self.rom_read_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.rom_read_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.rom_read_btn.setObjectName("rom_read_btn")
        self.horizontalLayout.addWidget(self.rom_read_btn)
        self.rom_write_btn = QtWidgets.QToolButton(self.frame)
        self.rom_write_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.rom_write_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.rom_write_btn.setObjectName("rom_write_btn")
        self.horizontalLayout.addWidget(self.rom_write_btn)
        self.verticalLayout_3.addWidget(self.frame)
        self.tabWidget.addTab(self.rom_tab, "")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.settings_tab)
        self.gridLayout.setObjectName("gridLayout")
        self.baud_combo = QtWidgets.QComboBox(self.settings_tab)
        self.baud_combo.setObjectName("baud_combo")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.baud_combo.addItem("")
        self.gridLayout.addWidget(self.baud_combo, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 47, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.settings_tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.settings_tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.port_combo = QtWidgets.QComboBox(self.settings_tab)
        self.port_combo.setObjectName("port_combo")
        self.gridLayout.addWidget(self.port_combo, 0, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.settings_tab)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.save_config_btn = QtWidgets.QToolButton(self.frame_3)
        self.save_config_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.save_config_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.save_config_btn.setObjectName("save_config_btn")
        self.horizontalLayout_3.addWidget(self.save_config_btn)
        self.read_btn_5 = QtWidgets.QToolButton(self.frame_3)
        self.read_btn_5.setMinimumSize(QtCore.QSize(70, 50))
        self.read_btn_5.setMaximumSize(QtCore.QSize(70, 50))
        self.read_btn_5.setText("")
        self.read_btn_5.setObjectName("read_btn_5")
        self.horizontalLayout_3.addWidget(self.read_btn_5)
        self.connect_btn = QtWidgets.QToolButton(self.frame_3)
        self.connect_btn.setMinimumSize(QtCore.QSize(70, 50))
        self.connect_btn.setMaximumSize(QtCore.QSize(70, 50))
        self.connect_btn.setObjectName("connect_btn")
        self.horizontalLayout_3.addWidget(self.connect_btn)
        self.gridLayout.addWidget(self.frame_3, 6, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.settings_tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.timeout_slider = QtWidgets.QSlider(self.settings_tab)
        self.timeout_slider.setMaximum(10)
        self.timeout_slider.setProperty("value", 1)
        self.timeout_slider.setOrientation(QtCore.Qt.Horizontal)
        self.timeout_slider.setObjectName("timeout_slider")
        self.gridLayout.addWidget(self.timeout_slider, 2, 1, 1, 1)
        self.connect_progress = QtWidgets.QProgressBar(self.settings_tab)
        self.connect_progress.setMaximum(10)
        self.connect_progress.setProperty("value", 0)
        self.connect_progress.setTextVisible(False)
        self.connect_progress.setObjectName("connect_progress")
        self.gridLayout.addWidget(self.connect_progress, 5, 0, 1, 2)
        self.tabWidget.addTab(self.settings_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuClose = QtWidgets.QMenu(self.menubar)
        self.menuClose.setObjectName("menuClose")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRead = QtWidgets.QAction(MainWindow)
        self.actionRead.setObjectName("actionRead")
        self.actionWrite = QtWidgets.QAction(MainWindow)
        self.actionWrite.setObjectName("actionWrite")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionAdd_Chip = QtWidgets.QAction(MainWindow)
        self.actionAdd_Chip.setObjectName("actionAdd_Chip")
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuClose.addAction(self.actionRefresh)
        self.menuClose.addAction(self.actionAdd_Chip)
        self.menuClose.addSeparator()
        self.menuClose.addAction(self.actionClose)
        self.menubar.addAction(self.menuClose.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.actionClose.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Programmer"))
        self.connection_status.setText(_translate("MainWindow", "PROGRAMMER CONNECTION"))
        self.wire_label.setText(_translate("MainWindow", "IC Model:"))
        self.wire_select.setToolTip(_translate("MainWindow", "Select Chip Model"))
        self.wire_select.setStatusTip(_translate("MainWindow", "Select Chip Model"))
        self.wire_read_btn.setToolTip(_translate("MainWindow", "Read Chip to file"))
        self.wire_read_btn.setStatusTip(_translate("MainWindow", "Read Chip to file"))
        self.wire_read_btn.setText(_translate("MainWindow", "Read"))
        self.wire_write_btn.setToolTip(_translate("MainWindow", "Write file to Chip"))
        self.wire_write_btn.setStatusTip(_translate("MainWindow", "Write file to Chip"))
        self.wire_write_btn.setText(_translate("MainWindow", "Write"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wire_tab), _translate("MainWindow", "OneWire"))
        self.rom_label.setText(_translate("MainWindow", "IC Model:"))
        self.rom_select.setToolTip(_translate("MainWindow", "Select Chip Model"))
        self.rom_select.setStatusTip(_translate("MainWindow", "Select Chip Model"))
        self.rom_clear_btn.setToolTip(_translate("MainWindow", "Clear Chip"))
        self.rom_clear_btn.setStatusTip(_translate("MainWindow", "Clear Chip"))
        self.rom_clear_btn.setText(_translate("MainWindow", "Clear"))
        self.rom_read_btn.setToolTip(_translate("MainWindow", "Read Chip to file"))
        self.rom_read_btn.setStatusTip(_translate("MainWindow", "Read Chip to file"))
        self.rom_read_btn.setText(_translate("MainWindow", "Read"))
        self.rom_write_btn.setToolTip(_translate("MainWindow", "Save file to Chip"))
        self.rom_write_btn.setStatusTip(_translate("MainWindow", "Save file to Chip"))
        self.rom_write_btn.setText(_translate("MainWindow", "Write"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rom_tab), _translate("MainWindow", "EPROM"))
        self.baud_combo.setToolTip(_translate("MainWindow", "Serial port baud, default 115200"))
        self.baud_combo.setItemText(0, _translate("MainWindow", "4800"))
        self.baud_combo.setItemText(1, _translate("MainWindow", "9600"))
        self.baud_combo.setItemText(2, _translate("MainWindow", "19200"))
        self.baud_combo.setItemText(3, _translate("MainWindow", "38400"))
        self.baud_combo.setItemText(4, _translate("MainWindow", "57600"))
        self.baud_combo.setItemText(5, _translate("MainWindow", "74880"))
        self.baud_combo.setItemText(6, _translate("MainWindow", "115200"))
        self.baud_combo.setItemText(7, _translate("MainWindow", "230400"))
        self.baud_combo.setItemText(8, _translate("MainWindow", "250000"))
        self.label_3.setText(_translate("MainWindow", "Timeout"))
        self.label_2.setText(_translate("MainWindow", "Baud Rate"))
        self.port_combo.setToolTip(_translate("MainWindow", "connected Serial port"))
        self.save_config_btn.setToolTip(_translate("MainWindow", "Save configuration settings"))
        self.save_config_btn.setStatusTip(_translate("MainWindow", "Save configuration settings"))
        self.save_config_btn.setText(_translate("MainWindow", "Save"))
        self.connect_btn.setToolTip(_translate("MainWindow", "Connect to programmer"))
        self.connect_btn.setStatusTip(_translate("MainWindow", "Connect to programmer"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "Port"))
        self.timeout_slider.setToolTip(_translate("MainWindow", "Serial port timeout"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), _translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "About"))
        self.menuClose.setTitle(_translate("MainWindow", "File"))
        self.actionRead.setText(_translate("MainWindow", "Read"))
        self.actionWrite.setText(_translate("MainWindow", "Write"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionHelp.setStatusTip(_translate("MainWindow", "Show programmer help..."))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setStatusTip(_translate("MainWindow", "About Programmer..."))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setStatusTip(_translate("MainWindow", "Quit programmer..."))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionRefresh.setStatusTip(_translate("MainWindow", "Refresh COM ports list..."))
        self.actionAdd_Chip.setText(_translate("MainWindow", "Add Chip"))
        self.actionAdd_Chip.setStatusTip(_translate("MainWindow", "Add chip to list..."))