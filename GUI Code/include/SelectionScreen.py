import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox,QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
from pyqtgraph import LegendItem
from include.GraphScreen import GraphWindow

class StationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('Station Selection Window')
        self.setGeometry(500, 450, 400, 300)
        self.station_selector = QComboBox(self)
        self.station_selector.addItem('-')
        self.station_selector.addItems(['Demiryurt Station', 'Arıkören Station', 'Karaman Station', 'Kaşınhanı Station', 'Çumra Station','Test Station','Bilkent Station'])
        self.station_selector.currentTextChanged.connect(self.show_graph)
        layout = QVBoxLayout()
        layout.addWidget(self.station_selector)
        self.setLayout(layout)
    def show_graph(self, selected_station):
        self.selected_station = selected_station
        self.close()
    def get_result(self):
        return self.selected_station
    def closeEvent(self, event):
        event.accept()