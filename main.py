from selenium import webdriver
import os

chrome_options = webdriver.Chrome("G:\My Drive\Programing\Personal scripts\Web\python selunium web bot\chromedriver.exe")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

input()