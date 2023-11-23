#!/bin/bash


cd   /home/ubuntu/ssgRecipeBook-flask-backend-main


echo ">>> pip install ----------------------"
pip install -r requirements.txt


echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt


echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/Back_Flask


echo ">>> run app --------------------------"
flask run
