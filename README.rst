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
