import os

import jinja2
import webapp2

import cgi
import re

import hashlib
import hmac

from google.appengine.ext import db

SECRET = "imsosecret"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


def escape_html(text):
    return cgi.escape(text, quote=True)

# User input validation

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EM_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def validate_username(username):
    return username and USER_RE.match(username)

def validate_password(password):
    return password and PW_RE.match(password)

def validate_verify(verify, password):
    return verify == password

def validate_email(email):
    if email == None or email == "":
        return True
    else:
        return email and EM_RE.match(email)

def all_valid(username, password, verify, email):
    return (validate_username(username) and 
            validate_password(password) and 
            validate_verify(verify, password) and 
            validate_email(email))
    ''' Note - can replace all_valid function by having default variable "have_error"
        set to False and then setting it to True if any of the validation formulas 
        fail.  In general, probably good to think about ways to eliminate extra functions'''


# hashing functions

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Signup(Handler):

    def get(self):
        self.render('sign_up_page.html')


    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        params = dict(username = user_username,
                      email = user_email)

        if not validate_username(user_username):
            params['username_error'] = "That's not a valid username."
        if not validate_password(user_password):
            params['password_error'] = "That's not a valid password."
        if not validate_verify(user_verify, user_password):
            params['verify_error'] = "Your passwords didn't match"
        if not validate_email(user_email):
            params['email_error'] = "That's not a valid email."

        if all_valid(user_username, user_password, user_verify, user_email):
            new_cookie_val = make_secure_val(str(user_username))
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % new_cookie_val)
            self.redirect("/welcome")
        else:
            self.render('sign_up_page.html', **params)


class Welcome(webapp2.RequestHandler):

    def get(self):
        username_cookie = self.request.cookies.get("username")
        username_val = check_secure_val(username_cookie)

        if username_val:
            self.response.write('Welcome %(username)s!' % {"username":username_val})
        else:
            self.render('sign_up_page.html')


app = webapp2.WSGIApplication([('/', Signup),
                               ('/signup', Signup),
                               ('/welcome', Welcome)
                                ],
                                debug=True) 