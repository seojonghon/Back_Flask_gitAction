#!/bin/bash

# 프로젝트 디렉터리로 이동
cd /home/ubuntu/Back_Flask

echo ">>> pip install ----------------------"
pip install -r requirements.txt

echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/Back_Flask

echo ">>> run app --------------------------"
chmod +x app.sh
./app.sh
