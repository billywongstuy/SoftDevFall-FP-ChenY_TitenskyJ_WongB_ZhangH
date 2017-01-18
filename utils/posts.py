import csv
import sqlite3

def addPost(user, title, content, language):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT MAX(postID) FROM posts"
	c.execute(q)
	lastPostID=c.fetchall()[0][0]
	if lastPostID is None:
		lastPostID=0
                print "Nothing"
        else:
                lastPostID += 1
	print lastPostID

        
        
	q="INSERT INTO posts VALUES (\'"+user+"\', "+ str(lastPostID) + ", \'" + title+ "\', \'" + content + "\', \'"+language+"\')"
	print q;
	c.execute(q)
	db.commit()
	db.close()

def viewPost(postID):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * from posts where postID="+str(postID)+""
	c.execute(q)
	postTuple=c.fetchall()[0]
	post=[]
	for x in range(len(postTuple)):
		post.append(str(postTuple[x]))
	c.execute(q)
	db.commit()
	db.close()
	return post

