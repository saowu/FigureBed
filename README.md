# FigureBed

>Flask 个人图床

demo website：http://esc.saowu.top:8000

[![GitHub issues](https://img.shields.io/github/issues/saowu/FigureBed?style=for-the-badge)](https://github.com/saowu/FigureBed/issues)
[![GitHub forks](https://img.shields.io/github/forks/saowu/FigureBed?style=for-the-badge)](https://github.com/saowu/FigureBed/network)
[![GitHub license](https://img.shields.io/github/license/saowu/FigureBed?style=for-the-badge)](https://github.com/saowu/FigureBed/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/saowu/FigureBed?style=for-the-badge)](https://github.com/saowu/FigureBed/stargazers)

#### 功能支持
```
1.支持多文件上传（set max=5）
2.支持导出csv上传路径
3.支持返回多种链接格式 （link, markdown, html, bbcode，removal）
4.可以通过removal链接自行删除图片文件
5.使用mysql数据库
6.支持拖动上传
```
#### Docker部署
```
#构建flask+gunicorn+gevent(+nginx)
$docker build -t saowu/figurebed:1.0 .
$docker run  -p 8000:8888 -v /home/myDataVolume:/home/myDataVolume -d saowu/figurebed:1.0

#构建nginx(cd /nginx)
$docker build -t saowu/nginx:1.0 .
$docker run --name nginx1 -p 80:80 -d saowu/nginx:1.0
```
#### UI展示
![FireShot Capture 017 - Figure bed - 127.0.0.1.png](https://i.loli.net/2020/03/13/raDBuAvLoT9Rw6I.png)

![FireShot Capture 018 - Figure bed - 127.0.0.1.png](https://i.loli.net/2020/03/13/S6ZJDbieEfmvaRX.png)
