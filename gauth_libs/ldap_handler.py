import ldap3
import logging
import sys


class LCON(object):
    def __init__(self, config=None):
        self.config = config
        self.config['user_details'] = {}
        ldap_server = config['server']
        self.bind_dn = config['bind_dn']
        self.search_base = config['search_base']
        self.bind_pass = config['bind_pass']
        tls_config = ldap3.Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1)
        self.server = ldap3.Server(ldap_server, use_ssl=True, tls=tls_config)

    def search_user(self, user=None):
        search_filter = ('(uid={})'.format(user))
        attribs = ['*']
        user_details = {}
        with ldap3.Connection(self.server, self.bind_dn, self.bind_pass, auto_bind=True) as conn:
            conn.search(self.search_base, search_filter, attributes=attribs)

        if len(conn) > 1:
            logging.Error("Error: More than 1 Entry Matched for %s :: Data Returned: %s ", user, conn.entries)
            sys.exit(1)
        user_info = conn.entries[0]
        user_details['uid'] = user_info.uid.value
        user_details['cn'] = user_info.cn.value
        user_details['sn'] = user_info.sn.value
        user_details['email'] = user_info.gecos.value
        user_details['given_name'] = user_info.givenName.value
        user_details['shell'] = user_info.loginShell.value
        user_details['home'] = user_info.homeDirectory.value
        self.config['user_details'].update(user_details)
        return user_details
