#! python

from selenium.webdriver.support.ui import Select
import unittest, time, re
from survey_script import SurveyScript

class GenerateReports(SurveyScript):
    
    def test_generate_reports(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

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

if __name__ == "__main__":
    unittest.main()
