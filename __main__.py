import sys
import PyQt5
from GazeDetection.gui import *


app = PyQt5.QtWidgets.QApplication(sys.argv)

window = VideoWindow()
window.resize(1000, 600)
window.show()

# run the app
return_code = app.exec_()
print("stopped")
sys.exit(return_code)
