import ldap
import logging
import sys


class LDAP(object):
    def __init__(self, config=None):
        self.config = config
        for server_count in config['ldap_config']['servers']:
            ldap_server = config['ldap_config'][server_count]['server']
            bind_dn = config['ldap_config'][server_count]['bind_dn']
            self.search_base = config['ldap_config'][server_count]['search_base']
            bind_pass = config['ldap_config'][server_count]['bind_pass']
            ldap_server_uri = ("ldaps://%s" % ldap_server)
            ldap.PORT = 636
            try:
                self.connect = ldap.initialize(ldap_server_uri)
                self.connect.set_option(ldap.OPT_REFERRALS, 0)
                self.connect.simple_bind_s(bind_dn, bind_pass)
                break
            except Exception as Err:
                logging.warning("Could not connect to ldap_server: %s :: Error: %s :: Trying next server",
                                ldap_server, str(Err))

    def search_user(self):
        search_filter = ('(uid=%s)' % self.config['user_name'])
        attribs = ['*']
        self.config['user_details'] = {}
        user_details = {}

        search_results = self.connect.search_s(
            self.search_base,
            ldap.SCOPE_ONELEVEL,
            search_filter,
            attribs,
        )

        if len(search_results.entries) > 1:
            logging.error("Error: More than 1 Entry Matched for %s :: Data Returned: %s ", user, search_results.entries)
            sys.exit(1)
        user_info = search_results.entries[0][1]
        user_details['uid'] = user_info['uid'][0]
        user_details['cn'] = user_info['cn'][0]
        user_details['sn'] = user_info['sn'][0]
        try:
            user_details['email'] = user_info['email'][0]
        except:
            user_details['email'] = user_info['gecos'][0]
        user_details['given_name'] = user_info['givenName'][0]
        user_details['shell'] = user_info['loginShell'][0]
        user_details['home'] = user_info['homeDirectory'][0]
        self.config['user_details'].update(user_details)
        return user_details
