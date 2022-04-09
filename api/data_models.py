from pydantic import BaseModel


class AccessMode(str):
    all_access = 'all-access'
    mobile_app = 'mobile-app'
    mobile_web = 'mobile-web'
    desktop = 'desktop'


class Agent(str):
    all_agents = 'all-agents'
    user = 'user'
    automated = 'automated'
    spider = 'spider'


class Granularity(str):
    daily = 'daily'
    monthly = 'monthly'


class UserRequestIn(BaseModel):
    # https://wikimedia.org/api/rest_v1/#/Pageviews%20data/get_metrics_pageviews_per_article__project___access___agent___article___granularity___start___end_
    # If you want to filter by project, use the domain of any Wikimedia project,
    # for example 'en.wikipedia.org', 'www.mediawiki.org' or 'commons.wikimedia.org'.
    project: str
    # If you want to filter by access method, use one of desktop, mobile-app or mobile-web.
    # If you are interested in pageviews regardless of access method, use all-access.
    access: AccessMode
    # If you want to filter by agent type, use one of user, automated or spider.
    # If you are interested in pageviews regardless of agent type, use all-agents.
    agent: Agent
    # The title of any article in the specified project.
    # Any spaces should be replaced with underscores.
    # It also should be URI-encoded, so that non-URI-safe characters like %, / or ? are accepted.
    # Example: Are_You_the_One%3F'
    article: str
    # The time unit for the response data
    granularity: Granularity
    # The date of the first day to include, in YYYYMMDD or YYYYMMDDHH format
    start: str
    # The date of the last day to include, in YYYYMMDD or YYYYMMDDHH format
    end: str


class AddArticleToDB(BaseModel):
    article: str


class EntityOut(BaseModel):
    pass


fake_request = UserRequestIn(
    project='en.wikipedia.org',
    access=AccessMode.all_access,
    agent=Agent.all_agents,
    article='Apple_Inc',
    granularity=Granularity.daily,
    start='20190626',
    end='20190701'
)


def fake_wiki_api_response():
    return {
        "items": [
            {
                "access": "all-access",
                "agent": "all-agents",
                "article": "Apple_Inc",
                "granularity": "daily",
                "project": "en.wikipedia",
                "timestamp": "2019062600",
                "views": 243
            },
            {
                "access": "all-access",
                "agent": "all-agents",
                "article": "Apple_Inc",
                "granularity": "daily",
                "project": "en.wikipedia",
                "timestamp": "2019062700",
                "views": 201
            },
            {
                "access": "all-access",
                "agent": "all-agents",
                "article": "Apple_Inc",
                "granularity": "daily",
                "project": "en.wikipedia",
                "timestamp": "2019062800",
                "views": 259
            },
            {
                "access": "all-access",
                "agent": "all-agents",
                "article": "Apple_Inc",
                "granularity": "daily",
                "project": "en.wikipedia",
                "timestamp": "2019062900",
                "views": 424
            },
            {
                "access": "all-access",
                "agent": "all-agents",
                "article": "Apple_Inc",
                "granularity": "daily",
                "project": "en.wikipedia",
                "timestamp": "2019063000",
                "views": 166
            },
            {
                "access": "all-access",
                "agent": "all-agents",
                "article": "Apple_Inc",
                "granularity": "daily",
                "project": "en.wikipedia",
                "timestamp": "2019070100",
                "views": 255
            }
        ]
    }
