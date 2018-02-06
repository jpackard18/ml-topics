from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ConfigurationWindow(QMainWindow):

    def __init__(self):
        super(ConfigurationWindow, self).__init__()


class VideoWindow(QMainWindow):

    def on_quit(self):
        self.close()

    def __init__(self, camera, parent=None):

        super(VideoWindow, self).__init__(parent)
        self.camera = camera
        self.camera.init_camera()
        self.camera.start_vid()
        # quit on alt+f4 or ctrl+w
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)
        # Create a widget for window contents
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # create the top status display row
        # create the main layout that contains the viewfinder and controls
        main_layout = QVBoxLayout()
        # mainLayout.addLayout(self.infoDisplay) # add the top status bar
        main_layout.addWidget(self.camera.getViewFinder())
        # apply the main layout
        central_widget.setLayout(main_layout)
