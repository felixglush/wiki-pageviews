import psycopg2
from configparser import ConfigParser


def read_db_ini(filename='db/database.ini', section='postgresql'):
    """Read in user and database parameters from file."""
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db


def get_db_connection():
    params = read_db_ini()
    connection = psycopg2.connect(**params)
    connection.autocommit = True
    cursor = connection.cursor()
    return connection, cursor
