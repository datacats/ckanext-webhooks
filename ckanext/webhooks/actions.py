import db
import logging

from ckan.plugins.toolkit import get_validator, ValidationError
from ckan.lib.dictization import table_dictize
from ckan.logic import NotFound
import ckan.lib.navl.dictization_functions as df

log = logging.getLogger(__name__)

schema = {
    'id': [get_validator('ignore_empty'), unicode],
    'address': [get_validator('not_empty'), unicode],
    'topic': [get_validator('not_empty'), unicode],
    'user_id': [get_validator('ignore_missing'), unicode],
    'created_at': [get_validator('ignore_missing'), get_validator('isodate')]
}

schema_get = {
    'id': [get_validator('not_empty'), unicode]
}

def webhook_create(context, data_dict):
    data, errors = df.validate(data_dict, schema, context)

    if errors:
        raise ValidationError(errors)

    webhook = db.Webhook()
    webhook.address = data['address']
    webhook.topic = data['topic']
    webhook.save()

    session = context['session']
    session.add(webhook)
    session.commit()

    return webhook.id

def webhook_show(context, data_dict):
    data, errors = df.validate(data_dict, schema_get, context)
    if errors:
        raise ValidationError(errors)

    webhook = db.Webhook.get(id=data['id'])
    if webhook is None:
        raise NotFound()

    return table_dictize(webhook, context)

def webhook_delete(context, data_dict):
    data, errors = df.validate(data_dict, schema_get, context)
    if errors:
        raise ValidationError(errors)

    webhook = db.Webhook.get(id=data['id'])
    session = context['session']
    session.delete(webhook)
    session.commit()

    return data['id']
