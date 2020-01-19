#!/bin/sh
pip3 install --user cmake cython gym==0.12.0 pyprind nose2 cached_property joblib dill lz4 ray==0.6.1 setproctitle psutil opencv-python boto3 redis tensorflow imutils lxml
cd ~
mkdir -p fil_rouge
cd fil_rouge
git clone https://github.com/tbinetruy/flow.git
git clone https://github.com/eclipse/sumo.git && cd sumo && git checkout 1d4338ab80
git clone https://github.com/tbinetruy/CIL4SYS.git
