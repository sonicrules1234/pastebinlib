#!/usr/bin/env python
 
# Copyright (c) 2010, Westly Ward
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

def paste(paste_code, paste_name=None, paste_subdomain=None, paste_private=None, paste_expire_date=None, paste_format=None) :
    """Pastes code to pastebin.  Takes the paramaters listed at http://pastebin.com/api.php"""
    data = {"paste_code":paste_code}
    possibles = {"paste_name":paste_name, "paste_subdomain":paste_subdomain, "paste_private":paste_private, "paste_expire_date":paste_expire_date, "paste_format":paste_format}
    for param in possibles.keys() :
        if possibles[param] != None :
            data[param] = possibles["param"]
    url = urllib.urlopen("http://pastebin.com/api_public.php", urllib.urlencode(data))
    url_read = url.read()
    url.close()
    return url_read
def get_paste_by_id(urlid, subdomain=None) :
    """Gets the contents of a paste with the given ID and option subdomain"""
    if subdomain == None :
        sub = ""
    else : sub = subdomain + "."
    url = "http://%spastebin.com/download.php?i=%s" % (sub, urlid)
    x = urllib.urlopen(url)
    y = x.read()
    x.close()
    return y
def get_info(url) :
    """Gets the ID of the paste url and subdomain if there is one"""
    x = re.match("http://(.*)pastebin\.com/(.*)", url).groups()
    if x[0] != "" :
        subdomain = x[0][:-1]
    else : subdomain = None
    return (x[1], subdomain)
def get_paste(url) :
    """Gets the contents of a paste by url"""
    info = get_info(url)
    return get_paste_by_id(info[0], info[1])

def paste_from_file(filename, paste_name=None, paste_subdomain=None, paste_private=None, paste_expire_date=None, paste_format=None) :
    """Opens a file and pastes the contents"""
    x = open(filename, "r")
    y = x.read()
    x.close()
    return paste(y, paste_name, paste_subdomain, paste_private, paste_expire_date, paste_format)
