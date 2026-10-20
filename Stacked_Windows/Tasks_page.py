from veltrio_icons import VeltrioIcons
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QCheckBox,
    QVBoxLayout, QHBoxLayout, QFrame,
    QScrollArea, QSizePolicy, QVBoxLayout,
    QGraphicsDropShadowEffect, 

)
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor


PALETTE = {
    "background": "#FFFFFF",
    "surface": "#FFFFFF",
    "text": "#303A36",
    "muted_text": "#659B86",
    "accent": "#168F80",
    "border": "#E1E7E3",
    "soft_green": "#EDF0E7",
    "hover": "#F4F7F4",
    "completed_text": "#9AA6A0",
}


def add_card_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(8)
    shadow.setOffset(0, 1)
    shadow.setColor(QColor(0, 0, 0, 22))
    widget.setGraphicsEffect(shadow)


class TasksPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TasksPage")
        self.tasks = []

        self.setup_ui()
        self.load_sample_tasks()

    # --------------------------------------------------
    # Main layout
    # --------------------------------------------------

    def setup_ui(self):
        self.setStyleSheet(f"""
            QWidget#TasksPage {{
                background: {PALETTE["background"]};
                color: {PALETTE["text"]};
                font-family: "Segoe UI";
                font-size: 14px;
            }}

            QLabel {{
                background: transparent;
                border: none;
                color: {PALETTE["text"]};
            }}

            QCheckBox {{
                spacing: 8px;
                background: transparent;
                color: {PALETTE["text"]};
            }}

            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 1px solid {PALETTE["border"]};
                border-radius: 5px;
                background: white;
            }}

            QCheckBox::indicator:checked {{
                background: {PALETTE["accent"]};
                border: 1px solid {PALETTE["accent"]};
            }}

            QScrollArea {{
                border: none;
                background: transparent;
            }}

            QScrollBar:vertical {{
                background: {PALETTE["soft_green"]};
                width: 8px;
                margin: 3px 1px;
                border-radius: 4px;
            }}

            QScrollBar::handle:vertical {{
                background: {PALETTE["accent"]};
                border-radius: 4px;
                min-height: 30px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: #11796D;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
                border: none;
            }}

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)

        self.main_hbox = QHBoxLayout(self)
        self.main_hbox.setContentsMargins(18, 16, 18, 16)
        self.main_hbox.setSpacing(16)

        # Left: task manager
        self.task_area = QFrame()
        self.task_area.setObjectName("TaskArea")
        self.task_area.setMinimumWidth(380)
        self.task_area.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.task_area.setStyleSheet(f"""
            QFrame#TaskArea {{
                background: {PALETTE["surface"]};
                border: 0px dashed {PALETTE["border"]};
                border-radius: 12px;
            }}
        """)

        self.task_vbox = QVBoxLayout(self.task_area)
        self.task_vbox.setContentsMargins(18, 16, 18, 16)
        self.task_vbox.setSpacing(12)
        add_card_shadow(self.task_area)

        self.create_header()

        # Three equal-height sections, stacked vertically
        self.sections_vbox = QVBoxLayout()
        self.sections_vbox.setContentsMargins(0, 0, 0, 0)
        self.sections_vbox.setSpacing(10)

        self.today_section = self.create_section("Today")
        self.yesterday_section = self.create_section("Yesterday")
        self.previously_section = self.create_section("Previously")

        self.sections_vbox.addWidget(self.today_section, 1)
        self.sections_vbox.addWidget(self.yesterday_section, 1)
        self.sections_vbox.addWidget(self.previously_section, 1)

        self.task_vbox.addLayout(self.sections_vbox, 1)

        # Right: insights panel
        self.insights_area = QFrame()
        self.insights_area.setObjectName("InsightsArea")
        self.insights_area.setMinimumWidth(150)
        self.insights_area.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        self.insights_area.setStyleSheet(f"""
            QFrame#InsightsArea {{
                background: {PALETTE["surface"]};
                border: 0px dashed {PALETTE["border"]};
                border-radius: 12px;
            }}
        """)

        add_card_shadow(self.insights_area)


        insights_layout = QVBoxLayout(self.insights_area)
        insights_layout.setContentsMargins(24, 24, 24, 24)
        insights_layout.setSpacing(10)
        insights_layout.setAlignment(Qt.AlignCenter)

        self.insights_placeholder = QLabel("Your insights will appear here")
        self.insights_placeholder.setAlignment(Qt.AlignCenter)
        self.insights_placeholder.setStyleSheet("""
            QLabel {
                color: #303A36;
                font-size: 18px;
                font-weight: 700;
                background: transparent;
            }
        """)

        self.insights_subtitle = QLabel(
            "Not yet Functional."
        )
        self.insights_subtitle.setAlignment(Qt.AlignCenter)
        self.insights_subtitle.setWordWrap(True)
        self.insights_subtitle.setStyleSheet("""
            QLabel {
                color: #8A9690;
                font-size: 13px;
                font-weight: 400;
                background: transparent;
            }
        """)

        insights_layout.addWidget(self.insights_placeholder)
        insights_layout.addWidget(self.insights_subtitle)

        self.main_hbox.addWidget(self.task_area, 7)
        self.main_hbox.addWidget(self.insights_area, 4)

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    def create_header(self):
        header_hbox = QHBoxLayout()
        header_hbox.setContentsMargins(0, 0, 0, 4)
        header_hbox.setSpacing(12)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(4)

        title = QLabel("My Tasks")
        title.setStyleSheet("""
            font-size: 27px;
            font-weight: 700;
        """)

        subtitle = QLabel("Plan your work. Own your time.")
        subtitle.setStyleSheet(f"""
            font-size: 13px;
            color: {PALETTE["muted_text"]};
        """)

        title_vbox.addWidget(title)
        title_vbox.addWidget(subtitle)

        self.new_task_button = QPushButton("New task")
        VeltrioIcons.apply(self.new_task_button, "increase_time")
        self.new_task_button.setCursor(Qt.PointingHandCursor)
        self.new_task_button.setMinimumHeight(42)

        self.new_task_button.setStyleSheet(f"""
            QPushButton {{
                background: {PALETTE["accent"]};
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background: #11796D;
            }}
        """)

        self.new_task_button.clicked.connect(self.add_new_task)

        header_hbox.addLayout(title_vbox)
        header_hbox.addStretch()
        header_hbox.addWidget(self.new_task_button)

        self.task_vbox.addLayout(header_hbox)

    # --------------------------------------------------
    # Independent task sections
    # --------------------------------------------------

    def create_section(self, section_name):
        section = QFrame()
        section.setObjectName("TaskSection")
        section.setSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Expanding
        )

        section.setStyleSheet("""
            QFrame#TaskSection {
                background-color: #FFFFFF;
                border: none;
            }

            QScrollArea {
                background-color: #FFFFFF;
                border: none;
            }

            QScrollArea QWidget#qt_scrollarea_viewport {
                background-color: #FFFFFF;
                border: none;
            }
        """)

        section_vbox = QVBoxLayout(section)
        section_vbox.setContentsMargins(12, 10, 10, 10)
        section_vbox.setSpacing(8)

        # Fixed heading
        heading = QLabel(section_name)
        heading.setStyleSheet("""
            font-size: 17px;
            font-weight: 700;
        """)

        section_vbox.addWidget(heading)

        # Each section has its own scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setMinimumHeight(0)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        scroll_area.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        scroll_content = QWidget()
        scroll_content.setStyleSheet(
            "background: transparent;"
        )

        task_layout = QVBoxLayout(scroll_content)
        task_layout.setContentsMargins(0, 0, 3, 0)
        task_layout.setSpacing(10)

        footer = QLabel("That's everything for now.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setWordWrap(True)
        footer.setStyleSheet(f"""
            font-size: 12px;
            color: {PALETTE["muted_text"]};
            padding: 12px 4px;
        """)

        task_layout.addWidget(footer)
        task_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        section_vbox.addWidget(scroll_area, 1)

        section.task_layout = task_layout
        section.task_count = 0
        section.section_name = section_name
        section.scroll_area = scroll_area
        section.scroll_content = scroll_content
        section.footer = footer

        

        return section

    # --------------------------------------------------
    # Task card
    # --------------------------------------------------

    def create_task_card(
        self,
        task_name,
        task_time,
        category,
        completed=False
    ):
        card = QFrame()
        card.setObjectName("TaskCard")

        card.setStyleSheet(f"""
            QFrame#TaskCard {{
                background: {PALETTE["surface"]};
                border: 1px solid {PALETTE["border"]};
                border-radius: 8px;
            }}

            QFrame#TaskCard:hover {{
                background: {PALETTE["hover"]};
            }}
        """)

        card_hbox = QHBoxLayout(card)

        # Increased vertical padding makes each task card taller
        card_hbox.setContentsMargins(14, 18, 14, 18)
        card_hbox.setSpacing(12)

        checkbox = QCheckBox()
        checkbox.setChecked(completed)
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.setToolTip("Mark task as completed")

        details_vbox = QVBoxLayout()
        details_vbox.setSpacing(5)

        name_label = QLabel(task_name)
        name_label.setWordWrap(True)
        name_label.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 600;
            color: {PALETTE["text"]};
        """)

        time_label = QLabel(f"◷  {task_time}")
        time_label.setStyleSheet(f"""
            font-size: 12px;
            color: {PALETTE["muted_text"]};
        """)

        details_vbox.addWidget(name_label)
        details_vbox.addWidget(time_label)

        category_label = QLabel(category)
        category_label.setAlignment(Qt.AlignCenter)
        category_label.setWordWrap(True)
        category_label.setStyleSheet(f"""
            background: {PALETTE["soft_green"]};
            color: {PALETTE["text"]};
            border-radius: 5px;
            padding: 5px 7px;
            font-size: 11px;
        """)

        card_hbox.addWidget(checkbox, 0, Qt.AlignVCenter)
        card_hbox.addLayout(details_vbox, 1)
        card_hbox.addWidget(category_label, 0, Qt.AlignVCenter)

        def update_completion(checked):
            if checked:
                name_label.setStyleSheet(f"""
                    font-size: 15px;
                    font-weight: 600;
                    color: {PALETTE["completed_text"]};
                    text-decoration: line-through;
                """)
            else:
                name_label.setStyleSheet(f"""
                    font-size: 15px;
                    font-weight: 600;
                    color: {PALETTE["text"]};
                """)

        checkbox.toggled.connect(update_completion)
        update_completion(completed)

        self.tasks.append({
            "name": task_name,
            "time": task_time,
            "category": category,
            "checkbox": checkbox,
            "card": card,
            "section": None,
        })

        return card

    # --------------------------------------------------
    # Add task
    # --------------------------------------------------

    def add_task(
        self,
        section,
        task_name,
        task_time,
        category,
        completed=False
    ):
        card = self.create_task_card(
            task_name,
            task_time,
            category,
            completed
        )

        footer_index = section.task_layout.indexOf(
            section.footer
        )

        section.task_layout.insertWidget(
            footer_index,
            card
        )

        section.task_count += 1
        self.tasks[-1]["section"] = section

        self.update_empty_state(section)

    # --------------------------------------------------
    # Empty-state message
    # --------------------------------------------------

    def update_empty_state(self, section):
        if section.task_count == 0:
            section.footer.setText(
                "No tasks yet.\nEnjoy the breathing room!"
            )
        else:
            section.footer.setText(
                "That's everything for now."
            )

    # --------------------------------------------------
    # Sample tasks and placeholders
    # --------------------------------------------------

    def load_sample_tasks(self):
        # Today
        self.add_task(
            self.today_section,
            "Revise DSA arrays",
            "09:00 AM",
            "School"
        )

        self.add_task(
            self.today_section,
            "Build the Tasks page",
            "11:30 AM",
            "Work",
            completed=True
        )

        for i in range(1, 11):
            self.add_task(
                self.today_section,
                f"Placeholder task {i}",
                "--:--",
                "Personal"
            )

        # Yesterday
        self.add_task(
            self.yesterday_section,
            "Finish college assignment",
            "04:00 PM",
            "School",
            completed=True
        )

        for i in range(1, 11):
            self.add_task(
                self.yesterday_section,
                f"Placeholder task {i}",
                "--:--",
                "Personal"
            )

        # Previously
        self.add_task(
            self.previously_section,
            "Organize project files",
            "Monday",
            "Personal"
        )

        for i in range(1, 11):
            self.add_task(
                self.previously_section,
                f"Placeholder task {i}",
                "--:--",
                "Personal"
            )

    # --------------------------------------------------
    # New task button (temporary)
    # --------------------------------------------------

    def add_new_task(self):
        print("New task button clicked!")