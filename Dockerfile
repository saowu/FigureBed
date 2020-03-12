
FROM python:3.7

# 设置工作区
RUN mkdir -p /home/FigureBed
WORKDIR /home/FigureBed
# 设置数据卷
VOLUME /home/myDataVolume

COPY requirements.txt ./
RUN pip3 install  --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple   -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
