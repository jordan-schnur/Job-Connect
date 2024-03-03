from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import sys
from PyQt5 import QtWidgets
from openai import OpenAI

from Config import Configuration
from Gmail import Gmail
from mainappwindow import MainApplicationWindow
from ui import Ui_MainWindow

if __name__ == '__main__':
    config = Configuration()
    gmail = Gmail()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainApplicationWindow(config, gmail)
    mainWin.show()
    sys.exit(app.exec_())

    # client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
    #
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system",
    #          "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    #         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    #     ]
    # )
    #
    # print(completion.choices[0].message)
