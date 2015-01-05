================
ckanext-webhooks
================

Webhooks for your CKAN. Allows users and services to register to be notified for
common CKAN events, such as:

- Dataset Events - new, update, delete
- Resource Events - new, update, delete

Subscribers provide a callback url when registering for an event, and CKAN will
call that url when the desired event happens.

Usage
=====
Add webhooks to your CKAN plugins:

.. code::

    ckan.plugins = ... webhooks

.. code:: python

    import ckanapi
    ckan = ckanapi.RemoteCKAN('http://some.ckan.org')

    #create webhook
    hook = ckan.action.webhook_create(topic="dataset/create", address="http://example.com/callback")

    #show webhook
    ckan.action.webhook_show(id=hook)

    #delete webhook
    ckan.action.webhook_delete(id=hook)

Design Decisions
==================
The extension allows users to create webhooks without logging in. This decreases
friction to creating webhooks and exposes the functionality to more users. The
main reason for the decision to do it this way is because most governments
(the primary users of CKAN) do not wish to allow account creation in CKAN to the
public. If we only allow Webhook creation for users with an API key, many CKAN
users will be left without a way to create Webhooks.

Because of this, the extension makes the following decisions:

- There is no way to list all existing webhooks. This would allow everyone to
  see everybody else's webhooks.
- Each webhook gets a random id that is sufficiently long to be impractical to
  guess.
- Consequently, a user needs to keep track of their webhook ids in order to
  delete a webhook. The id is returned on webhook creation, and it is also passed
  in the webhook execution call, so if the user loses it, they can fetch it next
  time the webhook is executed.
- This might create the problem of stale webhooks, but that is ok. If a webhook
  executes and the URL returns a 4xx error several times, the extension will
  eventually delete the webhook.

TODO
====

- Access control: Make sure access-restricted events do not leak
- API authentication - send webhooks to users who have API access to the dataset/
  resource for which the webhook is being fired.
- Filter: subscribe by entity id, for selective dataset/resource/etc...
- Celery tasks for retrying failed hooks
- Celery tasks for deleting stale unresponsive hooks
