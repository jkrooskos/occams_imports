OCCAMS Imports
==============

Application for data mapping and import from other databases


Rationale
---------

On some occasions, data teams will want to import external data sets into
OCCAMS. This tool will facilitate the pipelines necessary to continuously
integrate external data into a "master" OCCAMS installation.


Goals
-----

Some goals of this product:

  * PID translation
  * External codebook parsing
  * Schema mapping
  * External data upload


System Requirements
-------------------

  * Python 2.7+
  * npm
  * redis
  * PostgreSQL 9.5+


Authentication
++++++++++++++

Because many organizations have their politics of authentication, this app
tries to not force any authentication paradigm on the client and instead
uses `repoze.who` to allow clients to supply their own authentication via
customized-organization-specific plugins.


Development
-----------

This application uses Docker_ to setup a *development environment* with dummy
user accounts. It is recommended you familiarize yourself with some basic
knowledge of how it works.

.. _Docker: https://www.docker.com/

VirtualBox
++++++++++

Install Virtualbox from:

https://www.virtualbox.org/wiki/Downloads

This is required to install boot2docker on containers.


Machine and Compose
+++++++++++++++++++

You will neeed to install Docker Compose_ and Machine_ in order so setup
your environment. To do so, follow the instructions the following instructions
based on your host environment:

- macOS: https://docs.docker.com/docker-for-mac/
- Windows: https://docs.docker.com/docker-for-windows/
- Linux:  https://docs.docker.com/engine/installation/linux/

.. _Compose: https://docs.docker.com/compose/overview/
.. _Machine: https://docs.docker.com/machine/overview/


Installation
++++++++++++

#. Provision a new Docker machine called "imports-develop" by running the
   following command::

      > docker-machine create -d virtualbox imports-develop

#. Point Docker to the development machine::

      > eval $(docker-machine env imports-develop)
      > docker-machine ls
      NAME              ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER    ERRORS
      imports-develop   *        virtualbox   Running   tcp://192.168.99.101:2376           v1.12.1

   Note the asterisk in the "ACTIVE" column.

#. Clone the application and build the containers::

      > git clone https://github.com/razorlabs/occams_imports
      > cd occams_imports
      > docker-compose build

   This will take a moment, so it's a good idea to refill on coffee at this time.

#. Back? Ok, spin up the containers, there will some additional building for
   dependencies, this is normal::

      > docker-compose up -d

#. Build the static assess::

      > docker-compose run app bower install

#. Build the database tables::

      > docker-compose run app occams_initdb develop.ini

#. Build the participant number generator tables::

      > docker-compose run app or_initdb develop.ini

#. Get the IP address of the machine and use it to navigate to http://the.ip.addr.es:3000/ ::

      > docker-machine ip imports-develop


You now should have a working IMPORTS app.


Common Tasks
""""""""""""

How do I add more users?
''''''''''''''''''''''''

Modify the data setting in the `[plugin:dev_users]` section of the develop.ini
file. There is already a test user there for you, so use that a template.


How do I run the tests?
'''''''''''''''''''''''

Create a test user and database to run the tests.

::

    > psql -U occams -h `docker-machine ip imports-develop` -c "CREATE USER test"
    > psql -U occams -h `docker-machine ip imports-develop` -c "CREATE DATABASE test OWNER test"
    > docker-compose run app py.test --db postgresql://test@postgres/test --redis redis://redis/9


How do I check the logs?
''''''''''''''''''''''''

::

    > docker-compose logs -f

How do I access the database?
'''''''''''''''''''''''''''''

Install the Postgres client on the host machine and run::

  > psql -U occams -h `docker-machine ip imports-develop`

How do I restart the application?
'''''''''''''''''''''''''''''''''

::

    > docker-compose restart app


How do I reset the database and start over again?
'''''''''''''''''''''''''''''''''''''''''''''''''

::

    > docker-compose down
    > docker volume rm occams_db
    > docker-compose up -d
    > docker-compose run app occams_initdb develop.ini

