FROM andrewosh/binder-base

MAINTAINER Massimo Di Stefano <epiesasha@me.com>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -y graphviz grass=core gdal-bin texlive-latex-base texlive-latex-extra texlive-fonts-extra texlive-fonts-recommended

USER main

# Install requirements for Python 2
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install requirements for Python 3
RUN /home/main/anaconda/envs/python3/bin/pip install -r requirements.txt