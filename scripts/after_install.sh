#!/bin/bash

cd /home/ubuntu/Back_Flask

echo ">>> pip install ----------------------"
pip install -r requirements.txt

echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/Back_Flask

echo ">>> run app with Gunicorn -------------"

venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
