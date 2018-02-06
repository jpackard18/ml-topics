import sys
import PyQt5.QtGui
from .camera import *
from .gui import *


if __name__ == '__main__':

    app = PyQt5.QtWidgets.QApplication(sys.argv)
    camera = Camera()
    
    window = VideoWindow(camera)
    window.resize(1000, 600)
    window.show()
    
    # run the app
    return_code = app.exec_()
    camera.stop_recording()
    print("stopped")
    sys.exit(return_code)
