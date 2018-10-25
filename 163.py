#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.error
import urllib.parse
import json
import threading
from time import sleep
import os

json_path = 'data.json'

def get_all_hotSong():     #获取歌单所有歌曲名称和id
    # url='http://music.163.com/discover/toplist?id=3778678'    #网易云云音乐热歌榜url
    url='https://music.163.com/playlist?id=3778678'           #播放列表url z/mpi 2476005642 like 536254974
    header={    #请求头部
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request=urllib.request.Request(url=url, headers=header)
    html=urllib.request.urlopen(request).read().decode('utf8')   #打开url
    html=str(html)     #转换成str
    pat1=r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>'  #进行第一次筛选的正则表达式
    result=re.compile(pat1).findall(html)     #用正则表达式进行筛选
    result=result[0]     #获取tuple的第一个元素

    pat2=r'<li><a href="/song\?id=\d*?">(.*?)</a></li>' #进行歌名筛选的正则表达式
    pat3=r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'  #进行歌ID筛选的正则表达式
    hot_song_name=re.compile(pat2).findall(result)    #获取所有歌单的歌曲名称
    hot_song_id=re.compile(pat3).findall(result)    #获取所有歌单歌曲对应的Id

    return hot_song_name,hot_song_id

def download_song(hot_song_name,hot_song_id):
    singer_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(hot_song_id)
    res_path = '/Users/admin/Documents/songs/{}.mp3'.format(hot_song_name)
    if (os.path.exists(res_path)):
        print('{}---已存在！'.format(hot_song_name))
        return
    print('歌曲：{}'.format(hot_song_name),'ID:{}'.format(hot_song_id),'正在下载...')
    urllib.request.urlretrieve(singer_url,f_path) # 保存到本地目录    
    print('{}---下载完成'.format(hot_song_name))
    song_item = {'name':hot_song_name,'id':hot_song_id,'url':'http://music.163.com/song/media/outer/url?id={}.mp3'.format(hot_song_id)}
    songs.append(song_item)
    sleep(1)

hot_song_name,hot_song_id=get_all_hotSong()  #获取歌单所有歌曲名称和id
songs=[]
threads = []
files = range(len(hot_song_name))
num=0

while num < len(hot_song_name):    #下载歌单中的所有歌
    t = threading.Thread(target=download_song,args=(hot_song_name[num],hot_song_id[num]))
    threads.append(t)
    num+=1

runFiles = [];
for i in files:
    runFiles.append(i)
    if(len(runFiles)>=10):
        for i in runFiles:
            threads[i].start() 
        for i in runFiles:
            threads[i].join()
        runFiles=[]

if(len(runFiles)!=0):
    for i in runFiles:
        threads[i].start() 
    for i in runFiles:
        threads[i].join()

# 格式化数据，保存在json文件中
with open(json_path,'w') as dump_f:
    json.dump(songs,dump_f,ensure_ascii=False)


print('执行完毕')