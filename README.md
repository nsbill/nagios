# Plugins Nagios for FreeBSD MPD5 - status a user information

### Добавить в commands.cfg

ADD to /usr/local/etc/nagios/objects/commands.cfg
```
############## MPDUSER COMMAND ##################################

define command {
    command_name    check_usermpd
    command_line /usr/local/bin/python3 /home/scripts/check_usermpd.py $ARG1$
}
```

### Добавить в localhost.cfg или можно создать свой файл
ADD to /usr/local/etc/nagios/objects/localhost.cfg

check_usermpd!012500 -- какого пользователя мониторить.

012500 - это login пользователя 

```
##############  MPD USER SERVICE #########################

define service{
    use                     local-service    ; Inherit values from a template
    host_name               localhost        ; The name of the host the service is associated with
    service_description     MPD User 012500  ; The service description
    check_command           check_usermpd!012500 ; The command used to monitor the service
    normal_check_interval   2                ; Check the service every 5 minutes under normal conditions
    retry_check_interval    1                ; Re-check the service every minute until its final/hard state is determined
}
```
