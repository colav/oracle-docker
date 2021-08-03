<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>


# Oracle Docker Colav
Oracle docker Colav is a package that allows to deploy Oracle express 18.4 in a docker container to work with the Scientic database.
With the package you can deploy your own instance of oracle, load the database dump provided by minciencias and extract the information rquired.

We are providing an image already built, you dont have to build the image by your own.
This is an easy way to deploy a Oracle dabase engine, load the database dump provided by minciencias and extract the information rquired.

## Install docker compose

`
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
`

## Statring with docker compose
The first step is to edit the file config.env setting up there the required parameters.

then run:

`
source config.env
docker-compose up -d 
`

the system takes a while to start, you can check the progress with

`
docker-compose logs 
`

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
docker push colav/oracle-docker:latest
`




## Downloading the official Colav Docker Image
To download the image please run.
`
docker pull colav/oracle-docker:latest
`

## Starting the server (first time, developers only)

1) CPU and RAM that we are going to provide to the container (please see https://docs.docker.com/config/containers/resource_constraints/), this depends of the database we are going to use, and the queries we want to perform.
2) If we are going to load a dump, we need to pass to the container another volume with the path to the dump.

Lets start the server running 
`
docker run --name oracle-server -p 1521:1521 -p 5500:5500 -e ORACLE_PWD=colavudea -v /path_to_dump/:/home/oracle/dump colav/oracle-docker
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
`
docker exec -it #container_id bash
su oracle
cd
`
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
select * from nls_database_parameters where parameter='NLS_CHARACTERSET';
`

output should be like this:

`
SQL> select * from nls_database_parameters where parameter='NLS_CHARACTERSET';

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
impdp system/$PASSWORD@localhost:1521 directory=colav_dump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0

`

`
impdp UDEA_GR/colavudea@localhost:1521 schemas=UDEA_GR directory=colav_pump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0

impdp UDEA_CV/colavudea@localhost:1521 schemas=UDEA_CV directory=colav_pump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0

impdp UDEA_IN/colavudea@localhost:1521 schemas=UDEA_IN directory=colav_pump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0
`



# License
Colav codes under BSD-3-Clause License
Oracle code under UPL

# Links
http://colav.udea.edu.co/