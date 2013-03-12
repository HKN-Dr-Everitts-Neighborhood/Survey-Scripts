from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import requests

from secrets import netid, password

# the directory this script saves everything in.
survey_directory = "C:\\Users\\David\\Desktop\\Surveys\\"

class DownloadReports(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(30)
		self.base_url = "https://illinois.edu/"
		self.verificationErrors = []
		self.accept_next_alert = True
	
	def test_download_reports(self):
		driver = self.driver
		driver.get(self.base_url + "toolbox")
	
		# Authentication
		driver.find_element_by_id("UserID").clear()
		driver.find_element_by_id("UserID").send_keys(netid)
		driver.find_element_by_css_selector("input[type=\"submit\"]").click()
		driver.find_element_by_id("Password").clear()
		driver.find_element_by_id("Password").send_keys(password)
		driver.find_element_by_css_selector("input[type=\"submit\"]").click()
	
		# navigate to the reports page
		time.sleep(3)
		driver.find_element_by_id("survey-report").click()
		driver.find_element_by_link_text("My Reports").click()
		
		# find auth cookie
		cookie = driver.get_cookie("Bluestem_illinois.edu")
	
		# Extract links, survey names, and extensions
		links = driver.find_elements_by_link_text("download")
		names = driver.find_elements_by_css_selector("tbody > tr > th")
		exts = driver.find_elements_by_css_selector("td.t-col-one.t-col-download")
		
		# loop and save each as a file
		for (name, link, ext) in zip(names, links, exts):
			
			# construct filename.  This does rudimentary escaping - it isn't perfect, but at least takes care of slashes.
			filename = name.text
			filename = filename.replace("/", "_")
			filename = filename.replace("\\", "_")
			
			# fetch the data with the requests library.
			# the cookie is required to prove we have authenticated.
			# TODO: is this sending the cookie securely?  It may not be a problem since it should be using https anyway.
			response = requests.get(link.get_attribute("href"), cookies={cookie['name']: cookie['value']})
			
			with open(survey_directory + filename +"."+ ext.text, "w") as f:
				f.write(response.content)
	
	def is_element_present(self, how, what):
		try: self.driver.find_element(by=how, value=what)
		except NoSuchElementException, e: return False
		return True
	
	def close_alert_and_get_its_text(self):
		try:
			alert = self.driver.switch_to_alert()
			if self.accept_next_alert:
				alert.accept()
			else:
				alert.dismiss()
			return alert.text
		finally: self.accept_next_alert = True
	
	def tearDown(self):
		self.driver.quit()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	unittest.main()
