Survey-Scripts
==============

A repo for all the scripts we have to help out with surveys.

Scripts
=======

* generate_reports.py: makes 2 reports per survey - an html summary report, and a csv full report (single response checked).
* download_reports.py: downloads all reports that have been generated.  Note the global variable which specifies the folder to download to.
*delete_reports.py: deletes all reports that have been generated.  Meant to clean up the "My Reports" tab.

* add_user.py: goes through all surveys and shares them with a specified user giving them the specified privileges.
* survey_stats.py: a simple script that counts the number of responses in a set of data downloaded by download_reports.
* closed_to_draft.py: goes through all closed surveys and flips them into the draft phase.  ISSUE: if you have surveys that are open, it will try to move them to draft phase and fail.
* draft_to_open.py: goes through all surveys and opens them for responses.
* open_to_closed.py: goes through all surveys and closes the open ones (stop allowing responses).

* survey_stats.py: meant to help count the number of responses gathered from downloaded reports.

Dependencies
============

These scripts depend on selenium, requests, and beautifulsoup.  See setup_notes.txt for info on how to install these python packages.

Note also that you'll need to write your own secrets.py to get this to work.  secrets requires two variables: netid and password - i.e. your bluestem login credentials.
