# Important Setup Notes
- It is recommended to install the requirements.txt and run the instance inside a virtual environment.
- Use `pip3 install -r requirements.txt` to install Django on a cloud instance.
- To run the Django on a cloud instance, add the public IP to `ALLOWED_HOSTS` list in the file `GREvocabulary/settings.py`

# Where Are We Now?
The server is running on the VM instance now.

# To set up MySQL database (on debian)
First, install mysql-server:  
```
$ sudo apt-get -y install mysql-server
```  
Then set up a virtualenv for python to install later dependencies:
```
```
$ pip3 install virtualenv
```  
```
$ python3 -m virtualenv venv
```  
```
$ source venv/bin/activate
```  
Install mysqlclient for python:  
```
sudo apt -y install default-libmysqlclient-dev
```  
```
pip install mysqlclient
```

Finally, create the db user and database for this project:
```
$ sudo mysql -u root
```  
```
$ create database GRE;
```  
```
GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' IDENTIFIED BY 'pass';
```  
(These are the credentials put in settings.py, so no need to change them for development)  

To migrate the data model defined in models.py to mysql:  
```
$ python manage.py makemigrations GRE
```  
```
$ python manage.py migrate
```
