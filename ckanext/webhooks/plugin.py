import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model
import logging
import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from ckan.model.meta import metadata,  mapper, Session
from ckan.model.types import make_uuid

log = logging.getLogger(__name__)

webhook_table = Table('webhooks', metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('address', types.UnicodeText),
    Column('topic', types.UnicodeText),
    Column('user_id', types.UnicodeText, default=u''),
    Column('created_at', types.DateTime, default=datetime.datetime.utcnow)
)

class WebhooksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDomainObjectModification, inherit=True)
    plugins.implements(plugins.IActions, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'webhooks')

    #IDomainObjectNotification & #IResourceURLChange
    def notify(self, entity, operation=None):
        if isinstance(entity, model.Resource):
            if (operation == model.domain_object.DomainObjectOperation.new
                or not operation):
                pass
                #notify all registered parties of new resource

    def after_map(self, map):
        pass

    def get_actions(self):
        pass
