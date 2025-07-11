from PyQt6.QtWidgets import QMainWindow, QToolBar, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTabWidget, QTextEdit, QLabel, QMessageBox
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QAction
from browser_tab import BrowserTab
from pomodoro import PomodoroTimer

class StudyNavigator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Navigator")
        self.setGeometry(100, 100, 1080, 720)

        # --- Toolbar and Controls ---
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        self.back_button = QPushButton("<-")
        self.back_button.clicked.connect(self.go_back)
        self.toolbar.addWidget(self.back_button)

        self.forward_button = QPushButton("->")
        self.forward_button.clicked.connect(self.go_forward)
        self.toolbar.addWidget(self.forward_button)

        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)
        self.toolbar.addWidget(self.reload_button)

        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.address_bar)

        # --- Tabs ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)

        self.add_new_tab_button = QPushButton("+")
        self.add_new_tab_button.clicked.connect(lambda: self.add_new_tab())
        self.tabs.setCornerWidget(self.add_new_tab_button, Qt.Corner.TopLeftCorner)

        self.add_new_tab(QUrl("http://www.google.com"), "Homepage")

        # --- Study Mode ---
        self.study_mode_action = QAction("Study Mode", self)
        self.study_mode_action.setCheckable(True)
        self.study_mode_action.triggered.connect(self.toggle_study_mode)
        self.toolbar.addAction(self.study_mode_action)
        self.blocked_sites = ["www.youtube.com", "www.facebook.com", "www.reddit.com"]

        # --- Pomodoro Timer ---
        self.pomodoro_label = QLabel("Pomodoro: 25:00")
        self.toolbar.addWidget(self.pomodoro_label)
        self.start_pomodoro_button = QPushButton("Start Work")
        self.start_pomodoro_button.clicked.connect(self.toggle_pomodoro)
        self.toolbar.addWidget(self.start_pomodoro_button)

        self.pomodoro = PomodoroTimer()
        self.pomodoro.timer_updated.connect(self.update_pomodoro_label)
        self.pomodoro.state_changed.connect(self.handle_state_change)
        self.pomodoro.session_finished.connect(self.handle_session_finished)

    def add_new_tab(self, qurl=QUrl("http://www.google.com"), label="New Tab"):
        tab = BrowserTab(self)
        tab.browser.setUrl(qurl)
        i = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(i)

    def close_tab(self, i):
        if self.tabs.count() < 2:
            self.close() # Close the window if the last tab is closed
        else:
            self.tabs.removeTab(i)

    def tab_changed(self, i):
        if i != -1:
            tab = self.tabs.widget(i)
            self.address_bar.setText(tab.browser.url().toString())

    def navigate_to_url(self):
        qurl = QUrl(self.address_bar.text())
        if qurl.scheme() == "":
            qurl.setScheme("http")
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.setUrl(qurl)

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.forward()

    def reload_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.reload()

    def toggle_study_mode(self, checked):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            tab.blocker.set_blocked_sites(self.blocked_sites if checked else [])
            tab.blocker.toggle_study_mode(checked)
        if checked:
            QMessageBox.information(self, "Study Mode", "Study Mode is now ON.")
        else:
            QMessageBox.information(self, "Study Mode", "Study Mode is now OFF.")

    def toggle_pomodoro(self):
        if not self.pomodoro.is_running:
            self.pomodoro.reset(True)
            self.pomodoro.start()
            self.study_mode_action.setChecked(True)
            self.toggle_study_mode(True)
            self.start_pomodoro_button.setText("Pause")
        else:
            self.pomodoro.pause()
            self.start_pomodoro_button.setText("Start Work")

    def update_pomodoro_label(self, mins, secs):
        self.pomodoro_label.setText(f"Pomodoro: {mins:02d}:{secs:02d}")

    def handle_state_change(self, is_work_time):
        self.study_mode_action.setChecked(is_work_time)
        self.toggle_study_mode(is_work_time)

    def handle_session_finished(self, is_work_time):
        if is_work_time:
            QMessageBox.information(self, "Pomodoro", "Break is over. Time to work!")
        else:
            QMessageBox.information(self, "Pomodoro", "Work session is over. Time for a break!") 