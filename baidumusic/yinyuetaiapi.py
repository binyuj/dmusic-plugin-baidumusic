#!/usr/bin/env python
# -*- coding: utf-8 -*-

#yinyuetai音乐台

import sys
import urllib2
import re
import time
import logging
import json
from StringIO import StringIO
import gzip
import zlib

# http://www.yinyuetai.com/api/info/get-video-urls?callback=callback&videoId=
#
# http://v.yinyuetai.com/video/2045867
# http://m.yinyuetai.com/mv/get-simple-video-info?&videoId=1691   手机版，有dd，hc，hd没有he   http://m.yinyuetai.com/
# http://www.yinyuetai.com/api/info/get-video-urls?videoId=819374    只有下载地址
# http://ext.yinyuetai.com/main/get-h-mv-info?json=true&videoId=2297736  pad版，信息完整，封面，hc,hd,he,sh 文件大小
#


videoId = 2297736


def get_content(url):
    '''
    网络模块，获取内容
    '''
    start_time = time.time()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'),
                            ('Accept-Encoding', 'gzip,deflate'),
                            ('Accept-Language', 'zh-CN,zh;q=0.8'),
                            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                            ('Connection', 'keep-alive')]
    req = opener.open(url)
    logging.info('request timeuse: %s s', time.time() - start_time)
    logging.debug('status %s', req.getcode())
    headers = req.info()
    content = req.read()
    if headers['Content-Encoding'] == 'gzip':
        logging.debug('get gzip response\n%s', headers)
        gz = gzip.GzipFile(fileobj=StringIO(content))
        content = gz.read()
        gz.close()
    elif headers['Content-Encoding'] == 'deflate':
        logging.debug('get deflate response\n%s', headers)
        content = zlib.decompress(content)

    return content


def ext(videoId):
    '''
    使用html5版页面（pad版）获得的接口，直接得到json类型的数据
    '''
    api_url = 'http://ext.yinyuetai.com/main/get-h-mv-info?json=true&videoId=' + str(videoId)
    for x in xrange(5):
        try:
            content = get_content(api_url)
            break
        except Exception, e:
            logging.warning('timeout, retry. %s', e)

    obj = json.loads(content)
    return json.dumps(obj, indent=4, ensure_ascii=False)


def main(sysargv):
    arg_len = len(sysargv[1])
    if arg_len > 7:    # 目前还没有发现长度超过7的ID
        url = sysargv[1].split('?')[0]  # 去除timestamp之类的尾巴
        if not url.startswith('http://'):
            url = 'http://' + url
        videoId = re.search(r'http://\w+.yinyuetai.com/video/(\d+)$', url).group(1)
    else:
        videoId = sysargv[1]
    logging.debug('videoId is %s', videoId)
    return ext(videoId)


def test():
    '''
    just a test
    '''
    videoId = 2297736
    url = "http://ext.yinyuetai.com/main/get-h-mv-info?json=true&videoId=" + str(videoId)
    print get_content(url)


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - [%(asctime)s]: %(message)s', level=logging.DEBUG, datefmt='%b %d %H:%M:%S')

    if len(sys.argv) > 1:
        print main(sys.argv)
    else:
        test()


'''
http://m.yinyuetai.com/mv/get-simple-video-info?&videoId=2240030
{
    "message": "",
    "error": false,
    "logined": true,
    "videoInfo": {
        "id": 2240030,
        "userId": 36875358,
        "pubDate": "2015-02-13 17:13:06",
        "title": "EP5 TFboys 解密万千宠爱为哪般",
        "content": "有三位这样的小少年，他们2013年才正式出道，他们有一群死忠的阿姨粉、姐姐饭他们在第二届音悦V榜上锋芒毕露，在投票类获得内地最具人气歌手奖音悦直播人气歌手奖；他们就是TFboys~本期节目就带大家解密TFboys万千宠爱为哪般”~TFboys无需隐藏 炫出自我",
        "duration": 311,
        "state": 0,
        "publish": 1,
        "headImg": "http://img1.yytcdn.com/video/mv/150306/2240030/-M-49908c593a3dfb795f2ec9460eb65f72_120x67.jpg?t=20150306181928",
        "bigHeadImg": "http://img1.yytcdn.com/video/mv/150306/2240030/-M-49908c593a3dfb795f2ec9460eb65f72_240x135.jpg?t=20150306181928",
        "albumImg": "/video/mv/150213/2240030/-M-ada0645470eaae4623d5f3c1b76da10d_640x360.jpg?t=20150306181928",
        "videoUrl": "http://hc.yinyuetai.com/uploads/videos/common/406B014B8204FF3E5BB2E5E65CADA7A5.flv?sc=02acdfe0a0d95047",
        "videoUrl2": "http://hd.yinyuetai.com/uploads/videos/common/03A0014B8236859E54EC0B2383B65422.flv?sc=a7ea7ae8ff1c391b",
        "videoUrl3": "http://dd.yinyuetai.com/uploads/videos/common/BF08014B82368594F02AC8C482646E34.mp4?sc=eeb9b2fe85b92768",
        "height": "0",
        "width": "0",
        "personName": "先锋音乐人",
        "personHeadImg": "http://img2.yytcdn.com/user/avatar/150109/36875358/-M-a56e212dc02215186a50a15bdc5e03f4_50x50.jpg",
        "personBigHeadImg": "http://img2.yytcdn.com/user/avatar/150109/36875358/-M-a56e212dc02215186a50a15bdc5e03f4_100x100.jpg",
        "artists": [
            {
                "artistId": 38422,
                "artistName": "先锋音乐人",
                "enabled": 1,
                "area": "Other",
                "property": "Other",
                "enname": "X",
                "aliasName": "",
                "headImg": "http://img1.yytcdn.com/artist/fan/150519/0/-M-caaa9db4d614bc72402533f1c08e03b0_0x0.jpg",
                "bigHeadImg": "http://img1.yytcdn.com/artist/fan/150519/0/-M-caaa9db4d614bc72402533f1c08e03b0_0x0.jpg",
                "regdate": "May 19, 2015 11:47:39 AM",
                "totalViews": 0,
                "totalFanNum": 33,
                "fanMemberCountRank": 99999,
                "videoNum": 26,
                "videoCountRank": 99999,
                "topicNum": 0
            },
            {
                "artistId": 30905,
                "artistName": "TFBOYS",
                "enabled": 1,
                "area": "ML",
                "property": "Combo",
                "enname": "T",
                "aliasName": "",
                "headImg": "http://img4.yytcdn.com/uploads/artists/30905/REE590145400885082F50A9AA3836EEE7.jpg",
                "bigHeadImg": "http://img3.yytcdn.com/uploads/artists/30905/R87EF014540088418F8C3F40FBD6756A1.jpg",
                "regdate": "Aug 26, 2013 5:30:32 PM",
                "totalViews": 0,
                "totalFanNum": 187392,
                "fanMemberCountRank": 99999,
                "videoNum": 2777,
                "videoCountRank": 99999,
                "topicNum": 669
            }
        ]
    }
}



http://ext.yinyuetai.com/main/get-h-mv-info?json=true&videoId=2240030
{
    "message": "",
    "error": false,
    "logined": true,
    "videoInfo": {
        "pageUrl": "http://v.yinyuetai.com/video/2240030",
        "secretKeyUri": "http://api.yinyuetai.com/mv/secret-key",
        "coreVideoInfo": {
            "videoId": 2240030,
            "videoName": "EP5 TFboys 解密万千宠爱为哪般",
            "headImage": "http://img1.yytcdn.com/video/mv/150306/2240030/-M-49908c593a3dfb795f2ec9460eb65f72_120x67.jpg",
            "bigHeadImage": "http://img2.yytcdn.com/video/mv/150213/2240030/-M-ada0645470eaae4623d5f3c1b76da10d_640x360.jpg",
            "videoUrlModels": [
                {
                    "bitrateType": 1,
                    "bitrate": 780,
                    "qualityLevel": "hc",
                    "qualityLevelName": "流畅",
                    "QualityLevelName": "流畅",
                    "videoUrl": "http://hc.yinyuetai.com/uploads/videos/common/406B014B8204FF3E5BB2E5E65CADA7A5.flv?sc=02acdfe0a0d95047&br=780",
                    "fileSize": 30378100,
                    "sha1": "e7073d33951da616d58ce3e128211035a7dd25d2",
                    "md5": "ad969c8c1522299238b89d771c88c064"
                },
                {
                    "bitrateType": 2,
                    "bitrate": 1104,
                    "qualityLevel": "hd",
                    "qualityLevelName": "高清",
                    "QualityLevelName": "高清",
                    "videoUrl": "http://hd.yinyuetai.com/uploads/videos/common/03A0014B8236859E54EC0B2383B65422.flv?sc=a7ea7ae8ff1c391b&br=1104",
                    "fileSize": 43004438,
                    "sha1": "1fa9d5b75cdf2c5d06d93ba3473cdac28c9bc466",
                    "md5": "b74bf605e7cf7cbd8346306f4acd1bb3"
                },
                {
                    "bitrateType": 3,
                    "bitrate": 3160,
                    "qualityLevel": "he",
                    "qualityLevelName": "超清",
                    "QualityLevelName": "超清",
                    "videoUrl": "http://he.yinyuetai.com/uploads/videos/common/1CB9014B823685C37A35531E570A56C6.flv?sc=88b91e1ad0d0eac0&br=3160",
                    "fileSize": 122999938,
                    "sha1": "0445a462224b3e15ca2d4fbd67252c9c3af1425a",
                    "md5": "3f20f38f342e2b809e8d62835fe562c4"
                }
            ],
            "duration": 311,
            "artistIds": "38422,30905",
            "artistNames": "先锋音乐人,TFBOYS",
            "threeD": false,
            "error": false,
            "errorMsg": ""
        }
    }
}

'''
