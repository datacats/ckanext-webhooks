import logging

from pylons import config

import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.new_authz as new_authz

log = logging.getLogger(__name__)

def _user_has_minumum_role(context):
    """
    Determines whether the user has the minimum required role
    as specific in configuration. This is deliberately verbose.
    """
    roles = ['editor', 'admin', 'sysadmin']
    user = context['user']
    userobj = model.User.get(user)

    # Do we have a configured minimum role, if not just say ok now.
    minimum_role = config.get('ckanext.webhooks.minimum_auth', '').lower()
    if not minimum_role or minimum_role.lower() == 'none':
        return {'success': True}

    # Validate that the config option is valid and refuse, if we added
    # the option we probably wanted it to be *something*.
    if not minimum_role in roles:
        log.warning("ckanext.webhooks.minimum_auth has an invalid option")
        return {'success': False}

    # Always let sysadmins do their thing.
    if new_authz.is_sysadmin(user):
        return {'success': True}

    # We let sysadmins in just not, so just refuse if we get here.
    if minimum_role == 'sysadmin':
        return {'success': False}

    # Determine if the user has the required role in any organization
    q = model.Session.query(model.Member) \
        .filter(model.Member.table_name == 'user') \
        .filter(model.Member.table_id == userobj.id) \
        .filter(model.Member.state == 'active')
    roles_for_user = [m.capacity for m in q.all()]

    # If we want admins, let in anyone who has admin
    if minimum_role == 'admin':
        if 'admin' in roles_for_user:
            return {'success': True}

    # Only allow users who have editor
    if minimum_role == 'editor':
        if 'editor' in roles_for_user  or 'admin' in roles_for_user:
            return {'success': True}

    return {'success': False}

def webhook_create(context, data_dict):
    return _user_has_minumum_role(context)

def webhook_show(context, data_dict):
    return _user_has_minumum_role(context)

def webhook_delete(context, data_dict):
    return _user_has_minumum_role(context)