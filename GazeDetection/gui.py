from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QThread
import cv2

from camera import *
from CVEyeIsolation.EyeDetection import detectEyes

class EyeDetectionWorker(QThread):

    def __init__(self, cap, imageLabelDisplay):
        QThread.__init__(self)
        self.cap = cap
        self.imageLabelDisplay = imageLabelDisplay
        self.stopped = False

    def stopp(self):
        self.stopped = True

    #grabs an image and processes it
    def run(self):
        while(True and not self.stopped):
            startTime = time.time()
            ret, frame = self.cap.read()
            result_img, eyes = detectEyes(frame)
            print(eyes)
            qImage = VideoWindow.convertMatToQImage(result_img)
            self.imageLabelDisplay.setPixmap(QPixmap.fromImage(qImage))
            self.imageLabelDisplay.show()
            timeDelta = time.time() - startTime
            print("Time taken for eye detection: " + str(timeDelta))
        self.quit()


class VideoWindow(QMainWindow):

    def closeEvent(self, event):
        self.worker.stopp()
        self.cap.release()
        self.close()

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.cap = cv2.VideoCapture(0)
        # quit on alt+f4 or ctrl+w
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.closeEvent)
        # Create a widget for window contents
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # create the top status display row
        # create the main layout that contains the viewfinder and controls
        main_layout = QVBoxLayout()
        hor_layout = QHBoxLayout()
        #add a capture button
        self.imageLabel = QLabel()
        hor_layout.addWidget(self.imageLabel)
        main_layout.addLayout(hor_layout)
        # apply the main layout
        central_widget.setLayout(main_layout)

        #automatically capture stills
        self.worker = EyeDetectionWorker(self.cap, self.imageLabel)
        self.worker.start()

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

