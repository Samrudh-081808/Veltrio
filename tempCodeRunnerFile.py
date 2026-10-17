import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout,
                             QButtonGroup, QPushButton, QLineEdit)
from PyQt5.QtGui import (QIcon, QFont, QPixmap, QImage)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from pathlib import Path

SIDEBAR_W = 240
HEADER_H = 64
LOGO_PATH = Path(__file__).parent / "Resources" / "Images_" / "Veltrio Teal Ribbon Logo.png"  # adjust to your tree


def add_card_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(10)
    shadow.setOffset(0, 2)
    shadow.setColor(QColor(0, 0, 0, 30))   # about 12% black, keep it faint
    widget.setGraphicsEffect(shadow)

def add_control_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(8)
    shadow.setOffset(0, 1)
    shadow.setColor(QColor(0, 0, 0, 22))   # fainter than the cards
    widget.setGraphicsEffect(shadow)



class mainWindow(QMainWindow):                                 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veltrio")
        self.initUI()

    def initUI(self):
        self.setStyleSheet("QMainWindow { background-color: #F5F5F3; }")
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: #F5F5F3;")
        self.setCentralWidget(central_widget)

        main_vbox = QVBoxLayout()
        central_widget.setLayout(main_vbox)

        body_hbox = QHBoxLayout()
        main_vbox.addWidget(Header() , 0)
        main_vbox.addLayout(body_hbox , 1)
        body_hbox.addWidget(SideBar() , 2)
        body_hbox.addWidget(Main_Display() , 6)
        body_hbox.addWidget(Right_Bar() , 3)

        self.resize(1200, 750)
        self.setMaximumSize(1200, 750)



class Header(QWidget):

    def __init__(self):
        super().__init__()
        header_hbox = QHBoxLayout(self)
        header_hbox.setContentsMargins(0, 0, 0, 0)
        header_hbox.setSpacing(16)
        self.setFixedHeight(HEADER_H)
        header_hbox.addWidget(Brand())
        header_hbox.addWidget(TopBar(), 1)


class Brand(QWidget):

    LOGO_MAX_W = 128
    LOGO_MAX_H = 36

    def __init__(self):
        super().__init__()
        self.setFixedWidth(SIDEBAR_W)

        # same 12px side inset as the sidebar cards, so edges line up exactly
        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 4, 12, 4)

        card = QWidget()
        card.setObjectName("BrandCard")
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet("#BrandCard { background-color: #FFFFFF; border-radius: 12px; }")
        outer.addWidget(card)

        inner = QHBoxLayout(card)
        inner.setContentsMargins(16, 0, 16, 0)
        self.app_logo_label = QLabel()
        self.app_logo_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.app_logo_label)

        self._load_logo()

    @staticmethod
    def _trim(pm, tol=250):
        """Crop the white/transparent padding baked into the PNG."""
        img = pm.toImage()
        w, h = img.width(), img.height()

        def is_bg(x, y):
            c = img.pixelColor(x, y)
            return c.alpha() < 10 or (c.red() > tol and c.green() > tol and c.blue() > tol)

        def row_empty(y):
            return all(is_bg(x, y) for x in range(w))

        def col_empty(x, t, b):
            return all(is_bg(x, y) for y in range(t, b + 1))

        top = 0
        while top < h and row_empty(top):
            top += 1
        if top == h:
            return pm
        bottom = h - 1
        while row_empty(bottom):
            bottom -= 1
        left = 0
        while col_empty(left, top, bottom):
            left += 1
        right = w - 1
        while col_empty(right, top, bottom):
            right -= 1
        return pm.copy(left, top, right - left + 1, bottom - top + 1)

    def _load_logo(self):
        pm = QPixmap(str(LOGO_PATH))
        if pm.isNull():
            self.app_logo_label.setText("Veltrio")
            self.app_logo_label.setStyleSheet("font-size: 20px; font-weight: 700; color: #168F80;")
            return
        pm = self._trim(pm)
        dpr = self.devicePixelRatioF()
        scaled = pm.scaled(
            int(self.LOGO_MAX_W * dpr), int(self.LOGO_MAX_H * dpr),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        scaled.setDevicePixelRatio(dpr)
        self.app_logo_label.setPixmap(scaled)


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

        self.applyStyles()
        for w in (self.search_field,
          self.export_summary_button,
          self.timer_open_button,
          self.notification_panel_open_button,
          self.profile_icon_button):
          add_control_shadow(w)

    def applyStyles(self):
        
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #292D2B;
                font-family: Nunito Sans;
                font-size: 15px;
            }

            QLineEdit {
                background-color: #F5F5F3;
                border: 1px solid #E5E9E6;
                border-radius: 14px;
                padding: 12px 16px;
                min-height: 22px;
                color: #292D2B;
                selection-background-color: #168F80;
            }

            QLineEdit:focus {
                border: 1px solid #168F80;
                background-color: #FFFFFF;
            }

            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 12px;
                padding: 11px 16px;
                min-height: 22px;
                color: #292D2B;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #EDF0E7;
                border-color: #D5DED6;
            }

            QPushButton:pressed {
                background-color: #E1E9DF;
            }
        """)

        self.export_summary_button.setStyleSheet("""
            QPushButton {
                background-color: #168F80;
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 12px 18px;
                min-height: 22px;
                font-size: 15px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #11796D;
            }

            QPushButton:pressed {
                background-color: #0D655C;
            }
        """)


        


class SideBar(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(SIDEBAR_W)
        # Dashboard and stuff
        self.Dashboard_button = QPushButton("Dashboard", self)
        self.Tasks_button = QPushButton("Tasks", self)
        self.Calendar_button = QPushButton("Calendar", self)
        self.Notes_button = QPushButton("Notes", self)


        # List Area
        self.my_list_label = QLabel("My Lists", self)
        self.add_new_list_button = QPushButton("+", self)
        self.Inbox_button = QPushButton("Inbox", self)
        self.Work_button = QPushButton("Work", self)
        self.Study = QPushButton("Study", self)
        self.Health = QPushButton("Health", self)
        self.Holiday_trip_button = QPushButton("Holiday Trip", self)

        #Workspace Area
        self.Workspace_label = QLabel("Workspaces", self)
        self.add_new_workspace_button = QPushButton("+", self)
        self.add_sample_workspace_button_1 = QPushButton("Workspace 1", self)
        self.add_sample_workspace_button_2 = QPushButton("Workspace 2", self)
        self.initUI()
        
    def initUI(self):
        sidebar_vbox = QVBoxLayout()
        sidebar_vbox.setSpacing(20)
        sidebar_vbox.setContentsMargins(12, 16, 12, 16)
        self.setLayout(sidebar_vbox)

        #Dashboard and stuff
        Dashboard_container = QWidget()
        dashboard_items_vbox = QVBoxLayout()
        dashboard_items_vbox.setSpacing(4)
        dashboard_items_vbox.addWidget(self.Dashboard_button)
        dashboard_items_vbox.addWidget(self.Tasks_button)
        dashboard_items_vbox.addWidget(self.Calendar_button)
        dashboard_items_vbox.addWidget(self.Notes_button)
        Dashboard_container.setLayout(dashboard_items_vbox)
        sidebar_vbox.addWidget(Dashboard_container)


        # List Area
    
        list_items_container = QWidget()
        list_items_vbox = QVBoxLayout()
        list_items_vbox.setSpacing(4)
        list_name_hbox = QHBoxLayout()
        list_name_hbox.addWidget(self.my_list_label)
        list_name_hbox.addStretch(1)
        list_name_hbox.addWidget(self.add_new_list_button)
        list_items_vbox.addLayout(list_name_hbox)
        list_items_vbox.addWidget(self.Inbox_button)
        list_items_vbox.addWidget(self.Work_button)
        list_items_vbox.addWidget(self.Study)
        list_items_vbox.addWidget(self.Health)
        list_items_vbox.addWidget(self.Holiday_trip_button)
        list_items_container.setLayout(list_items_vbox)
        sidebar_vbox.addWidget(list_items_container)

        



        # Workspace Area
        workspace_items_container = QWidget()
        workspace_name_hbox = QHBoxLayout()
        workspace_name_hbox.addWidget(self.Workspace_label)
        workspace_name_hbox.addStretch(1)
        workspace_name_hbox.addWidget(self.add_new_workspace_button)
        workspace_items_vbox = QVBoxLayout()
        workspace_items_vbox.setSpacing(4)
        workspace_items_vbox.addLayout(workspace_name_hbox)
        workspace_items_vbox.addWidget(self.add_sample_workspace_button_1)
        workspace_items_vbox.addWidget(self.add_sample_workspace_button_2)
        workspace_items_container.setLayout(workspace_items_vbox)
        sidebar_vbox.addWidget(workspace_items_container)

        add_card_shadow(Dashboard_container)
        add_card_shadow(list_items_container)
        add_card_shadow(workspace_items_container)


        sidebar_vbox.addStretch(1)
        # Navigation selection
        nav_buttons = [
            self.Dashboard_button,
            self.Tasks_button,
            self.Calendar_button,
            self.Notes_button,
            self.Inbox_button,
            self.Work_button,
            self.Study,
            self.Health,
            self.Holiday_trip_button,
            self.add_sample_workspace_button_1,
            self.add_sample_workspace_button_2
        ]

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        for button in nav_buttons:
            button.setCheckable(True)
            self.nav_group.addButton(button)


        self.applyStyles()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #292D2B;
                font-family: Manrope;
                font-size: 15px;
                border-radius: 12px;
            }

            QPushButton {
                background-color: transparent;
                color: #292D2B;
                border: none;
                border-radius: 10px;
                padding: 12px 15px;
                min-height: 22px;
                text-align: left;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #EDF0E7;
            }

            QPushButton:checked {
                background-color: #EDF0E7;
                color: #168F80;
                font-weight: 600;
            }

            QLabel {
                background-color: transparent;
                color: #777D79;
                font-size: 16px;
            }
        """)




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
    app.setFont(QFont("Manrope", 16))                       
    window = mainWindow()                        
    window.show()                                 
    app.exec_()                                   
    
if __name__ == "__main__":
    main()