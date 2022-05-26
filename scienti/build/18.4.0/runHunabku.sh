#!/bin/bash
cd /tmp
nohup hunabku_server --port $HUNABKU_PORT > /tmp/hunabku.out &
cd -