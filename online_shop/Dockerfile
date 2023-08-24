FROM python:3.10
LABEL Maintainer="as.faraso.97@gmail.com"
LABEL Owner="kiana alamy"
LABEL version="v1"
WORKDIR /djangoonlineshop
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]