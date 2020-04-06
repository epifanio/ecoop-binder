FROM jupyter/base-notebook:17aba6048f44
ENV TAG="17aba6048f44"
COPY binder/index.ipynb .

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

RUN apt-get install -y git

RUN git clone https://github.com/epifanio/ecoop-binder && cd ecoop-binder && pip install -r requirements.txt && python setup.py install && cd .. && rm -rf ecoop-binder
COPY ESR_Test_executed.ipynb .



RUN chmod -R 777 /home/jovyan && chown -R jovyan /home/jovyan

USER jovyan
