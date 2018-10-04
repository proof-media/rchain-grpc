FROM python:3.7

RUN mkdir -p /project

WORKDIR /project
ADD . /project
RUN ["python", "setup.py", "develop"]
RUN ["pip", "install", "-r", "requirements_dev.txt"]
CMD ["python", "setup.py", "test"]
