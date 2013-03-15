#! python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from secrets import netid, password

import unittest, time, re

class DraftSurveys(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://illinois.edu/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_draft_surveys(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        driver.find_element_by_id("UserID").clear()
        driver.find_element_by_id("UserID").send_keys(netid)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_id("Password").clear()
        driver.find_element_by_id("Password").send_keys(password)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        # Go to setup tab
        driver.find_element_by_id("survey-setup").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-edit-form > a"))
        
        # so it turns out that only closed survyes have the t-col-edit-form class; hence why we are using
        # element 0 at each iteration
        for i in xrange(0, num_elements):
            # click edit form
            try:
                driver.find_elements_by_css_selector("td.t-col-edit-form > a")[0].click()
            except:
                # hit the toggle to show the folder contents
                driver.find_element_by_id("folder_2").click()
                # retry
                driver.find_elements_by_css_selector("td.t-col-edit-form > a")[0].click()
            
            # click edit survey
            driver.find_element_by_css_selector("input[value=\"Edit Survey\"]").click()
            
            # Go back to the setup page
            driver.find_element_by_css_selector("input[value=\"Back\"]").click()
    
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
