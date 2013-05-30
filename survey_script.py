#! python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import unittest, time, re
from secrets import netid, password

class SurveyScript(unittest.TestCase):
    
    def setUp(self, images=False):
        
        firefox_prof = webdriver.FirefoxProfile()
        #firefox_prof.add_extension('httpfox-0.8.10.xpi')
        
        if not images:
            firefox_prof.set_preference('permissions.default.image', 2)
        
        self.driver = webdriver.Firefox(firefox_profile=firefox_prof)
        
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
        
        # pause while page loads.
        # for whatever reason, our implicity_wait isn't good enough
        # for clicks on survey-setup / survey-report that usually come
        # right after authenticating - my guess is that these links are
        # displayed but don't have the proper click handlers right away.
        time.sleep(4)
    
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
