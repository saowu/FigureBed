FROM python:3.7
VOLUME /myDataVolume
COPY requirements.txt ./
RUN pip install  --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple   -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]