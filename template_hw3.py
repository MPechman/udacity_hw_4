import os

import jinja2

import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class Entry(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)


class Blog(Handler):

	def render_blog(self, subject="", content="", error=""):
		entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC")
		self.render("blog.html", entries=entries)

	def get(self):
		self.render_blog()


class NewPost(Handler):

	def render_entry_form(self, subject="", content="", error=""):
		self.render("entry.html", subject=subject, content=content, error=error)

	def get(self):
		self.render_entry_form()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			new = Entry(subject=subject, content=content)
			new.put()
			id = new.key().id()
			self.redirect("/blog/%d" % id)
		else:
			error = "We need both a subject and a blog entry"
			self.render_entry_form(subject=subject, content=content, error=error)

class BlogPost(Handler):

	def render_blog_post(self, id):
		# entry = db.GqlQuery("SELECT * FROM Entry WHERE id = ")
		entry = Entry.get_by_id(int(id))
		self.render("blogpost.html", entry = entry)

	def get(self, id):
		self.render_blog_post(id)		


app = webapp2.WSGIApplication([('/blog', Blog), 
							   ('/blog/newpost', NewPost),
							   ('/blog/(\d+)', BlogPost),
							   ('/', Blog)
								],
								debug=True)