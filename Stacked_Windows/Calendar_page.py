from PyQt5.QtCore import Qt, QRectF, QDate
from PyQt5.QtGui import (
    QColor,
    QPainter,
    QFont,
    QIcon,
    QTextCharFormat,
    QBrush,
)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QCalendarWidget,
    QStyledItemDelegate,
    QStyle,
    QTableView,
    QToolButton,
    QPushButton,
    QGraphicsDropShadowEffect,
)


# ---------------------------------------------------------------------------
# Layout scale (one set of numbers used everywhere on this page)
# ---------------------------------------------------------------------------

PAGE_MARGIN_X = 18
PAGE_MARGIN_Y = 16
GAP = 16               # between page header, cards, and card contents
CARD_PAD = 20          # inner padding of every card
CARD_HEADER_H = 32     # every card header row has the same height


# ---------------------------------------------------------------------------
# Helpers (same shadow as main.py)
# ---------------------------------------------------------------------------

def add_card_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(10)
    shadow.setOffset(0, 2)
    shadow.setColor(QColor(0, 0, 0, 30))
    widget.setGraphicsEffect(shadow)


def create_card(object_name):
    card = QWidget()
    card.setObjectName(object_name)
    card.setAttribute(Qt.WA_StyledBackground, True)
    add_card_shadow(card)
    return card


def create_label(text, object_name, wrap=False, center=False):
    label = QLabel(text)
    label.setObjectName(object_name)
    if wrap:
        label.setWordWrap(True)
    if center:
        label.setAlignment(Qt.AlignCenter)
    return label


# ---------------------------------------------------------------------------
# Calendar cell painter (identical to main.py)
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


# ---------------------------------------------------------------------------
# Calendar page
# ---------------------------------------------------------------------------

class CalendarPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("CalendarPage")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.initUI()
        self.styleNavButtons()
        self.styleDateFormats()
        self.applyStyles()
        self.styleCalendar()

        self.today_button.clicked.connect(self.go_to_today)

    # ---------------- layout ----------------

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            PAGE_MARGIN_X, PAGE_MARGIN_Y, PAGE_MARGIN_X, PAGE_MARGIN_Y
        )
        main_layout.setSpacing(GAP)

        # Page heading
        heading_layout = QVBoxLayout()
        heading_layout.setSpacing(4)
        heading_layout.addWidget(create_label("Calendar", "PageTitle"))
        heading_layout.addWidget(
            create_label("A clearer view of your days.", "PageSubtitle")
        )
        main_layout.addLayout(heading_layout)

        # Content: calendar (left) + coming soon (right)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(GAP)

        self.calendar_card = self.build_calendar_card()
        self.features_card = self.build_features_card()

        content_layout.addWidget(self.calendar_card, 6)
        content_layout.addWidget(self.features_card, 4)

        main_layout.addLayout(content_layout, 1)

    def build_calendar_card(self):
        card = create_card("ScheduleCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(CARD_PAD, CARD_PAD, CARD_PAD, CARD_PAD)
        layout.setSpacing(GAP)

        # Header row: title + Today button
        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        heading = create_label("Your Schedule", "CardTitle")
        heading.setMinimumHeight(CARD_HEADER_H)

        self.today_button = QPushButton("Today")
        self.today_button.setObjectName("TodayButton")
        self.today_button.setCursor(Qt.PointingHandCursor)
        self.today_button.setFixedHeight(CARD_HEADER_H)

        header_row.addWidget(heading)
        header_row.addStretch()
        header_row.addWidget(self.today_button)
        layout.addLayout(header_row)

        # Calendar (same configuration as main.py)
        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendar.setGridVisible(False)
        self.calendar.setNavigationBarVisible(True)
        self.calendar_view = self.calendar.findChild(QTableView)
        self.calendar_delegate = CalendarDateDelegate(self.calendar_view)
        self.calendar_view.setItemDelegate(self.calendar_delegate)

        layout.addWidget(self.calendar, 1)
        return card

    def build_features_card(self):
        card = create_card("FeaturesCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(CARD_PAD, CARD_PAD, CARD_PAD, CARD_PAD)
        layout.setSpacing(GAP)

        heading = create_label("Coming Soon", "CardTitle")
        heading.setMinimumHeight(CARD_HEADER_H)

        subtitle = create_label(
            "More ways to plan your time are on the way.",
            "CardSubtitle",
            wrap=True,
        )

        # Placeholder box
        placeholder = QWidget()
        placeholder.setObjectName("Placeholder")
        placeholder.setAttribute(Qt.WA_StyledBackground, True)

        placeholder_layout = QVBoxLayout(placeholder)
        placeholder_layout.setContentsMargins(CARD_PAD, CARD_PAD, CARD_PAD, CARD_PAD)
        placeholder_layout.setSpacing(8)
        placeholder_layout.setAlignment(Qt.AlignCenter)

        placeholder_layout.addWidget(
            create_label("✦", "PlaceholderIcon", center=True)
        )
        placeholder_layout.addWidget(
            create_label("Something new is coming", "PlaceholderTitle",
                         wrap=True, center=True)
        )
        placeholder_layout.addWidget(
            create_label("We're making space for more useful features.",
                         "PlaceholderText", wrap=True, center=True)
        )

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addWidget(placeholder, 1)
        return card

    # ---------------- calendar styling (same as main.py) ----------------

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

    def styleCalendar(self):
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

    # ---------------- page styling ----------------
    # Type scale (Nunito, same as main.py):
    #   26/800 page title - 19/800 card title - 14/700 placeholder title
    #   13/400 subtitles  - 12/400 small text - 12/700 buttons

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget#CalendarPage {
                background-color: #F5F5F3;
            }

            QWidget#ScheduleCard,
            QWidget#FeaturesCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E9E6;
                border-radius: 16px;
            }

            QLabel {
                background: transparent;
                border: none;
                font-family: Nunito;
            }

            QLabel#PageTitle {
                color: #1F2421;
                font-size: 26px;
                font-weight: 800;
            }

            QLabel#PageSubtitle {
                color: #5F6561;
                font-size: 13px;
                font-weight: 400;
            }

            QLabel#CardTitle {
                color: #1F2421;
                font-size: 19px;
                font-weight: 800;
            }

            QLabel#CardSubtitle {
                color: #5F6561;
                font-size: 13px;
                font-weight: 400;
            }

            QWidget#Placeholder {
                background-color: #F5F5F3;
                border: 1px dashed #D5DED6;
                border-radius: 12px;
            }

            QLabel#PlaceholderIcon {
                color: #168F80;
                font-size: 30px;
                font-weight: 700;
            }

            QLabel#PlaceholderTitle {
                color: #1F2421;
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#PlaceholderText {
                color: #777F79;
                font-size: 12px;
                font-weight: 400;
            }

            QPushButton#TodayButton {
                background-color: #E3F1EE;
                color: #0D6B60;
                border: none;
                border-radius: 10px;
                padding: 0px 14px;
                font-family: Nunito;
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#TodayButton:hover {
                background-color: #CFE7E2;
            }

            QPushButton#TodayButton:pressed {
                background-color: #BFDDD6;
            }
        """)

    # ---------------- behaviour ----------------

    def go_to_today(self):
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self.calendar.setCurrentPage(today.year(), today.month())