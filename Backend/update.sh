# Usage: pull the latest code form github and restart the uwsgi server
echo "start to close the uwsgi"
pkill -f uwsgi -9
echo "activate virtual environment"
source ../orchestral/bin/activate
echo "uwsgi closed"
echo "start to pull latest code from github"
git pull origin master
echo "code pulled!"
echo "update libraries"
pip3 install -r requirements.txt
echo "libraries updated"
echo "refresh database"
python3 manage.py makemigrations
python3 manage.py migrate
echo "database refreshed"
echo "start to restart uwsgi"
uwsgi --ini uwsgi.ini
echo "uwsgi started!"
