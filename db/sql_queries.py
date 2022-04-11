import schema_constants

insert_into_agents_table = \
    """
    INSERT INTO {table} ({column})
    VALUES
        ('{all_agents}'),
        ('{user}'),
        ('{automated}'),
        ('{spider}')
    ON CONFLICT ({column}) DO NOTHING;
    """.format(
        table=schema_constants.AGENTS_TABLE,
        column=schema_constants.AGENTS_NAME_COLUMN,
        all_agents='all-agents',
        user='user',
        automated='automated',
        spider='spider'
    )

insert_into_access_table = \
    """
    INSERT INTO {table} ({column})
    VALUES
        ('{all_access}'),
        ('{mobile_app}'),
        ('{mobile_web}'),
        ('{desktop}')
    ON CONFLICT ({column}) DO NOTHING;
    """.format(
        table=schema_constants.ACCESS_TABLE,
        column=schema_constants.ACCESS_NAME_COLUMN,
        all_access='all-access',
        mobile_app='mobile-app',
        mobile_web='mobile-web',
        desktop='desktop'
    )

insert_into_granularity_table = \
    """
    INSERT INTO {table} ({column})
    VALUES
        ('{daily}'),
        ('{monthly}')
    ON CONFLICT ({column}) DO NOTHING;
    """.format(
        table=schema_constants.GRANULARITY_TABLE,
        column=schema_constants.GRANULARITY_NAME_COLUMN,
        daily='daily',
        monthly='monthly'
    )


create_articles_table = \
    """
    CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """.format(
        schema_constants.ARTICLES_TABLES
    )

create_agents_table = \
    """
    CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """.format(
        schema_constants.AGENTS_TABLE
    )

create_access_table = \
    """
    CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """.format(
        schema_constants.ACCESS_TABLE
    )

create_granularity_table = \
    """
    CREATE TABLE IF NOT EXISTS {0} (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """.format(
        schema_constants.GRANULARITY_TABLE
    )

create_page_views_table = \
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


def does_db_exist(database):
    return "SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{0}';".format(database)


def create_db(database, user):
    return 'CREATE DATABASE {0} WITH OWNER = {1}'.format(database, user)


def create_role_if_not_exists(rolename, password):
    return \
        """
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
        $do$;""".format(rolename, password)


def insert_into_page_views_table():
    pass
