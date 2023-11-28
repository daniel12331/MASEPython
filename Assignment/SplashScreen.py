from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class SplashScreen(QtWidgets.QSplashScreen):

    def __init__(self, pathToGIF):
        self.movie = QtGui.QMovie(pathToGIF)
        self.movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(self.movie.frameRect().size())
        QtWidgets.QSplashScreen.__init__(self, pixmap)
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self, None)

def preformSplashScreen():
    app = QtWidgets.QApplication(sys.argv)

    pathToGIF = "images/eric-gif.gif"
    splash = SplashScreen(pathToGIF)
    splash.show()

    def showWindow():
        splash.close()
        form.close()

    QtCore.QTimer.singleShot(5200, showWindow)
    form = MainWindow()
    app.exec_()
    app.exit()
