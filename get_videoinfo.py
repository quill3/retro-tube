#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch

import re
import datetime
import time
import urllib

import datastores


def get_music():
    query = datastores.Musics.gql('ORDER BY checked_time ASC')
    music = query.get()

    if music:
        return music


def get_youtube_data(music):
    if not music:return

    youtube_url = 'http://gdata.youtube.com/feeds/api/videos?category=Music&max-results=1&vq=' + urllib.quote_plus(music.person.encode('utf8')) + '+' + urllib.quote_plus(music.title.encode('utf8'))

    try:
        get_result = urlfetch.fetch(youtube_url,deadline=10)
    except:
        parse_results1 = ['']
        parse_results2 = ['']
        parse_results3 = 'ERR'
    else:
        if get_result.status_code == 200:
            pattern = re.compile(r"<id>http://gdata.youtube.com/feeds/api/videos/(.*?)</id>")
            parse_results1 = pattern.findall(get_result.content)
            if not parse_results1:
                parse_results1 = ['']

            pattern = re.compile(r"thumbnail url='http://(.*?)/vi/")
            parse_results2 = pattern.findall(get_result.content)
            if not parse_results2:
                parse_results2 = ['']
            parse_results3 = 'OK'

        else:
            parse_results1 = ['']
            parse_results2 = ['']
            parse_results3 = 'NG'

    return {'music':music,
                'video_id':parse_results1[0],
                'tn_url':parse_results2[0],
                'get_result':parse_results3}


def put_music(music):
    if not music:return

    music['music'].video_id = music['video_id']
    music['music'].tn_url = music['tn_url']
    music['music'].get_result = music['get_result']
    music['music'].checked_time = datetime.datetime.today()
    music['music'].put()


if __name__ == "__main__":
#    for i in range(5):
    put_music(get_youtube_data(get_music()))
#        time.sleep(1)