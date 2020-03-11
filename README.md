# FigureBed

>Flask 个人图床

demo website：http://118.89.237.69:8000

[![Build Status](https://img.shields.io/travis/otale/tale.svg?style=flat-square)](https://github.com/saowu/FigureBed)
[![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg?style=flat-square)](https://github.com/saowu/FigureBed)
[![@saowu on zhihu](https://img.shields.io/badge/zhihu-saowu-red.svg?style=flat-square)](https://www.zhihu.com/people/saowu)
[![GitHub stars](https://img.shields.io/github/stars/saowu/FigureBed.svg?style=flat-square)](https://github.com/saowu/FigureBed/stargazers)

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
confug.py
修改为自己的公网域名用于返回图片链接
修改自己的数据库host:port

docker build -t saowu/figurebed:1.0 .
docker run  -p 8000:8888 -v /home/myDataVolume:/myDataVolume -d saowu/figurebed:1.0
```

#### UI展示

![FireShot Capture 016 - Figure bed - 127.0.0.1.png](https://i.loli.net/2020/03/08/w2DySmnMEWtFNck.png)

![FireShot Capture 015 - Figure bed - 127.0.0.1.png](https://i.loli.net/2020/03/07/q3H1JDFRSwCLm87.png)