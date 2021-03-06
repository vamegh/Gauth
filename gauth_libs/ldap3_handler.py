
import ldap3
import logging
import sys


class LDAP(object):
    def __init__(self, config=None):
        self.config = config
        tls_config = ldap3.Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1)
        for server_count in config['ldap_config']['servers']:
            ldap_server = config['ldap_config'][server_count]['server']
            bind_dn = config['ldap_config'][server_count]['bind_dn']
            self.search_base = config['ldap_config'][server_count]['search_base']
            bind_pass = config['ldap_config'][server_count]['bind_pass']
            server = ldap3.Server(ldap_server, use_ssl=True, tls=tls_config)
            try:
                self.conn = ldap3.Connection(server, bind_dn, bind_pass, auto_bind=True)
                break
            except Exception as Err:
                logging.warning("Could not connect to ldap_server: %s :: Error: %s :: Trying next server",
                                ldap_server, str(Err))

    def search_user(self, user=None):
        search_filter = ('(uid={})'.format(self.config['user_name']))
        attribs = ['*']
        self.config['user_details'] = {}
        user_details = {}
        search_results = self.conn.search(self.search_base, search_filter, attributes=attribs)

        if len(search_results.entries) > 1:
            logging.Error("Error: More than 1 Entry Matched for %s :: Data Returned: %s ", user, search_results.entries)
            sys.exit(1)
        user_info = search_results.entries[0]
        user_details['uid'] = user_info.uid.value
        user_details['cn'] = user_info.cn.value
        user_details['sn'] = user_info.sn.value
        try:
            user_details['email'] = user_info.email.value
        except:
            user_details['email'] = user_info.gecos.value
        user_details['given_name'] = user_info.givenName.value
        user_details['shell'] = user_info.loginShell.value
        user_details['home'] = user_info.homeDirectory.value
        self.config['user_details'].update(user_details)
        return user_details
