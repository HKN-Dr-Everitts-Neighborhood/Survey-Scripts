#! python

import unittest, time, re
from survey_script import SurveyScript

class CloseSurveys(SurveyScript):
    
    def test_close_surveys(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

        # Go to setup tab
        driver.find_element_by_id("survey-setup").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-edit-form > a"))
        
        # so it turns out that only closed survyes have the t-col-edit-form class; hence why we are using
        # element 0 at each iteration
        for i in xrange(0, num_elements):
            # click edit form
            try:
                driver.find_elements_by_css_selector("td.t-col-edit-form > a")[i].click()
            except:
                # hit the toggle to show the folder contents
                driver.find_element_by_id("folder_2").click()
                # retry
                driver.find_elements_by_css_selector("td.t-col-edit-form > a")[i].click()
            
            # click start survey
            end_button = driver.find_elements_by_css_selector("input[value=\"End Survey\"]")
            if (len(end_button) == 1):
                end_button[0].click()
                self.assertEqual(
                    "This will END the survey now. To EDIT the survey, click Edit survey.",
                    self.close_alert_and_get_its_text()
                )
            
            # Go back to the setup page
            driver.find_element_by_css_selector("input[value=\"Back\"]").click()

if __name__ == "__main__":
    unittest.main()
