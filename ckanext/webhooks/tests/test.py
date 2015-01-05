import nose
import pylons
import ckanapi
import paste.fixture
import ckan.tests as tests
import sqlalchemy.orm as orm

import ckan.plugins as p
import ckanext.webhooks.plugin as plugin
import ckan.config.middleware as middleware

from pylons import config

class TestWebhooks(tests.WsgiAppCase):

    @classmethod
    def setup_class(cls):
        wsgiapp = middleware.make_app(config['global_conf'], **config)
        cls.app = paste.fixture.TestApp(wsgiapp)

    def test_webhook_actions(self):
        ckan = ckanapi.LocalCKAN()
        callback = 'http://example.com/webhook_callback'
        
        hook = ckan.action.webhook_create(topic='dataset/create', address=callback)
        assert hook

        show = ckan.action.webhook_show(id=hook)
        assert show['id'] == hook

        delete = ckan.action.webhook_delete(id=hook)
        assert delete == hook

    def test_webhook_receive(self):
        pass
