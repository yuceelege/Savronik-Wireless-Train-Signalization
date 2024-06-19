import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QSizePolicy, QVBoxLayout,QGridLayout, QPushButton, QComboBox,QMainWindow,QShortcut,QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont ,QKeySequence
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from pyqtgraph import mkPen
import pandas as pd
from pyqtgraph import LegendItem, TextItem
from include.createTracks import create_scis_tracks,create_straight_tracks,create_all_tracks
import numpy as np

class GraphWindow(QWidget):
    def __init__(self, selected_station):
        super().__init__()
        self.selected_station = selected_station
        self.init_ui()
        
    def init_ui(self):

        width = 3
        self.closeButton = QPushButton('X', self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.closeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.closeButton.setGeometry(10, 10, 30, 30)
        
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
        self.setGeometry(200, 250, 1000, 700)

        self.setStyleSheet("background-color: white;")
        self.pt_csv = pd.read_csv("bildata/Balise Locations/pt2.csv", sep = ';')
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground('k')
        self.plot_widget.setGeometry(60, 60, 880, 500)
        #self.plot_widget.setFixedWidth(200)
        #self.plot_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.title = QLabel("Bilkent Station",self)
        self.title.setGeometry(420, 20, 160, 40)
        self.title.setStyleSheet("""
        QLabel {
            color: black;
            font-family: 'Arial';
            font-size: 20pt;
            font-weight: bold;
        }
    """)

        #self.plot_widget.plotItem.invertY(True)
        
        
        self.brieftitle = QLabel("Station Information: ",self)
        self.brieftitle.setGeometry(60,580,200,40)
        self.brieftitle.setStyleSheet("""
        QLabel {
            color: black;
            font-family: 'Arial';
            font-size: 20pt;
        }
    """)
        
        ########
        self.train_info = QLabel("Train 1, Expedition ID, Speed, Last Balise",self)
        self.train_info.setGeometry(60,620,300,40)
        self.train_info.setStyleSheet("""
        QLabel {
            color: blue;
            font-family: 'Arial';
            font-size: 15pt;
        }
    """)
        
        ########
        ########
        self.train_info = QLabel("Train 2, Expedition ID, Speed, Last Balise",self)
        self.train_info.setGeometry(60,660,300,40)
        self.train_info.setStyleSheet("""
        QLabel {
            color: blue;
            font-family: 'Arial';
            font-size: 15pt;
        }
    """)
        
        ########
        self.warning_label = QLabel('!!! Violation Alert in Station: \nBilkent', self)
        self.warning_label.setStyleSheet("""
            QLabel {
                font-size: 15pt;    /* Large text size */
                color: red;       /* White text color */
            }
        """)
        self.warning_label.setGeometry(600,600,200,100)
        ########
        
        self.plot_widget.setAspectLocked(True)
        self.gps_data_index = 0
        self.object_dots = {}
        self.object_plots = {}
        self.lastbilkent = pd.read_csv('bildata/Balise Locations/last2.csv',sep =';')
        self.makas_points = pd.read_csv(r"data/pt.csv")
        self.filtered_data = self.makas_points[self.makas_points['station'] == self.statdict[self.selected_station]]
        self.makasX = self.filtered_data['positionX'].tolist()
        self.makasY = self.filtered_data['positionY'].tolist()
        self.makas_names = self.filtered_data['name'].tolist()
        
        self.plot_widget.setBackground("k")
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
            text = TextItem(text=track_name, anchor=(0.5, 0.5),color = 'w')  # Anchor at center
            self.plot_widget.addItem(text)
            text.setPos(mid_x, mid_y+10)
            font = QFont()
            font.setPixelSize(8)  # You can change the size as needed
            text.setFont(font)
        
        self.plot_widget.plot(np.array(self.makasX)*self.xscale, np.array(self.makasY)*self.yscale, pen=None, symbol='s', symbolBrush='b')
        plotItem = self.plot_widget.getPlotItem()
        plotItem.getAxis('bottom').setStyle(showValues=False)
        plotItem.getAxis('left').setStyle(showValues=False)
        
        
        
    def balise_read(self,epc_no):
        balise = epc_no[-1]
        if balise == 'A':
            balise = 10
        return balise
    
    def update_dots(self):
        for obj_id in self.object_dots.keys():
            x = self.object_dots[obj_id][0] * self.xscale
            y = self.object_dots[obj_id][1] * self.yscale
            self.object_plots[obj_id].setData([x], [y])
    
    def projectCoordinate(self,loc,b,e):
        b = np.array(b)
        e = np.array(e)
        loc2 = np.array(loc-b)
        vec = (e-b)/np.linalg.norm(e-b)
        new_coordinate = np.dot(vec,loc2)*vec + b
        return new_coordinate.tolist()
    
    def project2screen(self,loc,b,e,pixelb,pixele):
        b = np.array(b)
        e = np.array(e)
        loc = self.projectCoordinate(loc,b,e)
        pixelb = np.array(pixelb)
        pixele = np.array(pixele)
        ratio = np.linalg.norm(loc-b)/np.linalg.norm(e-b)
        vec = (pixele-pixelb)/np.linalg.norm(pixele-pixelb)
        new_pixel = ratio*np.linalg.norm(pixele-pixelb)*vec + pixelb
        return new_pixel
    
    def handleRouteData(self,row):
        #row = row[0].split(',')        
        balise_id = str(self.balise_read(row[-1]))
        balise_name = "BL" + balise_id + "BIL"
        lookup_id = "BL" + balise_id
        obj_id = row[1]
        y_row = row[3].strip()
        x_row = row[4].strip()
        
        x = float(x_row[:3])+float(x_row[3:])/60
        y = float(y_row[:2])+float(y_row[2:])/60
        
        balise = self.lastbilkent[self.lastbilkent['source'] == lookup_id]
        source = balise['source'].item()
        destination = balise['destination'].item()
        pixelb = [balise['source_X'].item(), balise['source_Y'].item()]
        pixele = [balise['destination_X'].item(), balise['destination_Y'].item()]
        
        beg = self.pt_csv[self.pt_csv['name'] == source]
        eg = self.pt_csv[self.pt_csv['name'] == destination]
        
        b = [beg['longitude'].item(),beg['latitude'].item()]
        e = [eg['longitude'].item(),eg['latitude'].item()]
        
        gps_loc = self.project2screen([x,y],b,e,pixelb,pixele)
        
        x = gps_loc[0]
        y = gps_loc[1]
        
        if obj_id not in self.object_dots.keys():
           self.object_plots[obj_id] = self.plot_widget.plot([x], [y], pen=None, symbol='o', symbolBrush='y', symbolSize=10)
           self.object_dots[obj_id] = [x,y]
           self.update_dots()
        else: 
           self.object_dots[obj_id] = [x,y]
           self.update_dots()
        
        if balise_name[-3:] == self.statdict[self.selected_station]:
            self.trains[row[1]] = balise_name[:-3]
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
            
            


    