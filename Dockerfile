FROM andrewosh/binder-base

MAINTAINER Massimo Di Stefano <epiesasha@me.com>

USER root

RUN apt-get -qq update && apt-get install  -y locales
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
      && locale-gen en_US.utf8 \
      && /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

# Add dependency
RUN apt-get update
RUN apt-get install -y graphviz grass-core gdal-bin texlive-latex-base texlive-latex-extra texlive-fonts-extra texlive-fonts-recommended

RUN apt-get install -y rubygems
RUN gem install gist

USER main

# Install requirements for Python 2
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install requirements for Python 3
RUN /home/main/anaconda/envs/python3/bin/pip install -r requirements.txt
RUN /home/main/anaconda/envs/python3/bin/pip install -U ipython
