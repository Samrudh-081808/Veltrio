import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                            QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton    )
from PyQt5.QtGui import QIcon, QFont          
from PyQt5.QtCore import Qt



class mainWindow(QMainWindow):                                 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veltrio")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_vbox = QVBoxLayout()
        central_widget.setLayout(main_vbox)

        body_hbox = QHBoxLayout()
        main_vbox.addWidget(Header())
        main_vbox.addLayout(body_hbox)
        body_hbox.addWidget(SideBar())
        body_hbox.addWidget(Main_Display())
        body_hbox.addWidget(Right_Bar())


class Header(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        header_hbox = QHBoxLayout()
        self.setLayout(header_hbox)
        header_hbox.addWidget(Brand()) 
        header_hbox.addWidget(TopBar())


class Brand(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass


class TopBar(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        topbar_hbox = QHBoxLayout()
        self.setLayout(topbar_hbox)


class SideBar(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        sidebar_vbox = QVBoxLayout()
        self.setLayout(sidebar_vbox)


class Main_Display(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        main_display_vbox = QVBoxLayout()
        self.setLayout(main_display_vbox)


class Right_Bar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        right_bar_vbox = QVBoxLayout()
        self.setLayout(right_bar_vbox)

def main():
    app = QApplication([])                        
    window = mainWindow()                        
    window.show()                                 
    app.exec_()                                   
    
if __name__ == "__main__":
    main()

