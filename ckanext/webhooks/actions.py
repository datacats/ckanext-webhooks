import db
import logging

from ckan.plugins.toolkit import get_validator, ValidationError
import ckan.lib.navl.dictization_functions as df

log = logging.getLogger(__name__)

schema = {
    'id': [get_validator('ignore_empty'), unicode],
    'address': [get_validator('not_empty'), unicode],
    'topic': [get_validator('not_empty'), unicode],
    'user_id': [get_validator('ignore_missing'), unicode],
    'created_at': [get_validator('ignore_missing'), get_validator('isodate')]
}

def webhook_create(context, data_dict):
    log.info(data_dict)

    data, errors = df.validate(data_dict, schema, context)

    if errors:
        raise ValidationError(errors)

    webhook = db.webhook_table

def webhook_delete(context, data_dict):
    pass
