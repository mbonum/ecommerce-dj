FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /clvm
COPY requirements.txt ./
RUN pip install -r requirements.txt