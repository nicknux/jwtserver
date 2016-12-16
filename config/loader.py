import json
import os

class ConfigLoader(object):

    def __new__(cls):
        if not hasattr(cls, 'config_data'):
            env = os.getenv('JWTSERVER_ENV', 'local')
            cls.curr_dir = os.environ['PWD']
            config_file = "%s/config/%s.json" % (cls.curr_dir, env)
            with open(config_file) as file_data:
                cls.config_data = json.load(file_data)
        return super(ConfigLoader, cls).__new__(cls)

    @classmethod
    def current(cls):
        return cls.config_data

    @classmethod
    def current_path(cls):
        return cls.curr_dir
