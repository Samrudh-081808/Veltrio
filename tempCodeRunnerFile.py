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