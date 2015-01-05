import datetime
import ckan.model as model

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from ckan.model.meta import metadata,  mapper, Session
from ckan.model.types import make_uuid

webhook_table = Table('webhooks', metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('address', types.UnicodeText),
    Column('topic', types.UnicodeText),
    Column('user_id', types.UnicodeText, default=u''),
    Column('created_at', types.DateTime, default=datetime.datetime.utcnow)
)

class Webhook(model.DomainObject):
    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

model.meta.mapper(Webhook, webhook_table)
