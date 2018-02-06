from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import camera

class ConfigurationWindow(QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        

class VideoWindow(QMainWindow):

    def onQuit(self):
        self.close()

    def __init__(self, camera, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.camera = camera
        # quit on alt+f4 or ctrl+w
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)
        # Create a widget for window contents
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
		# create the top status display row
        
		
        # create the mainlayout that contains the viewfiner and controls
        mainLayout = QVBoxLayout()
        # mainLayout.addLayout(self.infoDisplay) # add the top status bar
        mainLayout.addWidget(self.camera.getViewFinder())

        # apply the mainlayout
        centralWidget.setLayout(mainLayout)
