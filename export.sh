#!/bin/sh

python export.py

./fix_time.sh

cd docs
python3 ../scripts/index.py .
touch .nojekyll
cd ..

python3 md_wrapper.py

git add .
git commit -m "update"
git push
