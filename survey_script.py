#! python

from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import unittest, time, re
from secrets import netid, password

class SurveyScript(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(6)
        self.base_url = "https://illinois.edu/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def authenticate(self):
        driver = self.driver
        driver.find_element_by_id("UserID").clear()
        driver.find_element_by_id("UserID").send_keys(netid)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_id("Password").clear()
        driver.find_element_by_id("Password").send_keys(password)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)