#
##
##########################################################################
#                                                                        #
#       gauth :: command_parser                                          #
#                                                                        #
#       (c) 2018 Vamegh Hedayati                                         #
#                                                                        #
#       Vamegh Hedayati <gh_vhedayati AT ev9 DOT io>                     #
#                                                                        #
#       Please see Copying for License Information                       #
#                             GNU/LGPL                                   #
##########################################################################
##
#

from optparse import OptionParser
import sys
from file_handler import FileHandler as file_handler


class Commands(object):
    def __init__(self, name='', version='0.0.1', message=''):
        self.name = name
        self.version = version
        self.message = message
        self.parser = OptionParser(version=self.version,
                                   usage='\n'.join([
                                       self.name + ' [options]',
                                       'Version: ' + self.version,
                                   ]))

    def add_config(self):
        self.parser.add_option('-c', '--config', action='store', default='/etc/gauth/config.yaml',
                               help=' '.join(['Provide a custom configuration file,',
                                              'defaults to /etc/gauth/config.yaml if none provided']))

    def add_debug(self):
        self.parser.add_option('-D', '--debug', action='store', type='int', default=None,
                               help=' '.join(['set debugging level: ',
                                              'an integer value between 1 to 5 (the higher the more',
                                              'debugging output that will be provided)']))
    def add_ldap(self):
        self.parser.add_option('-u', '--user_name', action='store', type='int', default=None,
                               help=' '.join(['The username or user id for the user to create the token,',
                                              'if this is not specified the username, will be gathered from env.'
                                              'Default: None']))

    def add_logging(self):
        self.parser.add_option('--log_file', action='store',
                               default=("/var/log/%s/%s.log" % (self.name, self.version)),
                               help=' '.join(['File to Log script run information',
                                              ', by default this is ',
                                              '/var/log/<name>/<name>_<version>_<date>.log (optional)']))

    def set_options(self):
        options, args = self.parser.parse_args()
        return options, args, self.parser


class CommandCheck(object):
    def __init__(self, options=None, parser=None):
        self.options = options
        self.parser = parser

    def config(self):
        if self.options.config:
            try:
                config_data = file_handler.read_file(config_file=self.options.config)
                return config_data
            except (IOError, ValueError) as err:
                print ("\nConfig File Issue: %s :: Error : %s\n" % (self.options.config, err))
                self.parser.print_help()
                sys.exit(1)

    def debug(self):
        if self.options.debug:
            print("Setting log level to match debug level")
