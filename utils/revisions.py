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

def getRevisions(postID):
	db=sqlite3.connect('../data/info.db')
	c=db.cursor()
	q="SELECT * from revisions where postID=\'"+str(postID)+"\'"
	c.execute(q)
	var=c.fetchall()
	revisions=[]
	for x in var:
		temp=[]
		for y in x:
			temp.append(str(y))
		comments.append(temp)
	db.commit()
	db.close()
	return revisions
