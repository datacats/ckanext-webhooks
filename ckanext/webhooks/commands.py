import ckan.plugins as p
import paste.script
import datetime

from ckan.lib.cli import CkanCommand
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types

from ckan.model.meta import metadata,  mapper, Session
from ckan.model.types import make_uuid

class WebhookCommands(CkanCommand):
    """
    ckanext-webhooks commands:

    Usage::

        paster webhooks migrate
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__

    parser = paste.script.command.Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', dest='config',
        default='development.ini', help='Config file to use.')

    def command(self):
        cmd = self.args[0]
        self._load_config()

        if cmd == 'migrate':
            self._migrate()
        else:
            print self.__doc__

    def _migrate():
        webhook_table = Table('webhooks', metadata,
            Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
            Column('address', types.UnicodeText),
            Column('topic', types.UnicodeText),
            Column('user_id', types.UnicoeText, default='u'),
            Column('created_at', types.DateTime, default=datetime.datetime.utcnow)
        )
