ckanext-webhooks
=============

Webhooks for your CKAN. Allows users and services to register to be notified for
common CKAN events, such as:

- Dataset Events - new, update, delete
- Resource Events - new, update, delete

Subscribers provide a callback url when registering for an event, and CKAN will
call that url when the desired event happens.
