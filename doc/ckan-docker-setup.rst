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


---------------------
Install (build and run) CKAN plus dependencies
---------------------
