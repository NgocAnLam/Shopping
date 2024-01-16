from configparser import ConfigParser

def read_config(filename, section, key):
    config = ConfigParser()
    config.read(filename)
    if section in config and key in config[section]:
        return config[section][key]
    else:
        return None