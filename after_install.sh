#!/bin/bash


cd   /home/ubuntu/recipe_BE


echo ">>> pip install ----------------------"
pip install -r requirements.txt


echo ">>> remove template files ------------"
rm -rf appspec.yml requirements.txt


echo ">>> change owner to ubuntu -----------"
chown -R ubuntu /home/ubuntu/recipe_BE

echo echo ">>> start server -----------"
flask run --host=0.0.0.0