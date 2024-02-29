import os

from PyQt5 import QtWidgets, QtCore
from dotenv import load_dotenv

from ui import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.common.by import By


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

    return driver


class MainApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    isBrowserOpen = False
    driver = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Apply the UI setup to this instance
        self.openButton.setText("Open Browser")  # Change the button text
        self.openButton.setToolTip("Click to open the browser")  # Add a tooltip to the button
        self.openButton.clicked.connect(self.onOpenButtonClicked)  # Connect the button to the function
        self.openButton.setEnabled(True)

        # self.textEdit.textChanged.connect(self.onTextChange)

    def onOpenButtonClicked(self, event):
        if not self.isBrowserOpen:
            self.isBrowserOpen = True
            self.driver = open_page()
        else:
            if self.driver:
                self.driver.quit()
            self.isBrowserOpen = False

    def mouseMoveEvent(self, event):
        print("Mouse moved")
        # open_page()
