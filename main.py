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
from google.appengine.api import users
import webapp2
import cgi
import re


MAIN_PAGE_HTML = """
<html>
  <body>
    <form method="post">
        <div><label>
            Username
            <input type="text" name="username" value="%(username)s">
            <span style="color:red">%(username_error)s</span>
        </label></div>
        <div><label>
            Password
            <input type="password" name="password" value="%(password)s">
            <span style="color:red">%(password_error)s</span>
        </label></div>
        <div><label>
            Verify Password
            <input name="verify" type="password" value="%(verify)s">
            <span style="color:red">%(verify_error)s</span>
        </label></div>
        <div><label>
            Email Address
            <input type="text" name="email" value="%(email)s">
            <span style="color:red">%(email_error)s</span>
        </label></div>
        <input type="submit">
    </form>
  </body>
</html>
"""

def escape_html(text):
    return cgi.escape(text, quote=True)

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
    return email and EM_RE.match(email)

def all_valid(username, password, verify, email):
    return (validate_username(username) and validate_password(password)
            and validate_verify(verify, password) and validate_email(email))

class MainPage(webapp2.RequestHandler):

    def write_form(self, username="", password="", verify="", email="",
                   username_error="", password_error="", verify_error="", email_error=""):
        self.response.write(MAIN_PAGE_HTML % {"username":escape_html(username),
                                              "password":escape_html(password),
                                              "verify": escape_html(verify),
                                              "email":escape_html(email),
                                              "username_error":username_error,
                                              "password_error":password_error,
                                              "verify_error":verify_error,
                                              "email_error":email_error})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        username_error_message = "That's not a valid username."
        password_error_message = "That's not a valid password."
        verify_error_message = "Your passwords didn't match"
        email_error_message = "That's not a valid email."

        username_error, password_error, verify_error, email_error = "","","",""

        if not validate_username(user_username):
            username_error = username_error_message
        if not validate_password(user_password):
            password_error = password_error_message
        if not validate_verify(user_verify, user_password):
            verify_error = verify_error_message
        if not validate_email(user_email):
            email_error = email_error_message

        if all_valid(user_username, user_password, user_verify, user_email):
            self.redirect("/welcome?username=" + user_username)
        else:
            self.write_form(user_username,user_password, user_verify, user_email, 
                            username_error, password_error, verify_error, email_error)


class Welcome(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        self.response.write('Welcome %(username)s!' % {"username":username})


app = webapp2.WSGIApplication([
    ('/', MainPage), ('/welcome', Welcome)
], debug=True)

