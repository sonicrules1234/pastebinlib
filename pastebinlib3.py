#!/usr/bin/env python
 
# Copyright (c) 2011, Westly Ward
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the pastebinlib team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY Westly Ward ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Westly Ward BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib, re

class pastebin :
    """To use this class, you need to make an instance of it first.
An example would be
import pastebinlib
instance = pastebinlib.pastebin(apikey)

Where apikey is the developer API key you get when registering on pastebin.com"""
    def __init__(self, apikey) :
        self.baseurl = "https://pastebin.com/api/api_post.php"
        self.loginurl = "https://pastebin.com/api/api_login.php"
        self.apikey = apikey
        self.regexcompile = re.compile("\<paste\>\r\n\<paste_key\>(.*)\<\/paste_key\>\r\n\<paste_date\>(\d*)\<\/paste_date\>\r\n\<paste_title\>(.*)<\/paste_title\>\r\n\<paste_size\>(\d*)\<\/paste_size\>\r\n\<paste_expire_date\>(\d*)\<\/paste_expire_date\>\r\n\<paste_private\>([0|1])\<\/paste_private\>\r\n\<paste_format_long\>(.*)\<\/paste_format_long\>\r\n\<paste_format_short\>(.*)\<\/paste_format_short\>\r\n\<paste_url\>(http[s]{0,1}\:\/\/pastebin.com/.*)\<\/paste_url\>\r\n\<paste_hits>(\d*)\<\/paste_hits\>\r\n\<\/paste\>")
    def paste(self, paste_code, user_key=None, paste_name=None, paste_format=None, paste_private=None, paste_expire_date=None) :
        """This pastes code"""
        data = {"api_paste_code":paste_code, "api_option":"paste", "api_dev_key":self.apikey}
        possibles = {"api_user_key":user_key, "api_paste_name":paste_name, "api_paste_format":paste_format, "api_paste_expire_date":paste_expire_date}
        if paste_private != None :
            if paste_private != "0" and pasteprivate != "1" :
                if paste_private == True :
                    paste_private = "1"
                elif paste_private == False :
                    paste_private = "0"
            data["api_paste_private"] = paste_private
        for param in possibles.keys() :
            if possibles[param] != None :
                data[param] = possibles[param]
        urlobj = urllib.urlopen(self.baseurl, urllib.urlencode(data))
        url_read = urlobj.read()
        urlobj.close()
        return url_read
    def get_user_key(self, username, password) :
        """This function gets the user session key, with which you can do operations having to do with this user"""
        data = {"api_dev_key":self.apikey, "api_user_name":username, "api_user_password":password}
        urlobj = urllib.urlopen(self.loginurl, urllib.urlencode(data))
        url_read = urlobj.read()
        urlobj.close()
        return url_read
    def get_pastes_list(self, user_key, results_limit=None) :
        """This gets a list of all the pastes made by this user, and returns a dictionary with information on each one"""
        data = {"api_dev_key":self.apikey, "api_user_key":user_key, "api_option":"list"}
        if results_limit != None :
            data["api_results_limit"] = results_limit
        urlobj = urllib.urlopen(self.baseurl, urllib.urlencode(data))
        url_read = urlobj.read()
        urlobj.close()
        reresults = self.regexcompile.findall(url_read)
        results = []
        for result in reresults :
            results.append({"paste_key":result[0], "paste_date":int(result[1]), "paste_title":result[2], "paste_size":int(result[3]), "paste_expire_date":int(result[4]), "paste_private":(result[5]=="1"), "paste_format_long":result[6], "paste_format_short":result[7], "paste_url":result[8], "paste_hits":int(result[9])})
        return results
