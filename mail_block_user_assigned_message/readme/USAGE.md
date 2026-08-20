To use this module, you need to:

1. Go to a model that has assign notifications. For example: res.partner (install the contacts module if you do not have the menu)
2. Login with a user that has permissions in that model with another browser or incognito mode. Create that user before if it does not exist
3. With the second user, assign a record to the first user selecting him on the user_id field. In our res.partner example, we will assign the first user as 'Salesperson'.
4. The first user will not receive the assignation notification if you have configured them to be blocked in that model. You can also review if the notifications are correcly received without this block.

Note: Notifications are, by default, handled by emails. You can change them, to be handled in odoo, in your preferences.
