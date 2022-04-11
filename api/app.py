import os
import json
import requests
import uvicorn
import yaml
import utils
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from data_models import UserRequestIn, AddArticleToDB

load_dotenv()  # take environment variables from .env.


def read_config(file='api/resource_config.yaml'):
    with open(file) as configuration_file:
        config_dict = yaml.load(configuration_file, Loader=yaml.FullLoader)
    return config_dict


app = FastAPI()
config = read_config()


@app.get('/')
def read_root():
    return {'message': 'Welcome to the Wikipedia Pageview Tracking API'}


@app.post('/add_article')
def add_article(user_request: AddArticleToDB):
    """Add article to table of articles to watch"""
    article_name = utils.preprocess_article_name(user_request.article)

    # TODO: implement endpoint to validate it's an actual article

    request_header = {
        'Content-Type': 'application/json',
        'User-Agent': os.environ['WikiUserAgent']
    }
    db_protocol_scheme = config['db_api']['dev']['protocol_scheme']
    db_host = config["db_api"]["dev"]["host"]
    db_port = config["db_api"]["dev"]["port"]
    add_article_endpoint = config["db_api"]["endpoints"]["add_article"]
    db_api = f'{db_protocol_scheme}://{db_host}:{db_port}/{add_article_endpoint}'
    data = {'article': article_name}
    try:
        requests.post(url=db_api, json=data, headers=request_header)
    except HTTPException as e:
        print(e)


@app.get('/page_views/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}')
def page_views(project: str, access: str, agent: str, article: str, granularity: str, start: str, end: str):
    """Get page views for an article"""

    request = UserRequestIn(
        project=project,
        access=access,
        agent=agent,
        article=article,
        granularity=granularity,
        start=start,
        end=end
    )

    response = query_wiki_api(request)
    return {'response': response}


def query_wiki_api(user_request: UserRequestIn):
    """Query the Wikipedia API for Page Views"""
    # Rate limit: 100 requests per second

    project = user_request.project
    access = user_request.access
    agent = user_request.agent
    article = user_request.article
    granularity = user_request.granularity
    start = user_request.start
    end = user_request.end

    request_header = {
        'Content-Type': 'application/json',
        'User-Agent': os.environ['WikiUserAgent']
    }
    wiki_api = config['api']['wiki_api']
    request_params = \
        f'{config["api"]["wiki_pageviews_endpoint"]}{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}'
    request_url = f'{wiki_api}{request_params}'

    response = requests.get(url=request_url, headers=request_header)
    json_response = json.loads(response.text)
    return json_response


def process_wiki_response(json_response):
    """Parse response and persist."""
    pass


def run_local():
    """Starts a local instance of the API."""
    uvicorn.run("app:app", host=config['api']['host'],
                port=config['api']['port'], log_level="info")


if __name__ == "__main__":
    run_local()
