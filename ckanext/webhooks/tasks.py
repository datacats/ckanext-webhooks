import db
import json
import logging
import requests
import ckan.model as models

from ckan.lib.celery_app import celery
from pylons import config

log = logging.getLogger(__name__)

@celery.task(name='webhooks.notify_hooks')
def notify_hooks(entity, topic):
    log.info('Firing webhooks for {0}'.format(topic))
    webhooks = db.Webhook.find(topic=topic)

    for hook in webhooks:

        user = model.User.get(hook.user_id)
        payload = {
            'entity': entity,
            'address': hook.address,
            'webhook_id': hook.id,
            'ckan': config.get('ckan.site_url'),
            'apikey': user.apikey
        }

        requests.post(hook.address, headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(payload),
            timeout=2
        )
