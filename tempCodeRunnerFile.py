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

