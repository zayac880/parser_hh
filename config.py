import configparser

import os


path_os = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(path_os, 'database.ini')


def config(filename=file_name, section="postgresql"):
    # create a parser
    parser = configparser.ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
