FROM python:3.7

RUN mkdir -p /project

WORKDIR /project
ADD . /project
RUN [python setup.py develop]

CMD ["python", "setup.py", "test"]
