# TODO
- When click on links, display notes to tell user their status update, for example, "you have learned the word", or "you have made a wrong choice"
- Write user activity log to `log` dir
- display result from user activity analytics on front page
- For words with difficulty greater than 0.5, display as red, otherwise green

# Setup
## Install and Use Virtual Environment
Set up a virtualenv for python to install later dependencies:

```
$ pip3 install virtualenv   
$ python3 -m virtualenv venv  
$ source venv/bin/activate
```  

## Install Dependencies
```
$ pip3 install -r requirements.txt
```
To run the Django on a cloud instance, add the public IP to `ALLOWED_HOSTS` list in the file `GREvocabulary/settings.py`

## To set up MySQL database (on debian)
First, install mysql-server:  
```
$ sudo apt-get -y install mysql-server
```  

Install mysqlclient for python:  
```
$ sudo apt -y install default-libmysqlclient-dev  
```

Finally, create the db user and database for this project:
```
$ sudo mysql -u root  
$ create database GRE;    
$ GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' IDENTIFIED BY 'pass';  
$ exit
```  
(These are the credentials put in settings.py, so no need to change them for development)  

To migrate the data model defined in models.py to mysql:  
```
$ python3 manage.py makemigrations GRE  
$ python3 manage.py migrate
```

## Create an user
A user is created automatically as you run the server. Credentials are as following:

Username: `yair`

Password: `1234`

To create a superuser,
```
$ python3 manage.py createsuperuser --username=nyuad
```

## Populate database with vocabulary
```
$ python3 populate_db.py
```

# Notes
- A good [turorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) on Django from Mozilla.
