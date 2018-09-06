#
##
##########################################################################
#                                                                        #
#       gauth :: file_handler                                            #
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
import sys
import yaml
import json
import logging


class FileHandle(object):

    def __init__(self, options, parser):
        self.options = options
        self.parser = parser

    def read_yaml(self, input_file=''):
        try:
            with open(input_file, "r") as config:
                yaml_data = yaml.safe_load(config)
            return yaml_data
        except (TypeError, IOError) as err:
            pass
        return False

    def read_json(self, input_file=''):
        try:
            with open(input_file, "r") as config:
                json_data = json.loads(config)
            return json_data
        except (TypeError, IOError) as err:
            pass
        return False

    def read_properties(self, input_file=''):
        data = {}
        try:
            with open(input_file, "r") as config:
                for line in config:
                    if line.startswith('#'):
                        continue
                    line = line.split('#', 1)[0]
                    line = line.rstrip()
                    print("%s\n" % (line))
                    key, value = line.split("=")
                    data[key] = value
            return data
        except (TypeError, IOError) as err:
            pass
        return False

    def read_file(self, input_file=''):
        config_data = self.read_yaml(input_file=input_file)
        if not config_data:
            config_data = self.read_json(input_file=input_file)
        if not config_data:
            config_data = self.read_properties(input_file=input_file)
        if not config_data:
            print("Error Cannot Read Config File: {} ... Aborting".format(input_file))
            sys.exit(1)
        return config_data

    def write_yaml(self, output_file=None, data=None):
        if not output_file or not data:
            logging.error("Error Data / Output file Not Provided")
            sys.exit(1)
        with open(output_file, 'w') as output_file:
            output_file.write(yaml.safe_dump(data, default_flow_style=False,
                                             allow_unicode=True, encoding=None,
                                             explicit_start=True))

    def write_json(self, output_file=None, data=None):
        if not output_file or not data:
            logging.error("Error Data / Output file Not Provided")
            sys.exit(1)
        with open(output_file, 'w') as output_file:
            json.dump(data, output_file, indent=4)

    def write_properties(self, output_file=None, data=None):
        if not output_file or not data:
            logging.error("Error Data / Output file Not Provided")
            sys.exit(1)
        with open(output_file, 'w') as outfile:
            for key, value in data.items():
                output_file.write("%s=%s\n" % (key, value))
