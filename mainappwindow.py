import json
import os
import random
import re
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication
from dotenv import load_dotenv

from Config import Configuration
from GetProspectAPI import get_contact_info, response_to_linkedin_contact
from Gmail import Gmail
from Job import Job
from Recruiter import Recruiter
from ui import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.common.by import By


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


javascript_content = read_file("injectables/select-jobs.js")
recruiter_select = read_file("injectables/select-recruiter.js")
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


def clean_location_string(location):
    return location.strip().strip('·').strip()


def process_job_description(description):
    baseHTML = "<html><head><style>{}</style></head><body>{}</body></html>"
    html = baseHTML.format(style_content, description)
    return html


def simplify_linkedin_url(url):
    return url.split('?')[0]


def get_people_url_from_company_url(company_url):
    base_url, _ = company_url.split('/life')
    new_url = base_url + '/people/?keywords=Recruiter'
    return new_url


class MainApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    isBrowserOpen = False
    driver = None
    worker = None
    timer = None
    jobs = []
    recruiters = []
    config: Configuration
    gmail: Gmail

    def __init__(self, config: Configuration, gmail: Gmail):
        super().__init__()
        self.config = config
        self.gmail = gmail
        self.setupUi(self)  # Apply the UI setup to this instance
        self.openButton.setText("Open Browser")  # Change the button text
        self.openButton.setToolTip("Click to open the browser")  # Add a tooltip to the button
        # self.timer = QtCore.QTimer(self)
        self.openButton.clicked.connect(self.onOpenButtonClicked)  # Connect the button to the function
        self.openButton.setEnabled(True)

        self.captureJobs.clicked.connect(self.jobChosen)
        self.getRecruiterEmail.clicked.connect(self.getRecruiterEmailClicked)
        self.listWidget.itemSelectionChanged.connect(self.selection_changed)
        self.copyButton.clicked.connect(self.onCopyButtonClicked)
        # self.textEdit.textChanged.connect(self.onTextChange)

    def onOpenButtonClicked(self, event):
        if not self.isBrowserOpen:
            self.isBrowserOpen = True
            self.driver = open_page()
            # self.worker = Worker(self.driver)
            # self.worker.buttonClicked.connect(self.jobChosen)
            self.openButton.setText("Close Browser")
            # self.worker.start()
            # self.timer.start()
        else:
            if self.driver:
                self.driver.quit()
            self.isBrowserOpen = False
            # self.timer.stop()
            self.openButton.setText("Open Browser")

    def jobChosen(self):
        jobsJson = self.fetch_jobs()

        jobs = json.loads(jobsJson)
        jobs_ids = ['3815613878', '3819426741', '3834897208', '3814486924']

        total_jobs = len(jobs_ids)

        if total_jobs == 0:
            self.jobSearchLabel.setText("No jobs found.")
            return

        # for job_id in jobs['job_ids']:
        for index, job_id in enumerate(jobs_ids):
            self.jobSearchLabel.setText(f"Fetching job {index + 1} of {total_jobs}...")
            self.jobSearchProgress.setValue((index + 1) * 100 / total_jobs)
            QApplication.processEvents()
            self.driver.get(f"https://www.linkedin.com/jobs/view/{job_id}/")

            if index == total_jobs - 1:
                self.jobSearchLabel.setText("Jobs fetched!")
                self.jobSearchProgress.setValue(100)
                QApplication.processEvents()
                time.sleep(random.uniform(0.5, 1.0))  # Random sleep time to avoid bot detection
            else:
                time.sleep(random.uniform(1.15, 7.35))  # Random sleep time to avoid bot detection

            self.driver.execute_script(f"document.querySelector('button.jobs-description__footer-button').click()")

            company_element = self.driver.find_element(By.CSS_SELECTOR,
                                                       "div.job-details-jobs-unified-top-card__primary-description-container")
            company_name = company_element.find_element(By.TAG_NAME, "a").text
            company_url = company_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            job_title = self.driver.find_element(By.CSS_SELECTOR,
                                                 "h1.job-details-jobs-unified-top-card__job-title").text
            company_element_text = company_element.text

            location = clean_location_string(self.driver.execute_script(
                f"return Array.from(document.querySelector('div.job-details-jobs-unified-top-card__primary-description-container').childNodes).filter(node => node.nodeType === Node.TEXT_NODE).map(node => node.textContent.trim()).join(' ')"))
            description = self.driver.execute_script(
                f"return document.querySelector('div.jobs-box__html-content').innerHTML")

            job = Job(job_id, job_title, company_name, company_url, location, description, None)
            self.add_job_to_list(job)
            QApplication.processEvents()

    def getRecruiterEmailClicked(self):
        selected_job = self.get_selected_job()
        if not selected_job:
            return

        recruiter_url = self.fetch_recruiter_url()

        if not recruiter_url:
            self.recruiterStatus.setText("Please select a recruiter.")
            return

        response = get_contact_info(simplify_linkedin_url(recruiter_url))

        if response == "Error: 404":
            self.recruiterStatus.setText("Recruiter Status: Not found. Please try another recruiter.")
            return

        linkedin_contact = response_to_linkedin_contact(response)

        position = ""

        if linkedin_contact.company.position:
            position = linkedin_contact.company.position

        recruiter = Recruiter(recruiter_url, linkedin_contact.first_name + " " + linkedin_contact.last_name,
                              linkedin_contact.email, position, linkedin_contact.company.name, linkedin_contact)

        if linkedin_contact.email is None:
            self.recruiterStatus.setText("Recruiter Status: No email found. Please try another recruiter.")
            return

        selected_job.recruiter = recruiter
        self.recruiterStatus.setText("Recruiter Status: Email found!")
        self.recruiters.append(recruiter)
        self.setup_recruiter_ui(selected_job.recruiter)

    def selection_changed(self):
        selected_job = self.get_selected_job()
        if not selected_job:
            return

        self.companyName.setText(selected_job.company_name)
        self.jobTitle.setText(selected_job.title)
        self.companyLocation.setText(selected_job.location)
        self.companyURL.setText("<a href='" + selected_job.company_url + "'>" + selected_job.company_url + "</a>")
        self.jobDescription.setHtml(process_job_description(selected_job.description))
        self.driver.get(get_people_url_from_company_url(selected_job.company_url))
        self.inject_people_content()

        if selected_job.recruiter:
            self.setup_recruiter_ui(selected_job.recruiter)

    def inject_people_content(self):
        self.driver.execute_script(recruiter_select)
        self.driver.execute_script(
            'document.head.appendChild(document.createElement("style")).innerHTML = `{}`'.format(style_content))

    def onCopyButtonClicked(self):
        clipboard = QtWidgets.QApplication.clipboard()
        content_to_copy = self.recruiterStatus.text()
        clipboard.setText(content_to_copy)
        self.statusbar.showMessage("Copied email to clipboard!", 3000)

    def fetch_jobs(self):
        return self.driver.execute_script("return document.getElementById('jca-job_ids').value;")

    def fetch_recruiter_url(self):
        return self.driver.execute_script("return document.getElementById('jca-recruiter_profile_url').value;")

    def get_email_from_url(self):
        pass

    def add_job_to_list(self, job):
        item = QtWidgets.QListWidgetItem()
        item.setText(job.title + " at " + job.company_name + " in " + job.location)
        self.listWidget.addItem(item)
        self.jobs.append(job)

    def get_selected_job(self):
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            # Get the first selected item (if multiple selection is not enabled)
            selected_item = selected_items[0]

            # Find the index of the selected item
            index = self.listWidget.row(selected_item)

            if selected_item:
                return self.jobs[index]

        return None

    def setup_recruiter_ui(self, recruiter: Recruiter):
        self.recruiterName.setText(recruiter.name)
        if recruiter.email:
            self.recruiterEmail.setText(recruiter.email)
        else:
            self.recruiterEmail.setText("No email found.")

        self.recruiterTitle.setText(recruiter.title)
        self.recruiterCompany.setText(recruiter.company_name)
        self.recruiterURL.setText("<a href='" + recruiter.url + "'>" + recruiter.url + "</a>")
