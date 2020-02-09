# Usage: pull the latest code form github and restart the uwsgi server
echo "start to close the uwsgi"
pkill -f uwsgi -9
echo "uwsgi closed"
echo "start to pull latest code from github"
git pull origin master
echo "code pulled!"
echo "start to restart uwsgi"
uwsgi --ini uwsgi.ini
echo "uwsgi started!"
