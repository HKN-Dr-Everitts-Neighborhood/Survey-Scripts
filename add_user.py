#! python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from secrets import netid, password

import unittest, time, re

text_field_ids = {
    "viewer": "viewer_add",
    "editor": "editor",
    "admin": "admin_add"
}

button_ids = {
    "viewer": "results_view_add",
    "editor": "editor_add",
    "admin": "admin_add_user"
}

class AddUser(unittest.TestCase):
    def setUp(self):
        # Get user input
        self.new_user = raw_input("netid of new user: ")
        
        self.new_user_type = ""
        while (self.new_user_type not in text_field_ids):
            self.new_user_type = raw_input("user type (editor, admin, or viewer): ")
        
        # Now open Firefox
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://illinois.edu/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_add_user(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        driver.find_element_by_id("UserID").clear()
        driver.find_element_by_id("UserID").send_keys(netid)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_id("Password").clear()
        driver.find_element_by_id("Password").send_keys(password)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        # Go to reports tab
        driver.find_element_by_id("survey-setup").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-role"))
        for i in xrange(0, num_elements):
            # select roles for the next survey
            try:
                driver.find_elements_by_css_selector("td.t-col-role")[i].click()
            except:
                # hit the toggle
                driver.find_element_by_id("folder_2").click()
                # retry
                driver.find_elements_by_css_selector("td.t-col-role")[i].click()
            
            # select correct box and type in netid
            netid_input = driver.find_element_by_id(text_field_ids[self.new_user_type])
            netid_input.clear()
            netid_input.send_keys(self.new_user)
            
            # submit the netid
            driver.find_element_by_id(button_ids[self.new_user_type]).click()
        
            # Go back to the setup page
            driver.find_element_by_css_selector("#back > input").click()
    
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
