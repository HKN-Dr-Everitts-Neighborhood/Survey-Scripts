Survey-Scripts
==============

A repo for all the scripts we have to help out with surveys.

Scripts
=======

Managing Reports:

* generate_reports.py: makes 2 reports per survey - an html summary report, and a csv full report (single response checked).  If this fails, run delete_reports.py to clean up and run it again, otherwise you'll generate/download duplicate reports.
* download_reports.py: downloads all reports that have been generated.  Note the global variable which specifies the folder to download to.
* delete_reports.py: deletes all reports that have been generated.  Meant to clean up the "My Reports" tab.

Managing existing surveys:

* add_user.py: goes through all surveys and shares them with a specified user giving them the specified privileges.
* closed_to_draft.py: goes through all closed surveys and flips them into the draft phase.  ISSUE: if you have surveys that are open, it will try to move them to draft phase and fail.
* draft_to_open.py: goes through all surveys and opens them for responses.
* open_to_closed.py: goes through all surveys and closes the open ones (stop allowing responses).

Creating more surveys:

* survey.py: a component meant for use with the new_surveys script.  Run alone, though, and it will read & validate the survey roster and survey template.  Note: this script works standalone (no need to install other packages).
* new_surveys.py: a script that examines a roster file and a template file and goes and creates surveys according to all this information.  More information below.  The script will tell you it's usage if run with the wrong number of arguments.

Data Processing:

* survey_stats.py: a simple script that counts the number of responses in a set of data downloaded by download_reports.

Dependencies
============

These scripts depend on selenium, requests, and beautifulsoup.  See setup_notes.txt for info on how to install these python packages.

Note also that you'll need to write your own secrets.py to get this to work.  secrets requires two variables: netid and password - i.e. your bluestem login credentials.

Design Philosophy
===============

While building a level on top of toolbox, because of the quirkiness in using toolbox via Selenium, it has been important to take into account how these scripts handle faults.  I decided to try to keep our abstractions on top of toolbox simple for this reason, since these scripts depend on the state of the surveys.  Most of the scripts were written to be idempotent - if they fail in the middle, you can just rerun them and they'll either skip or redo the work they've already done, with no problems caused - if the end successfully, the surveys will be in a valid state.

This philosophy has interesting consequences - e.g. generating & downloading the reports are separate steps to avoid trouble - if this was done in one step, the queue of reports to generate could get in the way at random times.

The main exception to this philosophy is new_surveys.py.  Creating new surveys is inherently a non-idempotent task (and toolbox has the unfortunate bug that creating two surveys with the same name hides the first one).  When this script crashes, it'll spit out a stack trace and a message (above the stack trace) telling you how to restart it so it picks up where it leaves off - this involves deleting any half-created survey (it'll tell you which) and then restarting the script with the proper parameters so it'll restart at the right spot.

Survey Roster & Template file formats
==============================

The roster is a csv file.  The first line contains the column headers, in any order.  These headers describe the information found in their column.

* "Name" - the name of the survey.  REQUIRED.
* "single submission" - a yes/no field - yes if each person should only be able to submit the survey once.  REQUIRED.
* "Custom" - a field for custom questions.  This field may be duplicated; any empty cells under such a column will be ignored.  This field should contain a valid json object representing a single question; an example is given below.
* "<question id>: answers" - a field used to enable answers choices for a question in the template to change across surveys.  Same format as answers field for the template.  <question id> must be a valid question id from the template file.

The template file is also a csv file.  The format for template files is much more strict (I got lazy).  The fields must be, in this order:

* "Id" - a unique identifier per question, used for custom answers; when custom answers are in use, this id is referenced by the roster file.
* "Question" - the text of the question that will be displayed.
* "Type" - valid entries are "Radio", "Long Answer", "Short Answer", and "Checkbox".  Radio = here's a bunch of choices, choose one; checkbox = here's a bunch of choices, choose as many as you want.
* "Required" - whether the question is required.  Valid entires: "yes" and "no"
* "Answers" - a comma separated list.  Note if 'other' or 'Other' is an option, it will be automatically treated specially.  Having multiple 'other's as options probably won't do what you expect; only the 'o' may be capitalized.  The other special case is if the field has value "#CUSTOM#"; then the answers will be fetched from the roster file.  This field is only used for Radio and Checkbox questions.
* "Rank" - an integer that tells the script how to order the questions - questions will be presented in order of increasing rank.  Ties will be arbitrarily broken.  The point of this is to allow custom questions to be inserted at arbitrary places without too much work.  So questions that should always be at the beginning have low ranks, questions that should always be at the end should have high ranks, and then custom questions can have intermediate ranks.


*Custom Questions*

Here is an example.  All fields but "required" are required; "required" defaults to False (no).  Note that answers is a proper json list, instead of a comma separated list.  In fact, the whole format is JSON - so order of the fields doesn't matter, but be sure to use doublequotes, colons, and commas properly.  No Id is needed for custom questions.

````
{"question": "Are you enrolled in or planning to take the lab, ECE 415 / BIOE 415?", "answers": ["currently enrolled", "planning to take it in the future", "not planning to take it in the future"], "type": "radio", "rank": 10, "required": true}
````
