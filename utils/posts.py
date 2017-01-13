import csv
import sqlite3

def addPost(user, title, content):
	db=sqlite3.connect('../data/info.db')
	c=db.cursor()
	q="SELECT MAX(postID) FROM posts"
	c.execute(q)
	lastPostID=c.fetchall()[0][0]
	if lastPostID is None:
		lastPostID=0
	print lastPostID
	q="INSERT INTO posts VALUES (\'"+user+"\', "+ str(lastPostID) + ", \'" + title+ "\', \'" + content + "\')"
	print q;
	c.execute(q)
	db.commit()
	db.close()
	
addPost('bruh', 'title', 'content')

