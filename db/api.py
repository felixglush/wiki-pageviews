import yaml
import uvicorn
from config import config as configure_db
from sql_queries import insert_into_page_views_table
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


def read_config(file='db/resource_config.yaml'):
    with open(file) as configuration_file:
        config_dict = yaml.load(configuration_file, Loader=yaml.FullLoader)
    return config_dict


db_app = FastAPI()
config = read_config()


class AddArticleToDB(BaseModel):
    article: str


@db_app.post('/add_article', status_code=201)
def add_article(user_request: AddArticleToDB):
    # TODO check if the item is already in the database
    print('DB add_article called with', user_request.article)
    item_already_tracked = False
    if item_already_tracked:
        raise HTTPException(
            status_code=202, detail='Article is already tracked in the database.')
    else:
        insert_into_page_views_table()


def run_local():
    uvicorn.run(
        'api:db_app', host=config['db_api']['dev']['host'], port=config['db_api']['dev']['port'], log_level='info'
    )


if __name__ == '__main__':
    configure_db()
    run_local()
