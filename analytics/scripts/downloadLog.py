
import requests
import time

public_ip = "http://35.237.113.206:8000/"
url = public_ip + 'GRE/log'
r = requests.get(url)

if r.status_code == 200:
    filename = "./log/log_{}.log".format( int(time.time()) )
    with open( filename, 'wb' ) as f:
        f.write(r.content)
else:
    raise Exception("Status code is {}.".format(r.status_code))
