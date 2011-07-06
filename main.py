# -*- coding: utf8 -*-
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp,db
from google.appengine.ext.webapp import util

# Model
class Comment(db.Model):
	pub_date = db.DateTimeProperty(auto_now_add=True)
	comment = db.StringProperty(multiline=True)
	image = db.BlobProperty()

class ImageHandler(webapp.RequestHandler):
	def get(self):
		c = db.get(self.request.get('img_id'))
#		if c.image:
#			self.response.headers['Content-Type'] = 'image/png'
#			self.response.out.write(c.image)
#		else:
#			self.response.out.write('No Image')


class MainHandler(webapp.RequestHandler):
    def get(self):
		self.response.out.write(u'<div><h1>webappで超簡易掲示板</h1></div>')
		self.response.out.write('''
			<form action="/post" method="post" enctype="multipart/form-data">
				<textarea name="comment" rows="3" cols="60" ></textarea><br/>
				<input type="file" name="image" />
				<input type="submit" value="Post" />
			</form>''')
		for c in Comment.all():
			self.response.out.write('<a href="/img?img_id=%s"><image height="50" width="50" src="/img?img_id=%s"/></a></div>' % (c.key, c.key))

	

class PostHandler(webapp.RequestHandler):
	def post(self):
		c = Comment()
		c.comment = self.request.get('comment')
		if self.request.get('image'):
			c.image = self.request.get('image')

		# データベースに登録
		c.put()
		# MainHandlerへリダイレクト
		self.redirect('/')


def main():
    application = webapp.WSGIApplication([
		('/', MainHandler),
		('/post', PostHandler),
		('/img', ImageHandler),
		],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
