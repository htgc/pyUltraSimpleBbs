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
from google.appengine.ext.webapp import util, template
import os

# Model
class Comment(db.Model):
	pub_date = db.DateTimeProperty(auto_now_add=True)
	comment = db.StringProperty(multiline=True)
	image = db.BlobProperty()

class MainHandler(webapp.RequestHandler):
    def get(self):
		comments = Comment.all()
		template_values = {'comments': comments,}

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class ImageHandler(webapp.RequestHandler):
	def get(self):
		try:
			c = db.get(self.request.get('img_id'))
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(c.image)
		except:
			self.response.out.write()

class PostHandler(webapp.RequestHandler):
	def post(self):
		c = Comment()
		c.comment = self.request.get('comment')
		img = self.request.get('image')
		if img:
			c.image = db.Blob(str(img))

		# データベースに登録
		c.put()
		# MainHandlerへリダイレクト
		self.redirect('/')


def main():
    application = webapp.WSGIApplication([
		('/', MainHandler),
		('/post', PostHandler),
		('/get_img', ImageHandler),
		],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
