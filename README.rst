============
TP-DeepSeach
============


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
        $ pip install -r misc/requirements.txt

More information about virtualenv can be found on documentation_. 

.. _documentation: https://virtualenv.pypa.io/en/stable/

Prepare MySQL database
::

NOTE: We expect you to have installed default MySQL server on your device.
If not, check basic way of apt-get install mysql server and MySQL documentation_.

.. _documentation: https://dev.mysql.com/doc/

Enter your MySQL server
::
        $ mysql -u root -p

and enter your password (default_notsafe: root, default_safe - at least 8 chars)

Create database and testing database
::
        $ create database tp;


        $ create database test;

Run table creating scripts of mysql_init_tables for creation of all tables or 
create them manually.

Fill data with db_filler script.

Usage
::

        $ python db_filler.py 'issue_name' 'absolute_path_to_xml' 'absolute_path_to_header_conf_file'
(leave ')

This script returns id of newly created entry in issues

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
