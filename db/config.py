import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
import schema_constants


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


def create_tables():
    """Creates the tables in the database created by `created_db()`."""
    articles_table = \
        """
        CREATE TABLE IF NOT EXISTS {0} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """.format(
            schema_constants.ARTICLES_TABLES
        )

    agents_table = \
        """
        CREATE TABLE IF NOT EXISTS {0} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """.format(
            schema_constants.AGENTS_TABLE
        )

    access_table = \
        """
        CREATE TABLE IF NOT EXISTS {0} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """.format(
            schema_constants.ACCESS_TABLE
        )

    granularity_table = \
        """
        CREATE TABLE IF NOT EXISTS {0} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """.format(
            schema_constants.GRANULARITY_TABLE
        )

    page_views_table = \
        """
        CREATE TABLE IF NOT EXISTS {0} (
            id SERIAL PRIMARY KEY,
            article_id INTEGER REFERENCES {1} (id),
            access_id INTEGER REFERENCES {2} (id),
            agent_id INTEGER REFERENCES {3} (id),
            granularity_id INTEGER REFERENCES {4} (id),
            pageviews INT,
            date DATE
        );
        """.format(
            schema_constants.PAGE_VIEWS_TABLE,
            schema_constants.ARTICLES_TABLES,
            schema_constants.ACCESS_TABLE,
            schema_constants.AGENTS_TABLE,
            schema_constants.GRANULARITY_TABLE
        )

    conn = None
    try:
        params = read_db_ini()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(articles_table)
        cursor.execute(access_table)
        cursor.execute(granularity_table)
        cursor.execute(agents_table)
        cursor.execute(page_views_table)

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
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{0}';".format(
                database_name)
        )
        exists = cursor.fetchone()
        # Create the database
        if not exists:
            print(f'Database does not exist. Creating {database_name}...')
            cursor.execute('CREATE DATABASE {0} WITH OWNER = {1}'.format(
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

        cur = conn.cursor()

        create_role_if_not_exists = """
                                    DO
                                    $do$
                                    BEGIN
                                        IF NOT EXISTS (
                                            SELECT FROM pg_catalog.pg_roles
                                            WHERE  rolname = '{0}') THEN
                                            CREATE ROLE {0} LOGIN PASSWORD {1};
                                            ALTER ROLE {0} WITH CREATEDB;
                                            GRANT {0} TO postgres;
                                    END IF;
                                    END
                                    $do$;"""

        query = sql.SQL(create_role_if_not_exists).format(
            sql.Identifier(params['user']),
            sql.Literal(params['password']),
        )
        cur.execute(query.as_string(conn))

        cur.execute("COMMIT")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print('User already exists.')
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_user()
    create_db()
    create_tables()
