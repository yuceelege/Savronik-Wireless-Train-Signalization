import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,QSizePolicy, QVBoxLayout,QGridLayout, QPushButton, QComboBox,QMainWindow,QShortcut,QHBoxLayout
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
        self.statdict = {
            'Demiryurt Station' : 'DEM', 
            'Arıkören Station' : 'ARI', 
            'Karaman Station' : 'KAR', 
            'Kaşınhanı Station':  'KAS', 
            'Çumra Station': 'CUM',
            'Bilkent Station': 'BIL'
            }
        self.line_width = 3
        self.width = 1470
        self.height = 956
        self.Res = (self.width,self.height)
        self.selected_station = selected_station
        self.balise_data = pd.read_csv("bildata/Balise Locations v2/pt3.csv", sep = ';')
        self.lastbilkent = pd.read_csv('bildata/Balise Locations v2/last3.csv',sep =';')
        self.xscale = 1
        self.yscale = 1
        self.all_track_lines = create_all_tracks(self.selected_station)
        self.train_cnt = 0
        self.all_trains = {}
        self.warning_label = 0
        self.init_ui(background_color="white")
        self.showFullScreen()
        
        
    def init_ui(self,background_color):        
        self.createCloseButton([10,10,30,30])
        self.createTrackPens()
        self.setWindowTitle('Railway Map of {}'.format(self.selected_station))
        self.setStyleSheet("background-color: {};".format(background_color))
        self.createPlotWidget([ 60, 120, 1350, 500])
        self.createStationName(self.selected_station,[650,60,400,30])
        self.createBriefTitle([60,680,200,20])
        #self.createWarning([600,600,200,100])
        self.train_infos = {}
        self.plot_widget.setAspectLocked(True)
        self.object_dots = {}
        self.object_plots = {}
        self.object_names = {}
        self.plotline = {}
        self.drawTracks()
        
        plotItem = self.plot_widget.getPlotItem()
        plotItem.getAxis('bottom').setStyle(showValues=False)
        plotItem.getAxis('left').setStyle(showValues=False)
        
    def createBriefTitle(self,orientation):
        self.brieftitle = QLabel("Station Information: ",self)
        self.brieftitle.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
        self.brieftitle.setStyleSheet("""
        QLabel {
            color: black;
            font-family: 'Segoe UI';
            font-size: 20pt;
        }
    """)
    
    def createCloseButton(self,orientation):
        self.closeButton = QPushButton('X', self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.closeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.closeButton.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
    
    
    def createWarning(self,orientation):
        self.list_parser()
        warns = self.all_warn
        text = ""
        for i in range(len(warns)):
            warning = warns[i]
            if "speedWarning" in warning:
                text += "{}! --> Train {} goes with excess speed {} km/h on block BL{}".format(warning[3],warning[0],round(float(warning[2])*1.8,2),warning[1][-1]) + "\n"
            elif "proximityWarning" in warning:
                text += "{}! --> Trains {} and {} are on the blocks BL{} and BL{} with risk of collision".format(warning[-1],warning[0],warning[1],warning[2][-1],warning[3][-1]) + "\n"
        
        if self.warning_label == 0:
            self.warning_label = QLabel(text, self)
            self.warning_label.setStyleSheet("""
                QLabel {
                    font-size: 15pt;    /* Large text size */
                    color: red;       /* White text color */
                }
            """)
            self.warning_label.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
            self.warning_label.setVisible(True)
        else: 
            self.warning_label.setText(text)
        
    def removeWarning(self):
        self.warning_label.hide()

    def createTrackPens(self):
        self.trains = {}
        self.available_pen = QPen()
        self.available_pen.setColor(QColor("green"))  # Set the color of the pen
        self.available_pen.setWidth(self.line_width)
        #self.available_pen.setStyle(Qt.DashLine)
        self.busy_pen = QPen()
        self.busy_pen.setColor(QColor("red"))  # Set the color of the pen
        self.busy_pen.setWidth(self.line_width)
        #self.busy_pen.setStyle(Qt.DashLine)
    
    def createStationName(self,name,orientation):
        self.title = QLabel(name,self)
        self.title.setGeometry(orientation[0], orientation[1], orientation[2], orientation[3])
        self.title.setStyleSheet("""
        QLabel {
            color: black;
            font-family: 'Segoe UI';
            font-size: 20pt;
            font-weight: bold;
        }
    """)
    def createTrainInfo(self,name,text,orientation):
        self.train_infos[name] = QLabel(text,self)
        self.train_infos[name].setGeometry(orientation[0],orientation[1],orientation[2],orientation[3])
        self.train_infos[name].setStyleSheet("""
        QLabel {
            color: blue;
            font-family: 'Segoe UI';
            font-size: 15pt;
        }
    """)
        self.train_infos[name].setVisible(True)
    
    
    
    def updateAllInfo(self):
        train_count = len(self.object_dots.keys())
        train_names = [i for i in self.object_dots.keys()]
        for i in range(train_count):
            row = self.all_trains[train_names[i]]
            if train_names[i] in self.train_infos.keys():
                new_text = "Train: {},Expedition ID: {},Speed: {} km/h, Last Balise: {}".format(row[1],row[2],round(float(row[5])*1.8,2),"BL" + str(self.balise_read(row[-1])))
                self.train_infos[train_names[i]].setText(new_text)
            else:
                new_text = "Train: {},Expedition ID: {},Speed: {} km/h, Last Balise: {}".format(row[1],row[2],round(float(row[5])*1.8,2),"BL" + str(self.balise_read(row[-1])))
                self.createTrainInfo(train_names[i],new_text,[60,700+20*i,1000,20])

                
                
    def createPlotWidget(self,orientation):
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground('k')
        self.plot_widget.setGeometry(orientation[0],orientation[1],orientation[2],orientation[3])
        
    def balise_read(self,epc_no):
        balise = epc_no[-1]
        if balise == 'A':
            balise = 10
        return balise
    
    def drawTracks(self):
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
        
    def update_dots(self):
        for obj_id in self.object_dots.keys():
            x = self.object_dots[obj_id][0] * self.xscale
            y = self.object_dots[obj_id][1] * self.yscale
            self.object_plots[obj_id].setData([x], [y])
            self.object_names[obj_id].setPos(x, y)
    
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
    
    def keep_alphanumeric(self,input_string):
        result = ''.join([char for char in input_string if char.isalnum()])
        return result
    
    def list_parser(self):
        self.all_warn = []
        for warning in self.warning_list:
            dum_warn = []
            if warning.strip() != '0':
                m = warning.split(" ")
                for word in m:
                    if word.strip() != '':
                        word = word.strip()
                        dum_warn.append(word)
                self.all_warn.append(dum_warn)
        return self.all_warn
    
    def handleWarningData(self,warning):
        self.warning_list = warning.split(",")
        if self.warning_list != []:
            self.createWarning([700,760,900,80])
        else:
            if self.warning_label != 0:
                self.removeWarning()
    def handleRouteData(self,row):
        self.all_trains[row[1]] = row
        balise_id = str(self.balise_read(row[-1]))
        balise_name = "BL" + balise_id + "BIL"
        lookup_id = "BL" + balise_id
        obj_id = row[1]
        y_row = row[3].strip()
        x_row = row[4].strip()
        
        x = float(x_row[:3])+float(x_row[3:])/60
        y = float(y_row[:2])+float(y_row[2:])/60
        
        balise = self.lastbilkent[self.lastbilkent['source'] == lookup_id]
        #print(self.lastbilkent)
        #print(balise['source'])
        source = balise['source'].item()
        destination = balise['destination'].item()
        pixelb = [balise['source_X'].item(), balise['source_Y'].item()]
        pixele = [balise['destination_X'].item(), balise['destination_Y'].item()]
        
        beg = self.balise_data[self.balise_data['name'] == source]
        eg = self.balise_data[self.balise_data['name'] == destination]
        
        b = [beg['Longitude'].item(),beg['Latitude'].item()]
        e = [eg['Longitude'].item(),eg['Latitude'].item()]
        
        gps_loc = self.project2screen([x,y],b,e,pixelb,pixele)
        
        x = gps_loc[0]
        y = gps_loc[1]
        
        if obj_id not in self.object_dots.keys():
           self.object_plots[obj_id] = self.plot_widget.plot([x], [y], pen=None, symbol='o', symbolBrush='y', symbolSize=10)
           self.object_names[obj_id] = TextItem(text=obj_id, color='w', anchor=(0.5, -1))
           self.object_names[obj_id].setPos(x, y)
           self.plot_widget.addItem(self.object_names[obj_id])
           self.object_dots[obj_id] = [x,y]
           self.update_dots()
        else: 
           self.object_dots[obj_id] = [x,y]
           self.update_dots()
        
        if balise_name[-3:] == self.statdict[self.selected_station]:
            self.trains[row[1]] = balise_name[:-3]
            self.changeTrackColor()
            
            
        self.updateAllInfo()

    
    def changeTrackColor(self):
        for i in self.plotline.keys():
            if i.split('-')[0] in self.trains.values():
                self.plotline[i].setPen(self.busy_pen)
            else:
                self.plotline[i].setPen(self.available_pen)
    
        self.plot_widget.repaint()

            
            


    