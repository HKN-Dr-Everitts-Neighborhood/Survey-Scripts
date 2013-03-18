#! python

import unittest, time, re
from survey_script import SurveyScript

class OpenSurveys(SurveyScript):
    
    def test_open_surveys(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

        # Go to setup tab
        driver.find_element_by_id("survey-setup").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-edit > a"))
        
        # so it turns out that only closed survyes have the t-col-edit-form class; hence why we are using
        # element 0 at each iteration
        for i in xrange(0, num_elements):
            # click edit form
            try:
                driver.find_element_by_css_selector("td.t-col-edit > a").click()
            except:
                # hit the toggle to show the folder contents
                driver.find_element_by_id("folder_2").click()
                # retry
                driver.find_element_by_css_selector("td.t-col-edit > a").click()
            
            # click start survey
            driver.find_element_by_css_selector("input[value=\"Start Survey\"]").click()
            self.assertEqual(
                "No further changes will be allowed to your questions, Survey will begin on the start date.",
                self.close_alert_and_get_its_text()
            )
            
            # Go back to the setup page
            driver.find_element_by_css_selector("input[value=\"Back\"]").click()

if __name__ == "__main__":
    unittest.main()
