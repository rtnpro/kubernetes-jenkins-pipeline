FROM centos:latest

RUN yum update -y && \
    yum install -y python-flask && \
    yum clean all

WORKDIR /src

ADD app.py /src

EXPOSE 5000

ENV RELEASE master
ENV HOST 0.0.0.0
ENV PORT 5000

CMD python app.py
