import csv
import sqlite3

def displayPosts():
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * FROM posts"
	c.execute(q)
	var=c.fetchall()
	print var
	posts=[]
	for x in var:
		temp=[]
		for y in x:
			temp.append(str(y))
		posts.append(temp)

	return posts
	db.commit()
	db.close()

def selectPosts(language):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * FROM posts"
	c.execute(q)
	var=c.fetchall()
	print var
	posts=[]
	for x in var:
		temp=[]
		for y in x:
			temp.append(str(y))
		posts.append(temp)

	return posts
	db.commit()
	db.close()
	

