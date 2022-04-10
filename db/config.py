import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
import sql_queries


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


def populate_tables_with_defaults():
    """Populates agents, access methods, and granularity tables with default values."""

    conn = None
    try:
        params = read_db_ini()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql_queries.insert_into_access_table)
        cursor.execute(sql_queries.insert_into_agents_table)
        cursor.execute(sql_queries.insert_into_granularity_table)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Exception: {error}')
    finally:
        if conn is not None:
            conn.close()


def create_tables():
    """Creates the tables in the database created by `created_db()`."""

    conn = None
    try:
        params = read_db_ini()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql_queries.create_articles_table)
        cursor.execute(sql_queries.create_access_table)
        cursor.execute(sql_queries.create_granularity_table)
        cursor.execute(sql_queries.create_agents_table)
        cursor.execute(sql_queries.create_page_views_table)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Exception: {error}')
    finally:
        if conn is not None:
            conn.close()


def create_db():
    """If it doesn't exist yet, creates the application's database owned by the user created in `create_user()`."""

    conn = None

    try:
        params = read_db_ini()
        database_name = params['database']
        # establish the connection
        conn = psycopg2.connect(
            user='postgres',
            host='127.0.0.1',
            port='5432',
        )
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing query to create a database
        cursor.execute(sql_queries.does_db_exist(database_name))
        exists = cursor.fetchone()
        # Create the database
        if not exists:
            print(f'Database does not exist. Creating {database_name}...')
            cursor.execute(sql_queries.create_db(
                database_name, params['user']))
        else:
            print(f'Database {database_name} already exists.')
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Exception:', error)
    finally:
        if conn is not None:
            conn.close()


def create_user():
    """If user doesn't exist yet, creates a user that will own the application's database."""

    conn = None

    try:
        params = read_db_ini()

        conn = psycopg2.connect(
            user='postgres',
            host='127.0.0.1',
            port='5432',
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql_queries.create_role_if_not_exists(
            params['user'], params['password']))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print('User already exists.')
    finally:
        if conn is not None:
            conn.close()


def config():
    create_user()
    create_db()
    create_tables()
    populate_tables_with_defaults()


if __name__ == '__main__':
    config()
