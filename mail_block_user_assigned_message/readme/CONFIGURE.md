To configure this module, you need to:

1. Go to the "Preferences" tab in an internal user.
2. Activate the "Block Assigned Message" option.
3. Select the models for which assignation notifications don't have to be generated.

It is important to keep in mind that automatic assignment notifications are only created when a model meets the following requirements:

- The model is subclass of the abstract class mail.thread.
- The model has a user_id field.
- The tracking parameter of the user_id field is different to False.

This module will not work with models that do not meet all those three requirements. Also, notification methods can be overriden, so the module would not work in those cases either.

A particular example of a model that does not work is the project.task model. It does not have a user_id field, but a Many2many user_ids field. Assignment notifications are created using a specific custom method for this model, so are not blocked using this module.
