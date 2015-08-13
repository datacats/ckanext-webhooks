import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging

import db
import uuid
import json
import auth
import actions
import requests
import ckan.model as model

from pylons import config
from ckan.lib.celery_app import celery
from ckan.lib.dictization import table_dictize
from ckan.model.domain_object import DomainObjectOperation

log = logging.getLogger(__name__)

class WebhooksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IDomainObjectModification, inherit=True)
    plugins.implements(plugins.IActions, inherit=True)
    plugins.implements(plugins.IAuthFunctions, inherit=True)

    # IConfigurable
    def configure(self, config):
        if not db.webhook_table.exists():
            db.webhook_table.create()

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'webhooks')

    #IDomainObjectNotification & #IResourceURLChange
    def notify(self, entity, operation=None):
        context = {'model': model, 'ignore_auth': True, 'defer_commit': True}

        if isinstance(entity, model.Resource):
            if not operation:
                #This happens on IResourceURLChange, but I'm not sure whether
                #to make this into a webhook.
                return
            elif operation == DomainObjectOperation.new:
                topic = 'resource/create'

            if operation == DomainObjectOperation.changed:
                topic = 'resource/update'

            elif operation == DomainObjectOperation.deleted:
                topic = 'resource/delete'

            else:
                return

        if isinstance(entity, model.Package):
            if operation == DomainObjectOperation.new:
                topic = 'dataset/create'

            elif operation == DomainObjectOperation.changed:
                topic = 'dataset/update'

            elif operation == DomainObjectOperation.deleted:
                topic = 'dataset/delete'

            else:
                return

        webhooks = db.Webhook.find(topic=topic)

        for hook in webhooks:
            resource = table_dictize(entity, context)
            webhook = table_dictize(hook, context)
            celery.send_task(
                'webhooks.notify_hooks',
                args=[resource, webhook, config.get('ckan.site_url')],
                task_id='{}-{}'.format(str(uuid.uuid4()), topic)
            )

    def get_actions(self):
        actions_dict = {
            'webhook_create': actions.webhook_create,
            'webhook_delete': actions.webhook_delete,
            'webhook_show': actions.webhook_show
        }
        return actions_dict

    def get_auth_functions(self):
        auth_dict = {
            'webhook_create': auth.webhook_create,
            'webhook_delete': auth.webhook_delete,
            'webhook_show': auth.webhook_show
        }
        return auth_dict
