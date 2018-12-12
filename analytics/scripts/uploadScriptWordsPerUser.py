import mysql.connector
from mysql.connector import errorcode
import sys
import glob
import errno

mydb = mysql.connector.connect(user='user', password='pass',
                               host='35.243.212.94', database='GRE')
mycursor = mydb.cursor()

path = 'output/wordsPerUser/*'   
files = glob.glob(path)   
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    try:
        with open(name) as f: # No need to specify 'r': this is the default.
            content = f.readlines()
            for x in content:
                line = x.strip().split(" ")
                user = line[0]
                wordsLearnt = line[1]
                #print(user, " : ", wordsLearnt)
                sql = "UPDATE GRE_profile SET learnt_count=%s WHERE user = %s"
                val = (int(wordsLearnt), user)
                mycursor.execute(sql, val)

    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.


mydb.commit()
print(mycursor.rowcount, "record inserted.")

mycursor.close()
mydb.close()

