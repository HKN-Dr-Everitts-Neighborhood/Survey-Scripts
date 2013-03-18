#! python

import unittest, time, re
import requests

from survey_script import SurveyScript

# the directory this script saves everything in.
survey_directory = "C:\\Users\\David\\Desktop\\Surveys\\"

class DownloadReports(SurveyScript):
    
    def test_download_reports(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
    
        # Authentication
        self.authenticate()
    
        # navigate to the reports page
        time.sleep(3)
        driver.find_element_by_id("survey-report").click()
        driver.find_element_by_link_text("My Reports").click()
        
        # find auth cookie
        cookie = driver.get_cookie("Bluestem_illinois.edu")
    
        # Extract links, survey names, and extensions
        links = driver.find_elements_by_link_text("download")
        names = driver.find_elements_by_css_selector("tbody > tr > th")
        exts = driver.find_elements_by_css_selector("td.t-col-one.t-col-download")
        
        # loop and save each as a file
        for (name, link, ext) in zip(names, links, exts):
            
            # construct filename.  This does rudimentary escaping - it isn't perfect, but at least takes care of slashes.
            filename = name.text
            filename = filename.replace("/", "_")
            filename = filename.replace("\\", "_")
            
            # fetch the data with the requests library.
            # the cookie is required to prove we have authenticated.
            # TODO: is this sending the cookie securely?  It may not be a problem since it should be using https anyway.
            response = requests.get(link.get_attribute("href"), cookies={cookie['name']: cookie['value']})
            
            with open(survey_directory + filename +"."+ ext.text, "w") as f:
                f.write(response.content)

if __name__ == "__main__":
    unittest.main()
