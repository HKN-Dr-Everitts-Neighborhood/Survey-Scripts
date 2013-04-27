#! python

import csv, sys, json

class Question:
    def __init__(self, question, type, answers, rank, required=False):
        '''constructor for Question object
        
        question: the question, as a string
        type: the type of question, e.g. Checkbox, Radio, Long Answer, or Short Answer
        answers: list of possible answers.  Note "Other" is treated specially.
        rank: used to sort the questions
        required: whether or not the question is required.  Default is not required.
        '''
	
	assert type in ['Long Answer', 'Short Answer', 'Radio', 'Checkbox'] , "Question type %s is not supported" % type
	assert isinstance(required, bool), "Required must be a boolean, but %s is not a boolean" % required
	assert isinstance(question, basestring), "question must be a string, but %s is not a string" % question 
	assert isinstance(answers, list), "answers must be a list of strings; %s is not a list" % answers
	for a in answers:
		assert isinstance(a, basestring), "answers must be a list of strings; %s is not a string" % a
	assert isinstance(rank, int), "rank must be an integer, not %s" % rank
	
        self.required = required
        self.question = question
        self.type = type
        self.answers = answers
        self.rank = rank

class Survey:
    def __init__(self, name, submit_once):
        self.name = name
        self.questions = []
        self.submit_once = submit_once
        
    def add_question(self, q):
        self.questions.append(q)

def parse_args():
    '''reads command line parameters and returns (roster_filename, template_filename, restart_at)
    
    If the command line parameters don't match the intended usage, this should throw an exception.
    '''
    
    if len(sys.argv) == 5 and sys.argv[3] == '-restart':
        restart_at = int(sys.argv[4])
    else:
        assert len(sys.argv) == 3, "Usage: %s <survey_roster> <survey_template> [-restart <number>]" % sys.argv[0]
        restart_at = 0
    
    return (sys.argv[1], sys.argv[2], restart_at)

def make_surveys(roster_filename, template_filename, restart_at):
    '''open up the files and generate surveys from them'''
    
    with open(roster_filename, 'r') as survey_roster:
        roster_csv = [line for line in csv.reader(survey_roster)]
    
    with open(template_filename, 'r') as template_file:
        template_csv = [line for line in csv.reader(template_file)]
    
    roster_header = roster_csv[0]
    roster_rows = roster_csv[1:][restart_at:] # ignore all rows before restart_at
    
    return [ instantiate_template(template_csv, zip(roster_header, roster_line))
                for roster_line in roster_rows ]

def yesno_to_bool(input, error_in):
    '''Takes in input, returns True for yes, False for no.  If input is neither of these things,
    an error will be raised, with error_in as part of the error message.'''
    if input == 'yes':
        return True
    elif input == 'no':
        return False
    else:
        assert False, "Value '%s' for %s should be yes or no" % (repr(input), error_in)    

ignore_cols = set()

def instantiate_template(template_csv, survey_info):
    '''Does all the actual interpretation of the csv data.  Returns a Survey.'''
    
    # first line of each file is a header that tells us how to interpret it.
    template_header = template_csv[0]
    template_rows = template_csv[1:]
    
    # read the row from the survey roster that describes this survey
    custom_answers = {}
    custom_questions = []
    name, submit_once = None, None
    for (col, datum) in survey_info:
        if col == "Name":
            name = datum
        elif col == "single submission":
            submit_once = yesno_to_bool(datum, 'single submission')
        elif col == "Custom":
            # custom question; multiple of these are allowed.
            if datum: # ignore empty strings
                try:
                    custom_questions.append(Question(**json.loads(datum)))
                except Exception as e:
                    print 'Error loading custom question %s' % datum
                    raise
        elif col.endswith(": answers"):
            # custom answers
            custom_answers[col.partition(':')[0]] = datum
        else:
            if col not in ignore_cols:
                print "ignoring column '%s' in survey roster" % col
                ignore_cols.add(col)
    
    assert name is not None and submit_once is not None, "Missing Name or single submission column"
    
    survey = Survey(name, submit_once)
    
    # verify template validity
    # Going for a very strict format for easier parsing.  Columns must be in specified order.
    assert len(template_header) == 6, "Missing column in template!"
    for colhead, shouldbe in zip(template_header, ['Id', 'Question', 'Type', 'Required', 'Answers', 'Rank']):
        assert colhead == shouldbe, "Invalid column in template: %s" % colhead
    
    for line in template_rows:
        id = line[0]
        question = line[1]
        type = line[2]
        required = yesno_to_bool(line[3], 'required')
        
        # deal with custom answers per survey.
        # note we check one of the two error cases - where the survey roster is missing the column for
        # custom answers; the other case, where the survey roster has extra columns, is unlikely to happen;
        # if it does, it will most likely be a mislabeled column.
        raw_answers = custom_answers.get(id) if (line[4] == '#CUSTOM#') else line[4]
        assert raw_answers is not None, "Survey roster is missing the column for custom answers for question %s" % id
        
        answers = map(lambda x: x.strip(), raw_answers.split(',')) # strip removes excess whitespace
        rank = int(line[5])
        
        survey.add_question(Question(question, type, answers, rank, required))
    
    # add in custom questions
    map(survey.add_question, custom_questions)
    
    return survey

if __name__ == '__main__':
    make_surveys(*parse_args())
