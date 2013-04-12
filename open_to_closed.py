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
        
        # closed and open surveys have the t-col-edit-form class.
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
	    
	    # check if we found the button; if not, this survey wasn't open (it was probably closed, since we are
	    # looking at all surveys with the t-col-edit-form class, which is both open and closed surveys).
	    # We should ignore it and move on; this makes this script more fault-tolerant.
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
