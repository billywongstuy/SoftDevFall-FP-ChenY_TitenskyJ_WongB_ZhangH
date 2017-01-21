import csv
import sqlite3

def addComment(user, postID, content):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT MAX(commentID) FROM comments"
	c.execute(q)
	lastCommentID=c.fetchall()[0][0]
	if lastCommentID is None:
		lastCommentID=0
                print "Nothing"
        else:
        	lastCommentID += 1
	print lastCommentID
	q="INSERT INTO comments VALUES (\'"+user+"\', "+ str(postID) + ", " + str(lastCommentID)+ ", \'" + content + "\')"
	print q
	c.execute(q)
	db.commit()
	db.close()


#returns all data and posts belonging to a postID
def getComments(postID):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * from comments where postID=\'"+str(postID)+"\'"
	c.execute(q)
	var=c.fetchall()
	comments=[]
	for x in var:
		temp=[]
		for y in x:
			temp.append(str(y))
		comments.append(temp)
	db.commit()
	db.close()
	return comments


print getComments(1)
