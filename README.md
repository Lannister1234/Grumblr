To turn in homework 5, create files (and subdirectories if needed) in this directory, add and commit those files to your cloned repository, and push your commit to your bare repository on GitHub.

Add any general notes or instructions for the TAs to this README file. The TAs will read this file before evaluating your work.

The resources I use:
1. https://www.digitalocean.com/community/tutorials/how-to-use-the-django-one-click-install-image-for-ubuntu-14-04
2. https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

The url for running my application: 
http://178.128.155.171:8888/

I add three sample users in database for testing, they are: <br/>
User1: Username: mm           password: 123456 <br/>
User2: Username: lulu         password: 123456 <br/>
User3: Username: nan11111111  password: 123456 <br/>

Some configurations:
1. Change the email setting in settings.py to allow sending real emails.
2. Change the database setting in settings.py to use mysql as our database.
3. Install uwsgi and nginx, start nginx with sudo /etc/init.d/nginx start
4. The configuration files are uwsgi_params and grumblr_nginx.conf
4. Deploying static files with python manage.py collectstatic
5. Migrate: python manage.py makemigrations, python manage.py migrate
6. Run uWSGI: uwsgi --socket :8006 --module webapps.wsgi
