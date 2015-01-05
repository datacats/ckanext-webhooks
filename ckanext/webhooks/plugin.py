import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model

log = logging.getLogger(__name__)

webhook_table = None

def setup():
    webhook_table = Table('webhooks', metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('address', types.UnicodeText),
        Column('topic', types.UnicodeText),
        Column('user_id', types.UnicoeText, default='u'),
        Column('created_at', types.DateTime, default=datetime.datetime.utcnow)
    )

class WebhooksPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDomainObjectNotification inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'webhooks')

    #IDomainObjectNotification & #IResourceURLChange
    def notify(self, entity, operation=None):
        if isinstance(entity, model.Resource):
            if (operation == model.domain_object.DomainObjectOperation.new
                or not operation)

                #notify all registered parties of new resource
