import csv
import sqlite3

def displayPost(language):
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

	print posts
	db.commit()
	db.close()
	
displayPost('eng')

