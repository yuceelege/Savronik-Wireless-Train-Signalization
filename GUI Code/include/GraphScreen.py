import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox,QMainWindow,QShortcut
from PyQt5.QtGui import QPainter, QColor, QPen, QFont ,QKeySequence
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from pyqtgraph import mkPen
import pandas as pd
from pyqtgraph import LegendItem, TextItem
from include.createTracks import create_all_tracks
import numpy as np

class GraphWindow(QWidget):
    def __init__(self, selected_station):
        super().__init__()
        self.selected_station = selected_station
        self.init_ui()
        
    def init_ui(self):
        width = 3
        closeButton = QPushButton('Close', self)
        closeButton.clicked.connect(self.close)
        self.trains = {}
        self.available_pen = QPen()
        self.available_pen.setColor(QColor("green"))  # Set the color of the pen
        self.available_pen.setWidth(width)
        #self.available_pen.setStyle(Qt.DashLine)
        
        self.busy_pen = QPen()
        self.busy_pen.setColor(QColor("red"))  # Set the color of the pen
        self.busy_pen.setWidth(width)
        #self.busy_pen.setStyle(Qt.DashLine)
        
        self.xscale = 1
        self.yscale = 1
        self.statdict = {
            'Demiryurt Station' : 'DEM', 
            'Arıkören Station' : 'ARI', 
            'Karaman Station' : 'KAR', 
            'Kaşınhanı Station':  'KAS', 
            'Çumra Station': 'CUM',
            'Bilkent Station': 'BIL'
            }
        self.setWindowTitle('Railway Map of {}'.format(self.selected_station))
        self.setGeometry(80, 80, 800, 600)
        self.toggle_fullscreen()

        self.setStyleSheet("background-color: black;")

        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground('k')
        #self.plot_widget.plotItem.invertY(True)
        self.plot_widget.setAspectLocked(True)

        self.makas_points = pd.read_csv(r"data/pt.csv")
        self.filtered_data = self.makas_points[self.makas_points['station'] == self.statdict[self.selected_station]]
        self.makasX = self.filtered_data['positionX'].tolist()
        self.makasY = self.filtered_data['positionY'].tolist()
        self.makas_names = self.filtered_data['name'].tolist()
        
        
        self.scis_track_lines = create_scis_tracks(self.selected_station)
        self.str_track_lines = create_straight_tracks(self.selected_station)
        self.all_track_lines = create_all_tracks(self.selected_station)
        self.plotline = {}
        for x, y, name in zip(self.makasX, self.makasY, self.makas_names):
            text = pg.TextItem(text=name, color=(0, 0, 255), anchor=(0, 0))
            text.setPos(np.array(x)*self.xscale, np.array(y)*self.yscale)
            self.plot_widget.addItem(text)
            
        
        for track_name, track_points in self.all_track_lines.items():
            x_pt = [np.array(track_points[0][0])*self.xscale, np.array(track_points[1][0])*self.xscale]
            y_pt = [np.array(track_points[0][1])*self.yscale, np.array(track_points[1][1])*self.yscale]
        
            # Plot the line
            self.plotline[track_name] = self.plot_widget.plot(x_pt, y_pt, pen=self.available_pen)
        
            # Calculate the midpoint
            mid_x = (x_pt[0] + x_pt[1]) / 2
            mid_y = (y_pt[0] + y_pt[1]) / 2
        
            # Create a TextItem at the midpoint
            text = TextItem(text=track_name, anchor=(0.5, 0.5))  # Anchor at center
            self.plot_widget.addItem(text)
            text.setPos(mid_x, mid_y+10)
            font = QFont()
            font.setPixelSize(8)  # You can change the size as needed
            text.setFont(font)
        
        self.plot_widget.plot(np.array(self.makasX)*self.xscale, np.array(self.makasY)*self.yscale, pen=None, symbol='s', symbolBrush='b')

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        
    def balise_read(self,epc_no):
        balise = epc_no[-1]
        if balise == 'A':
            balise = 10
        return balise
    
    def handleRouteData(self,row):
        balise_id = self.balise_read(row[-1])
        balise_name = "BL" + balise_id + "BIL"
        if balise_name[-3:] == self.statdict[self.selected_station]:
            self.trains[row[-1]] = balise_name[:-3]
            self.changeTrackColor()
    
    def changeTrackColor(self):
        for i in self.plotline.keys():
            if i.split('-')[0] in self.trains.values():
                self.plotline[i].setPen(self.busy_pen)
            else:
                self.plotline[i].setPen(self.available_pen)
    
        self.plot_widget.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:  # F key to toggle fullscreen mode
            self.toggle_fullscreen()
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
            


    