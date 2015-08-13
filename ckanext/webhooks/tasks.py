import requests

from ckan.lib.celery_app import celery

@celery.task(name='webhooks.notify_hooks')
def notify_hooks(self, entity, context, topic):
    log.info('Firing webhooks for {0}'.format(topic))
    webhooks = db.Webhook.find(topic=topic)

    for hook in webhooks:
        dictized = table_dictize(entity, context)

        user = model.User.get(hook.user_id)
        url = config.get('ckanext.webhooks.eventloop', hook.address)
        payload = {
            'entity': dictized,
            'address': hook.address,
            'webhook_id': hook.id,
            'ckan': config.get('ckan.site_url'),
            'apikey': user.apikey
        }

        requests.post(url, headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(payload),
            timeout=2
        )
