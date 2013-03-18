#! python

import unittest, time, re
from survey_script import SurveyScript

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

class AddUser(SurveyScript):
    def setUp(self):
        # Get user input
        self.new_user = raw_input("netid of new user: ")
        
        self.new_user_type = ""
        while (self.new_user_type not in text_field_ids):
            self.new_user_type = raw_input("user type (editor, admin, or viewer): ")
        
        super(AddUser, self).setUp()
    
    def test_add_user(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

        # Go to reports tab
        driver.find_element_by_id("survey-setup").click()

        num_elements = len(driver.find_elements_by_css_selector("td.t-col-role"))
        for i in xrange(0, num_elements):
            # select roles for the next survey
            try:
                driver.find_elements_by_css_selector("td.t-col-role")[i].click()
            except:
                # hit the toggle to show the folder contents
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

if __name__ == "__main__":
    unittest.main()
