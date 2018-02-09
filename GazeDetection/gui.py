from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import cv2

from camera import *
from CVEyeIsolation.EyeDetection import detectEyes

class ConfigurationWindow(QMainWindow):

    def __init__(self):
        super(ConfigurationWindow, self).__init__()


class VideoWindow(QMainWindow):

    def on_quit(self):
        self.close()

    def __init__(self, parent=None):

        super(VideoWindow, self).__init__(parent)
        self.camera = Camera()
        self.camera.init_camera()
        self.camera.setOnCapture(callback=self.on_capture_still)
        # quit on alt+f4 or ctrl+w
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.on_quit)
        # Create a widget for window contents
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # create the top status display row
        # create the main layout that contains the viewfinder and controls
        main_layout = QVBoxLayout()
        hor_layout = QHBoxLayout()
        #add a capture button
        self.imageLabel = QLabel()
        self.cap_button = QPushButton()
        self.cap_button.clicked.connect(self.capture_still)
        self.cap_button.setText("Capture Still")
        hor_layout.addWidget(self.camera.camvfind)
        hor_layout.addWidget(self.imageLabel)
        main_layout.addLayout(hor_layout)
        main_layout.addWidget(self.cap_button)
        # apply the main layout
        central_widget.setLayout(main_layout)

        #automatically capture stills
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.capture_still)
        #self.timer.start(200)

    def capture_still(self):
        self.cam.searchAndLock()
        self.camera.capture_still()
        self.cam.unlock()

    def on_capture_still(self, id, img):
        self.displayQImageInCv(img)

    def displayQImageInCv(self, qImage):
        startTime = time.time()
        cv_img = VideoWindow.convertQImageToMat(qImage)
        cv_img, eyes = detectEyes(cv_img)
        print(eyes)
        qImage = VideoWindow.convertMatToQImage(cv_img)
        self.imageLabel.setPixmap(QPixmap.fromImage(qImage))
        self.imageLabel.show()
        timeDelta = time.time() - startTime
        print("Time taken for eye detection: " + str(timeDelta))

    @staticmethod
    def convertQImageToMat(qImage):
        '''  Converts a QImage into an opencv MAT format  '''
        qImage = qImage.convertToFormat(4)
        width = qImage.width()
        height = qImage.height()
        
        ptr = qImage.bits()
        ptr.setsize(qImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr

    @staticmethod
    def convertMatToQImage(cv_mat):
        '''  Converts an opencv MAT image to a QImage  '''
        # convert to rgb
        cv_mat = cv2.cvtColor(cv_mat, cv2.COLOR_BGR2RGB)
        height, width, channel = cv_mat.shape
        bytesPerLine = 3 * width
        qImage = QImage(cv_mat.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImage

