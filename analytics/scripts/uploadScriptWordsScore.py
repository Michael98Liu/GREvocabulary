import mysql.connector
from mysql.connector import errorcode
import sys
import glob
import errno

# mydb = mysql.connector.connect(user='user', password='pass',
#                               host='localhost',
#                               database='GRE')
# mycursor = mydb.cursor()

path = '/Users/yana/Documents/classes/Senior2018/LargeScaleWeb/GREWordApp/GREvocabulary/analytics/scripts/output/wordScore/*'   
files = glob.glob(path)   
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    try:
        with open(name) as f: # No need to specify 'r': this is the default.
            content = f.readlines()
            for x in content:
            	line = x.strip().split(" ")
            	word = line[0]
            	score = line[1]
            	print(word, " : ", score)
				# sql = "UPDATE GRE_word SET difficulty=%s WHERE word = %s"
				# val = (float(score), lword)
				# mycursor.execute(sql, val)

    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.


# mydb.commit()
# print(mycursor.rowcount, "record inserted.")

# mycursor.close()
# mydb.close()

