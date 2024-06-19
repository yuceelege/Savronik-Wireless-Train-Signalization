import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox,QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
from pyqtgraph import LegendItem

user_credentials = {
    'tarhan': ['22002840', 'Efe Tarhan'],
    'ozmisir': ['22003257', 'Özge Özmısır'],
    'yuceel': ['22003324', 'Ege Yüceel'],
    'balci': ['22003796', 'Gökay Balcı'],
    'ozkurt' : ['22003187', 'Rıfat Özkurt']
}

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login Window')
        self.setGeometry(500, 450, 400, 300)
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_credentials)

        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red')

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if user_credentials.get(username)[0] == password:
            self.accept_credentials(username)
        else: 
            self.error_label.setText('Wrong username or password!')

    def accept_credentials(self,username):
        self.user = user_credentials.get(username)[1]
        self.close()

    def get_result(self):
        return self.user

    def closeEvent(self, event):
        event.accept()
