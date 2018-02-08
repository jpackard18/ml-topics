import sys
import PyQt5.QtGui
from gui import *


if __name__ == '__main__':

    app = PyQt5.QtWidgets.QApplication(sys.argv)
    
    window = VideoWindow()
    window.resize(1000, 600)
    window.show()
    
    # run the app
    return_code = app.exec_()
    camera.stop_recording()
    print("stopped")
    sys.exit(return_code)
