## Mozevent (mozilla events)

This django app allows you to set up an event system for you meetings, talks, parties...

### Features

* Upcoming and past events listing.
* Event registration.
* Scheduled registration time range.
* Places limit.
* Places queue and auto handling/emailing new available places.
* Automatic emails for confirmation and declination.
* Attendees check-in feature for the day of the event.
* Twitter, flickr and google maps integration.
* Basic global stats.
* Mozilla sandstone theme.
* Full localization support.

You can see it working here:

https://eventos.mozilla-hispano.org

### License

Check ``LICENSE`` file.

### Installation

#### Requirements

You just need ``python`` and ``git`` installed on your system.

It's recomendable too, use a virtual environment for python (``virtualenv`` or similars).

#### Get the code and requirements

Clone this repo

    $ git clone git@github.com:mozillahispano/mozevents.git
    
You should be using a ``virtualenv`` for this project, and ``pip``,``libmysqlclient-dev``, ``python-dev``, and ``libssl-dev`` are needed for install some packages from pip.

    $ sudo aptitude install pip libmysqlclient-dev python-dev libssl-dev
    $ sudo pip install virtualenv

Create and enable the ``virtualenv``, project is at ``/var/lib/mozevents``:

    $ cd /var/lib/
    $ virtualenv mozevents
    $ cd mozevents
    $ source bin/activate

You'll need to install python packages used in this project. These are in ``requirements.txt``.
The best way to install these packages is using ``pip``:

    $ pip install -r requirements.txt

#### Configure your local site

Create and fill your local settings (database, email, url and recaptcha keys)

    $ cp mozevents/settings_local.py.example mozevents/settings_local.py
    $ vim mozevents/settings_local.py

Fill the initial database

    $ python manage.py syncdb

Collect the static files (not required for local development with ``DEBUG=True``)

    $ python manage.py collectstatic

Run the testserver

    $ python manage.py runserver

#### Run tests

To run tests

    $ python manage.py test

#### Nginx

We need ``nginx``, ``uwsgi`` and ``uwsgi-plugin-python`` packages.

Create a virtualhost at ``/etc/nginx/sites-enabled/mozevents``

```
server {
  listen  80;
  server_name eventos.mozilla-hispano.org;
  access_log /var/log/nginx/eventos.mozilla-hispano.org.access.log;
  error_log /var/log/nginx/eventos.mozilla-hispano.org.error.log;

    location / {
        uwsgi_pass unix:///tmp/eventos.mozilla-hispano.org.sock;
        include uwsgi_params;
    }
    
    
    location /media/ {
        alias /var/www/mozevents/public/media/;
    }
    
    
    location /static/ {
        alias /var/www/mozevents/static/;
    }
}
```

Create uwsgi app at ``/etc/uwsgi/apps-enabled/eventos.mozilla-hispano.org.ini``

```
[uwsgi]
vhost = true
plugins = python
socket = /tmp/eventos.mozilla-hispano.org.sock
master = true
enable-threads = true
processes = 2
wsgi-file = /var/www/mozevents/public/wsgi_handler.py
virtualenv = /var/www/mozevents/
chdir = /var/www/mozevents
```

Restart services:

    $ sudo service nginx restart
    $ sudo service uwsgi restart
