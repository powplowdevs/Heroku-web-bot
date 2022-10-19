import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWebEngineWidgets import *

app=QtWidgets.QApplication(sys.argv)
w=QWebEngineView()
w.load(QtCore.QUrl('https://google.com')) ## load google on startup
w.showMaximized()

app.exec_()