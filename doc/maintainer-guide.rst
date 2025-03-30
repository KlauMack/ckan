=========
Maintainer's guide
=========
This documentation sections describes how to setup and maintain a CKAN site, including installing, upgrading and configuring
CKAN and its features and extensions.

---------------------
Installing CKAN
---------------------
.. note::
  The currently supported CKAN version is ``CKAN 2.11.2``. Security and performance fixes are also provided for ``CKAN 2.10.7``.

**CKAN 2.10** supports ``Python 3.7`` to ``Python 3.10``.

There are three ways to install CKAN:

#. `Package install <https://docs.ckan.org/en/2.11/maintaining/installing/install-from-package.html>`_ (Easiest)
#. `Source install <https://docs.ckan.org/en/2.11/maintaining/installing/install-from-source.html>`_ (For development, for multiple CKAN sites on one server or source OS is not Ubuntu)
#. `Docker Compose install <https://github.com/ckan/ckan-docker>`_ (Flexible, for checking CKAN and Docker compatibility)

---------------------
 Database Management
---------------------
Initialization
============================
Before running CKAN for the first time, you need to run ``db init`` to initialize your database::

  ckan -c /etc/ckan/default/ckan.ini db init

If this is not done, an error message will appear::

  503 Service Unavailable: This site is currently off-line. Database is not initialised.

Cleaning
============================
**Warning!** This will delete all data from your CKAN database!

To start a database from scratch, everything in it can be deleted like so::

  ckan -c /etc/ckan/default/ckan.ini db clean

After cleaning the database, you need to either initialize it or import a previously created dump.

Import and Export
============================
Dumping and Loading databases to/from a file
**********
These examples use **PostgreSQL** and its command line tools, like ``pg_dump`` and ``pg_restore``.

To dump and restore a database and its content to/from a file::

  sudo -u postgres pg_dump --format=custom -d ckan_default > ckan.dump

**Warning!** The exported file is a complete backup of the database, and includes ``API keys`` and other user data which may be
regarded as private.

To restore it again::

  ckan -c /etc/ckan/default/ckan.ini db clean
  sudo -u postgres pg_restore --clean --if-exists -d ckan_default < ckan.dump

If a dump from an older version of CKAN is being imported, you must upgrade the database schema after the import (next section).

Once the import (and a potential upgrade) is complete, rebuild the search index::

  ckan -c /etc/ckan/default/ckan.ini search-index rebuild

Exporting Datasets to JSON Lines
**********
To export all of CKAN site’s datasets from the database to a **JSON Lines** file use ``ckanapi``::

  ckanapi dump datasets -c /etc/ckan/default/ckan.ini --all -O my_datasets.jsonl

This is useful to create a simple public listing of the datasets, with no user information.

Import and Export
============================
**Warning!** Create a backup of the databae before upgrading. To avoid problems during the database upgrade, comment out any plugins that are enabled in the ``ini`` file. Re-enable them after the upgrade.

If upgrading to a new CKAN major release, update the CKAN database’s schema using the ``ckan db upgrade`` command::

  ckan -c /etc/ckan/default/ckan.ini db upgrade

This command applies all CKAN core migrations and all unapplied migrations from enabled plugins. Use:

* ``--skip-core`` flag to run only core migration,
* ``--skip-plugins`` flag to run only migrations from enabled plugins.

---------------------
Command Line Interface (CLI)
---------------------
.. Note::

  From **CKAN 2.9** onwards the CKAN configuration file is named ``ckan.ini`` (previously named: ``production.ini`` and ``development.ini``).

  The ``paster`` command used for common CKAN administration tasks has been replacedwith the ``ckan`` command.

It's best to activate the CKAN virtualenv before running the ``ckan`` command, as this will allow the command to be run from any location within the host environment.  Otherwise, a full path to the virtualenv ckan script has to be provided with the ckan command.

The general form of the ``ckan`` command::

  ckan --config=/etc/ckan/default/ckan.ini command

* ``--config`` or ``-c`` - points to the CKAN config file, usually named ``ckan.ini``

.. Note::

  To void using the configurtion flag in the ckan command, you can specify the config file location, like so::

    export CKAN_INI=/etc/ckan/default/ckan.ini

For a list of all available commands, see `CKAN Commands Reference <https://docs.ckan.org/en/2.11/maintaining/cli.html#ckan-commands-reference>`_
