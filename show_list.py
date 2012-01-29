#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

import datastores


class ShowList(webapp.RequestHandler):
    def get(self):

        year = self.request.get("year")
        data = memcache.get(year)
        if data is None:
            query = datastores.Musics.gql("WHERE year = '" + year + "' ORDER BY person ASC")
            fetched_musics = query.fetch(500)
            data = [[m.person,m.title,m.video_id,m.tn_url] for m in fetched_musics if m.video_id != '']
            memcache.add(year, data, 600)

        outhtml = '<h2 id="title">' + year + u'年のヒット曲' + '</h2>'
        self.response.out.write(outhtml)
        for x in data:
            outhtml = '<a rel="prettyPhoto" href="http://www.youtube.com/watch?v=' + x[2] + '" title=""><img src="http://' + x[3] + '/vi/' + x[2] + '/2.jpg" alt="' + x[1] + ' - ' + x[0] + ' (' + year + ')' + '" />' + x[1] + '<br />' + x[0] +'</a>'
            self.response.out.write(outhtml)


application = webapp.WSGIApplication(
                                     [('/show_list', ShowList)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()