#! python

import unittest, time, re
from survey_script import SurveyScript

class DeleteReports(SurveyScript):
    
    def test_delete_reports(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

        # Go to reports tab
        driver.find_element_by_id("survey-report").click()
        driver.find_element_by_link_text("My Reports").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-delete"))
        for i in xrange(0, num_elements):
            driver.find_element_by_css_selector("td.t-col-delete").click()
            self.assertEqual(
                "Confirm delete?",
                self.close_alert_and_get_its_text()
            )
        
if __name__ == "__main__":
    unittest.main()
