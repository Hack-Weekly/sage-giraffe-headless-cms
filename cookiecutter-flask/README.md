# cookiecutter-flask

Install steps

Copy the {{cookiecutter.app_name}} directory from:

```
{install directory}\cookiecutter-flask\
```

and paste it in a folder called webapp (or name it whatever you will recognize later as the new project source folder for this webapp)



install steps:  
- create virtual venv  
    a.
    ``` 
    virtualenv -p C:/Python27/python.exe venv
    ```  
    b. 
    ```
    source venv/scripts/activate
    ```  
- install cookie cutter
```
 pip install cookiecutter
```

- run cookiecutter
    
```
    $ cookiecutter webapp/
    full_name [Steven Loria]: ACME Company
    email [sloria1@gmail.com]: support@acmecompany.com
    github_username [sloria]: nf3
    project_name [My Flask App]: My Flask App
    app_name [myflaskapp]: myflaskapp
    db_user [splashbannerwebuser]: websqluser
    db_password [rabbitname]: bugsbunny
    db_hash [867698F5EB930333A757F20691CB53FF161AF063]: *7B7F9C2C8E01F4911B09A37A958CD1448E8E01BF
    db_server [volcanodb.ctiz9sttcvnc.us-west-2.rds.amazonaws.com]: localhost
    core_table_title [Event]: License
    core_table_titlelower [event]: license
    detail_table_title [Post]: ProductKey
    sendgrid_client_id [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]:
    sendgrid_from [Splash Banner<noreply@acmecompany.com>]:
    project_short_description [A flasky app.]:
```    

- ran the scripts/db_create.sql (with the right mysql version uncommented out)
- ran the scripts/set_env.bat from Administrator command prompt
- restarted console (ran env command to see it there)
- $ pip install -r myflaskapp/requirements/dev.txt  (use prod if in prod, myflaskapp is the app_name from above)
- (if dev on windows then you need to install the mysql wheel)
    ○ MySQL_python-1.2.5-cp27-none-win32.whl
    ○ $ pip install MySQL_python-1.2.5-cp27-none-win32.whl
- python manage.py db init
- python manage.py db migrate
- python manage.py db upgrade
- python manage.py CreateRole --role=admin --desc=admin
- python manage.py server
- python manage.py AddRoleToUser --role=admin --user=admin@acmecompany.com
