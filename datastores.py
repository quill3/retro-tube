#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Musics(db.Model):
    year = db.StringProperty()
    person = db.StringProperty()
    title = db.StringProperty()
    video_id = db.StringProperty()
    tn_url = db.StringProperty()
    get_result = db.StringProperty()
    checked_time = db.DateTimeProperty()