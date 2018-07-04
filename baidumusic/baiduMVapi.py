#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-04 06:29:32
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import sys
import time
import hashlib
try:
    import urllib.request as urllib2
except:
    import urllib2
import json
try:
    import urllib.parse as urlparse
except:
    import urlparse

import re
from yinyuetaiapi import ext



def getMVfromSongid(songid):
    url = "http://musicmini2013.qianqian.com/app/mv/getMV.php?songid=" + songid
    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    json_content = json.loads(content)
    if json_content["re"]:
        source = json_content["source"]
        print(source)

        data = json_content["flashvars"]
        print(data)
        dic = dict([(k, v[0]) for k, v in urlparse.parse_qs(data).items()])


        if source == "iqiyi":
            return iqiyi(songid, dic)

        elif source == "yinyuetai":
            return yinyuetai(dic)

    else:
        return taihe(songid)
 

def iqiyi(songid, dic):
    try:
        vid = dic["vid"] #有些视频这个接口没有vid
    except:
        file_link = taihe(songid)
        dic2 = dict([(k, v[0]) for k, v in  urlparse.parse_qs(file_link.split('?')[-1]).items()])
        vid = dic2["vid"]

    
    tvid = dic["tvid"]

    #vid = "548b3764395eaeb2aa7dba0fc606c59d"
    #tvid = "497168500"
    t = int(time.time() * 1000)
    print(t)
    src = '76f90cbd92f94a2e925d83e8ccd22cb7'
    key = 'd5fb4bd9d50c4be6948c97edd7254b0e'
    try:
        sc = hashlib.new('md5', bytes(str(t) + key  + vid, 'utf-8')).hexdigest()
    except:
        md5 = hashlib.md5()
        md5.update((bytes(str(t) + key  + vid).encode('utf-8')))
        sc = md5.hexdigest()


    url = 'http://cache.m.iqiyi.com/tmts/{0}/{1}/?t={2}&sc={3}&src={4}'.format(tvid,vid,t,sc,src)

    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    json_content = json.loads(content)
    #print(json.dumps(json_content, indent=2))

    return json_content["data"]["m3utx"]



def yinyuetai(dic):
    videoId = dic["videoId"]
    url = "http://ext.yinyuetai.com/main/get-h-mv-info?json=true&videoId=" + str(videoId)
    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    json_content = json.loads(content)
    #print(json.dumps(json_content, indent=2))

    pageUrl = json_content["videoInfo"]["pageUrl"]
    return pageUrl
    info = json_content["videoInfo"]["coreVideoInfo"]


def taihe(songid):
    url = "http://music.taihe.com/mv/" +songid
    req = urllib2.urlopen(url)
    content = req.read().decode('utf-8')
    #print content
    regx = r"data\.push\({[^;]*}"
    pattern = re.compile(regx)
    m = pattern.search(content)
    #print m.group().lstrip("data.push(")
    match = m.group().lstrip("data.push(")
    content = json.loads(match)
    #print content
    source = content["source"]
    if source == "own":
        print u"标题: " + content["title"]
        return content["file_link"]
    elif source == "iqiyi":
        return content["file_link"]

    elif "yinyuetai" in content["file_link"]:
        print u"标题: " + content["title"]
        print "tvid: " + content["tvid"]
        return ext(content["tvid"])
        #print content["file_link"]
    else:
        print "not support"


def main():
      songid = sys.argv[1]
      print(getMVfromSongid(songid))

if __name__ == '__main__':
    main()