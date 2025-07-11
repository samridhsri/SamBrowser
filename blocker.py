from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl

class Blocker(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocked_sites = []
        self.study_mode_enabled = False

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if self.study_mode_enabled and isMainFrame:
            host = url.host()
            for site in self.blocked_sites:
                if site in host:
                    self.setUrl(QUrl("about:blank")) # Or a custom blocked page
                    return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

    def set_blocked_sites(self, sites):
        self.blocked_sites = sites

    def toggle_study_mode(self, enabled):
        self.study_mode_enabled = enabled 