import csv
import sqlite3

def addComment(user, postID, content):
	db=sqlite3.connect('../data/info.db')
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

addComment('test', '1', 'Test comment')