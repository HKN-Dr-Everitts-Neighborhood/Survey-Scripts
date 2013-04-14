#! python

from survey_script import SurveyScript

import survey

class NewSurveys(SurveyScript):
    def __init__(self):
        
	self.surveys = survey.make_surveys()
	
        super(NewSurveys, self).setUp()
    
    def make_new_surveys(self):
        driver = self.driver
        driver.get(self.base_url + "toolbox")
        
        # Authenticate
        self.authenticate()

	for i, survey in enumerate(self.surveys):
		try:
			# Go to survey setup tab and click create
			driver.find_element_by_id("survey-setup").click()
			driver.find_element_by_link_text("Create").click()
			
			# Enter a name for the survey
			survey_name = driver.find_element_by_id("name")
			survey_name.clear()
			survey_name.send_keys(survey.name)
			
			# Save it
			driver.find_element_by_css_selector("input[value=\"Save\"]").click()
			
			if (survey.submit_once):
				# go to security tab
				driver.find_element_by_link_text("Security").click()
				driver.find_element_by_css_selector("div.pc-form-row > div.general-action-list a.opt-not-selected").click()
			
			driver.find_element_by_link_text("Questions").click()
			
			# Now add questions
			for j, question in enumerate(sorted(survey.questions, key=lambda q : q.rank)):
				if (j == 0):
					driver.find_element_by_link_text("insert new question").click()
				else:
					# use the last add question button, so our new question goes last
					driver.find_elements_by_link_text("add question")[-1].click()
				
				q_field = driver.find_element_by_css_selector("#question")
				q_field.clear()
				q_field.send_keys(question.question)
				
				if (question.required):
					driver.find_element_by_css_selector("#response_yes").click()
				
				if (question.type == "Short Answer"):
					# short answer is default
					pass
				elif (question.type == "Long Answer"):
					driver.find_element_by_link_text("Long Answer").click()
				elif (question.type == "Radio" or question.type == "Checkbox"):
					
					driver.find_element_by_link_text(question.type).click()
					
					# handle other
					if "Other" in question.answers or "other" in question.answers:
						driver.find_element_by_link_text("yes").click()
						
					answers = filter(lambda x: x != 'Other' and x != 'other', question.answers)
					
					answer_box = driver.find_element_by_css_selector("#addAnswers")
					answer_box.clear()
					answer_box.send_keys('\n'.join(answers))
				
				driver.find_element_by_css_selector("input[value=\"Save\"]").click()
				driver.find_element_by_css_selector("input[value=\"Back\"]").click()
			
			driver.find_element_by_css_selector("input[value=\"Save\"]").click()
			driver.find_element_by_css_selector("input[value=\"Back\"]").click()
				
		except Exception:
			print "Warning: exception encountered while generating survey %s.  Delete the survey and restart on survey #%s." % (survey.name, i)
			raise

if __name__ == "__main__":
    NewSurveys().make_new_surveys()
