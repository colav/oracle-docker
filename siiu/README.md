<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# Oracle Docker Colav

Oracle docker Colav is a package that allows to deploy Oracle express 18.4 in a docker container to work with the SIIU database.
With the package you can deploy your own instance of oracle, load the database dump provided by minciencias and extract the information rquired.

We are providing an image already built, you dont have to build the image by your own.
This is an easy way to deploy a Oracle dabase engine, load the database dump provided by minciencias and extract the information rquired.

## Install Docker

1) `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
2) `sudo chmod +x /usr/local/bin/docker-compose`
3) Follow the steps at [https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user] to work with the docker command as a non-root-user

## Statring with docker compose

1) Edit the config.env file, then use `source config.env`, if you do not do this, then docker will create a process where the variables inside the config.env do not exist.
2) Execute `docker-compose up -d`
3) Optional: you can see the progress with `docker-compose logs`

# ADVANCED FOR DEVELOPERS

## Building Docker image (Only for Developer, read using the image below.)

With the  next commands you can build the docker image for oracle database express version.

For the express edition the latest version available is 18.4.0, then please go to  
`
cd build/
`

To build the image run
`
./buildContainerImage.sh 
`
To upload the image to docker hub
`
docker login 
docker push colav/siiu-oracle-docker:latest
`

## Downloading the official Colav Docker Image
To download the image please run.
`
docker pull colav/siiu-oracle-docker:latest
`

## Starting the server (first time, developers only)

1) CPU and RAM that we are going to provide to the container (please see https://docs.docker.com/config/containers/resource_constraints/), this depends of the database we are going to use, and the queries we want to perform.
2) If we are going to load a dump, we need to pass to the container another volume with the path to the dump.

Lets start the server running 
`
docker run --name oracle-server -p 1521:1521 -e ORACLE_PWD=colavudea -v /path_to_dump/:/home/oracle/dump colav/siiu-oracle-docker
`

call the next command to set the pass

` 
docker exec oracle-server /opt/oracle/setPassword.sh colavudea 
`


## Oracle Client

At the point the server should be already running the in container, the next step is to connect the server
using the oracle client. For that we need to install couple to packages like ODBC connector and sqlplus package.

### Installing oracle client packages
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

Run like root user:

`
apt install libaio-dev alien
cd /tmp/
wget https://download.oracle.com/otn_software/linux/instantclient/211000/oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm

alien oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm 
dpkg -i oracle-instantclient-basic_21.1.0.0.0-2_amd64.deb
https://download.oracle.com/otn_software/linux/instantclient/211000/oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm
cd /usr/lib/oracle/21/client64/lib/
ldconfig
`
check the example in the notebook folder.


### Python SDK
https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html

Instructions here are to work in your default user name in you local computer on debian/ubutu system
`
pip3 install cx_oracle
`


# CHECK SYSTEM CONFIG

start the bash session inside the container

1) `docker exec -it #container_id bash`
2) `su oracle`

Checking the locale config

`
[oracle@dd60c9eafff7 ~]$ locale
LANG=es_CO.UTF-8
LC_CTYPE="es_CO.UTF-8"
LC_NUMERIC="es_CO.UTF-8"
LC_TIME="es_CO.UTF-8"
LC_COLLATE="es_CO.UTF-8"
LC_MONETARY="es_CO.UTF-8"
LC_MESSAGES="es_CO.UTF-8"
LC_PAPER="es_CO.UTF-8"
LC_NAME="es_CO.UTF-8"
LC_ADDRESS="es_CO.UTF-8"
LC_TELEPHONE="es_CO.UTF-8"
LC_MEASUREMENT="es_CO.UTF-8"
LC_IDENTIFICATION="es_CO.UTF-8"
LC_ALL=es_CO.UTF-8
`

Checking the NLS_LANG

`
[oracle@dd60c9eafff7 ~]$ echo $NLS_LANG
SPANISH_COLOMBIA.WE8MSWIN1252
`

checking the charset on the DB

`
sqlplus / as sysdba
`

then run the next SQL command

`
SQL> select * from nls_database_parameters where parameter='NLS_CHARACTERSET';
`

output should be like this:

`
PARAMETER
--------------------------------------------------------------------------------
VALUE
----------------------------------------------------------------
NLS_CHARACTERSET
WE8MSWIN1252
`


# Import manually the dump

To import all in one shot please run inside the container

`
impdp system/$PASSWORD@localhost:1521 directory=colav_dump_dir dumpfile=expdp_bupp_12_mayo2022.dmp logfile=expdp_bupp_12_mayo2022.log version=11.2.0.4.0
`

## Some errors
in case of error

`
[WARNING] ORA-00821: Specified value of sga_target 1536M is too small, needs to be at least 4304M
`

it is because free oracle only allows 1 cpu, you have to set cpu 1 in docker compose files or calling docker from command line.

`
[WARNING] ORA-12954: The request exceeds the maximum allowed database size of 12 GB
`

This error gets triggered for free oracle, you can add to the import comamnd:
`
tables="TABLE_SPACE_NAME.TABLE_NAME","TABLE_SPACE_NAME.TABLE_NAME", this includes those tables only or
you can exclude tables that occupy too much space with exclude=table:\"IN \'TABLE_NAME\'\",
`, if you use either, then you must also include data_options=skip_constraint_errors


# Private docker image
https://github.com/oracle/docker-images/issues/1527

# License
Colav codes under BSD-3-Clause License
Oracle code under UPL

# Links
http://colav.udea.edu.co/
