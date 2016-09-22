# Dockerfile for for web application service
#
# Installs the web application in "edit" mode so that modifications are
# immediately reflected .
#
# DO NOT USE FOR PRODUCTION

FROM centos:7

RUN yum update -y
RUN yum groupinstall -y 'Development Tools'
RUN yum install -y epel-release
RUN yum install -y nodejs npm magic postgresql-devel python-pip python-devel

# for Pillow
RUN yum install -y libjpeg-devel zlib-devel

RUN npm install -g less && npm install -g bower
RUN echo '{ "allow_root": true }' > /root/.bowerrc

# Install dependencies first so they are cached
COPY ./requirements*.txt /tmp/
RUN pip install --upgrade -r /tmp/requirements-develop.txt

ADD ./ /app
WORKDIR /app
RUN pip install -e .


