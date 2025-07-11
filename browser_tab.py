from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from blocker import Blocker

class BrowserTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout(self)

        self.browser = QWebEngineView()
        self.blocker = Blocker()
        self.browser.setPage(self.blocker)
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.note_editor = QTextEdit()
        self.note_editor.setPlaceholderText("Notes for this page...")
        self.note_editor.setFixedHeight(100)

        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.note_editor)

        self.browser.urlChanged.connect(self.update_url_in_address_bar)
        self.browser.loadFinished.connect(self.update_tab_title)

    def update_url_in_address_bar(self, qurl):
        # Only update the main window's address bar if this tab is the current one
        if self.main_window.tabs.currentWidget() == self:
            self.main_window.address_bar.setText(qurl.toString())

    def update_tab_title(self):
        index = self.main_window.tabs.indexOf(self)
        if index != -1:
            title = self.browser.page().title()
            self.main_window.tabs.setTabText(index, title[:20]) # Truncate title 