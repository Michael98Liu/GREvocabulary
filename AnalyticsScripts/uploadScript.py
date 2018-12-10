import mysql.connector
from mysql.connector import errorcode
import sys
import glob
import errno

path = '/home/mypc/download/*.html'   
files = glob.glob(path)   
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    try:
        with open(name) as f: # No need to specify 'r': this is the default.
            sys.stdout.write(f.read())
    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.

mydb = mysql.connector.connect(user='user', password='pass',
                              host='localhost',
                              database='GRE')

mycursor = mydb.cursor()



sql = "UPDATE GRE_word SET difficulty=%s WHERE word = %s"
val = (0.6, "test")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")



mycursor.close()

mydb.close()

