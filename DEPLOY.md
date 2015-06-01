# Actualizamos los repositorios y el sistema
apt-get update
apt-get upgrade

# Añadimos el usuario 'deploy'
useradd -r -m -s /bin/bash deploy

# Instalamos python stuff
apt-get install python-setuptools
apt-get install python-pip
apt-get install git
pip install virtualenv
pip install virtualenvwrapper


# Iniciamos con el user deploy
su - deploy

# Configuramos virtualenvwrapper
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh

# Nos vamos al home del user deploy
# Clonamos el backend en la carpeta ~/backend
cd ~
git clone https://github.com/kaseOga/gistter backend
cd backend
mkvirtualenv gistter
pip install -r requirements.txt

gunicorn --bind 0.0.0.0:8000 wsgi:app

# Volvemos a root (ctrl + d) e instalamos Nginx
apt-add-repository ppa:nginx/stable
apt-get update
apt-get install nginx

# Configuramos nginx
vim /etc/nginx/conf.d/gistter.conf

	server {
	    listen 80;

	    server_name gistter.me;
	    keepalive_timeout 5;
	    root /home/deploy/frontend;
	    charset utf-8;

	    access_log  /var/log/nginx/access.log;
	    error_log  /var/log/nginx/error.log;

	    location /api {
	        proxy_pass         http://127.0.0.1:8000/;
	        proxy_redirect     off;

	        proxy_set_header   Host             $host;
	        proxy_set_header   X-Real-IP        $remote_addr;
	        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
	    }

	    location / {
	    	try_files $uri /index.html;
	    }
	}

# Comentar línea de la config de nginx por defecto:
# vim /etc/nginx/nginx.conf
# # include /etc/nginx/sites-enabled/*;
# Reiniciar Nginx
service nginx reload

# Volvemos a deploy e iniciamos gunicorn (ahora funciona con nginx)
su - deploy
cd backend
workon gistter
# -D para iniciar como demonio
gunicorn -D wsgi:app --bind 0.0.0.0:8000
# Matar proceso
killall gunicorn
# Reiniciar proceso despues de hacer pull
killall -HUP gunicorn
-----------
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get install -y mongodb-org
sudo service mongod start
-----------
cd ~
git clone https://github.com/kaseOga/gistter_frontend frontend

apt-get install nodejs
sudo ln -s /usr/bin/nodejs /usr/bin/node
apt-get install npm

su - deploy
echo 'prefix = ~/.node' >> ~/.npmrc
export PATH="$PATH:$HOME/.node/bin"
npm install
npm install -g bower
npm install -g gulp
bower install
