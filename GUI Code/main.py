import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
import firebase_admin
from firebase_admin import credentials, db
import time
from include.LoginScreen import LoginWindow
from include.SelectionScreen import StationWindow
from include.GraphScreen_v5 import GraphWindow

class FirebaseClient(QThread):
    service_account_path = '/Users/efetarhan/Desktop/Savronik/GUI/include/serviceAccountKey.json'  # Update the path
    database_url = 'https://wireless-train-signalization-default-rtdb.europe-west1.firebasedatabase.app/'  # Your Firebase database URL
    reference_path = 'data'
    message_received = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.initial_data_loaded = False
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.service_account_path)
            firebase_admin.initialize_app(cred, {'databaseURL': self.database_url})

    def listener(self, event):
        if not self.initial_data_loaded:
            self.initial_data_loaded = True
            return 
        message = event.data if event.data else {}
        if type(message) == dict:
            message = list(message.values())[0]
            message = checkData(message)
        elif type(message) == str:
            message = checkData(message)
        if message != -1 :
            self.message_received.emit(message)

    def run(self):
        ref = db.reference(self.reference_path)
        ref.listen(self.listener)
        while True:
            time.sleep(1)


class WarningClient(QThread):
    service_account_path = '/Users/efetarhan/Desktop/Savronik/GUI/include/serviceAccountKey.json'
    database_url = 'https://wireless-train-signalization-default-rtdb.europe-west1.firebasedatabase.app/'
    reference_path = 'warning'
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.service_account_path)
            firebase_admin.initialize_app(cred, {'databaseURL': self.database_url})

    def listener(self, event):
        # Get all data each time, no initial data check
        message = event.data if event.data else ""

        self.message_received.emit(message)

    def run(self):
        ref = db.reference(self.reference_path)
        ref.listen(self.listener)
        while True:
            time.sleep(1)

def checkData(data):    
    if data[0] == "":
        data = " " + data
    if len([i for i in data.split(',') if i != '']) != 7:
        return -1
    else:
        return data.split(",")
                                        
def createLoginWindow():
    dialog = LoginWindow()
    dialog.exec_()
    return dialog.get_result()


def createStationWindow():
    dialog = StationWindow()
    dialog.exec_()
    return dialog.get_result()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = createLoginWindow()
    print(f'{login} has logged into the system!')
    station = createStationWindow()
    print(f'{station} is selected!')
    graph_window = GraphWindow(station)
    graph_window.show()
    
    firebase_client = FirebaseClient()
    firebase_client.message_received.connect(graph_window.handleRouteData)
    firebase_client.start()
    
    warning_client = WarningClient()
    warning_client.message_received.connect(graph_window.handleWarningData)
    warning_client.start()
    
    


    sys.exit(app.exec_())
