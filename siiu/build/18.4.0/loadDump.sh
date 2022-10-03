#!/bin/bash

#(name) -> Creates Table Space
createTablespace(){
name=$1
extension="_01.dbf"
dbf_file="$name$extension"
sqlplus -s / as sysdba << EOF
create tablespace $name
default storage (
initial     40960
next        40960
minextents  1
maxextents  unlimited
pctincrease 0
)
permanent
datafile
'$dbf_file' size 50m
autoextend on next 50m maxsize 14000m;
exit;
EOF
}

#(user, password, tablespace) -> Creates User
createUser(){
new_user=$1
password=$2
tablespace=$3
sqlplus -s / as sysdba << EOF
alter session set "_ORACLE_SCRIPT"=true;  
create user $new_user
identified by $password
default tablespace $tablespace
temporary tablespace temp 
profile default;
grant connect to $new_user; 
grant resource to $new_user; 
grant create any view to $new_user; 
grant debug connect session to $new_user; 
grant unlimited tablespace to $new_user;
grant create session, create table, create procedure, exp_full_database, imp_full_database to $new_user;
GRANT IMP_FULL_DATABASE to $new_user;
ALTER USER $new_user DEFAULT ROLE ALL;
alter user $new_user identified by $new_user quota unlimited on indx; 
grant read, write on directory siiu_pump_dir to $new_user;
exit;
EOF
}

sqlplus -s / as sysdba << EOF
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
'idx_01.dbf' size 50m
autoextend on next 50m maxsize 4000m
;
create directory siiu_pump_dir as '/tmp/dump';

exit;
EOF

IFS=', ' read -r -a array <<< "$SIIU_TABLESPACES"
for tablespace in "${array[@]}"
do
    echo "Creating Table Space: $tablespace"
    createTablespace $tablespace
done

IFS=', ' read -r -a array <<< "$SIIU_USERS"
for user in "${array[@]}"
do
    echo "Creating User: $user"
    createUser $user $ORACLE_PWD "BUPP"
done

IFS=', ' read -r -a array <<< "$DUMP_FILES"
for dump_file in "${array[@]}"
do
    echo "Loading dump file $dump_file"
    impdp system/$ORACLE_PWD@localhost:1521 exclude=table:\"IN \'SIIU_ARCHIVO_ADJUNTO\'\"  \
    directory=siiu_pump_dir dumpfile=$dump_file data_options=skip_constraint_errors version=11.2.0.4.0
done



