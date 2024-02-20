import json, platform
from time import sleep

import serial
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from serial.tools import list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QWidget, QDialogButtonBox, QLabel, QVBoxLayout, QComboBox, QLineEdit
from ui import Ui_MainWindow

BUFFER_SIZE = 32
SERIAL_PREFIX = '/dev/' if platform.system()=='Linux' else ''
ROMS_DIR = 'roms'


class AddChipDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new Chip")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox= QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            return        
    
        self.layout = QVBoxLayout()
        self.category = QComboBox(self)
        self.category.addItems(self.settings.get("CHIPS",{}).keys())
        self.name = QLineEdit(self)
        self.total = QLineEdit(self)
        self.layout.addWidget(QLabel("Chip type:"))
        self.layout.addWidget(self.category)
        self.layout.addWidget(QLabel("Chip name:"))
        self.layout.addWidget(self.name)
        self.layout.addWidget(QLabel("Total Memory:"))
        self.layout.addWidget(self.total)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        category = self.category.currentText()
        name = self.name.text()
        total = self.total.text()
        try:
            b = {'B':1, 'b':1/8}.get(total[-1],1)
            f = {'k':1024, 'm':1024*1024}.get(total[-2].lower(), 1)
            t = int(total.split(' ')[0])
            if (t*f*b)%BUFFER_SIZE == 0:
                blocks = str(int(t*f*b/BUFFER_SIZE))
                self.settings["CHIPS"][category][name]={"total":total, "blocks":blocks}
                with open('settings.json', 'w') as f:
                    json.dump(self.settings, f, indent=2)
                return super().accept()
        except:
            return super().reject()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.programmer_ready = False
        self.pr = None
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            pass
        self.port_combo.addItems([port.name for port in list_ports.comports()])
        self.port_combo.setCurrentText(str(self.settings.get('PORT', 'COM1')))
        self.baud_combo.setCurrentText(str(self.settings.get('BAUD', 9800)))
        self.timeout_slider.setValue(int(self.settings.get('TIMEOUT', 0.1) * 10))
        self.wire_select.addItems(list(self.settings.get('CHIPS', {'WIRE':{}}).get('WIRE', {}).keys()))
        self.rom_select.addItems(list(self.settings.get('CHIPS', {'EEPROM':{}}).get('EEPROM', {}).keys()))
        self.rom_progress.hide()
        self.wire_progress.hide()
        self.connect_progress.hide()

        self.actionAbout.triggered.connect(self.show_about)
        self.save_config_btn.clicked.connect(self.save_settings)
        self.connect_btn.clicked.connect(self.connect_programmer)
        self.wire_read_btn.clicked.connect(self.read_1wire)
        self.wire_write_btn.clicked.connect(self.write_1wire)
        self.rom_read_btn.clicked.connect(self.read_rom)
        self.actionRefresh.triggered.connect(self.refresh_ports)
        self.actionAdd_Chip.triggered.connect(self.add_chip)

    def add_chip(self):
        dlg = AddChipDialog()
        if dlg.exec_() == QDialog.Accepted:
            try:
                with open('settings.json', 'r') as f:
                    self.settings = json.load(f)
            except:
                pass
            self.wire_select.clear()
            self.rom_select.clear()
            self.wire_select.addItems(list(self.settings.get('CHIPS', {'WIRE':{}}).get('WIRE', {}).keys()))
            self.rom_select.addItems(list(self.settings.get('CHIPS', {'EEPROM':{}}).get('EEPROM', {}).keys()))

    def refresh_ports(self):
        self.statusbar.showMessage('Refreshing COM ports...')
        self.port_combo.clear()
        self.port_combo.addItems([port.name for port in list_ports.comports()])
        self.statusbar.showMessage('Refreshing COM ports...Done.', 2000)

    def show_about(self):
        msg = QMessageBox()
        msg.setWindowTitle('About Us...')
        msg.setText('ARM Programmer')
        msg.setInformativeText('Arpa Medical Co')
        # msg.setIcon(QMessageBox.Information)
        img = QPixmap('logo.jpeg').scaled(50,50)
        msg.setIconPixmap(img)
        msg.setDetailedText('This Application can program 1Wire and EEPROM Chips. Currently supported chips are: ' +
                            f"{','.join(list(self.settings['CHIPS']['WIRE'].keys()) + list(self.settings['CHIPS']['EEPROM'].keys()))}")
        msg.setStandardButtons(QMessageBox.Close)
        msg.exec_()

    def save_settings(self):
        self.statusbar.showMessage('Saving Configuration Settings...')
        self.settings['BAUD'] = int(self.baud_combo.currentText())
        self.settings['PORT'] = self.port_combo.currentText()
        self.settings['TIMEOUT'] = self.timeout_slider.value() / 10
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)
        self.statusbar.showMessage('Saving Configuration Settings...Done.', 2000)

    def ic_blocks(self, category, name):
        return 'M'+self.settings["CHIPS"][category][name]['blocks']

    def connect_programmer(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Error!')
        
        self.statusbar.showMessage('Connecting...')
        try:
            self.pr = serial.Serial(port= SERIAL_PREFIX + self.port_combo.currentText(),
                                    baudrate=int(self.baud_combo.currentText()),
                                    timeout=int(self.timeout_slider.value() / 10))
            self.pr.isOpen()
            self.pr.reset_input_buffer()
            self.connect_progress.show()
            for _ in range(11):
                self.connect_progress.setValue(_)
                self.pr.write(b'C')
                sleep(1)
                r = self.pr.read()
                if r == b'>':
                    self.connection_status.setText('CONNECTED')
                    self.pr.reset_input_buffer()
                    sleep(1)
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle('Successful')
                    msg.setText("Successfully Connected.")
                    msg.exec_()
                    self.programmer_ready = True
                    self.tabWidget.setCurrentIndex(0)
                    break
                elif _==10:
                    msg.setText("Connection Timed out.")
                    msg.exec_()
            self.statusbar.showMessage('Done.', 2000)
            self.connect_progress.hide()
        except serial.serialutil.SerialException:
            msg.setText('Wrong Port or Permission Denied.')
            msg.exec_()

    def read_1wire(self):
        # DS2506 : 64kb = 2000*32
        category = "WIRE"
        name = self.wire_select.currentText()
        blocks = self.ic_blocks(category, name)
        if self.programmer_ready:
            try:
                file_name, _ = QFileDialog.getSaveFileName(self, "Select File", ROMS_DIR, "ROM files (*.rom)")
                if file_name:
                    print('Reading...', end='')
                    self.pr.write(b'S1')
                    sleep(1)
                    self.pr.write(blocks.encode('utf-8'))
                    sleep(1)
                    print(self.pr.readall())
                    sleep(1)
                    self.pr.write(b'R1')
                    sleep(1)
                    with open(file_name, 'bw') as file:
                        file.write(self.pr.readall())
                    print('Done.')
            except serial.serialutil.SerialException:
                self.programmer_ready = False
                self.tabWidget.setCurrentIndex(2)
                QMessageBox.critical(self, 'Error', 'Programmer is not responding, please reconnect.', QMessageBox.Ok)
        else:
            self.tabWidget.setCurrentIndex(2)

    def write_1wire(self):
        category = "WIRE"
        name = self.wire_select.currentText()
        blocks = self.ic_blocks(category, name)
        if self.programmer_ready:
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File", ROMS_DIR, "ROM files (*.rom)")
            if file_name:
                print('Writing...', end='')
                self.pr.write(b'S1')
                sleep(1)
                self.pr.write(blocks.encode('utf-8'))
                sleep(1)
                print(self.pr.readall())
                sleep(1)
                self.pr.write(b'W1')
                sleep(1)
                with open(file_name, 'br') as file:
                    self.pr.write(file.read())
                print('Done.')
                sleep(5)
                print(self.pr.readall())

        else:
            self.programmer_ready = False
            self.tabWidget.setCurrentIndex(2)
            QMessageBox.critical(self, 'Error', 'Programmer is not responding, please reconnect.', QMessageBox.Ok)

    def read_rom(self):
        blocks = self.ic_blocks("EEPROM", self.rom_select.currentText())
        if self.programmer_ready:
            file_name, _ = QFileDialog.getSaveFileName(self, "Select File", ROMS_DIR, "ROM files (*.rom)")
            if file_name:
                print('Reading...', end='')
                self.pr.write(b'S0')
                sleep(1)
                self.pr.write(blocks.encode('utf-8'))
                sleep(1)
                print(self.pr.readall())
                sleep(1)
                self.pr.write(b'RR')
                sleep(1)
                with open(file_name, 'bw') as file:
                    file.write(self.pr.readall())
                print('Done.')
        else:
            self.programmer_ready = False
            self.tabWidget.setCurrentIndex(2)
            QMessageBox.critical(self, 'Error', 'Programmer is not responding, please reconnect.', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

m = 0xd35400

# try:
#     pr = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=0.1)
#     pr.isOpen()
#     sleep(2)
#     pr.write(b'C')
#     print(pr.read())
#     pr.write(b'R1')
#     sleep(1)
#     s = pr.readall()
#     print(s)
#     with open('knee3T.CoilID', 'bw') as f:
#         f.write(s)
# except PermissionError:
#     print('permission')
