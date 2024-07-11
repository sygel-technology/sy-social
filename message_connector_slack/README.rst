.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

=======================
Message Connector Slack
=======================

This module allows you to send automatic messages to the slack chat. 

To create the messages you need to have the message_connector_base module installed.


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To configure Slack chat:

#. It will be necessary to create an app in https://api.slack.com/apps/ in the workspace we want to work and define its name: Odoo and the Bot Token Scopes: channels:read + chat:write.

#. To upload files to the chat it is also necessary to set file:write.

#. For Slack to work correctly in the channels, it will be necessary to click on "Add applications" in the channel, in "More" and add the Odoo application previously created.

For more information go to: https://api.slack.com/start/quickstart


To configure this module:

#. To use the Slack connector activate the connector from Setting -> Active Slack

#. To delete old Slack log messages set the message log deletion frequency higher than zero.

If you have two Slack accounts, one for Test and one for Production, you can configure them from the connector settings. To do this:

#. Select Slack environment: Test or Production.

#. Select a test channel.

#. Paste the token generated when creating the Slack application in the 'API token' field. 



Usage
=====

To use this module, you need to:

#. Create and validate a channel. Go to Message Connector -> Channel -> Create
#. Create a message. Go to Message Connector -> Message Builder -> Once created you can send test messages to the selected channel. 
#. Create an automatic action from the Settings tab.
#. Validate the message
#. Execute the action that triggers the automatic action to send the message.


ROADMAP
=======

[ Enumerate known caveats and future potential improvements.
  It is mostly intended for end-users, and can also help
  potential new contributors discovering new features to implement. ]

* ...


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
