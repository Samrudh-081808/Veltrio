import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                            QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton    )
from PyQt5.QtGui import QIcon, QFont          
from PyQt5.QtCore import Qt



class mainWindow(QMainWindow):                                 

    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Veltrio")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_vbox = QVBoxLayout(self)
        



def main():
    app = QApplication([])                        
    window = mainWindow()                        
    window.show()                                 
    app.exec_()                                   
    
if __name__ == "__main__":
    main()

