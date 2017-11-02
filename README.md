# Plugins Nagios MPD5 - status a user information

### Добавить в commands.cfg

ADD to /usr/local/etc/nagios/objects/commands.cfg

############## MPDUSER COMMAND ##################################

\ndefine command {
\n\t command_name    check_usermpd
\n\t command_line /usr/local/bin/python3 /home/scripts/check_usermpd.py $ARG1$
\n\t}


### Добавить в localhost.cfg или можно создать свой файл
ADD to /usr/local/etc/nagios/objects/localhost.cfg

check_usermpd!012500 -- какого пользователя мониторить

##############  MPD USER SERVICE #########################
\ndefine service{
\n\t use                     local-service    ; Inherit values from a template
\n\t host_name               localhost        ; The name of the host the service is associated with
\n\t service_description     MPD User 012500  ; The service description
\n\t check_command           check_usermpd!012500 ; The command used to monitor the service
\n\t normal_check_interval   2                ; Check the service every 5 minutes under normal conditions
\n\t retry_check_interval    1                ; Re-check the service every minute until its final/hard state is determined
\n\t }

