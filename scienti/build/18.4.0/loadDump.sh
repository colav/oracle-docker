#!/bin/bash

sqlplus -s / as sysdba << EOF
create tablespace datos 
default storage (
initial     40960
next        40960
minextents  1
maxextents  unlimited
pctincrease 0
)
permanent
datafile
'datos_01.dbf' size 50m
autoextend on next 50m maxsize 4000m;

create tablespace indx
default storage (
initial     40960
next        40960
minextents  1
maxextents  unlimited
pctincrease 0
)
permanent
datafile
'indices_01.dbf' size 50m
autoextend on next 50m maxsize 4000m
;

create directory colav_pump_dir as '/tmp/dump';

alter session set "_ORACLE_SCRIPT"=true;  
create user $GRUPLAC_USER 
 identified by $ORACLE_PWD
 default tablespace datos 
 temporary tablespace temp 
 profile default; 
grant connect to $GRUPLAC_USER; 
grant resource to $GRUPLAC_USER; 
grant create any view to $GRUPLAC_USER; 
grant debug connect session to $GRUPLAC_USER; 
grant unlimited tablespace to $GRUPLAC_USER;
grant create session, create table, create procedure, exp_full_database, imp_full_database to $GRUPLAC_USER;
GRANT IMP_FULL_DATABASE to $GRUPLAC_USER;
ALTER USER $GRUPLAC_USER DEFAULT ROLE ALL;
alter user $GRUPLAC_USER identified by $GRUPLAC_USER quota unlimited on indx; 
grant read, write on directory colav_pump_dir to $GRUPLAC_USER;


alter session set "_ORACLE_SCRIPT"=true;  
create user $CVLAC_USER 
 identified by $ORACLE_PWD
 default tablespace datos 
 temporary tablespace temp 
 profile default; 
grant connect to $CVLAC_USER; 
grant resource to $CVLAC_USER; 
grant create any view to $CVLAC_USER; 
grant debug connect session to $CVLAC_USER; 
grant unlimited tablespace to $CVLAC_USER;
grant create session, create table, create procedure, exp_full_database, imp_full_database to $CVLAC_USER;
GRANT IMP_FULL_DATABASE to $CVLAC_USER;
ALTER USER $CVLAC_USER DEFAULT ROLE ALL;
alter user $CVLAC_USER identified by $CVLAC_USER quota unlimited on indx; 
grant read, write on directory colav_pump_dir to $CVLAC_USER;


alter session set "_ORACLE_SCRIPT"=true;  
create user $INSTITULAC_USER 
 identified by $ORACLE_PWD
 default tablespace datos 
 temporary tablespace temp 
 profile default; 
grant connect to $INSTITULAC_USER; 
grant resource to $INSTITULAC_USER; 
grant create any view to $INSTITULAC_USER; 
grant debug connect session to $INSTITULAC_USER; 
grant unlimited tablespace to $INSTITULAC_USER;
grant create session, create table, create procedure, exp_full_database, imp_full_database to $INSTITULAC_USER;
GRANT IMP_FULL_DATABASE to $INSTITULAC_USER;
ALTER USER $INSTITULAC_USER DEFAULT ROLE ALL;
alter user $INSTITULAC_USER identified by $INSTITULAC_USER quota unlimited on indx; 
grant read, write on directory colav_pump_dir to $INSTITULAC_USER;

alter session set "_ORACLE_SCRIPT"=true;  
create user CIENCIA 
 identified by $ORACLE_PWD
 default tablespace datos 
 temporary tablespace temp 
 profile default; 
grant connect to CIENCIA; 
grant resource to CIENCIA; 
grant create any view to CIENCIA; 
grant debug connect session to CIENCIA; 
grant unlimited tablespace to CIENCIA;
grant create session, create table, create procedure, exp_full_database, imp_full_database to CIENCIA;
GRANT IMP_FULL_DATABASE to CIENCIA;
ALTER USER CIENCIA DEFAULT ROLE ALL;
alter user CIENCIA identified by CIENCIA quota unlimited on indx; 
grant read, write on directory colav_pump_dir to CIENCIA;


exit;
EOF
IFS=', ' read -r -a array <<< "$DUMP_FILES"
for element in "${array[@]}"
do
    echo "Loading dump file $element"
    impdp system/$ORACLE_PWD@localhost:1521 directory=colav_pump_dir dumpfile=$element version=11.2.0.4.0 
    #logfile=$DUMP_LOG_FILE
done

echo "Finished loading dumps"
