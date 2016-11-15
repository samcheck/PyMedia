#!/usr/bin/python3
# scrapeTVDB.py - pass a tv series, season and episode and returns JSON
# does require an api key that can be obtained by signing up to thetvdb website
# api documentation: https://api.thetvdb.com/swagger

import logging

import requests
from apikeys import TVDB_apikey

URL_BASE = 'https://api.thetvdb.com'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='scrapeTVDB.log',level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger.addHandler(logging.StreamHandler()) #uncomment to log to terminal as well


def auth():
    AUTH = {"apikey": TVDB_apikey}
    headers = {'content-type': 'application/json'}
    login_url = URL_BASE + '/login'
    logger.info("Requesting JWT auth token.")

    auth_resp = requests.post(login_url, json=AUTH, headers=headers)
    auth_resp.raise_for_status()
    logger.info("Received JWT auth token.")

    return(auth_resp.json()['token'])


def theTVDB(tvTitle, tvSeason, tvEpisode, JWT=None):
    if not JWT:
        JWT = auth()
    headers = {'content-type': 'application/json',
               'Authorization': ('Bearer ' + JWT)}

    # Need to replace spaces (%20)
    logger.info("Searching for %s" % tvTitle)
    tv_url = URL_BASE + '/search/series?name=' + tvTitle
    tv_resp = requests.get(tv_url, headers=headers)
    tv_resp.raise_for_status()

    # this matches the first series title returned, w/o checking...
    likely_tv_id = tv_resp.json()['data'][0]['id']
    logger.info("Found %s." % tv_resp.json()['data'][0]['seriesName'])

    ep_url = URL_BASE + '/series/' + str(likely_tv_id) + '/episodes/query?airedSeason=' + str(tvSeason) + '&airedEpisode=' + str(tvEpisode)

    ep_resp = requests.get(ep_url, headers=headers)
    ep_resp.raise_for_status()
    logger.info("Found episode: %s." % ep_resp.json()['data'][0]['episodeName'])

    return(ep_resp.json())


def episode_id(TVDB_id, JWT=None):
    if not JWT:
        JWT = auth()
    headers = {'content-type': 'application/json',
               'Authorization': ('Bearer ' + JWT)}

    ep_url = URL_BASE + '/episodes/' + str(TVDB_id)

    ep_resp = requests.get(ep_url, headers=headers)
    ep_resp.raise_for_status()
    logger.info("Found episode: %s." % ep_resp.json()['data']['episodeName'])

    return(ep_resp.json())


def series_id(TVDB_id, JWT=None):
    if not JWT:
        JWT = auth()
    headers = {'content-type': 'application/json',
               'Authorization': ('Bearer ' + JWT)}

    series_url = URL_BASE + '/series/' + str(TVDB_id)

    series_resp = requests.get(series_url, headers=headers)
    series_resp.raise_for_status()
    logger.info("Found Series: %s." % series_resp.json()['data']['seriesName'])

    return(series_resp.json())
