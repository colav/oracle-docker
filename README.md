# Building Docker image (Only for Developer, read using the image below.)

With the  next commands you can build the docker image for oracle database express version.

For the express edition the latest version available is 18.4.0, then please go to  
`
cd build/dockerfiles
`

To build the image run
`
./buildContainerImage.sh -x -v 18.4.0 -t colav/oracle-docker:latest
`
To upload the image to docker hub
`
docker login 
docker push colav/oracle-docker:latest
`


# Using  the dokcer image

We are providing an image already built, you dont have to build the image by your own.

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


## Downloading the official Colav Docker Image
To download the image please run.
`
docker pull colav/oracle-docker:latest
`

## Starting the server (first time, developers only)

the firt step is to create an user oracle in the host with UID = 54321, for that run the next command.
`
useradd -m -d /var/lib/oracle oracle -u 54321
`
in this case I am set the home path to var lib where is suppose to be the SDD disk with the other databases data.

In this step we are going to start the server, this could be a complicated procedure and requires to have the next information clear.

1) The persisten volumen (path) that we are going to provide to oracle to store its files.
2) CPU and RAM that we are going to provide to the container (please see https://docs.docker.com/config/containers/resource_constraints/), this depends of the database we are going to use, and the queries we want to perform.
3) If we are going to load a dump, we need to pass to the container another volume with the path to the dump.

Lets start the server running 
`
docker run --name oracle-server -p 1521:1521 -p 5500:5500 -e ORACLE_PWD=colavudea -v /var/lib/oracle/:/var/lib/oracle colav/oracle-docker
`

call the next command to set the pass
` 
docker exec oracle-server /opt/oracle/setPassword.sh colavudea 
`

## Loading the dump


# Oracle Client

At the point the server should be already running the in container, the next step is to connect the server
using the oracle client. For that we need to install couple to packages like ODBC connector and sqlplus package.

## Installing oracle client packages
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

# Python SDK
https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html


# import

To import all in one shot please run

`
impdp system/colavudea@localhost:1521 directory=colav_dump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0

`

`
impdp UDEA_GR/colavudea@localhost:1521 schemas=UDEA_GR directory=colav_pump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0

impdp UDEA_CV/colavudea@localhost:1521 schemas=UDEA_CV directory=colav_pump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0

impdp UDEA_IN/colavudea@localhost:1521 schemas=UDEA_IN directory=colav_pump_dir dumpfile=UDEA_20210304.dmp logfile=UDEA_20210304.log version=11.2.0.4.0
`

# SQLPLUS from oracle docker client
`
docker run  --network="host"  --rm -ti colav/oracle-docker  bash
sqlplus system/colavudea@//localhost:1521/
sqlplus system/colavudea@//localhost:1521/XE
`



