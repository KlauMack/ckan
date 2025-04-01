=========
Docker Compise CKAN Setup
=========

For development setup or if a different OS is being used for maintaining CKAN site, a Docker Compose setup works great. In this section a brief setup instrunctions will be described.

For a more detailed setup go here: `ckan-docker <https://github.com/ckan/ckan-docker>`_

---------------------
Overview
---------------------
The ``ckan-docker`` repository contains neccessary files for the CKAN site setup.

The repo includes these images:

* CKAN (from official CKAN `ckan-docker <https://github.com/ckan/ckan-docker-base>`_ repo).
* DataPusher: web serivce that automatically downloads, parses and pushes any tabular data files like CSV or Excel from a CKAN site's resources when they are added to the CKAN site, into the CKAN site's DataStore. This makes the data from the resource files available via CKAN's DataStore API.
* PostgreSQL: for storing database files in a named volume.
* Solr: standalone search platform. Enables data search of the CKAN site.
* Redis: for asynchronous background jobs. While CKAN itself doesn't use async, it's required as some CKAN extension do use it.
* NGINX: SSL and Non-SSL endpoints (for production deployment purposes).

---------------------
Installing Docker Compose
---------------------

A ``Docker Engine`` and ``Docker Compose`` installation is needed. Simply, install `Docker Desktop <https://docs.docker.com/desktop/>`_ on the machine, as this will install both tools.

Run ``docker version`` in the terminal of your machine to check if installation was successfull.

---------------------
Install (build and run) CKAN plus dependencies
---------------------
Clone the CKAN Docker Repository
**********
Install ``git`` if not done yet: `git installation <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_

Run the following command to fetch the neccessary CKAN Docker setup files from the repo::

  git clone https://github.com/ckan/ckan-docker
  cd ckan-docker

Create Environment Configuration
**********
Create a ``.env`` file in the root directory::

  cp .env.template .env

Change any configuration values if neeeded.

.. Note ::

  There is a sysadmin user created by default with the values defined in ``CKAN_SYSADMIN_NAME`` and ``CKAN_SYSADMIN_PASSWORD`` (``ckan_admin`` and ``test1234`` by default). These must be changed before running this setup as a public CKAN instance.

Start CKAN Using Docker Compose
**********
Run the following command to build and start CKAN::

  docker compose up -d

If development environemnt is needed, specify the ``docker-compose.dev.yml``. This setup is prefferd for testing, as there might be issues with access to the CKAN site through the back-end (correct NGINX setup is needed with verified SSL certifications):

  docker compose -f .../paht/to/docker-compose.dev.yml up -d

* ``up``: This tells Docker Compose to start and run the containers defined in ``docker-compose.yml`.
* ``-d`` (detached mode): Runs the containers in the background, so they continue running even after you close the terminal.

This will start:

* CKAN
* PostgreSQL + PostGIS (database)
* Solr (search)
* Redis (cache)

Run this command to check if the containers are running (or check through the Docker Desktop app)::

  docker compose ps

Successfull return::

      NAME                       IMAGE                              COMMAND                  SERVICE      CREATED         STATUS                   PORTS
    ckan-docker-ckan-1         ckan-docker-ckan                   "/srv/app/start_ckan…"   ckan         4 minutes ago   Up 3 minutes (healthy)   5000/tcp
    ckan-docker-datapusher-1   ckan/ckan-base-datapusher:0.0.20   "sh -c 'uwsgi --plug…"   datapusher   4 minutes ago   Up 4 minutes (healthy)   8800/tcp
    ckan-docker-db-1           ckan-docker-db                     "docker-entrypoint.s…"   db           4 minutes ago   Up 4 minutes (healthy)
    ckan-docker-nginx-1        ckan-docker-nginx                  "/bin/sh -c 'openssl…"   nginx        4 minutes ago   Up 2 minutes             80/tcp, 0.0.0.0:8443->443/tcp
    ckan-docker-redis-1        redis:6                            "docker-entrypoint.s…"   redis        4 minutes ago   Up 4 minutes (healthy)
    ckan-docker-solr-1         ckan/ckan-solr:2.10-solr9          "docker-entrypoint.s…"   solr         4 minutes ago   Up 4 minutes (healthy)

Access CKAN
**********
If setup was successfull, a CKAN site can be reached at ``http://localhost:8443`` (default port) or ``http://localhost:5000`` (development environment).

The site is ready to be developed, tested and published either through the site's web interface or APIs.
