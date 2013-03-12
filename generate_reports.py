from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from secrets import netid, password

import unittest, time, re

class GenerateReports(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://illinois.edu/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_generate_reports(self):
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
        driver.find_element_by_id("survey-report").click()


        num_elements = len(driver.find_elements_by_link_text("create new report"))
        for i in xrange(0, num_elements):
            # generate spreadsheet
            driver.find_elements_by_link_text("create new report")[i].click()
            Select(driver.find_element_by_name("REPORT_TYPE")).select_by_visible_text("CSV - Full Spreadsheet")
            driver.find_element_by_xpath("//a[@onclick=\"checkAll('single_result_')\"]").click()
            driver.find_element_by_css_selector("input[type=\"button\"]").click()

            # generate html report
            driver.find_elements_by_link_text("create new report")[i].click()
            Select(driver.find_element_by_name("REPORT_TYPE")).select_by_visible_text("HTML - Summary")
            driver.find_element_by_css_selector("input[type=\"button\"]").click()
    
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
