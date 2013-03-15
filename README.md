Survey-Scripts
==============

A repo for all the scripts we have to help out with surveys.

Scripts
=======

* generate_reports.py: makes 2 reports per survey - an html summary report, and a csv full report (single response checked).
* download_reports.py: downloads all reports that have been generated.  Note the global variable which specifies the folder to download to.
* add_user.py: goes through all surveys and shares them with a specified user giving them the specified privileges.

Dependencies
============

These scripts depend on selenium, requests, and beautifulsoup.  See setup_notes.txt for info on how to install these python packages.

Note also that you'll need to write your own secrets.py to get this to work.  secrets requires two variables: netid and password - i.e. your bluestem login credentials.
