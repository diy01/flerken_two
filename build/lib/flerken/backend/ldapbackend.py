# -*- coding: utf-8 -*-
import ldap
import warnings

import django
from django_auth_ldap.backend import LDAPBackend, LDAPSettings
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion

from modules.users.models import LDAP


class SSOLDAPSettings(LDAPSettings):

    def __init__(self, prefix='AUTH_LDAP_', defaults={}):
        """
        Loads our settings from django.conf.settings, applying defaults for any
        that are omitted.
        """
        self._prefix = prefix

        defaults = dict(self.defaults, **defaults)
        for name, default in defaults.items():
            value = getattr(django.conf.settings, prefix + name, default)
            setattr(self, name, value)

        ssoldap = LDAP.objects.filter(status=0).first()
        setattr(self, "USER_SEARCH", LDAPSearchUnion())
        if ssoldap:
            setattr(self, "SERVER_URI", ssoldap.server_uri)
            setattr(self, "BIND_DN", ssoldap.bind_dn)
            setattr(self, "BIND_PASSWORD", ssoldap.password)
            authDN = [LDAPSearch(unicode(dn), ldap.SCOPE_SUBTREE, ssoldap.user_filter) for dn in
                      ssoldap.user_ou.split("\n")]
            setattr(self, "USER_SEARCH", LDAPSearchUnion(*authDN))

        # Compatibility with old caching settings.
        if getattr(django.conf.settings, self._name('CACHE_GROUPS'), defaults.get('CACHE_GROUPS')):
            warnings.warn(
                'Found deprecated setting AUTH_LDAP_CACHE_GROUP. Use '
                'AUTH_LDAP_CACHE_TIMEOUT instead.',
                DeprecationWarning,
            )
            self.CACHE_TIMEOUT = getattr(
                django.conf.settings,
                self._name('GROUP_CACHE_TIMEOUT'),
                defaults.get('GROUP_CACHE_TIMEOUT', 3600),
            )


class SSOLDAPBackend(LDAPBackend):

    @property
    def settings(self):
        if self._settings is None:
            self._settings = SSOLDAPSettings(self.settings_prefix, self.default_settings)
        return self._settings
