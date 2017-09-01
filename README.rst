=============
TP-DeepSearch
=============


Installation
============

Virtualenv
""""""""""

Virtualenv preparation
::
        $ virtualenv ENV

To activate newly created virtualenv, you can run
::
        $ source ENV/bin/activate

Install all requirements
::
        $ pip3 install -r misc/requirements.txt

Install Python3 external dependency
::
        $ sudo apt-get install python3-tk

Install key words processing dependency
::
        $ pip3 install -m textblob.download_corpora

More information about virtualenv can be found on documentation_. 

.. _documentation: https://virtualenv.pypa.io/en/stable/

REQUISITES
""""""""""
* Database initialization
  * execute script from python project TP-DeepSearch, with name helper/reset_elastic_indices.py (You need to check documentation for proper understanding)

Basic orientation
=================

There are 4 folders:

- tests
- parser
- misc
- other

There is no main directory for all functionality of the project, but there may be several directoreis such as 'parser' where are scripts inserted in the hierarchy defined by methodology.

Tests is the main directory for tests.

Misc is used as the main directory for installation and setup scripts, files and so on.

Other is the main directory for code that is hardly descripable, used as help in some
user stories, tasks or some other way.


Path Validation
===============
Firstly, you need to download content of folder path_validator located in folder /helper in this repository. This folder path_validator should contain these files:
::
    issue_xml_schema.xsd
    MARC21_journal_schema.xsd
    Path Validator.bat
    path_validator.py

Secondly, download Python installer from this link:
::
    https://drive.google.com/file/d/0Bwbz4DMi5b1vdUtjX0RsYmZ4dU0/view?usp=sharing

All these files (including Python installer) must be placed in the same folder, for example:
::
    C:\Documents\Work

Make sure that you have in the same directory all needed files:
::
    issue_xml_schema.xsd
    MARC21_journal_schema.xsd
    Path Validator.bat
    path_validator.py
    python-3.6.2.exe

To run path validation, double click on Path Validator.bat, wait few minutes for python installation (if it is needed) and then, when prompted, enter the path to validate, and if desired also enter limiting path up to which will be searched for marc_journal, or leave blank if marc_journal is expected only in the validating path and its subpaths. Paths should be entered in the form of absolute path for example:
::
    C:\Documents\Work\Journals\Slovak

Path can also be entered in the form of relative path, for example if you placed these path_validator files in
::
    C:\Documents\Work

then enter path for files starting from this directory, for example to validate the same files like in example before, enter path:
::
    Journals\Slovak

After validation, press any key to start validation again with new parameters. To stop or end validation, click red X in the corner of the output console