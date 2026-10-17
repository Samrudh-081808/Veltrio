import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtGui import (QIcon, QFont)          
from PyQt5.QtCore import (Qt)



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
        main_vbox.addWidget(Header() , 0)
        main_vbox.addLayout(body_hbox , 1)
        body_hbox.addWidget(SideBar() , 1)
        body_hbox.addWidget(Main_Display() , 4)
        body_hbox.addWidget(Right_Bar() , 2)


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
        self.search_field = QLineEdit(self)
        self.export_summary_button = QPushButton(self)
        self.timer_open_button = QPushButton(self)
        self.notification_panel_open_button = QPushButton(self)
        self.profile_icon_button = QPushButton(self)
        self.initUI()
        
    def initUI(self):
        topbar_hbox = QHBoxLayout()
        self.setLayout(topbar_hbox)

        topbar_hbox.addWidget(self.search_field)
        topbar_hbox.addWidget(self.export_summary_button)
        topbar_hbox.addWidget(self.timer_open_button)
        topbar_hbox.addWidget(self.notification_panel_open_button)
        topbar_hbox.addWidget(self.profile_icon_button)

        self.search_field.setPlaceholderText("Search task")
        self.export_summary_button.setText("📂 Export Summary")
        self.timer_open_button.setText("🕛")
        self.notification_panel_open_button.setText("🔔")
        self.profile_icon_button.setText("👤")

        


class SideBar(QWidget):

    def __init__(self):
        super().__init__()
        # Dashboard and stuff
        self.Dashboard_button = QPushButton("Dashboard", self)
        self.Tasks_button = QPushButton("Tasks", self)
        self.Calendar_button = QPushButton("Calendar", self)
        self.Notes_button = QPushButton("Notes", self)

        # List Area
        self.my_list_label = QLabel("My List", self)
        self.add_new_list_button = QPushButton("+", self)
        self.Inbox_button = QPushButton("Inbox", self)
        self.Work_button = QPushButton("Work", self)
        self.Study = QPushButton("Study", self)
        self.Health = QPushButton("Health", self)
        self.Holiday_trip_button = QPushButton("Holiday Trip", self)

        #Workspace Area
        self.Workspace_label = QLabel("Workspace", self)
        self.add_new_workspace_button = QPushButton("+", self)
        self.add_sample_workspace_button_1 = QPushButton("Workspace 1", self)
        self.add_sample_workspace_button_2 = QPushButton("Workspace 2", self)
        self.initUI()
        
    def initUI(self):
        sidebar_vbox = QVBoxLayout()
        self.setLayout(sidebar_vbox)

        #Dashboard and stuff
        Dashboard_container = QWidget()
        dashboard_items_vbox = QVBoxLayout()
        dashboard_items_vbox.addWidget(self.Dashboard_button)
        dashboard_items_vbox.addWidget(self.Tasks_button)
        dashboard_items_vbox.addWidget(self.Calendar_button)
        dashboard_items_vbox.addWidget(self.Notes_button)
        Dashboard_container.setLayout(dashboard_items_vbox)
        sidebar_vbox.addWidget(Dashboard_container)


        # List Area
        list_name_area_container = QWidget()
        list_name_hbox = QHBoxLayout()
        list_name_hbox.addWidget(self.my_list_label)
        list_name_hbox.addStretch(1)
        list_name_hbox.addWidget(self.add_new_list_button)
        list_name_area_container.setLayout(list_name_hbox)
        sidebar_vbox.addWidget(list_name_area_container)

        # List Area
        list_items_container = QWidget()
        list_items_vbox = QVBoxLayout()
        list_items_vbox.addWidget(self.Inbox_button)
        list_items_vbox.addWidget(self.Work_button)
        list_items_vbox.addWidget(self.Study)
        list_items_vbox.addWidget(self.Health)
        list_items_vbox.addWidget(self.Holiday_trip_button)
        list_items_container.setLayout(list_items_vbox)
        sidebar_vbox.addWidget(list_items_container)



        # Workspace Area
        workspace_name_area_container = QWidget()
        workspace_name_hbox = QHBoxLayout()
        workspace_name_hbox.addWidget(self.Workspace_label)
        workspace_name_hbox.addStretch(1)
        workspace_name_hbox.addWidget(self.add_new_workspace_button)
        workspace_name_area_container.setLayout(workspace_name_hbox)
        sidebar_vbox.addWidget(workspace_name_area_container)

        #Workspace Area
        workspace_items_container = QWidget()
        workspace_items_vbox = QVBoxLayout()
        workspace_items_vbox.addWidget(self.add_sample_workspace_button_1)
        workspace_items_vbox.addWidget(self.add_sample_workspace_button_2)
        workspace_items_container.setLayout(workspace_items_vbox)
        sidebar_vbox.addWidget(workspace_items_container)



        sidebar_vbox.addStretch(1)  # Add stretch to push the buttons to the top
        





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

