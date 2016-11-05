#!/usr/bin/python3
# scrapeTVDB.py - pass a tv series, season and episode and returns JSON
# does require an api key that can be obtained by signing up to thetvdb website
# api documentation: https://api.thetvdb.com/swagger

import requests
from apikeys import TVDB_apikey
URL_BASE = 'https://api.thetvdb.com'

def auth():
    AUTH = {"apikey": TVDB_apikey}
    headers = {'content-type': 'application/json'}
    login_url = URL_BASE + '/login'

    auth_resp = requests.post(login_url, json=AUTH, headers=headers)
    auth_resp.raise_for_status()

    return(auth_resp.json()['token'])

def theTVDB(tvTitle, tvSeason, tvEpisode):
    JWT = auth()
    headers = {'content-type': 'application/json',
               'Authorization': ('Bearer ' + JWT)}

    # Need to replace spaces (%20)
    tv_url = URL_BASE + '/search/series?name=' + tvTitle
    tv_resp = requests.get(tv_url, headers=headers)
    tv_resp.raise_for_status()

    # this matches the first series title returned, w/o checking...
    likely_tv_id = tv_resp.json()['data'][0]['id']

    ep_url = URL_BASE + '/series/' + str(likely_tv_id) + '/episodes/query?airedSeason=' + str(tvSeason) + '&airedEpisode=' + str(tvEpisode)

    ep_resp = requests.get(ep_url, headers=headers)
    ep_resp.raise_for_status()

    return(ep_resp.json())
