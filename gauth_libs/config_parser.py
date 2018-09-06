#
##
##########################################################################
#                                                                        #
#       gauth :: config_parser                                           #
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
import gauth_libs.file_handler
import os.path
import re
import sys

class ConfigParse(object):
    def __init__(self, options=None, parser=None):
        self.options = options
        self.parser = parser
        self.file = gauth_libs.file_handler.FileHandle()

    def combine_config(self, cfg_data=None):
        try:
            color_map = cfg_data['color_map']
            color_data = self.file.read_file(config_file=color_map)
            if color_data:
                cfg_data.update(color_data)
        except KeyError as err:
            print("color map not supplied :: Error: %s :: skipping", err)
        try:
            git_config = cfg_data['git_config']
            git_data = self.file.read_file(config_file=git_config)
            if git_data:
                cfg_data.update(git_data)
        except KeyError as err:
            print("git config not supplied :: Error: %s :: exiting", err)
            sys.exit(1)
        return cfg_data

    def scan_config(self, raw_cfg=None):
        ## combine the various configs into 1 config
        raw_cfg = self.combine_config(cfg_data=raw_cfg)
        ## process the config
        if self.options.debug:
            debug = self.options.debug
            if debug == 1:
                debug_name = 'critical'
            elif debug == 2:
                debug_name = 'error'
            elif debug == 3:
                debug_name = 'warning'
            elif debug == 4:
                debug_name = 'info'
            elif debug == 5:
                debug_name = 'debug'
            else:
                print("Invalid debug level set, using default")
                debug_name = None
            if debug_name:
                raw_cfg['logging_config']['log_level'] = debug_name

        for key in raw_cfg:
            if key == 'git_config':
                for repo in raw_cfg[key]:
                    try:
                        if self.option.branch:
                            raw_cfg[key][repo]['branch'] = self.options.branch
                    except AttributeError:
                        pass
                    try:
                        raw_cfg[key][repo]['branch']
                    except KeyError:
                        # ''' still cant find a branch - force it to be master '''
                        raw_cfg[key][repo]['branch'] = 'master'

                    try:
                        clone_path = raw_cfg[key][repo]['clone_path']
                        if not re.search(user, clone_path):
                            gitclone_path, gitclone_dir = os.path.split(clone_path)
                            gitclone_path = os.path.join(gitclone_path, user)
                            clone_path = os.path.join(gitclone_path, gitclone_dir)
                            raw_cfg[key][repo]['clone_path'] = clone_path
                    except KeyError as err:
                        print ("Error :: %s", str(err))
                        sys.exit(1)

        '''add all of the command options to the config file for good measure'''
        raw_cfg['options'] = self.options
        return raw_cfg

