import csv
import sqlite3

def addRevision(user, postID, content):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT MAX(revisionID) FROM revisions"
	c.execute(q)
	lastRevisionID=c.fetchall()[0][0]
	if lastRevisionID is None:
		lastRevisionID=0
                print "Nothing"
        else:
        	lastRevisionID += 1
	q="INSERT INTO revisions VALUES (\'"+user+"\', "+ str(postID) + ", " + str(lastRevisionID)+ ", \'" + content + "\')"
	c.execute(q)
	db.commit()
	db.close()
