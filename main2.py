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
import webapp2
import cgi

form="""
<form method="post">
	<label>
		Username
		<input name = "username" type="text" value = %(val)s >
	</label>
    <br>
    <label>
        Password
        <input name = "password" type = "password">
    </label>
    <br>
    <label>
        Verify Password
        <input name = "password_verify" type = "password" >
    </label>
    <br>
    <label>
        Email Address
        <input name = "email" type = "text" >
    </label>
    <br>
	<input type="submit">
	<br>
</form>
"""

def escape_html(text):
    return cgi.escape(text, quote=True)

class MainPage(webapp2.RequestHandler):
    def write_form(self, s = ""):
    	self.response.out.write(form % {"val":escape_html(s)})

    def get(self):
    	self.write_form()

    #def validate_name(self, s):

    def post(self):
    	text = self.request.get("text");
    	self.write_form()


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

