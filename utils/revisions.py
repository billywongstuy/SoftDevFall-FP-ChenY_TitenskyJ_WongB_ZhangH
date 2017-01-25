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
        con = content
        con.encode("utf-8")
	q="INSERT INTO revisions VALUES (\'"+user+"\', "+ str(postID) + ", " + str(lastRevisionID)+ ", \'" + con + "\')"
	c.execute(q)
	db.commit()
	db.close()

def getRevisions(postID):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * from revisions where postID=\'"+str(postID)+"\'"
	c.execute(q)
	var=c.fetchall()
	revisions=[]
	for x in var:
		temp=[]
		for y in x:
			try:
                                u = str(y)
                                u.decode("utf-8")
                        except:
                                u = y
	                temp.append(u)
		#comments.append(temp)
                revisions.append(temp)
	db.commit()
	db.close()
	return revisions
