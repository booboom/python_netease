# 网易云音乐爬虫
##环境
python3+

##运行
1. git clone https://git.coding.net/booboom/python_netease.git
2. cd py_bao/
3. 修改`url='https://music.163.com/playlist?id=3778678'`的id，改为目标歌单id
4. 修改`res_path = '/Users/admin/Documents/songs/{}.mp3'.format(hot_song_name)`花括号前的歌曲存放路径（ps：要先创建好文件夹）
5. 执行python3 ./163.py
