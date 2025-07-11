from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class PomodoroTimer(QObject):
    timer_updated = pyqtSignal(int, int)  # minutes, seconds
    state_changed = pyqtSignal(bool)      # is_work_time
    session_finished = pyqtSignal(bool)   # is_work_time

    def __init__(self, work_duration=25*60, break_duration=5*60):
        super().__init__()
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.is_work_time = True
        self.is_running = False
        self.time_left = self.work_duration
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)

    def pause(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()

    def reset(self, is_work_time=True):
        self.is_work_time = is_work_time
        self.time_left = self.work_duration if is_work_time else self.break_duration
        self.timer_updated.emit(*divmod(self.time_left, 60))
        self.state_changed.emit(self.is_work_time)

    def _tick(self):
        self.time_left -= 1
        mins, secs = divmod(self.time_left, 60)
        self.timer_updated.emit(mins, secs)
        if self.time_left <= 0:
            self.is_work_time = not self.is_work_time
            self.time_left = self.work_duration if self.is_work_time else self.break_duration
            self.session_finished.emit(self.is_work_time)
            self.state_changed.emit(self.is_work_time)
            self.timer_updated.emit(*divmod(self.time_left, 60)) 