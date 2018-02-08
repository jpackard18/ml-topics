from PyQt5.QtMultimedia import QMediaRecorder, QCamera, QCameraInfo, QCameraViewfinderSettings, QAudioEncoderSettings, QVideoEncoderSettings, QCameraImageCapture
import PyQt5.QtMultimedia as QtMultimedia
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtGui import QImage
#cv imports
import cv2
import numpy as np

import os
import time
from threading import Thread

def convertQImageToMat(qImage):
    '''  Converts a QImage into an opencv MAT format  '''
    
    qImage = qImage.convertToFormat(4)
    
    width = qImage.width()
    height = qImage.height()
    
    ptr = qImage.bits()
    ptr.setsize(qImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

def convertMatToQImage(cv_mat):
    height, width, channel = cv_mat.shape
    bytesPerLine = 3 * width
    qImg = QImage(cv_mat.data, width, height, bytesPerLine, QImage.Format_RGB888)

def displayQImageInCv(qImage):
    startTime = time.time()
    cv_img = convertQImageToMat(qImage)
    qImage = convertMatToQImage(cv_img)
    print(time.time() - startTime)


class Camera(QObject):
    def __init__(self, parent=QObject()):
        super(Camera, self).__init__(parent)
        # chooses the system default camera
        self.cam = QCamera()
        self.imageCapture = QCameraImageCapture(self.cam)
        self.caminfo = QCameraInfo(self.cam)
        self.camvfind = QCameraViewfinder()
        self.camvfindset = QCameraViewfinderSettings()
        self.recorder = QMediaRecorder(self.cam)

    def init_camera(self):
        cameras = QCameraInfo.availableCameras()
        for cameraInfo in cameras:
            # select the capturing device if it is available
            if (cameraInfo.description().find("Capture") is not -1):
                self.cam = QCamera(cameraInfo)
                self.caminfo = QCameraInfo(self.cam)
                self.recorder = QMediaRecorder(self.cam)
            print("Camera Chosen: " + self.caminfo.description())
        print(self.cam.supportedViewfinderFrameRateRanges())
        self.cam.setCaptureMode(QCamera.CaptureStillImage)
        if self.cam.isCaptureModeSupported(QCamera.CaptureStillImage):
            print("Capturemode supported")
        self.cam.load()
        self.cam.setViewfinder(self.camvfind)
        self.cam.start()
        
        self.imageCapture = QCameraImageCapture(self.cam)
        self.imageCapture.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)
        self.imageCapture.imageCaptured.connect(self.on_capture_still)
        self.capture_still()

    def on_capture_still(self, id, img):
        print(img)
        t = Thread(target=displayQImageInCv, args=(img,))
        t.start()
        t.join()
    def capture_still(self):
        self.cam.start()
        self.cam.searchAndLock()
        self.imageCapture.capture()
        self.cam.unlock()

    def start_vid(self):
        self.cam.load()
        # self.camvfind.show()
        self.cam.setViewfinder(self.camvfind)
        self.cam.setCaptureMode(QCamera.CaptureVideo)
        self.cam.start()

        audio = QAudioEncoderSettings()
        audio.setCodec("audio/amr")
        audio.setQuality(QtMultimedia.QMultimedia.NormalQuality)
        video = QVideoEncoderSettings()
        # video.setCodec("video/mp4")
        video.setQuality(QtMultimedia.QMultimedia.NormalQuality)
        video.setResolution(1920, 1080)
        video.setFrameRate(30.0)
        # self.recorder.setAudioSettings(audio)
        self.recorder.setVideoSettings(video)
        self.recorder.setContainerFormat("mp4")

        print("Output Loc: " + str(self.recorder.outputLocation()))

    def start_recording(self):
        directory = os.path.abspath(str(os.getcwd()))
        filename = "test" + str(time.time()) + ".mp4"
        abs_path = os.path.join(directory, filename)
        self.recorder.setOutputLocation(QUrl(abs_path))
        self.recorder.record()

    def stop_recording(self):
        self.recorder.stop()
