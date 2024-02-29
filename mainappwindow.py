import os
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from dotenv import load_dotenv

from ui import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.common.by import By


def load_javascript(filename):
    with open(filename, 'r') as file:
        return file.read()


javascript_content = load_javascript("./injectables/button.js")


def was_button_clicked(driver):
    return driver.execute_script("return document.getElementById('seleniumHiddenInput').value;") == "clicked"


class Worker(QThread):
    buttonClicked = pyqtSignal()

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def run(self):
        while True:
            if was_button_clicked(self.driver):
                self.buttonClicked.emit()
                break
            time.sleep(1)


def open_page():
    # Load environment variables
    load_dotenv()

    # Your LinkedIn credentials from environment variables
    username = os.getenv("LINKEDIN_USER")
    password = os.getenv("LINKEDIN_PASS")

    # Set up the WebDriver
    driver = webdriver.Chrome()

    # Open LinkedIn
    driver.get("https://www.linkedin.com/login")

    # Use the updated method to find the element
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    # Add further automation steps here...

    driver.find_element(By.CSS_SELECTOR, ".login__form_action_container ").click()

    driver.execute_script(javascript_content)

    return driver


class MainApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    isBrowserOpen = False
    driver = None
    worker = None
    timer = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Apply the UI setup to this instance
        self.openButton.setText("Open Browser")  # Change the button text
        self.openButton.setToolTip("Click to open the browser")  # Add a tooltip to the button
        self.timer = QtCore.QTimer(self)
        self.openButton.clicked.connect(self.onOpenButtonClicked)  # Connect the button to the function
        self.openButton.setEnabled(True)

        # self.textEdit.textChanged.connect(self.onTextChange)

    def onOpenButtonClicked(self, event):
        if not self.isBrowserOpen:
            self.isBrowserOpen = True
            self.driver = open_page()
            self.worker = Worker(self.driver)
            self.worker.buttonClicked.connect(self.jobChosen)
            self.worker.start()
            self.timer.start()
        else:
            if self.driver:
                self.driver.quit()
            self.isBrowserOpen = False
            self.timer.stop()

    def mouseMoveEvent(self, event):
        print("Mouse moved")
        # open_page()

    def jobChosen(self):
        print("Job chosen")
