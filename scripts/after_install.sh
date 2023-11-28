#!/bin/bash

cd   /home/ubuntu/recipe_BE


echo ">>> pip install ----------------------"
pip install -r requirements.txt


echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/recipe_BE

sudo chown -R ubuntu:ubuntu /home/ubuntu/recipe_BE/

touch /home/ubuntu/recipe_BE/log.txt

echo ">>> set env --------------------------"
export FLASK_APP=app
export REDIS_HOST=redis
export APP_CONFIG_FILE=/home/ubuntu/recipe_BE/config/production.py
export DB_USER=admin
export DB_PASSWORD=password
export DB_HOST=hwan-db.cwjlce28o2o9.ap-southeast-1.rds.amazonaws.com
export DB_PORT=3306
export DB_NAME=recipe
export SECRET_KEY=b'X2t\x05\xf5\xcb\xc1\xa5`\xd6"\xfb \x0c\x14\xb5'
export JWT_SECRET_KEY=b'\x10\xc8\xf9S\x1c&\x9fAD\x82\xf5\xa1\xdbx\xea>'

cd   /home/ubuntu/recipe_BE

echo ">>> start server ---------------------"
nohup flask run --host=0.0.0.0 > log.txt 2>&1 &
