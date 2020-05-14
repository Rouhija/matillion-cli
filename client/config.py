import sys
import os.path
from os.path import dirname, realpath
from configparser import ConfigParser


class Config:
    def __init__(self):
        self.work_dir = dirname(realpath(__file__))
        self.config_path = f'{self.work_dir}/config.ini'
        self.config_parser = ConfigParser()

    def write_config(self, rewrite: bool):

        if os.path.isfile(self.config_path):
            config_exists = True
        else:
            config_exists = False

        if rewrite is True or config_exists is False:
            try:
                self.config_parser.read('config.ini')
                self.config_parser.add_section('matillion')

                if config_exists is False:
                    print('First time configuration, please provide following values')

                print('instance address (eg. 12.12.123.123): ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('matillion', 'instance_addr', val)

                print('api user: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('matillion', 'api_user', val)

                print('api password: ' , end='', flush=True)
                val = sys.stdin.readline().replace('\n', '')
                self.config_parser.set('matillion', 'api_password', val)

                with open(self.config_path, 'w') as f:
                    self.config_parser.write(f)
            except KeyboardInterrupt:
                print('\nconfig file was not updated')
            except Exception as e:
                sys.exit(f'error while writing configuration: {e}')
        return

    def read_config(self):
        try:
            r = {}
            self.config_parser.read(self.config_path)
            r['addr'] = self.config_parser['matillion']['instance_addr']
            r['user'] = self.config_parser['matillion']['api_user']
            r['password'] = self.config_parser['matillion']['api_password']
            return r
        except KeyError as e:
            sys.exit(f'missing values in configuration: {e}')