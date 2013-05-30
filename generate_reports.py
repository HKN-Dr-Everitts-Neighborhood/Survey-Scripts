#! python

from selenium.webdriver.support.ui import Select
import unittest, time, re
from datetime import datetime

from survey_script import SurveyScript

class GenerateReports(SurveyScript):
    
    def setUp(self):
        
        time_string = raw_input("Generate reports for datetime after (format: month/day/fullyear hour:minutes am/pm): ")
        self.cutoff = datetime.strptime(time_string, "%m/%d/%Y %I:%M %p")
        
        super(GenerateReports, self).setUp(images=True)
    
    def test_generate_reports(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

        # Go to reports tab
        driver.find_element_by_id("survey-report").click()

        while (True):
            num_elements = len(driver.find_elements_by_link_text("create new report"))
            
            for i in xrange(0, num_elements):
                # grab close date and time.  Looking at the generated html, these columns (and only these columns) use the t-col-two class.
                date = driver.find_elements_by_css_selector("td.t-col-two")[2*i].text
                time_ = driver.find_elements_by_css_selector("td.t-col-two")[2*i+1].text
                end_time = datetime.strptime(date + " " + time_, "%m/%d/%Y %I:%M %p") # output is a datetime, not a string
                
                print repr(end_time), repr(self.cutoff)

                if (end_time > self.cutoff):
                    # generate spreadsheet
                    # but make sure page is done loading first.
                    time.sleep(1)
                    driver.find_elements_by_link_text("create new report")[i].click()
                    Select(driver.find_element_by_name("REPORT_TYPE")).select_by_visible_text("CSV - Full Spreadsheet")
                    driver.find_element_by_xpath("//a[@onclick=\"checkAll('single_result_')\"]").click()
                    driver.find_element_by_css_selector("input[type=\"button\"]").click()

                    # generate html report, but make sure page loads first.
                    time.sleep(1)
                    driver.find_elements_by_link_text("create new report")[i].click()
                    Select(driver.find_element_by_name("REPORT_TYPE")).select_by_visible_text("HTML - Summary")
                    driver.find_element_by_css_selector("input[type=\"button\"]").click()

            time.sleep(1)

            # This is the reason that images are enabled; otherwise, the
            # next/prev page links wouldn't be visible and they can't be
            # selected by the driver.
            pagination_imgs = driver.find_elements_by_css_selector("div.next-prev-buttons a img")
            for image in pagination_imgs:
                if (image.get_attribute('src').endswith('/pgnext.png')):
                    image.click()
                    break
            else: #if the loop never breaks
                return

if __name__ == "__main__":
    unittest.main()
