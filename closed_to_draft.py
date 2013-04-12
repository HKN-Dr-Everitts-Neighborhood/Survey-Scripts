#! python

from selenium import webdriver
import unittest, time, re
from survey_script import SurveyScript

class DraftSurveys(SurveyScript):
    
    def test_draft_surveys(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

        # Go to setup tab
        driver.find_element_by_id("survey-setup").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-edit-form > a"))
        
        # so it turns out that only open & closed surveys have the t-col-edit-form class; hence why we are using
        # element 0 at each iteration.  This might cause trouble if we have some open surveys.
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

if __name__ == "__main__":
    unittest.main()
