
from PyQt5.QtCore import Qt, QRectF, QDate
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QCalendarWidget,
    QStyledItemDelegate,
    QStyle,
    QTableView,
    QPushButton,
    QGraphicsDropShadowEffect,
)


PALETTE = {
    "background": "#FFFFFF",
    "surface": "#FFFFFF",
    "text": "#303A36",
    "muted_text": "#659B86",
    "accent": "#168F80",
    "border": "#E1E7E3",
    "soft_green": "#EDF0E7",
    "hover": "#F4F7F4",
}


def add_card_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(8)
    shadow.setOffset(0, 1)
    shadow.setColor(QColor(0, 0, 0, 22))
    widget.setGraphicsEffect(shadow)


def create_card():
    card = QFrame()
    card.setObjectName("CalendarCard")
    card.setStyleSheet("""
        QFrame#CalendarCard {
            background-color: #FFFFFF;
            border: 1px solid #E1E7E3;
            border-radius: 16px;
        }
    """)
    add_card_shadow(card)
    return card


class CalendarDateDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.setRenderHint(QPainter.Antialiasing)

            rect = QRectF(option.rect).adjusted(3, 3, -3, -3)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(PALETTE["accent"]))
            painter.drawRoundedRect(rect, 7, 7)

            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(
                option.rect,
                Qt.AlignCenter,
                str(index.data())
            )
        else:
            painter.setRenderHint(QPainter.Antialiasing)

            if option.state & QStyle.State_MouseOver:
                rect = QRectF(option.rect).adjusted(4, 4, -4, -4)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(PALETTE["hover"]))
                painter.drawRoundedRect(rect, 7, 7)

                painter.setPen(QColor(PALETTE["text"]))
                painter.drawText(
                    option.rect,
                    Qt.AlignCenter,
                    str(index.data())
                )
            else:
                super().paint(painter, option, index)

        painter.restore()


class CalendarPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("CalendarPage")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget#CalendarPage {
                background-color: #FFFFFF;
            }
        """)

        self.initUI()

    def initUI(self):

        # Main page layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(22)

        # --------------------------------------------------
        # Page heading
        # --------------------------------------------------

        heading_layout = QVBoxLayout()
        heading_layout.setSpacing(5)

        title = QLabel("Calendar")
        title.setFont(QFont("Segoe UI", 25, QFont.Bold))
        title.setStyleSheet(f"""
            color: {PALETTE["text"]};
            background: transparent;
            border: none;
        """)

        subtitle = QLabel("A clearer view of your days.")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet(f"""
            color: {PALETTE["muted_text"]};
            background: transparent;
            border: none;
        """)

        heading_layout.addWidget(title)
        heading_layout.addWidget(subtitle)

        main_layout.addLayout(heading_layout)

        # --------------------------------------------------
        # Main content: left features + right calendar
        # --------------------------------------------------

        content_layout = QHBoxLayout()
        content_layout.setSpacing(22)

        # ================= LEFT SECTION ===================

        self.features_card = create_card()

        features_layout = QVBoxLayout(self.features_card)
        features_layout.setContentsMargins(24, 24, 24, 24)
        features_layout.setSpacing(14)

        features_heading = QLabel("Coming Soon")
        features_heading.setFont(QFont("Segoe UI", 20, QFont.Bold))
        features_heading.setStyleSheet(f"""
            color: {PALETTE["text"]};
            background: transparent;
            border: none;
        """)

        features_subtitle = QLabel(
            "More ways to plan your time are on the way."
        )
        features_subtitle.setWordWrap(True)
        features_subtitle.setFont(QFont("Segoe UI", 11))
        features_subtitle.setStyleSheet(f"""
            color: {PALETTE["muted_text"]};
            background: transparent;
            border: none;
            line-height: 150%;
        """)

        # Coming soon placeholder
        self.features_placeholder = QWidget()
        self.features_placeholder.setAttribute(
            Qt.WA_StyledBackground, True
        )
        self.features_placeholder.setStyleSheet("""
            QWidget {
                background-color: #F4F7F4;
                border: 1px dashed #D5DFD9;
                border-radius: 12px;
            }
        """)

        placeholder_layout = QVBoxLayout(self.features_placeholder)
        placeholder_layout.setContentsMargins(20, 24, 20, 24)
        placeholder_layout.setSpacing(10)
        placeholder_layout.setAlignment(Qt.AlignCenter)

        placeholder_icon = QLabel("✦")
        placeholder_icon.setAlignment(Qt.AlignCenter)
        placeholder_icon.setFont(QFont("Segoe UI", 30, QFont.Bold))
        placeholder_icon.setStyleSheet("""
            color: #168F80;
            background: transparent;
            border: none;
        """)

        placeholder_title = QLabel("Something new is coming")
        placeholder_title.setAlignment(Qt.AlignCenter)
        placeholder_title.setWordWrap(True)
        placeholder_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        placeholder_title.setStyleSheet("""
            color: #303A36;
            background: transparent;
            border: none;
        """)

        placeholder_subtitle = QLabel(
            "We're making space for more useful features."
        )
        placeholder_subtitle.setAlignment(Qt.AlignCenter)
        placeholder_subtitle.setWordWrap(True)
        placeholder_subtitle.setFont(QFont("Segoe UI", 10))
        placeholder_subtitle.setStyleSheet("""
            color: #659B86;
            background: transparent;
            border: none;
        """)

        placeholder_layout.addWidget(placeholder_icon)
        placeholder_layout.addWidget(placeholder_title)
        placeholder_layout.addWidget(placeholder_subtitle)

        features_layout.addWidget(features_heading)
        features_layout.addWidget(features_subtitle)
        features_layout.addSpacing(8)
        features_layout.addWidget(self.features_placeholder, 1)
        features_layout.addStretch()

        # ================= RIGHT SECTION ==================

        self.calendar_card = create_card()

        calendar_layout = QVBoxLayout(self.calendar_card)
        calendar_layout.setContentsMargins(20, 20, 20, 20)
        calendar_layout.setSpacing(16)

        # Calendar heading row
        calendar_heading_row = QHBoxLayout()
        calendar_heading_row.setSpacing(10)

        calendar_heading = QLabel("Your Schedule")
        calendar_heading.setFont(QFont("Segoe UI", 17, QFont.Bold))
        calendar_heading.setStyleSheet(f"""
            color: {PALETTE["text"]};
            background: transparent;
            border: none;
        """)

        calendar_heading_row.addWidget(calendar_heading)
        calendar_heading_row.addStretch()

        self.today_button = QPushButton("Today")
        self.today_button.setCursor(Qt.PointingHandCursor)
        self.today_button.setFixedHeight(34)
        self.today_button.setStyleSheet("""
            QPushButton {
                background-color: #EDF0E7;
                color: #168F80;
                border: none;
                border-radius: 8px;
                padding: 0 14px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #DDE8DF;
            }
            QPushButton:pressed {
                background-color: #D1E0D6;
            }
        """)

        calendar_heading_row.addWidget(self.today_button)
        calendar_layout.addLayout(calendar_heading_row)

        # Actual calendar
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumHeight(370)
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.NoVerticalHeader
        )
        self.calendar.setHorizontalHeaderFormat(
            QCalendarWidget.ShortDayNames
        )
        self.calendar.setGridVisible(False)
        self.calendar.setNavigationBarVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.Monday)

        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #FFFFFF;
                border: none;
            }

            QCalendarWidget QWidget {
                background-color: #FFFFFF;
                color: #303A36;
            }

            QCalendarWidget QToolButton {
                color: #303A36;
                background-color: #FFFFFF;
                border: none;
                border-radius: 7px;
                padding: 6px;
                font-size: 13px;
                font-weight: 600;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #F4F7F4;
                color: #168F80;
            }

            QCalendarWidget QToolButton::menu-indicator {
                image: none;
            }

            QCalendarWidget QSpinBox {
                color: #303A36;
                background-color: #FFFFFF;
                border: 1px solid #E1E7E3;
                border-radius: 5px;
                padding: 3px;
            }

            QCalendarWidget QTableView {
                background-color: #FFFFFF;
                alternate-background-color: #FFFFFF;
                selection-background-color: #168F80;
                selection-color: #FFFFFF;
                border: none;
                outline: none;
                gridline-color: #FFFFFF;
                font-size: 13px;
            }

            QCalendarWidget QTableView::item {
                border: none;
                padding: 4px;
            }

            QCalendarWidget QTableView::item:hover {
                background-color: #F4F7F4;
            }

            QCalendarWidget QHeaderView::section {
                color: #659B86;
                background-color: #FFFFFF;
                border: none;
                padding: 8px 0;
                font-size: 11px;
                font-weight: 600;
            }
        """)

        self.calendar_view = self.calendar.findChild(QTableView)

        if self.calendar_view is not None:
            self.calendar_delegate = CalendarDateDelegate(
                self.calendar_view
            )
            self.calendar_view.setItemDelegate(
                self.calendar_delegate
            )

        calendar_layout.addWidget(self.calendar, 1)

        # Add both cards
        content_layout.addWidget(self.features_card, 4)
        content_layout.addWidget(self.calendar_card, 6)

        main_layout.addLayout(content_layout, 1)

        # Buttons
        self.today_button.clicked.connect(self.go_to_today)

    def go_to_today(self):
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self.calendar.setCurrentPage(today.year(), today.month())
