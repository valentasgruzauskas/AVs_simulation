FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
MAINTAINER nejumi <dr_jingles@mac.com>

##############################################################################
# Miniconda python
##############################################################################
RUN apt-get update && \
    apt-get install -y wget bzip2 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh && \
    /bin/bash Miniconda3-py37_4.8.3-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-py37_4.8.3-Linux-x86_64.sh

ENV PATH /opt/conda/bin:$PATH
RUN pip install --upgrade pip

RUN apt-get update && \
    # Miniconda's build of gcc is way out of date; monkey-patch some linking problems that affect
    # packages like xgboost and Shapely
    rm /opt/conda/lib/libstdc++* && rm /opt/conda/lib/libgomp.* && \
    ln -s /usr/lib/x86_64-linux-gnu/libgomp.so.1 /opt/conda/lib/libgomp.so.1 && \
    ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /opt/conda/lib/libstdc++.so.6

##############################################################################
# Dependecies
##############################################################################

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /home

EXPOSE 8888

#CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]