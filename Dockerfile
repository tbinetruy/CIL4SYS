FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

# Set the working directory to /app
WORKDIR /app

# Install system deps
RUN apt update
RUN apt -y install python-pip git wget

# install anaconda
## Copy the anaconda script
RUN cd /app && wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh
RUN cd /app && chmod +x Anaconda3-5.3.1-Linux-x86_64.sh
RUN cd /app && ./Anaconda3-5.3.1-Linux-x86_64.sh -b

# install Flow and Sumo
RUN  cd /app && git clone https://github.com/flow-project/flow.git  && cd flow && git checkout d1cf643c
RUN ln -s /root/anaconda3/bin/conda /usr/bin
RUN cd /app/flow && conda env create -f environment.yml
RUN echo ". /root/anaconda3/etc/profile.d/conda.sh" > ~/.bashrc
RUN echo "conda activate flow" >> ~/.bashrc
ENV PATH /opt/conda/envs/flow/bin:$PATH
RUN cat ~/.bashrc
RUN source ~/.bashrc && cd /app/flow && conda activate flow && pip install -e . && scripts/setup_sumo_ubuntu1804.sh

# SUMO deps
RUN apt update
RUN apt -y install cmake swig libgtest-dev python-pygame python-scipy autoconf libtool pkg-config libgdal-dev libxerces-c-dev libproj-dev libfox-1.6-dev libxml2-dev libxslt1-dev build-essential curl unzip flex bison python python-dev python3-dev libsm6 libxext6

# Make port 80 available to the world outside this container
EXPOSE 80
