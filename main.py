from pathlib import Path
import ctypes

from PyQt5.QtCore import (
    Qt,
    QDate,
    QRectF,
    QTimer,
)

from PyQt5.QtGui import (
    QIcon,
    QFont,
    QPixmap,
    QFontDatabase,
    QColor,
    QTextCharFormat,
    QBrush,
    QPainter,
)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QButtonGroup,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QCalendarWidget,
    QToolButton,
    QFrame,
    QTableView,
    QStyledItemDelegate,
    QStyle,
)

from veltrio_icons import VeltrioIcons


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# UI dimensions
SIDEBAR_W = 240
HEADER_H = 64

# Resource paths
LOGO_PATH = Path(__file__).parent / "Resources" / "Images_" / "Veltrio Teal Ribbon Logo.png"
LANDSCAPE_PATH = Path(__file__).parent / "Resources" / "Images_" / "Pastel Mint Landscape with Lake and Birds.png"
FONT_DIR = Path(__file__).parent / "Resources" / "Fonts" / "Amaranth,Nunito,Signika_Negative" / "Nunito" / "static"

# Font configuration
FONT_FAMILY = "Nunito"

# Color palette
color = {
    # Main backgrounds
    "background": "#F5F5F3",
    "surface": "#FFFFFF",
    "input_background": "#F5F5F3",

    # Text
    "text_primary": "#1F2421",
    "text_secondary": "#5F6561",
    "text_muted": "#777F79",
    "text_subtle": "#9AA19C",
    "text_disabled": "#B8C0BB",

    # Teal accents
    "accent": "#168F80",
    "accent_hover": "#11796D",
    "accent_pressed": "#0D5B52",
    "accent_dark": "#0D6B60",

    # Selection and hover
    "selected_background": "#E3F1EE",
    "hover_background": "#F1F3EE",
    "hover_background_alt": "#F1F2F0",
    "pressed_background": "#E1E9DF",
    "selected_pressed": "#CFE7E2",

    # Borders
    "border": "#E5E9E6",
    "border_hover": "#D5DED6",
    "border_checkbox": "#C9D1CC",

    # Task states
    "task_text_completed": "#8A918C",

    # Timer card
    "timer_border": "#293641",
    "timer_button": "#34434D",
    "timer_button_hover": "#425660",
    "timer_subtitle": "#A8B8BD",
    "timer_disabled": "#A8CFC8",

    # Utility
    "white": "#FFFFFF",
    "transparent": "transparent",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# UI effects
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


# Font loading
def load_fonts():
    for ttf in FONT_DIR.glob("*.ttf"):
        QFontDatabase.addApplicationFont(str(ttf))


# ---------------------------------------------------------------------------
# Main application window
# ---------------------------------------------------------------------------

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Configure the application window
        self.setWindowTitle("Veltrio")
        icon_path = Path(__file__).parent / "Resources" / "veltrio-icons" / "veltrio.ico"
        self.setWindowIcon(QIcon(str(icon_path)))

        # Windows only: set the title bar color to the app background (#F5F5F3)
        DWMWA_CAPTION_COLOR = 35

        color = 0x00F3F5F5  # RGB #F5F5F3 in Windows COLORREF format

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            int(self.winId()),
            DWMWA_CAPTION_COLOR,
            ctypes.byref(ctypes.c_int(color)),
            ctypes.sizeof(ctypes.c_int)
        )

        self.initUI()

    def initUI(self):
        # Set up the main window background
        self.setStyleSheet("QMainWindow { background-color: #F5F5F3; }")

        # Create the central widget and main vertical layout
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: #F5F5F3;")
        self.setCentralWidget(central_widget)

        main_vbox = QVBoxLayout()
        central_widget.setLayout(main_vbox)

        # Header on top, body (sidebar / main display / right bar) below
        body_hbox = QHBoxLayout()
        main_vbox.addWidget(Header(), 0)
        main_vbox.addLayout(body_hbox, 1)

        # Sidebar
        body_hbox.addWidget(SideBar(), 2)

        # Dashboard container
        dashboard_hbox = QHBoxLayout()
        body_hbox.addLayout(dashboard_hbox, 9)

        # Dashboard sections
        dashboard_hbox.addWidget(Main_Display(), 6)
        dashboard_hbox.addWidget(Right_Bar(), 3)

        # Set the initial window dimensions
        self.resize(1200, 1000)

        # Optional: enforce a maximum or minimum window size
        # self.setMaximumSize(1200, 750)
        self.setMinimumSize(1400, 1000)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

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
        topbar_hbox.setContentsMargins(0, 0, 0, 0)
        topbar_hbox.setSpacing(12)
        self.setLayout(topbar_hbox)

        topbar_hbox.addWidget(self.search_field)
        topbar_hbox.addWidget(self.export_summary_button)
        topbar_hbox.addWidget(self.switch_light_modes)
        topbar_hbox.addWidget(self.notification_panel_open_button)
        topbar_hbox.addWidget(self.profile_icon_button)

        self.search_field.setPlaceholderText("Search task")
        # self.export_summary_button.setText(" Export Summary")
        VeltrioIcons.apply_stateful(self.export_summary_button, "export_summary")
        VeltrioIcons.apply_stateful(self.switch_light_modes, "theme_day")
        VeltrioIcons.apply_stateful(self.notification_panel_open_button, "notifications")
        VeltrioIcons.apply_stateful(self.profile_icon_button, "profile")

        self.applyStyles()
        for w in (
            self.search_field,
            self.export_summary_button,
            self.switch_light_modes,
            self.notification_panel_open_button,
            self.profile_icon_button
        ):
            add_control_shadow(w)

        self.search_field.addAction(
            QIcon(str(VeltrioIcons.path("search"))),
            QLineEdit.LeadingPosition
        )

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


# ---------------------------------------------------------------------------
# Left sidebar
# ---------------------------------------------------------------------------

class SideBar(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(SIDEBAR_W)

        # Dashboard and stuff
        self.Dashboard_button = QPushButton(" Dashboard", self)
        self.Tasks_button = QPushButton(" Tasks", self)
        self.Calendar_button = QPushButton(" Calendar", self)
        self.Notes_button = QPushButton(" Notes", self)

        # List area
        self.my_list_label = QLabel("My Lists", self)
        self.add_new_list_button = QPushButton("+", self)
        self.Inbox_button = QPushButton(" Inbox", self)
        self.Work_button = QPushButton(" Work", self)
        self.Study = QPushButton(" Study", self)
        self.Health = QPushButton(" Health", self)
        self.Holiday_trip_button = QPushButton(" Holiday Trip", self)

        # Workspace area
        self.Workspace_label = QLabel("Workspaces", self)
        self.add_new_workspace_button = QPushButton("+", self)
        self.add_sample_workspace_button_1 = QPushButton(" Workspace 1", self)
        self.add_sample_workspace_button_2 = QPushButton(" Workspace 2", self)
        self.initUI()

    def initUI(self):
        sidebar_vbox = QVBoxLayout()
        sidebar_vbox.setSpacing(20)
        sidebar_vbox.setContentsMargins(12, 16, 12, 16)
        self.setLayout(sidebar_vbox)

        # Dashboard and stuff
        Dashboard_container = QWidget()
        dashboard_items_vbox = QVBoxLayout()
        dashboard_items_vbox.setSpacing(4)
        dashboard_items_vbox.addWidget(self.Dashboard_button)
        dashboard_items_vbox.addWidget(self.Tasks_button)
        dashboard_items_vbox.addWidget(self.Calendar_button)
        dashboard_items_vbox.addWidget(self.Notes_button)
        Dashboard_container.setLayout(dashboard_items_vbox)
        sidebar_vbox.addWidget(Dashboard_container)

        # List area
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

        # Workspace area
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

        # Sidebar icons
        VeltrioIcons.apply_stateful(self.Dashboard_button, "dashboard")
        VeltrioIcons.apply_stateful(self.Tasks_button, "tasks")
        VeltrioIcons.apply_stateful(self.Calendar_button, "calendar")
        VeltrioIcons.apply_stateful(self.Notes_button, "notes")
        VeltrioIcons.apply_stateful(self.Inbox_button, "inbox")
        VeltrioIcons.apply_stateful(self.Work_button, "work")
        VeltrioIcons.apply_stateful(self.Study, "study")
        VeltrioIcons.apply_stateful(self.Health, "health")
        VeltrioIcons.apply_stateful(self.Holiday_trip_button, "holiday_trip")
        VeltrioIcons.apply_stateful(self.add_sample_workspace_button_1, "workspace")
        VeltrioIcons.apply_stateful(self.add_sample_workspace_button_2, "workspace")

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


# ---------------------------------------------------------------------------
# Main display (greeting, add-task bar, today's tasks)
# ---------------------------------------------------------------------------

class Main_Display(QWidget):

    def __init__(self):
        super().__init__()

        # Top section: greeting + "Up Next" card
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

        # Middle section: add-task input and date buttons
        self.middle_widget = QWidget()
        self.add_task_input = QLineEdit()
        self.send_task_button = QPushButton()
        self.list_button = QPushButton(" Inbox")
        self.now_button = QPushButton(" Now")
        self.tomorrow_button = QPushButton(" Tomorrow")
        self.next_week_button = QPushButton(" Next week")
        self.custom_button = QPushButton(" Custom")
        self.date_button_group = QButtonGroup(self)
        self.date_button_group.setExclusive(True)

        # Bottom section: today's tasks
        self.bottom_widget = QWidget()
        self.todays_tasks_label = QLabel("Today's Tasks")
        self.heading_line = QFrame()
        self.heading_line.setFixedSize(132, 2)
        self.heading_line.setStyleSheet("""
            QFrame {
                background-color: #A8C5B5;
                border: none;
            }
        """)
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

        # Top section
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
        add_card_shadow(self.up_next_widget)

        self.task_widget_1.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.task_widget_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )

        self.task_widget_1.setFixedHeight(75)
        self.task_widget_2.setFixedHeight(75)

        topwidget_hbox.addWidget(self.greeting_widget, 3)
        topwidget_hbox.addWidget(self.up_next_widget, 2, alignment=Qt.AlignBottom)
        self.top_widget.setObjectName("top_widget")

        # Middle section
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
            self.custom_button,
            self.list_button
        ]:
            button.setCheckable(True)
            self.date_button_group.addButton(button)

        self.now_button.setChecked(True)
        VeltrioIcons.apply_stateful(self.send_task_button, "task_submit")
        VeltrioIcons.apply_stateful(self.list_button, "inbox")
        VeltrioIcons.apply_stateful(self.now_button, "date_today")
        VeltrioIcons.apply_stateful(self.tomorrow_button, "date_tomorrow")
        VeltrioIcons.apply_stateful(self.next_week_button, "date_next_week")
        VeltrioIcons.apply_stateful(self.custom_button, "date_custom")

        # Bottom section
        bottom_vbox = QVBoxLayout()
        bottom_vbox.setContentsMargins(16, 16, 16, 16)
        bottom_vbox.setSpacing(2)
        self.bottom_widget.setLayout(bottom_vbox)

        bottom_vbox.addWidget(self.todays_tasks_label)
        bottom_vbox.addWidget(self.heading_line)

        for task_widget, task_name, location, time in [
            (self.today_task_1, "Complete Python project", "Inbox", "10:00 AM"),
            (self.today_task_2, "Review DSA concepts", "Study", "2:00 PM"),
            (self.today_task_3, "Finish workout", "Health", "6:00 PM"),
        ]:
            task_hbox = QHBoxLayout(task_widget)
            task_hbox.setContentsMargins(8, 14, 8, 14)
            task_hbox.setSpacing(14)

            task_details_vbox = QVBoxLayout()
            task_details_vbox.setContentsMargins(0, 0, 0, 0)
            task_details_vbox.setSpacing(5)

            task_checkbox = QCheckBox(task_name)
            task_location_label = QLabel(location)
            task_time_label = QLabel(time)

            task_details_vbox.addWidget(task_checkbox)
            task_details_vbox.addWidget(task_location_label)

            task_time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            task_hbox.addLayout(task_details_vbox, 1)
            task_hbox.addWidget(task_time_label)

            bottom_vbox.addWidget(task_widget, 1)

        self.no_more_tasks_label.setAlignment(Qt.AlignCenter)
        self.no_more_tasks_subtitle.setAlignment(Qt.AlignCenter)

        bottom_vbox.addSpacing(12)
        bottom_vbox.addWidget(self.no_more_tasks_label)
        bottom_vbox.addWidget(self.no_more_tasks_subtitle)
        self.applyStyles()

    def applyStyles(self):
        # Top section
        self.top_widget.setStyleSheet("""
            QWidget#top_widget {
                border-image: url("Resources/Images_/Pastel Mint Landscape with Lake and Birds.png") 0 0 0 0 stretch stretch;
                border-radius: 20px;
            }

            QWidget#GreetingCard {
                background-color: #E3F1EE;
                border-radius: 20px;
            }
        """)
        self.greeting_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.greeting_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
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
                    font-weight: 600;
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

        # Send button
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
                padding: 0px 0px 10px 0px;
                margin: 0px;
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
                    background: transparent;
                    border: none;
                    border-radius: 0px;
                    margin: 0px;
                    padding: 0px;
                    border-bottom: 1px solid #E5E9E6;
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
                        margin-left: 28px;
                    }
                """)

        # Empty-state labels (applied after the loop above so they take precedence)
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


# ---------------------------------------------------------------------------
# Right bar (calendar + focus timer)
# ---------------------------------------------------------------------------

# Paints the selected calendar cell as a rounded teal square
class CalendarDateDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.setRenderHint(QPainter.Antialiasing)
            rect = QRectF(option.rect).adjusted(3, 3, -3, -3)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#168F80"))
            painter.drawRoundedRect(rect, 7, 7)

            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(
                option.rect,
                Qt.AlignCenter,
                str(index.data())
            )
        else:
            super().paint(painter, option, index)

        painter.restore()


class Right_Bar(QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.initUI()

    def initUI(self):
        right_bar_vbox = QVBoxLayout()
        self.setLayout(right_bar_vbox)

        # Object name so the card style does NOT cascade onto the calendar's children
        self.calendar_container = QWidget()
        self.calendar_container.setObjectName("CalendarCard")
        self.calendar_container.setAttribute(Qt.WA_StyledBackground, True)
        self.calendar_container.setStyleSheet("""
            QWidget#CalendarCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 16px;
            }
        """)

        calendar_layout = QVBoxLayout(self.calendar_container)
        calendar_layout.setContentsMargins(12, 12, 12, 12)
        calendar_layout.setSpacing(0)

        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendar.setGridVisible(False)
        self.calendar.setNavigationBarVisible(True)
        self.calendar_view = self.calendar.findChild(QTableView)
        self.calendar_delegate = CalendarDateDelegate(self.calendar_view)
        self.calendar_view.setItemDelegate(self.calendar_delegate)
        # VeltrioIcons.apply(self.calendar.findChild(QToolButton, "qt_calendar_prevmonth"), "previous")
        # VeltrioIcons.apply(self.calendar.findChild(QToolButton, "qt_calendar_nextmonth"), "next")

        calendar_layout.addWidget(self.calendar)

        self.timer_widget = QWidget()
        self.timer_widget.setObjectName("TimerCard")
        self.timer_widget.setAttribute(Qt.WA_StyledBackground, True)

        timer_vbox = QVBoxLayout(self.timer_widget)
        timer_vbox.setContentsMargins(20, 20, 20, 20)
        timer_vbox.setSpacing(18)

        # Timer heading and subtitle
        self.timer_heading = QLabel()
        self.timer_heading.setTextFormat(Qt.RichText)
        self.timer_heading.setText("""
            <div style="text-align: left; line-height: 125%;">
                <span style="color: #1F2421; font-size: 26px; font-weight: 800;">
                    Focus Timer
                </span>
                <br>
                <span style="color: #5F6561; font-size: 13px; font-weight: 400;">
                    Make it count.
                </span>
            </div>
        """)
        self.timer_heading.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.timer_heading.setContentsMargins(0, 0, 0, 0)

        timer_vbox.addWidget(self.timer_heading)

        # Time display and adjustment buttons
        time_row = QHBoxLayout()
        time_row.setSpacing(12)

        self.minus_button = QPushButton()
        self.minus_button.setFixedSize(36, 36)

        self.time = "15:00"
        self.minutes, self.seconds = map(int, self.time.split(":"))
        self.time_label = QLabel(f"{self.minutes:02} : {self.seconds:02}")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumWidth(150)

        self.plus_button = QPushButton()
        self.plus_button.setFixedSize(36, 36)

        time_row.addStretch()
        time_row.addWidget(self.minus_button)
        time_row.addWidget(self.time_label)
        time_row.addWidget(self.plus_button)
        time_row.addStretch()

        timer_vbox.addLayout(time_row)

        # Start/Stop and Reset controls
        controls_row = QHBoxLayout()
        controls_row.setContentsMargins(0, 0, 0, 0)
        controls_row.setSpacing(10)
        controls_row.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.start_button = QPushButton()
        self.start_button.setFixedSize(46, 46)

        self.reset_button = QPushButton()
        self.reset_button.setFixedSize(46, 46)

        controls_row.addWidget(self.start_button)
        controls_row.addWidget(self.reset_button)

        timer_vbox.addLayout(controls_row)

        right_bar_vbox.addWidget(self.calendar_container, 1)
        right_bar_vbox.addWidget(self.timer_widget, 1)
        add_card_shadow(self.calendar_container)
        add_card_shadow(self.timer_widget)

        VeltrioIcons.apply(self.start_button, "timer_start")
        VeltrioIcons.apply(self.reset_button, "timer_reset")
        VeltrioIcons.apply(self.plus_button, "increase_time")
        VeltrioIcons.apply(self.minus_button, "decrease_time")

        self.styleNavButtons()
        self.styleDateFormats()
        self.applyStyles()
        self.styleTimer()

        self.plus_button.clicked.connect(self.increase_timer_time)
        self.minus_button.clicked.connect(self.decrease_timer_time)
        self.reset_button.clicked.connect(self.reset_timer_time)
        self.timer.timeout.connect(self.update_timer)
        self.start_button.clicked.connect(self.change_start_button_to_pause)

    # Timer logic
    def increase_timer_time(self):

        if self.minutes >= 60:
            self.plus_button.setEnabled(False)
            self.minus_button.setEnabled(True)
        else:
            self.plus_button.setEnabled(True)
            self.minus_button.setEnabled(True)
            self.minutes += 5
            self.time_label.setText(f"{self.minutes:02} : {self.seconds:02}")

    def decrease_timer_time(self):

        if self.minutes <= 5:
            self.minus_button.setEnabled(False)
            self.plus_button.setEnabled(True)

        else:
            self.minus_button.setEnabled(True)
            self.plus_button.setEnabled(True)
            self.minutes -= 5
            self.time_label.setText(f"{self.minutes:02} : {self.seconds:02}")

    def reset_timer_time(self):
        self.timer.stop()
        self.minutes = 15
        self.seconds = 0
        VeltrioIcons.apply(self.start_button, "timer_start")
        self.time_label.setText(f"{self.minutes:02} : {self.seconds:02}")

    def update_timer(self):

        if self.minutes <= 0 and self.seconds <= 0:
            self.timer.stop()
            VeltrioIcons.apply(self.start_button, "timer_start")
            self.time_label.setText(f"{self.minutes:02} : {self.seconds:02}")

        elif self.seconds <= 0:
            self.seconds = 59
            self.minutes -= 1
            self.time_label.setText(f"{self.minutes:02} : {self.seconds:02}")
        else:
            self.seconds -= 1
            self.time_label.setText(f"{self.minutes:02} : {self.seconds:02}")

    def change_start_button_to_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            VeltrioIcons.apply(self.start_button, "timer_start")

        else:
            self.timer.start()
            VeltrioIcons.apply(self.start_button, "timer_pause")

    # Calendar styling
    def styleNavButtons(self):
        # Replace the default green circle arrows with clean text arrows
        for name, text in (("qt_calendar_prevmonth", "‹"),
                           ("qt_calendar_nextmonth", "›")):
            btn = self.calendar.findChild(QToolButton, name)
            if btn:
                btn.setIcon(QIcon())
                btn.setText(text)
                btn.setToolButtonStyle(Qt.ToolButtonTextOnly)
                btn.setCursor(Qt.PointingHandCursor)

    def styleDateFormats(self):
        # Header (Sun, Mon, ...)
        header_fmt = QTextCharFormat()
        header_fmt.setForeground(QBrush(QColor("#5F6561")))
        header_fmt.setFontWeight(QFont.DemiBold)
        self.calendar.setHeaderTextFormat(header_fmt)

        # Remove Qt's default red weekends; use the app's text colour for all days
        day_fmt = QTextCharFormat()
        day_fmt.setForeground(QBrush(QColor("#303A36")))
        for day in (Qt.Monday, Qt.Tuesday, Qt.Wednesday, Qt.Thursday,
                    Qt.Friday, Qt.Saturday, Qt.Sunday):
            self.calendar.setWeekdayTextFormat(day, day_fmt)

        # Highlight today in the teal accent
        today_fmt = QTextCharFormat()
        today_fmt.setForeground(QBrush(QColor("#0D6B60")))
        today_fmt.setBackground(QBrush(QColor("#E3F1EE")))
        today_fmt.setFontWeight(QFont.Bold)
        self.calendar.setDateTextFormat(QDate.currentDate(), today_fmt)

    def applyStyles(self):
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #FFFFFF;
                border: none;
            }

            QCalendarWidget QWidget {
                background-color: #FFFFFF;
                alternate-background-color: #FFFFFF;
                color: #303A36;
                border: none;
                font-family: Nunito;
            }

            /* Navigation bar */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #FFFFFF;
                border: none;
                padding: 2px 0px 8px 0px;
            }

            QCalendarWidget QToolButton {
                color: #1F2421;
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 14px;
                font-weight: 700;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #E3F1EE;
                color: #0D6B60;
            }

            QCalendarWidget QToolButton:pressed {
                background-color: #CFE7E2;
            }

            /* Prev / next arrows */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                font-size: 20px;
                min-width: 28px;
                padding: 2px 8px;
            }

            /* Month dropdown: remove the odd arrow */
            QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator {
                image: none;
                width: 0px;
            }

            QCalendarWidget QMenu {
                background-color: #FFFFFF;
                color: #303A36;
                border: 1px solid #E5E9E6;
                border-radius: 8px;
                padding: 4px;
            }

            QCalendarWidget QMenu::item {
                padding: 6px 18px;
                border-radius: 6px;
            }

            QCalendarWidget QMenu::item:selected {
                background-color: #E3F1EE;
                color: #0D6B60;
            }

            QCalendarWidget QSpinBox {
                color: #303A36;
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 8px;
                padding: 4px 8px;
                selection-background-color: #168F80;
            }

            /* Date grid */
            QCalendarWidget QAbstractItemView {
                background-color: #FFFFFF;
                alternate-background-color: #FFFFFF;
                selection-background-color: #168F80;
                selection-color: #FFFFFF;
                outline: none;
                border: none;
            }

            QCalendarWidget QAbstractItemView:enabled {
                color: #303A36;
            }

            QCalendarWidget QAbstractItemView:disabled {
                color: #B8C0BB;
            }

        """)

    # Timer card styling
    def styleTimer(self):
        self.timer_widget.setStyleSheet("""
            QWidget#TimerCard {
                border-image: url("Resources/Images_/timer_bg.png") 0 0 0 0 stretch stretch;
                border: 1px solid #293641;
                border-radius: 16px;
            }

            QLabel {
                background: transparent;
                border: none;
                color: #F5F5F3;
                font-family: Nunito;
            }

            QLabel#TimerTitle {
                color: #A8B8BD;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton {
                border: none;
                border-radius: 18px;
                background-color: #34434D;
                color: #F5F5F3;
                font-size: 20px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #425660;
            }

            QPushButton:pressed {
                background-color: #168F80;
                padding-top: 2px;
                padding-left: 2px;
            }
        """)

        self.timer_heading.setStyleSheet("""
            QLabel {
                color: #F5F5F3;
                font-family: Nunito;
                background: transparent;
                border: none;
            }
        """)

        self.time_label.setStyleSheet("""
            QLabel {
                color: #1F2421;
                font-family: Nunito;
                font-size: 38px;
                font-weight: 800;
                background: transparent;
                border: none;
            }
        """)

        button_style = """
            QPushButton {
                background-color: #168F80;
                color: #FFFFFF;
                border: none;
                border-radius: 23px;
                font-size: 18px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #11796D;
            }

            QPushButton:pressed {
                background-color: #0D5B52;
                padding-top: 2px;
                padding-left: 2px;
            }

            QPushButton:disabled {
                background-color: #A8CFC8;
                color: #F5F5F3;
            }
        """

        self.start_button.setStyleSheet(button_style)
        self.reset_button.setStyleSheet(button_style)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

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