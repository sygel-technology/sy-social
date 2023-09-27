.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

======================
Message Connector Base
======================

This module provides the basic functions necessary to
#. Create messages.
#. Create automatic actions for sending messages. 
#. Keep a log of sent or failed messages.
#. General connector settings

This module is not to be used as is. Example implementation:

#. message_connector_slack


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To configure this module, you need to:

#. To use the connector activate the connector from Setting -> Active Message Connector

#.	To delete old log messages set the message log deletion frequency higher than zero.


Usage
=====

To use this module, you need to:

#. Go to ...


ROADMAP
=======

Possible improvements:

#. Filtering of fields to write messages with fields based on a domain. Example: if a sales order includes a shipping service, send the carrier data in the message.

#. Currently, if the planned actions have a message template, the view does not allow to modify the model, the type of action or the code. We will consider changing this in future versions.  

Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/REPOSITORY/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/REPOSITORY/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Ángel García de la Chica Herrera <angel.garcia@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/REPOSITORY <https://github.com/sygel-technology/REPOSITORY>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
