import json
import os
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from dotenv import load_dotenv

from Job import Job
from ui import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.common.by import By


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


javascript_content = read_file("./injectables/button.js")
style_content = read_file("injectables/jca-style.css")


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

    driver.get("https://www.linkedin.com/jobs/collections/recommended")
    driver.execute_script(javascript_content)
    driver.execute_script(
        'document.head.appendChild(document.createElement("style")).innerHTML = `{}`'.format(style_content))

    return driver


class MainApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    isBrowserOpen = False
    driver = None
    worker = None
    timer = None
    jobs = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Apply the UI setup to this instance
        self.openButton.setText("Open Browser")  # Change the button text
        self.openButton.setToolTip("Click to open the browser")  # Add a tooltip to the button
        # self.timer = QtCore.QTimer(self)
        self.openButton.clicked.connect(self.onOpenButtonClicked)  # Connect the button to the function
        self.openButton.setEnabled(True)

        self.captureJobs.clicked.connect(self.jobChosen)

        # self.textEdit.textChanged.connect(self.onTextChange)

    def onOpenButtonClicked(self, event):
        if not self.isBrowserOpen:
            self.isBrowserOpen = True
            self.driver = open_page()
            # self.worker = Worker(self.driver)
            # self.worker.buttonClicked.connect(self.jobChosen)
            self.openButton.text = "Close Browser"
            # self.worker.start()
            # self.timer.start()
        else:
            if self.driver:
                self.driver.quit()
            self.isBrowserOpen = False
            # self.timer.stop()
            self.openButton.text = "Close Browser"

    def mouseMoveEvent(self, event):
        print("Mouse moved")
        # open_page()

    def jobChosen(self):
        jobsJson = self.fetch_jobs()

        jobs = json.loads(jobsJson)
        print(jobs['job_ids'])

        for job_id in jobs['job_ids']:
            item = QtWidgets.QListWidgetItem()
            self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}/")

            company_element = self.driver.find_element(By.CSS_SELECTOR,
                                                       ".job-details-jobs-unified-top-card__primary-description-container")
            company_name = self.driver.find_element(By.TAG_NAME, "a").text
            company_url = self.driver.find_element(By.TAG_NAME, "a").get_attribute("href")
            job_title = self.driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title").text
            job = Job(job_id, job_title, company_name, company_url, "Location")
            item.setText(job_title)
            self.listWidget.addItem(item)
            self.jobs.append(job)

        print(self.jobs)

    def fetch_jobs(self):
        return self.driver.execute_script("return document.getElementById('jca-job_ids').value;")
