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
		ROT13
		<br>
		<textarea name="text">%(val)s</textarea>
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

    def rot13(self, s):
        out=""
        #abc1 = "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz"
        #abc2 = "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
        abc1 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        abc2 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','A','B','C','D','E','F','G','H','I','J','K','L','M','n','o','p','q','r','s','t','u','v','w','x','y','z','a','b','c','d','e','f','g','h','i','j','k','l','m']
    	for ch in s:
    		if ch in abc1:
    			c = abc1.index(ch)
    			out += ch.replace(ch, (abc2[c]))
    		else:
    			out += ch
	return(out)

    def post(self):
    	text = self.request.get("text");
        new_text = self.rot13(text)
    	self.write_form(new_text)


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

