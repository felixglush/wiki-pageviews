import os
import json
import requests
import uvicorn
from fastapi import FastAPI
from api.data_models import AddArticleToDB
from data_models import UserRequestIn

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Welcome to the Wikipedia Pageview Tracking API'}


@app.post('/add_article')
def add_article(user_request: AddArticleToDB):
    """Add article to database of articles to watch"""
    article = user_request.article


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
    api = 'https://wikimedia.org/api/rest_v1/'
    request_params = f'metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}'
    request_url = f'{api}{request_params}'

    response = requests.get(url=request_url, headers=request_header)
    json_response = json.loads(response.text)
    return json_response


def process_wiki_response(json_response):
    """Parse response and persist"""
    pass


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8888, log_level="info")
