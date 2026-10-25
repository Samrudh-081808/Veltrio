from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QButtonGroup,
    QTextEdit, QMenu, QAction, QDialog, QLabel, QSpacerItem, QSizePolicy, QCalendarWidget, QWidgetAction
)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QDate
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QTextCharFormat
from veltrio_icons import VeltrioIcons

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
            if not (option.state & QStyle.State_Enabled):
                painter.fillRect(option.rect, QColor("#FFFFFF"))
                painter.setPen(QColor("#B8BFBB"))
                painter.drawText(
                    option.rect,
                    Qt.AlignCenter,
                    str(index.data())
                )
            else:
                super().paint(painter, option, index)

        painter.restore()

class TaskComposer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TaskComposer")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Create the same controls as the original middle widget
        self.add_task_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Add a description...")
        self.description_input.setFixedHeight(150)
        self.send_task_button = QPushButton()

        self.list_button = QPushButton(" Inbox")
        self.selected_list = "Inbox"
        self.task_list_menu = QMenu(self)
        self.list_button.setMenu(None)
        self.list_button.clicked.connect(self.show_task_list_menu)
        self.selected_date = QDate.currentDate()

        self.task_list_menu.setWindowFlags(
            Qt.Popup |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint
        )

        self.task_list_menu.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.task_lists = {
            "Inbox": "inbox",
            "Health": "health",
            "Work": "work",
            "Study": "study",
            "Holiday": "holiday_trip",
        }

        for list_name, icon_name in self.task_lists.items():
            action = self.task_list_menu.addAction(
                QIcon(str(VeltrioIcons.path(icon_name))),
                list_name
            )

            action.triggered.connect(
                lambda checked=False, name=list_name:
                    self.select_task_list(name)
            )

        self.now_button = QPushButton(" Now")
        self.tomorrow_button = QPushButton(" Tomorrow")
        self.next_week_button = QPushButton(" Next week")
        self.custom_button = QPushButton(" Custom")
        self.custom_button.clicked.connect(self.show_calendar)

        self.date_button_group = QButtonGroup(self)
        self.date_button_group.setExclusive(True)

        self.selected_date = QDate.currentDate()

        self.calendar = QCalendarWidget(self)
        self.calendar.setObjectName("DatePopup")

        weekday_format = QTextCharFormat()
        weekday_format.setForeground(QColor("#111111"))

        for day in range(1, 8):
            self.calendar.setWeekdayTextFormat(day, weekday_format)

        self.calendar.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.calendar.setAttribute(Qt.WA_StyledBackground, True)

        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.NoVerticalHeader
        )
        self.calendar.setGridVisible(False)
        self.calendar.setMinimumSize(320, 290)
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.NoVerticalHeader
        )
        self.calendar.setFocusPolicy(Qt.StrongFocus)

        self.calendar_delegate = CalendarDateDelegate(self.calendar)

        calendar_view = self.calendar.findChild(
            QTableView, "qt_calendar_calendarview"
        )

        if calendar_view is not None:
            calendar_view.setItemDelegate(self.calendar_delegate)

        self.calendar.clicked.connect(self.on_custom_date_picked)

        self.initUI()


    def initUI(self):
        middle_vbox = QVBoxLayout()
        middle_vbox.setContentsMargins(12, 8, 12, 8)
        middle_vbox.setSpacing(10)
        self.setLayout(middle_vbox)

        input_hbox = QHBoxLayout()
        input_hbox.setSpacing(10)

        self.add_task_input.setPlaceholderText("Add task for today")
        input_hbox.addWidget(self.add_task_input, 1)
        input_hbox.addWidget(self.send_task_button)
        self.list_button.clicked.connect(self.show_task_list_menu)

        middle_vbox.addLayout(input_hbox)
        

        options_hbox = QHBoxLayout()
        options_hbox.setSpacing(8)

        buttons = [
            self.list_button,
            self.now_button,
            self.tomorrow_button,
            self.next_week_button,
            self.custom_button
        ]

        for button in buttons:
            button.setMinimumWidth(0)
            button.setMaximumWidth(16777215)
            options_hbox.addWidget(button, 1)

        options_hbox.setStretch(0, 1)
        options_hbox.setStretch(1, 1)
        options_hbox.setStretch(2, 1)
        options_hbox.setStretch(3, 1)
        options_hbox.setStretch(4, 1)

        middle_vbox.addLayout(options_hbox)

        for button in [
            self.now_button,
            self.tomorrow_button,
            self.next_week_button,
            self.custom_button,
        ]:
            button.setCheckable(True)
            self.date_button_group.addButton(button)

        self.now_button.setChecked(True)
        VeltrioIcons.apply_stateful(self.send_task_button, "task_submit")
        VeltrioIcons.apply_stateful(self.now_button, "date_today")
        VeltrioIcons.apply_stateful(self.tomorrow_button, "date_tomorrow")
        VeltrioIcons.apply_stateful(self.next_week_button, "date_next_week")
        VeltrioIcons.apply_stateful(self.custom_button, "date_custom")
        VeltrioIcons.apply_stateful(self.list_button, "inbox")
        middle_vbox.addWidget(self.description_input)

        self.now_button.clicked.connect(lambda: self.set_date(QDate.currentDate()))
        self.tomorrow_button.clicked.connect(lambda: self.set_date(QDate.currentDate().addDays(1)))
        self.next_week_button.clicked.connect(lambda: self.set_date(QDate.currentDate().addDays(7)))

        
        self.apply_styles()
        self.task_list_menu.setWindowFlags(
            self.task_list_menu.windowFlags() | Qt.FramelessWindowHint
        )
        self.task_list_menu.setAttribute(Qt.WA_TranslucentBackground)

    def select_task_list(self, list_name):
        self.selected_list = list_name
        self.list_button.setText(f" {list_name}")
        self.list_button.setIcon(
            QIcon(str(VeltrioIcons.path(
                self.task_lists[list_name]
            )))
        )


    def set_date(self, date):
                self.selected_date = date
                self.custom_button.setText(" Custom")
    
    def apply_styles(self):
        # Middle widget
        self.setStyleSheet("""
            QWidget#TaskComposer {
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
            
                QPushButton::menu-indicator {
                    image : none;
                    widht: 0px;
                    height: 0px;
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

            QPushButton:hover {
                background-color: #11796D;
            }

            QPushButton:pressed {
                background-color: #0D655B;
                padding-top: 2px;
                padding-left: 2px;
            }
        """)

        self.description_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 14px;
                padding: 10px 14px;
                color: #1F2421;
                font-family: Nunito;
                font-size: 14px;
                selection-background-color: #168F80;
            }

            QTextEdit:focus {
                border: 1px solid #168F80;
            }
        """)

        # Menu
        self.task_list_menu.setStyleSheet("""
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 12px;
                padding: 6px;
                color: #5F6561;
                font-family: Nunito;
                font-size: 13px;
            }   

            QMenu::item {
                background-color: transparent;
                padding: 11px 24px 11px 14px;
                border-radius: 9px;
                min-width: 130px;
            }

            QMenu::icon {
                background-color: transparent;
                padding-left: 6px;
            }

            QMenu::item:selected {
                background-color: #E3F1EE;
                color: #11796D;
                
            }

            QMenu::item:disabled {
                color: #A5AAA6;
            }

            
        """)


 
        self.calendar.setStyleSheet("""
            QCalendarWidget#DatePopup {
                background-color: #FFFFFF;
                color: #111111;
                border: 1px solid #E5E9E6;
                font-family: Nunito;
                font-size: 12px;
            }

            QWidget#qt_calendar_navigationbar {
                background-color: #FFFFFF;
                border: none;
                min-height: 38px;
            }

            QToolButton#qt_calendar_monthbutton,
            QToolButton#qt_calendar_yearbutton {
                color: #111111;
                background-color: transparent;
                border: none;
                border-radius: 5px;
                padding: 4px 6px;
                font-family: Nunito;
                font-size: 13px;
                font-weight: 600;
            }

            QToolButton#qt_calendar_monthbutton:hover,
            QToolButton#qt_calendar_yearbutton:hover {
                background-color: #F1F2F0;
            }

            QWidget#qt_calendar_prevmonth,
            QWidget#qt_calendar_nextmonth {
                color: #111111;
                background-color: transparent;
                border: none;
                border-radius: 5px;
                padding: 3px;
            }

            QWidget#qt_calendar_prevmonth:hover,
            QWidget#qt_calendar_nextmonth:hover {
                background-color: #F1F2F0;
            }

            QSpinBox#qt_calendar_yearedit {
                color: #111111;
                background-color: #FFFFFF;
                border: none;
                font-family: Nunito;
                font-size: 13px;
                font-weight: 600;
            }

            QCalendarWidget QHeaderView::section {
                background-color: #FFFFFF;
                color: #111111;
                border: none;
                padding: 6px 0;
                font-family: Nunito;
                font-size: 12px;
            }

            QCalendarWidget QTableView {
                background-color: #FFFFFF;
                alternate-background-color: #FFFFFF;
                color: #111111;
                border: none;
                outline: none;
                gridline-color: transparent;
                font-family: Nunito;
                font-size: 12px;
            }

            QCalendarWidget QTableView::item {
                border: none;
                padding: 3px;
            }

            QCalendarWidget QTableView::item:hover {
                background-color: #E3F1EE;
            }

            QCalendarWidget QTableView::item:selected {
                background-color: #168F80;
                color: #FFFFFF;
            }
        """)


    def show_task_list_menu(self):
        pos = self.list_button.mapToGlobal(
            self.list_button.rect().bottomLeft()
        )
        self.task_list_menu.popup(pos + QPoint(0, 8))

    def show_calendar(self):
        pos = self.custom_button.mapToGlobal(
            self.custom_button.rect().bottomLeft()
        )
        self.calendar.move(pos + QPoint(0, 8))
        self.calendar.show()

    def on_custom_date_picked(self, date):
        print("Selected date:", date.toString("yyyy-MM-dd"))

        self.selected_date = date
        self.custom_button.setText(" " + date.toString("d MMM"))
        self.custom_button.setChecked(True)