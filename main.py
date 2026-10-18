import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout,
                             QButtonGroup, QPushButton, QLineEdit,
                             QCheckBox)
from PyQt5.QtGui import (QIcon, QFont, QPixmap, QImage, QFontDatabase)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSettings
from pathlib import Path
from PyQt5.QtWidgets import QSizePolicy

SIDEBAR_W = 240
HEADER_H = 64
LOGO_PATH = Path(__file__).parent / "Resources" / "Images_" / "Veltrio Teal Ribbon Logo.png"  # adjust to your tree
FONT_DIR = Path(__file__).parent / "Resources" / "Fonts" / "Amaranth,Nunito,Signika_Negative" / "Nunito" / "static"
FONT_FAMILY = "Nunito"
LANDSCAPE_PATH = Path(__file__).parent / "Resources" / "Images_" / "Pastel Mint Landscape with Lake and Birds.png"


def add_card_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(10)
    shadow.setOffset(0, 2)
    shadow.setColor(QColor(0, 0, 0, 30))   
    widget.setGraphicsEffect(shadow)

def add_control_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(8)
    shadow.setOffset(0, 1)
    shadow.setColor(QColor(0, 0, 0, 22))   
    widget.setGraphicsEffect(shadow)

def load_fonts():
    for ttf in FONT_DIR.glob("*.ttf"):
        QFontDatabase.addApplicationFont(str(ttf))



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
        # self.setMaximumSize(1200, 750)



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

        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 4, 12, 4)

        card = QWidget()
        card.setObjectName("BrandCard")
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet("#BrandCard { background-color: #F5F5F3; border-radius: 12px; }")
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
        self.switch_light_modes = QPushButton(self)
        self.notification_panel_open_button = QPushButton(self)
        self.profile_icon_button = QPushButton(self)
        self.initUI()

    def initUI(self):
        topbar_hbox = QHBoxLayout()
        self.setLayout(topbar_hbox)

        topbar_hbox.addWidget(self.search_field)
        topbar_hbox.addWidget(self.export_summary_button)
        topbar_hbox.addWidget(self.switch_light_modes)
        topbar_hbox.addWidget(self.notification_panel_open_button)
        topbar_hbox.addWidget(self.profile_icon_button)

        self.search_field.setPlaceholderText("Search task")
        self.export_summary_button.setText("📂 Export Summary")
        self.switch_light_modes.setText("🌗")
        self.notification_panel_open_button.setText("🔔")
        self.profile_icon_button.setText("👤")

        self.applyStyles()
        for w in (self.search_field,
          self.export_summary_button,
          self.switch_light_modes,
          self.notification_panel_open_button,
          self.profile_icon_button):
          add_control_shadow(w)

    def applyStyles(self):

        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #1F2421;
                font-family: Nunito;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #F5F5F3;
                border: 1px solid #E5E9E6;
                border-radius: 14px;
                padding: 12px 16px;
                min-height: 22px;
                color: #1F2421;
                font-size: 14px;
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
                color: #1F2421;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #F1F3EE;
                border-color: #D5DED6;
            }

            QPushButton:pressed {
                background-color: #E1E9DF;
            }
        """)

        self.export_summary_button.setStyleSheet("""
            QPushButton {
                background-color: #11796D;
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 12px 18px;
                min-height: 22px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #0F6A60;
            }

            QPushButton:pressed {
                background-color: #0D5B52;
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
        self.Dashboard_button.setChecked(True)


        self.applyStyles()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #1F2421;
                font-family: Nunito;
                font-size: 14px;
                border-radius: 12px;
            }

            QPushButton {
                background-color: transparent;
                color: #1F2421;
                border: none;
                border-radius: 10px;
                padding: 12px 15px;
                min-height: 22px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #F1F3EE;
            }

            QPushButton:checked {
                background-color: #E3F1EE;
                color: #0D6B60;
                font-weight: 600;
            }

            QLabel {
                background-color: transparent;
                color: #5F6561;
                font-size: 12px;
                font-weight: 600;
            }
        """)




class Main_Display(QWidget):

    def __init__(self):
        super().__init__()
        self.top_widget = QWidget()
        self.greeting_widget = QWidget()
        self.greeting_label = QLabel("Good Morning, Rudy")
        self.no_of_tasks_label = QLabel("You have 5 tasks today.")

        self.up_next_widget = QWidget()
        self.up_next_label = QLabel("Up Next")
        self.task_widget_1 = QWidget()
        self.task_name_1 = QLabel("Task Name Placeholder")
        self.task_time_1 = QLabel("Task Time Placeholder")
        
        self.task_widget_2 = QWidget()
        self.task_name_2 = QLabel("Task Name Placeholder")
        self.task_time_2 = QLabel("Task Time Placeholder")

        

        self.middle_widget = QWidget()
        self.add_task_input = QLineEdit()
        self.send_task_button = QPushButton("➣")
        self.list_button = QPushButton("🔵  Inbox  ▾")
        self.now_button = QPushButton("🕒  Now")
        self.tomorrow_button = QPushButton("🕒  Tomorrow")
        self.next_week_button = QPushButton("🕒  Next week")
        self.custom_button = QPushButton("🗓️  Custom")
        self.date_button_group = QButtonGroup(self)
        self.date_button_group.setExclusive(True)   
        
        
        
        self.bottom_widget = QWidget()
        self.todays_tasks_label = QLabel("Today's Tasks")
        self.today_task_1 = QWidget()
        self.today_task_2 = QWidget()
        self.today_task_3 = QWidget()
        self.no_more_tasks_label = QLabel("No more tasks for today")
        self.no_more_tasks_subtitle = QLabel("You're all caught up. Enjoy the rest of your day.")
        self.initUI()

    def initUI(self):
        main_display_vbox = QVBoxLayout()
        self.setLayout(main_display_vbox)
        main_display_vbox.addWidget(self.top_widget, 4)
        main_display_vbox.addWidget(self.middle_widget, 1)
        main_display_vbox.addWidget(self.bottom_widget, 3)

        topwidget_hbox = QHBoxLayout()
        self.top_widget.setLayout(topwidget_hbox)

        greeting_vbox = QVBoxLayout()
        greeting_vbox.setAlignment(Qt.AlignTop)
        greeting_vbox.addWidget(self.greeting_label)
        greeting_vbox.addWidget(self.no_of_tasks_label)
        self.greeting_widget.setLayout(greeting_vbox)

        up_next_vbox = QVBoxLayout()
        task_1_vbox = QVBoxLayout(self.task_widget_1)
        task_1_vbox.addWidget(self.task_name_1)
        task_1_vbox.addWidget(self.task_time_1)

        task_2_vbox = QVBoxLayout(self.task_widget_2)
        task_2_vbox.addWidget(self.task_name_2)
        task_2_vbox.addWidget(self.task_time_2)
        up_next_vbox.setContentsMargins(10, 10, 10, 10)
        up_next_vbox.setSpacing(12)
        up_next_vbox.addWidget(self.up_next_label)
        up_next_vbox.addWidget(self.task_widget_1)
        up_next_vbox.addWidget(self.task_widget_2)
        up_next_vbox.addStretch(1)
        self.up_next_widget.setLayout(up_next_vbox)

        self.task_widget_1.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.task_widget_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )

        self.task_widget_1.setFixedHeight(75)
        self.task_widget_2.setFixedHeight(75)

        topwidget_hbox.addWidget(self.greeting_widget , 3)
        topwidget_hbox.addWidget(self.up_next_widget, 2 , alignment=Qt.AlignBottom)

        middle_vbox = QVBoxLayout()
        middle_vbox.setContentsMargins(12, 8, 12, 8)
        middle_vbox.setSpacing(10)
        self.middle_widget.setLayout(middle_vbox)


        input_hbox = QHBoxLayout()
        input_hbox.setSpacing(10)

        self.add_task_input.setPlaceholderText("Add task for today")
        input_hbox.addWidget(self.add_task_input, 1)
        input_hbox.addWidget(self.send_task_button)

        middle_vbox.addLayout(input_hbox)

        options_hbox = QHBoxLayout()
        options_hbox.setSpacing(8)

        for button in [
            self.list_button,
            self.now_button,
            self.tomorrow_button,
            self.next_week_button,
            self.custom_button
        ]:
            options_hbox.addWidget(button)

        middle_vbox.addLayout(options_hbox)

        for button in [
            self.now_button,
            self.tomorrow_button,
            self.next_week_button,
            self.custom_button
        ]:
            button.setCheckable(True)
            self.date_button_group.addButton(button)

        self.now_button.setChecked(True)


        bottom_vbox = QVBoxLayout()
        bottom_vbox.setContentsMargins(16, 16, 16, 16)
        bottom_vbox.setSpacing(12)
        self.bottom_widget.setLayout(bottom_vbox)

        bottom_vbox.addWidget(self.todays_tasks_label)

        for task_widget, task_name, location, time in [
            (self.today_task_1, "Complete Python project", "Inbox", "10:00 AM"),
            (self.today_task_2, "Review DSA concepts", "Study", "2:00 PM"),
            (self.today_task_3, "Finish workout", "Health", "6:00 PM"),
        ]:
            task_hbox = QHBoxLayout(task_widget)
            task_hbox.setContentsMargins(12, 8, 12, 8)
            task_hbox.setSpacing(12)

            task_details_vbox = QVBoxLayout()
            task_details_vbox.setContentsMargins(0, 0, 0, 0)
            task_details_vbox.setSpacing(4)

            task_checkbox = QCheckBox(task_name)
            task_location_label = QLabel(location)
            task_time_label = QLabel(time)

            task_details_vbox.addWidget(task_checkbox)
            task_details_vbox.addWidget(task_location_label)

            task_time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            task_hbox.addLayout(task_details_vbox, 1)
            task_hbox.addWidget(task_time_label)

            bottom_vbox.addWidget(task_widget)

        bottom_vbox.addStretch()
        self.no_more_tasks_label.setAlignment(Qt.AlignCenter)
        self.no_more_tasks_subtitle.setAlignment(Qt.AlignCenter)

        bottom_vbox.addSpacing(12)
        bottom_vbox.addWidget(self.no_more_tasks_label)
        bottom_vbox.addWidget(self.no_more_tasks_subtitle)
        self.applyStyles()



    
    def applyStyles(self):
        self.top_widget.setStyleSheet("""
            QWidget {
                background-color: #E3F1EE;
                border-radius: 20px;
            }

            QWidget#GreetingCard {
                background-color: #E3F1EE;
                border-radius: 20px;
            }
        """)

        self.greeting_label.setStyleSheet("""
            QLabel {
                color: #1F2421;
                font-family: Nunito;
                font-size: 26px;
                font-weight: 800;
                background-color: transparent;
                border: none;
            }
        """)

        self.no_of_tasks_label.setStyleSheet("""
            QLabel {
                color: #5F6561;
                font-family: Nunito;
                font-size: 13px;
                background-color: transparent;
                border: none;
            }
        """)
        self.up_next_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #E5E9E6;
                border-radius: 18px;
            }
        """)

        self.up_next_label.setStyleSheet("""
            font-family: Nunito;
            font-size: 18px;
            font-weight: 800;
            color: #1F2421;
            background: transparent;
            border: none;
        """)

        for task_widget in [self.task_widget_1, self.task_widget_2]:
            task_widget.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                    border-left: 4px solid #168F80;
                    border-radius: 1px;
                }
        """)
        self.task_name_1.setStyleSheet("""
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        self.task_name_2.setStyleSheet("""
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        self.task_time_2.setStyleSheet("""
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        self.task_time_1.setStyleSheet("""
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        # Middle widget
        self.middle_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 22px;
            }
        """)

        # Task input
        self.add_task_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 22px;
                padding: 12px 18px;
                color: #1F2421;
                font-family: Nunito;
                font-size: 14px;
                selection-background-color: #168F80;
            }

            QLineEdit:focus {
                border: 1px solid #168F80;
            }
        """)

        # Send button
        self.send_task_button.setStyleSheet("""
            QPushButton {
                background-color: #168F80;
                color: white;
                border: none;
                border-radius: 24px;
                min-width: 44px;
                max-width: 44px;
                min-height: 44px;
                max-height: 44px;
                font-size: 18px;
            }

            QPushButton:hover {
                background-color: #11796D;
            }
        """)

        # Date and list buttons
        for button in [
            self.list_button,
            self.now_button,
            self.tomorrow_button,
            self.next_week_button,
            self.custom_button
        ]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #F1F2F0;
                    color: #5F6561;
                    border: none;
                    border-radius: 18px;
                    padding: 10px 14px;
                    font-family: Nunito;
                    font-size: 13px;
                }

                QPushButton:hover {
                    background-color: #E3F1EE;
                    color: #11796D;
                }

                QPushButton:checked {
                    background-color: #E3F1EE;
                    color: #11796D;
                    border: 1px solid #168F80;
                    font-weight: 600;
                }
            """)

        self.send_task_button.setStyleSheet("""
                QPushButton {
                    background-color: #168F80;
                    color: white;
                    border: none;
                    border-radius: 22px;
                    min-width: 44px;
                    max-width: 44px;
                    min-height: 44px;   
                    max-height: 44px;
                    font-size: 18px;
                }
            """)

        # Today's Tasks container
        self.bottom_widget.setStyleSheet("""
            QWidget#bottom_widget {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 18px;
            }
        """)
        self.bottom_widget.setObjectName("bottom_widget")

        # Section heading
        self.todays_tasks_label.setStyleSheet("""
            QLabel {
                font-family: Nunito;
                font-size: 19px;
                font-weight: 800;
                color: #1F2421;
                background: transparent;
                border: none;
            }
        """)

        # Individual task rows
        for task_widget in [
            self.today_task_1,
            self.today_task_2,
            self.today_task_3
        ]:
            task_widget.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #E5E9E6;
                    border-radius: 12px;
                    margin : 1px 0px;
                }
            """)

        # Task checkboxes
        for checkbox in self.bottom_widget.findChildren(QCheckBox):
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-family: Nunito;
                    font-size: 14px;
                    font-weight: 700;
                    color: #1F2421;
                    spacing: 10px;
                    background: transparent;
                    border: none;
                }

                QCheckBox::indicator {
                    width: 17px;
                    height: 17px;
                    border: 2px solid #C9D1CC;
                    border-radius: 5px;
                    background-color: white;
                }

                QCheckBox::indicator:hover {
                    border-color: #168F80;
                }

                QCheckBox::indicator:checked {
                    background-color: #168F80;
                    border-color: #168F80;
                }

                QCheckBox:checked {
                    color: #8A918C;
                }
            """)

        # Task location labels
        for label in self.bottom_widget.findChildren(QLabel):
            if label is not self.todays_tasks_label:
                label.setStyleSheet("""
                    QLabel {
                        font-family: Nunito;
                        font-size: 12px;
                        color: #777F79;
                        background: transparent;
                        border: none;
                    }
                """)
        self.no_more_tasks_label.setStyleSheet("""
                QLabel {
                    font-family: Nunito;
                    font-size: 14px;
                    font-weight: 600;
                    color: #5F6561;
                    background: transparent;
                    border: none;
                }
            """)

        self.no_more_tasks_subtitle.setStyleSheet("""
                QLabel {
                    font-family: Nunito;
                    font-size: 12px;
                    font-weight: 400;
                    color: #9AA19C;
                    background: transparent;
                    border: none;
                }
            """)


class Right_Bar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        right_bar_vbox = QVBoxLayout()
        self.setLayout(right_bar_vbox)

def main():
    app = QApplication([])
    load_fonts()                                   
    font = QFont(FONT_FAMILY)
    font.setPixelSize(14)
    app.setFont(font)
    window = mainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()