CREATE DATABASE {{cookiecutter.app_name}};

#v5.7
#CREATE USER `{{cookiecutter.db_user}}`@`%` IDENTIFIED WITH mysql_native_password as '*{{cookiecutter.db_hash}}';

#v5.6
#CREATE USER `{{cookiecutter.db_user}}`@`%` IDENTIFIED BY PASSWORD '*{{cookiecutter.db_hash}}';

GRANT USAGE ON *.* TO `{{cookiecutter.db_user}}`@`%`;

GRANT SELECT, INSERT, DELETE, UPDATE, ALTER, CREATE, INDEX, REFERENCES ON {{cookiecutter.app_name}}.* TO `{{cookiecutter.db_user}}`@`%`;

FLUSH PRIVILEGES;

#manual override incase the other version create missed
#SET password FOR `{{cookiecutter.db_user}}`@`%` = '*{{cookiecutter.db_hash}}'


