from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import sys
from PyQt5 import QtWidgets

from mainappwindow import MainApplicationWindow
from ui import Ui_MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainApplicationWindow()
    mainWin.show()
    sys.exit(app.exec_())
