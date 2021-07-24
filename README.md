# Building Docker image (Only for Developer, read using the image below.)

With the  next commands you can build the docker image for oracle database express version.

For the express edition the laest version available is 18.4.0, then please go to  
`
cd build/dockerfiles
`

To build the image run
`
./buildContainerImage.sh -x -v 18.4.0 -t colav/oracle-docker:latest
`

# Using  the dokcer image

We are providing an image already built, you dont have to build the image by your own.

## Downloading the official Colav Docker Image
To download the image please run.
`
docker pull colav/oracle-docker:latest
`

## Starting the server

In this step we are going to start the server, this could be a complicated procedure and requires to have the next information clear.

1) The persisten volumen (path) that we are going to provide to oracle to store its files.
2) CPU and RAM that we are going to provide to the container (please see https://docs.docker.com/config/containers/resource_constraints/), this depends of the database we are going to use, and the queries we want to perform.
3) If we are going to load a dump, we need to pass to the container another volume with the path to the dump.


## Loading the dump


# Oracle Client

At the point the server should be already running the in container, the next step is to connect the server
using the oracle client. For that we need to install couple to packages like ODBC connector and sqlplus package.

## Installing oracle client packages
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

# Python SDK
https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html





